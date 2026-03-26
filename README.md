# Departure Mono — Unicode Block Glyphs

Unicode block character representations of every glyph in [Departure Mono](https://departuremono.com) v1.500, generated from the font file itself.

## Origin

[@joeldrapper](https://github.com/joeldrapper) opened [an issue](https://github.com/rektdeckard/departure-mono/issues/25) on the Departure Mono repo asking whether the font's glyphs could be reproduced as Unicode block characters for use in terminal UIs — and whether the process could be automated. This repo is that automation.

## What's here

**`departure-mono-glyphs.txt`** — 1,079 glyphs, each rendered as a 7×7 grid of block characters (encoding 7×14 pixels at the font's native pixel grid).

**`generate_glyphs.py`** — the script that produced it, using Pillow to rasterize the OTF at 11pt/72dpi, where 1 font unit = 1/50 px and the advance width lands exactly on 7px.

## Encoding

Each glyph occupies 7 lines of 7 characters. Two pixel rows are packed into one line using:

| Character | Meaning |
|-----------|---------|
| `█` U+2588 | both rows on |
| `▀` U+2580 | top row on, bottom off |
| `▄` U+2584 | top row off, bottom on |
| ` ` space  | both rows off |

## Format

```
U+0041 A LATIN CAPITAL LETTER A

   ▄
 ▄▀ ▀▄
 █▄▄▄█
 █   █
 ▀   ▀

```

Each entry: a `U+XXXX <char> NAME` header, 7 lines of block characters, then a blank line.

## License

The glyphs are derived from [Departure Mono](https://github.com/rektdeckard/departure-mono) by [Tobias Fried](https://github.com/rektdeckard), released under the [SIL Open Font License 1.1](https://scripts.sil.org/OFL). The generation script is MIT licensed.
