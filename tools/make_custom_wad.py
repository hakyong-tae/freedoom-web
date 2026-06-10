#!/usr/bin/env python3
"""Build public/custom.wad (PWAD) with custom art converted to DOOM format.

Usage: python3 tools/make_custom_wad.py <titlepic-image>

- Extracts PLAYPAL from public/freedoom1.wad
- Center-crops the source to 4:3, squashes to 320x200 (DOOM pixels are
  displayed 20% taller, so the on-screen result matches the source crop)
- Quantizes to the DOOM palette and encodes the patch (column/post) format
"""
import struct
import sys

from PIL import Image

IWAD = 'public/freedoom1.wad'
OUT = 'public/custom.wad'
W, H = 320, 200


def read_lump(wad_path, want):
    with open(wad_path, 'rb') as f:
        data = f.read()
    magic, numlumps, diroffs = struct.unpack_from('<4sii', data, 0)
    assert magic in (b'IWAD', b'PWAD')
    for i in range(numlumps):
        pos, size, name = struct.unpack_from('<ii8s', data, diroffs + 16 * i)
        if name.rstrip(b'\0').decode('ascii', 'ignore').upper() == want:
            return data[pos:pos + size]
    raise KeyError(want)


def to_doom_patch(im, palette):
    """Encode a fully-opaque image as a DOOM patch graphic."""
    pal_img = Image.new('P', (1, 1))
    pal_img.putpalette(palette + palette[:3] * (256 - len(palette) // 3))
    idx = im.convert('RGB').quantize(palette=pal_img, dither=Image.FLOYDSTEINBERG)
    px = idx.load()
    w, h = im.size

    header = struct.pack('<HHhh', w, h, 0, 0)
    col_offsets = []
    body = bytearray()
    base = len(header) + 4 * w
    for x in range(w):
        col_offsets.append(base + len(body))
        # single opaque post per column (h <= 254)
        body += bytes([0, h, 0])
        body += bytes(px[x, y] for y in range(h))
        body += bytes([0, 0xFF])
    return header + b''.join(struct.pack('<i', o) for o in col_offsets) + bytes(body)


def build_pwad(lumps, out_path):
    body = bytearray()
    directory = []
    offs = 12
    for name, data in lumps:
        directory.append((offs + len(body), len(data), name))
        body += data
    with open(out_path, 'wb') as f:
        f.write(struct.pack('<4sii', b'PWAD', len(lumps), 12 + len(body)))
        f.write(body)
        for pos, size, name in directory:
            f.write(struct.pack('<ii8s', pos, size, name.encode('ascii')))


def main():
    src = sys.argv[1]
    playpal = read_lump(IWAD, 'PLAYPAL')
    palette = list(playpal[:768])

    im = Image.open(src)
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, (0, 0, 0))
        bg.paste(im, mask=im.split()[3])
        im = bg
    # center-crop to 4:3, then squash to 320x200
    w, h = im.size
    crop_w = min(w, int(h * 4 / 3))
    crop_h = min(h, int(crop_w * 3 / 4))
    left = (w - crop_w) // 2
    top = (h - crop_h) // 2
    im = im.crop((left, top, left + crop_w, top + crop_h)).resize((W, H), Image.LANCZOS)

    titlepic = to_doom_patch(im, palette)
    build_pwad([('TITLEPIC', titlepic)], OUT)
    print(f'{OUT}: TITLEPIC {W}x{H}, {len(titlepic)} bytes')


if __name__ == '__main__':
    main()
