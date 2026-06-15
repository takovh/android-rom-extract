import argparse
import struct
from pathlib import Path
from typing import BinaryIO, Union

SPARSE_HEADER_MAGIC = 0xED26FF3A
SPARSE_HEADER_SIZE = 28
SPARSE_CHUNK_HEADER_SIZE = 12


class SparseHeader:
    def __init__(self, buffer):
        fmt = '<I4H4I'
        (
            self.magic,
            self.major_version,
            self.minor_version,
            self.file_hdr_sz,
            self.chunk_hdr_sz,
            self.blk_sz,
            self.total_blks,
            self.total_chunks,
            self.image_checksum
        ) = struct.unpack(fmt, buffer[:struct.calcsize(fmt)])


class SparseChunkHeader:
    def __init__(self, buffer):
        fmt = '<2H2I'
        (
            self.chunk_type,
            self.reserved,
            self.chunk_sz,
            self.total_sz,
        ) = struct.unpack(fmt, buffer[:struct.calcsize(fmt)])


class SparseImage:
    def __init__(self, fd: BinaryIO):
        self._fd = fd
        self.header = None

    def check(self) -> bool:
        self._fd.seek(0)
        self.header = SparseHeader(self._fd.read(SPARSE_HEADER_SIZE))
        return self.header.magic == SPARSE_HEADER_MAGIC

    def _read_data(self, chunk_data_size: int):
        if self.header.chunk_hdr_sz > SPARSE_CHUNK_HEADER_SIZE:
            self._fd.seek(self.header.chunk_hdr_sz - SPARSE_CHUNK_HEADER_SIZE, 1)
        return self._fd.read(chunk_data_size)

    def unsparse(self, output_path: Union[str, Path]) -> Path:
        if not self.header:
            self._fd.seek(0)
            self.header = SparseHeader(self._fd.read(SPARSE_HEADER_SIZE))
        chunks = self.header.total_chunks
        self._fd.seek(self.header.file_hdr_sz - SPARSE_HEADER_SIZE, 1)
        output_path = Path(output_path)
        with open(str(output_path), 'wb') as out:
            while chunks > 0:
                chunk_header = SparseChunkHeader(self._fd.read(SPARSE_CHUNK_HEADER_SIZE))
                sector_size = (chunk_header.chunk_sz * self.header.blk_sz) >> 9
                chunk_data_size = chunk_header.total_sz - self.header.chunk_hdr_sz
                if chunk_header.chunk_type == 0xCAC1:
                    data = self._read_data(chunk_data_size)
                    if len(data) == (sector_size << 9):
                        out.write(data)
                elif chunk_header.chunk_type == 0xCAC2:
                    data = self._read_data(chunk_data_size)
                    out.truncate(out.tell() + (sector_size << 9))
                    out.seek(0, 2)
                elif chunk_header.chunk_type == 0xCAC3:
                    data = self._read_data(chunk_data_size)
                    out.truncate(out.tell() + (sector_size << 9))
                    out.seek(0, 2)
                else:
                    out.truncate(out.tell() + (sector_size << 9))
                    out.seek(0, 2)
                chunks -= 1
        return output_path


def convert(input_path: Union[str, Path], output_path: Union[str, Path]) -> Path:
    """Convert an Android sparse image to a raw image."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    with open(str(input_path), 'rb') as fd:
        img = SparseImage(fd)
        if not img.check():
            raise ValueError(f'{input_path} is not a valid sparse image')
        img.unsparse(output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Convert Android sparse image to raw image'
    )
    parser.add_argument('input', type=Path, help='Input sparse image')
    parser.add_argument('output', type=Path, help='Output raw image')
    args = parser.parse_args()
    convert(args.input, args.output)


if __name__ == '__main__':
    main()
