#!/usr/bin/env python3
"""Build public/custom.wad (PWAD) with custom art converted to DOOM format.

Usage: python3 tools/make_custom_wad.py <titlepic-image> [interpic-image] [menu-logo-rgba]

- Extracts PLAYPAL from public/freedoom1.wad
- Fullscreen lumps: center-crops to 4:3, squashes to 320x200 (DOOM pixels are
  displayed 20% taller, so the on-screen result matches the source crop)
- Menu logo (M_DOOM): keeps alpha as patch-format transparency, scales to
  60px-high buffer, sets leftoffset so the engine centers it at x=160
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


def quantize(im, palette):
    pal_img = Image.new('P', (1, 1))
    pal_img.putpalette(palette + palette[:3] * (256 - len(palette) // 3))
    return im.convert('RGB').quantize(palette=pal_img, dither=Image.FLOYDSTEINBERG)


def to_doom_patch(im, palette, leftoffset=0, topoffset=0):
    """Encode an image as a DOOM patch; RGBA alpha becomes post transparency."""
    alpha = im.split()[3].load() if im.mode == 'RGBA' else None
    idx = quantize(im, palette)
    px = idx.load()
    w, h = im.size

    header = struct.pack('<HHhh', w, h, leftoffset, topoffset)
    col_offsets = []
    body = bytearray()
    base = len(header) + 4 * w
    for x in range(w):
        col_offsets.append(base + len(body))
        y = 0
        while y < h:
            while y < h and alpha and alpha[x, y] <= 127:
                y += 1
            if y >= h:
                break
            top = y
            while y < h and (not alpha or alpha[x, y] > 127):
                y += 1
            body += bytes([top, y - top, 0])
            body += bytes(px[x, yy] for yy in range(top, y))
            body += bytes([0])
        body += bytes([0xFF])
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


def load_fullscreen(path):
    im = Image.open(path)
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
    return im.crop((left, top, left + crop_w, top + crop_h)).resize((W, H), Image.LANCZOS)


def main():
    playpal = read_lump(IWAD, 'PLAYPAL')
    palette = list(playpal[:768])

    lumps = [('TITLEPIC', to_doom_patch(load_fullscreen(sys.argv[1]), palette))]
    if len(sys.argv) > 2:
        lumps.append(('INTERPIC', to_doom_patch(load_fullscreen(sys.argv[2]), palette)))
    if len(sys.argv) > 3:
        logo = Image.open(sys.argv[3]).convert('RGBA')
        hb = 60  # menu logo sits above the items (y=2..62); engine draws it at x=94
        wb = round(logo.size[0] / logo.size[1] * 1.2 * hb)
        logo = logo.resize((wb, hb), Image.LANCZOS)
        lumps.append(('M_DOOM', to_doom_patch(logo, palette, leftoffset=wb // 2 - 66)))
    build_pwad(lumps, OUT)
    for name, data in lumps:
        w, h = struct.unpack_from('<HH', data, 0)
        print(f'{OUT}: {name} {w}x{h}, {len(data)} bytes')


if __name__ == '__main__':
    main()
