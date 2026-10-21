# pc-ffcceotwii

Toward a native PC port of **Final Fantasy Crystal Chronicles: Echoes of
Time** (Wii, Square Enix, 2009), the Wii edition of a game made for the
DS: the same game on both, built on Square Enix's Pollux Engine ("Cross
Platform System"), whose Wii players and DS players played together. It
was never re-released. The goal is the game running natively on PC, played
with the keyboard and the mouse.

The route is static recompilation: the game's own PowerPC code, translated
to C++ and built for the PC, running on a replacement for the Wii's
hardware and system software. Nothing is emulated at the instruction
level, and nothing of the game is rewritten.

This repository documents the port and holds its own tools and layer. It is
built on **[wiikit](https://github.com/vs-sr-dev/wiikit)**, the
game-agnostic Wii toolkit, taken here as a submodule at `wiikit/`. Where
this game needs something every Wii game would need, it goes into wiikit,
not here.

Its DS edition is a candidate for [ndskit](https://github.com/vs-sr-dev/ndskit),
wiikit's sibling for the DS. The two editions talked over the DS's own
wireless protocol (MP), which the Wii spoke through its RVL SDK's MP and
MPDS libraries; getting the two PC ports to talk is the long-term aim
(`docs/07-next-session.md`).

## Where it stands

After one session **the game plays**, recompiled and booted at the first
try; wiikit gained one fix:

- The strap screen, the Square Enix and Pollux Engine logos, the title.
- A new hero created, named, and into the game (the user, by hand):
  "everything seems to work".
- Picture and sound right, at 30 frames a second: the DS's two screens
  side by side on the cork board, as on the Wii.
- The mouse as the pointer (the touch screen), the keyboard as the Remote's
  buttons and the Nunchuk.
- wiikit empties the NAND's `/tmp` at boot, as IOS does: the game copies
  41 MB of the disc there and stopped at the second boot without it.

Not yet: playing with the DS edition (local wireless) or online (Nintendo
Wi-Fi Connection, closed in 2014).

See [docs/00-sessions.md](docs/00-sessions.md) and the plan in
[docs/07-next-session.md](docs/07-next-session.md).

## BYOA — Bring Your Own Assets

This repository contains **documentation and tools only**. No game data, no
executables, no assets. You need your own original disc. The work is done on
the European release, RFFP; the addresses in `tools/` and `docs/` are
that executable's.

## Layout

    docs/     the executable, the plan, the session log
    tools/    Echoes of Time-specific tools, the port's layer (eot.cpp), its keys
    wiikit/   game-agnostic Wii toolkit (submodule: github.com/vs-sr-dev/wiikit)
    build/    (not in git) the disc, everything derived from it, the build

## Building

As for the other wiikit ports: Python 3.8+, CMake, Ninja, clang (MSYS2) and
SDL3; OpenGL 4.5 to run. From the root:

```sh
python -m wiikit.disc GAME.rvz --extract build/extract
python tools/sigmatch.py build/extract/sys/main.dol --dsy <Dolphin>/Sys/totaldb.dsy \
    --out build/sig_guess.tsv
python tools/kinmatch.py build/extract/sys/main.dol \
    --kin <crystal bearers>/build/extract/sys/main.dol <crystal bearers>/build/names.tsv \
    --kin <castlevania judgment>/build/extract/sys/main.dol <castlevania judgment>/build/names.tsv \
    --out build/kin_guess.tsv                               # more kin: docs/03-executable.md
python tools/names.py build/extract/sys/main.dol          # -> build/names.tsv
python -m wiikit.recomp build/extract/sys/main.dol --out build/recomp \
    --symbols build/names.tsv --hooks tools/eot-hooks.txt
cmake -S build/recomp -B build/recomp-build -G Ninja -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE=-O1 -DWIIKIT_EXTRA=$PWD/tools/eot.cmake
ninja -C build/recomp-build
cp tools/eot-keys.txt build/keys.txt
cd build/run1 && ../recomp-build/wiiboot ../extract --symbols ../recomp/symbols.tsv \
    --nand ../nand --fonts ../fonts
```

`build/fonts` holds the boot ROM's fonts and `dsp_coef.bin` (Dolphin's
`Sys/GC` has free ones). The names come from the other ports' named
executables (`tools/kinmatch.py`, by hash, by place and by order), from
Dolphin's `totaldb.dsy`, and from `tools/names-manual.tsv`, each with its
evidence. `tools/look.py` is `wiikit.ppc` on the stripped DOL.

## Playing

The game makes a DS's buttons from the Wii's (`docs/03-executable.md`);
`tools/eot-keys.txt` puts them on the keyboard and the mouse:

| Keys | Wii | DS |
|---|---|---|
| W A S D | the Nunchuk's stick | the cross |
| the mouse | the pointer | the touch screen |
| left button, Return, J | A | A |
| Space, right button, K | B | B |
| Q | Z | Y |
| E | C | L |
| Tab, 1 | 1 | START |
| Backspace, 2 | 2 | SELECT |
| arrows | the Remote's cross | |

Esc opens wiikit's pause box, F11 fullscreen, F12 a GX trace.

## Documentation

    00-sessions.md            progress log
    03-executable.md          the disc, the stripped DOL, its SDK, its names, its input
    07-next-session.md        the plan for the next session, the DS link
    10-wiikit.md              how this port uses and grows wiikit

## Licence

MIT. This covers the documentation and tools in this repository only. It
says nothing about Final Fantasy Crystal Chronicles: Echoes of Time, which
remains the property of its rights holders.
