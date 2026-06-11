#!/usr/bin/env python3
"""
YAFFS1 extractor for stripped (no-spare/OOB) format.
Format: block_pages=8, page_size=512, no spare data.
Each block's page 0 = object header; subsequent pages = file data.
"""
import struct, os, stat, sys

def extract(img_path, out_dir):
    data = open(img_path, 'rb').read()

    PAGE = 512
    BLOCK_PAGES = 8
    TOTAL_BLOCKS = len(data) // (PAGE * BLOCK_PAGES)

    def read_u32(off): return struct.unpack_from('<I', data, off)[0]
    def read_u16(off): return struct.unpack_from('<H', data, off)[0]

    def scan_headers():
        hdrs = {}
        for block in range(TOTAL_BLOCKS):
            page = block * BLOCK_PAGES
            off = page * PAGE
            t = read_u32(off)
            if t not in {1,2,3,4,5}: continue
            if read_u16(off+8) != 0xffff: continue
            parent = read_u32(off+4)
            if parent == 0 or parent > 200000: continue
            name_raw = data[off+10:off+266].split(b'\x00')[0]
            if not name_raw or not all(32<=b<127 for b in name_raw): continue
            name = name_raw.decode('ascii')
            mode  = read_u32(off+268)
            uid   = read_u32(off+272)
            gid   = read_u32(off+276)
            mtime = read_u32(off+284)
            file_size = read_u32(off+292) if t == 1 else 0
            alias = ''
            if t == 2:
                alias = data[off+300:off+460].split(b'\x00')[0].decode('utf-8', 'replace')
            hdrs[page] = dict(type=t, parent=parent, name=name, mode=mode,
                              uid=uid, gid=gid, mtime=mtime,
                              file_size=file_size, alias=alias, block=block)
        return hdrs

    hdrs = scan_headers()
    print(f"[*] Found {len(hdrs)} valid object headers")

    # Build parent->children index
    children_by_parent = {}
    for p, h in hdrs.items():
        children_by_parent.setdefault(h['parent'], []).append(p)

    all_pids = sorted(set(h['parent'] for h in hdrs.values()))

    # Assign obj_id to every object header by page order.
    # YAFFS reserves obj_id 1 for root (page 0); all subsequent objects
    # are allocated sequentially starting at 257 (YAFFS_NOBJECT_BUCKETS+1).
    page_to_objid = {0: 1}
    oid_counter = 256
    for page in sorted(hdrs):
        if page == 0:
            continue
        oid_counter += 1
        page_to_objid[page] = oid_counter
    objid_to_page = {v: k for k, v in page_to_objid.items()}

    # Build path for each object
    objid_to_path = {1: out_dir}
    for page, oid in sorted(page_to_objid.items()):
        if oid == 1: continue
        h = hdrs.get(page)
        if not h: continue
        parent_path = objid_to_path.get(h['parent'], os.path.join(out_dir, f'_unk_{h["parent"]}'))
        objid_to_path[oid] = os.path.join(parent_path, h['name'])

    mview = memoryview(data)

    # Write file data directly to an open file object, page by page (zero-copy)
    def write_file_data(f, header_block, file_size):
        if file_size == 0:
            return
        pages_needed = (file_size + PAGE - 1) // PAGE
        remaining = file_size
        for i in range(pages_needed):
            data_block = header_block + 1 + (i // BLOCK_PAGES)
            data_page_in_block = i % BLOCK_PAGES
            abs_page = data_block * BLOCK_PAGES + data_page_in_block
            off = abs_page * PAGE
            chunk = min(PAGE, remaining)
            f.write(mview[off:off+chunk])
            remaining -= chunk

    # Create output directories
    os.makedirs(out_dir, exist_ok=True)
    for page, oid in sorted(page_to_objid.items()):
        if oid == 1: continue
        h = hdrs.get(page)
        if h and h['type'] == 3:
            path = objid_to_path.get(oid, '')
            if path:
                os.makedirs(path, exist_ok=True)

    # Also create directories for unresolved parent IDs
    for pid in all_pids:
        if pid not in objid_to_page and pid != 1:
            unknown_dir = os.path.join(out_dir, f'_parent_{pid}')
            objid_to_path[pid] = unknown_dir
            os.makedirs(unknown_dir, exist_ok=True)

    # Extract all files and symlinks
    stats = dict(files=0, dirs=0, symlinks=0, skipped=0)
    for page, h in sorted(hdrs.items()):
        parent_path = objid_to_path.get(h['parent'])
        if parent_path is None:
            stats['skipped'] += 1
            continue
        dest = os.path.join(parent_path, h['name'])

        if h['type'] == 3:  # directory
            os.makedirs(dest, exist_ok=True)
            stats['dirs'] += 1

        elif h['type'] == 1:  # file
            try:
                with open(dest, 'wb') as f:
                    write_file_data(f, h['block'], h['file_size'])
                mode = h['mode'] & 0o777
                os.chmod(dest, mode)
                stats['files'] += 1
            except Exception as e:
                print(f"  [!] Failed to write {dest}: {e}")
                stats['skipped'] += 1

        elif h['type'] == 2:  # symlink
            target = h['alias']
            if target:
                try:
                    if os.path.lexists(dest):
                        os.remove(dest)
                    os.symlink(target, dest)
                    stats['symlinks'] += 1
                except Exception as e:
                    print(f"  [!] Failed symlink {dest} -> {target}: {e}")
                    stats['skipped'] += 1

    print(f"[+] Extracted: {stats['files']} files, {stats['dirs']} dirs, "
          f"{stats['symlinks']} symlinks, {stats['skipped']} skipped")
    print(f"[+] Output: {out_dir}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <image.img> <output_dir>")
        sys.exit(1)
    extract(sys.argv[1], sys.argv[2])
