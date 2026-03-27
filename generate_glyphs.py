#!/usr/bin/env python3
"""
Generate unicode block character representations of all Departure Mono glyphs.

Each glyph is rendered to a 7x14 pixel grid, then encoded using:
  █  (U+2588) FULL BLOCK       — both pixel rows on
  ▀  (U+2580) UPPER HALF BLOCK — top pixel on, bottom off
  ▄  (U+2584) LOWER HALF BLOCK — top pixel off, bottom on
     (space)                   — both pixel rows off

Output: 7 characters wide × 7 lines tall per glyph.
"""

import argparse
import sys
import unicodedata
from fontTools import ttLib
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser(description="Generate unicode block glyphs from a font file.")
parser.add_argument("--font", help="Path to the .otf/.ttf font file")
parser.add_argument("--output", help="Path for the output .txt file")
args = parser.parse_args()

FONT_PATH = args.font or input("Font path: ").strip()
OUTPUT_PATH = args.output or input("Output path: ").strip()

FONT_SIZE = 11   # 11pt @ 72dpi → 7px advance width, 14px cell height
CELL_W = 7
CELL_H = 14
BASELINE_Y = 11  # pixels from top (= ascender height)
THRESHOLD = 64   # alpha threshold for "pixel on"

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# Verify metrics match expectations
ascent, descent = font.getmetrics()
assert ascent == 11 and descent == 3, f"Unexpected metrics: {ascent}, {descent}"

def render_char(char):
    """Render a single character to a 7×14 binary bitmap."""
    img = Image.new('L', (CELL_W, CELL_H), 0)
    draw = ImageDraw.Draw(img)
    draw.text((0, BASELINE_Y), char, font=font, fill=255, anchor='ls')
    return [[img.getpixel((x, y)) > THRESHOLD for x in range(CELL_W)]
            for y in range(CELL_H)]

def bitmap_to_blocks(bitmap):
    """Convert 7×14 bitmap to 7 lines of 7 block characters (2 rows per line)."""
    lines = []
    for pair in range(7):  # 7 pairs of rows = 14 rows total
        top = bitmap[pair * 2]
        bot = bitmap[pair * 2 + 1]
        line = ''
        for x in range(CELL_W):
            t, b = top[x], bot[x]
            if t and b:
                line += '█'
            elif t:
                line += '▀'
            elif b:
                line += '▄'
            else:
                line += ' '
        lines.append(line)
    return lines

def char_name(cp):
    """Get Unicode name for a codepoint, or a fallback."""
    try:
        return unicodedata.name(chr(cp))
    except ValueError:
        return f'U+{cp:04X}'

# Load all codepoints from font
tt = ttLib.TTFont(FONT_PATH)
cmap = tt.getBestCmap()
codepoints = sorted(cmap.keys())
tt.close()

print(f"Rendering {len(codepoints)} glyphs...", file=sys.stderr)

lines_out = []
lines_out.append("# Departure Mono — Unicode Block Character Glyphs")
lines_out.append("# Font: Departure Mono v1.500 by Tobias Fried")
lines_out.append("# License: SIL Open Font License 1.1")
lines_out.append("#")
lines_out.append("# Each glyph is 7 columns × 14 rows rendered as 7 lines of block characters.")
lines_out.append("# Encoding uses: █ (U+2588), ▀ (U+2580), ▄ (U+2584), and space.")
lines_out.append("# Two pixel rows are combined into one line of block characters.")
lines_out.append("#")
lines_out.append("# Format:")
lines_out.append("#   U+XXXX <char> NAME")
lines_out.append("#   <7 lines of 7 block chars>")
lines_out.append("#")
lines_out.append("")

failed = []
for cp in codepoints:
    char = chr(cp)
    try:
        bitmap = render_char(char)
        block_lines = bitmap_to_blocks(bitmap)
        name = char_name(cp)
        # Header line: skip printing the char itself if it's a control/invisible char
        display = char if unicodedata.category(char)[0] not in ('C', 'Z') else ''
        lines_out.append(f"U+{cp:04X} {display} {name}")
        lines_out.extend(block_lines)
        lines_out.append("")
    except Exception as e:
        failed.append((cp, str(e)))
        print(f"  FAILED U+{cp:04X}: {e}", file=sys.stderr)

if failed:
    print(f"\n{len(failed)} glyphs failed to render.", file=sys.stderr)

output = '\n'.join(lines_out)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Written {len(codepoints) - len(failed)} glyphs to {OUTPUT_PATH}", file=sys.stderr)
print(f"File size: {len(output.encode('utf-8')) / 1024:.1f} KB", file=sys.stderr)
