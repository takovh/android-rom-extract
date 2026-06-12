"""
rkunpack - Rockchip firmware unpacker

Python port of rkunpack from https://github.com/naoki/rkflashtool
Supports RKAF, RKFW, and RKFP firmware container formats.
"""

import argparse
import os
import struct
import sys


OUTDIR = '.'
RECURSIVE = False


def get32le(data: bytes, offset: int) -> int:
    return struct.unpack_from('<I', data, offset)[0]


def write_file(path: str, data: bytes) -> None:
    full = os.path.join(OUTDIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'wb') as f:
        f.write(data)
    if RECURSIVE and data[:4] in {b'RKAF', b'RKFW', b'RKFP'}:
        _recursive_unpack(full, data)


def _recursive_unpack(filepath: str, data: bytes) -> None:
    global OUTDIR
    old = OUTDIR
    base = os.path.splitext(os.path.basename(filepath))[0]
    OUTDIR = os.path.join(os.path.dirname(filepath), base)
    try:
        if data[:4] == b'RKAF':
            unpack_rkaf(data, len(data))
        elif data[:4] == b'RKFW':
            unpack_rkfw(data, len(data))
        elif data[:4] == b'RKFP':
            unpack_rkfp(data, len(data))
    finally:
        OUTDIR = old


def unpack_rkaf(buf: bytes, size: int) -> None:
    print('rkunpack: info: RKAF signature detected')

    fsize = get32le(buf, 4) + 4
    if fsize != size:
        print(f'rkunpack: info: invalid file size (should be {fsize} bytes)')
    else:
        print(f'rkunpack: info: file size matches ({fsize} bytes)')

    manufacturer = buf[0x48:0x48+64].split(b'\x00', 1)[0].decode('ascii', errors='replace')
    model = buf[0x08:0x08+64].split(b'\x00', 1)[0].decode('ascii', errors='replace')
    print(f'rkunpack: info: manufacturer: {manufacturer}')
    print(f'rkunpack: info: model: {model}')

    count = get32le(buf, 0x88)
    print(f'rkunpack: info: number of files: {count}')

    for i in range(count):
        p = 0x8c + i * 0x70
        name = buf[p:p+32].split(b'\x00', 1)[0].decode('ascii', errors='replace')
        path = buf[p+0x20:p+0x20+64].split(b'\x00', 1)[0].decode('ascii', errors='replace')

        ioff = get32le(buf, p + 0x60)
        noff = get32le(buf, p + 0x64)
        isize = get32le(buf, p + 0x68)
        fsize = get32le(buf, p + 0x6c)

        if path.startswith('SELF'):
            print('rkunpack: info: skipping SELF entry')
            continue

        print(f'rkunpack: info: {ioff:08x}-{ioff + isize - 1:08x} {path:<26} (size: {fsize})')

        if name.startswith('parameter'):
            ioff += 8
            fsize -= 12

        write_file(path, buf[ioff:ioff + fsize])


def unpack_rkfw(buf: bytes, size: int) -> None:
    print('rkunpack: info: RKFW signature detected')

    ver_major = buf[9]
    ver_middle = buf[8]
    ver_minor = buf[7] << 8 | buf[6]
    print(f'rkunpack: info: version: {ver_major}.{ver_middle}.{ver_minor}')

    year = buf[0x0f] << 8 | buf[0x0e]
    month = buf[0x10]
    day = buf[0x11]
    hour = buf[0x12]
    minute = buf[0x13]
    second = buf[0x14]
    print(f'rkunpack: info: date: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}')

    chip_codes = {
        0x50: 'rk29xx',
        0x60: 'rk30xx',
        0x70: 'rk31xx',
        0x80: 'rk32xx',
        0x41: 'rk3368',
    }
    chip_byte = buf[0x15]
    chip = chip_codes.get(chip_byte)
    if chip is None:
        print(f'rkunpack: info: You got a brand new chip ({chip_byte:#x}), congratulations!!!')
        chip = 'unknown'
    print(f'rkunpack: info: family: {chip}')

    ioff = get32le(buf, 0x19)
    isize = get32le(buf, 0x1d)

    if buf[ioff:ioff+4] != b'BOOT':
        print('rkunpack: fatal: cannot find BOOT signature', file=sys.stderr)
        sys.exit(1)

    print(f'rkunpack: info: {ioff:08x}-{ioff + isize - 1:08x} {"BOOT":<26} (size: {isize})')
    write_file('BOOT', buf[ioff:ioff + isize])

    ioff = get32le(buf, 0x21)
    isize = get32le(buf, 0x25)

    if buf[ioff:ioff+4] != b'RKAF':
        print('rkunpack: fatal: cannot find embedded RKAF update.img', file=sys.stderr)
        sys.exit(1)

    print(f'rkunpack: info: {ioff:08x}-{ioff + isize - 1:08x} {"embedded-update.img":<26} (size: {isize})')
    write_file('embedded-update.img', buf[ioff:ioff + isize])


