#!/usr/bin/env python3
"""news-23 b81 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(here)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo (%s)" % out_dir)
    if not os.path.isfile(src):
        return fail("entry.png not found next to main.py")
    data = open(src, "rb").read()
    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("entry.png is not a PNG file")
    # Parse the IHDR chunk manually (stdlib struct, no PIL).
    if len(data) < 33:
        return fail("entry.png too short for an IHDR chunk")
    length, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or length != 13:
        return fail("first chunk is not a 13-byte IHDR")
    width, height, depth, colour, comp, filt, inter = struct.unpack(
        ">IIBBBBB", data[16:29])
    if (width, height) != (1024, 1024):
        return fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if depth != 8 or colour not in (2, 6):
        return fail("unexpected bit depth %d / colour type %d" % (depth, colour))
    if comp != 0 or filt != 0 or inter != 0:
        return fail("unexpected compression/filter/interlace flags")
    ihdr_crc = binascii.crc32(data[12:29]) & 0xFFFFFFFF
    stored_crc = struct.unpack(">I", data[29:33])[0]
    if ihdr_crc != stored_crc:
        return fail("IHDR CRC mismatch")
    # Walk every chunk: verify each CRC, require an IDAT, and require the
    # last chunk to be a well-formed 12-byte IEND trailer.
    pos, seen_idat, last_type = 8, False, None
    while pos + 8 <= len(data):
        clen, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        if pos + 12 + clen > len(data):
            return fail("truncated %s chunk" % ctype.decode("ascii", "replace"))
        crc = binascii.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF
        stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if crc != stored:
            return fail("%s chunk CRC mismatch" % ctype.decode("ascii", "replace"))
        if ctype == b"IDAT":
            seen_idat = True
        last_type = ctype
        pos += 12 + clen
    if pos != len(data):
        return fail("trailing bytes after the last chunk")
    if not seen_idat:
        return fail("no IDAT chunk found")
    if last_type != b"IEND":
        return fail("last chunk is not IEND")
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    back = open(dst, "rb").read()
    if back != data:
        return fail("output does not match entry.png byte-for-byte")
    print("wrote %s (%d bytes, sha256 %s)"
          % (dst, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