def unpack_rkfp(buf: bytes, size: int) -> None:
    print('rkunpack: info: RKFP signature detected')

    ver_major = buf[15]
    ver_middle = buf[14]
    ver_minor = buf[13] << 8 | buf[12]
    print(f'rkunpack: info: version: {ver_major}.{ver_middle}.{ver_minor}')

    year = buf[0x05] << 8 | buf[0x04]
    month = buf[0x06]
    day = buf[0x07]
    hour = buf[0x08]
    minute = buf[0x09]
    second = buf[0x0a]
    print(f'rkunpack: info: date: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}')

    pss = get32le(buf, 0x10)
    peo = get32le(buf, 0x14)
    pbeo = get32le(buf, 0x18)
    pes = get32le(buf, 0x1c)
    pec = get32le(buf, 0x20)

    print(f'rkunpack: info: partition sector size: {pss} bytes')
    print(f'rkunpack: info: partition entry offset: {peo} sectors, backup partition entry offset: {pbeo} sectors')
    print(f'rkunpack: info: partition entry size: {pes} bytes')
    print(f'rkunpack: info: partition entry count: {pec}')
    print(f'rkunpack: info: fw size: {get32le(buf, 0x24)}')
    print(f'rkunpack: info: partition entry crc: {get32le(buf, 504):08x}')
    print(f'rkunpack: info: header crc: {get32le(buf, 508):08x}')

    for count in range(1, pec + 1):
        p = pss * peo + (count - 1) * pes
        path = buf[p:p+32].split(b'\x00', 1)[0].decode('ascii', errors='replace')
        ioff = get32le(buf, p + 36)
        isize = get32le(buf, p + 40)
        fsize = get32le(buf, p + 44)
        ptype = get32le(buf, p + 32)
        prop = get32le(buf, p + 48)

        print(f'rkunpack: info: {ioff * pss:08x}-{(ioff + isize) * pss:08x} {path:<26} (type: {ptype:02x}) (property: {prop:02x}) (size: {fsize})')
        write_file(path, buf[ioff * pss:ioff * pss + fsize])


def main() -> None:
    global OUTDIR, RECURSIVE

    parser = argparse.ArgumentParser(prog='rkunpack')
    parser.add_argument('-o', '--output', default='.', help='output directory')
    parser.add_argument('-r', '--recursive', action='store_true', help='recursively unpack embedded images')
    parser.add_argument('firmware', help='update.img file')
    args = parser.parse_args()

    OUTDIR = args.output
    RECURSIVE = args.recursive

    with open(args.firmware, 'rb') as f:
        buf = f.read()

    size = len(buf)

    if buf[:4] == b'RKAF':
        unpack_rkaf(buf, size)
    elif buf[:4] == b'RKFW':
        unpack_rkfw(buf, size)
    elif buf[:4] == b'RKFP':
        unpack_rkfp(buf, size)
    else:
        print(f'rkunpack: fatal: {args.firmware}: invalid signature', file=sys.stderr)
        sys.exit(1)

    print('unpacked')


if __name__ == '__main__':
    main()
