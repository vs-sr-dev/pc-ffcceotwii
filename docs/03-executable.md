# The executable

## The disc

RFFP (`RFFPGD`, "FFCC EOT"), the European release, English, French, German
and Spanish, as RVZ. `wiikit.disc` extracts its DATA partition in about a
minute: 97 files, 2.4 GB. Few files, and most of them the DS game's:

- `coolres.rsb`, `coolres0.rsb`-`coolres4.rsb`, `coolresn.rsb`: the
  game's resources (124 MB in all; `coolres%d.rsb` by language).
- `sound/<eu|us|jp>/music.sdat`, `se.sdat`: **SDAT**, the NitroSDK's
  sound archive, the DS's own format (sequences, banks, wave archives),
  beside `music.brstm`, `se.brstm` and `music.wii`, `se.wii`.
- `movie/movie001.mods`-`movie038.mods`: **Mobiclip for the DS**
  (Actimagine), 2 GB of cut-scenes; `movie/caster.thp`, the one THP.
- The Wii's own: `strap/` (the wrist-strap screens), `hbm/` (the HOME
  Menu), `mii/RFLRes01.arc`, `misc/`, `opening.bnr`.

The game is the DS game on the Wii. Its boot screen names Square Enix's
**Pollux Engine, "Cross Platform System"**; it draws the DS's two screens
side by side on a cork board, and the game's logic, its sound and its
movies are the DS's.

## The DOL

Stripped. Entry `8000403C`; text `80004000`-`800064E0` and
`80006F80`-`802AA000` (2.6 MB, 692 403 instructions); BSS `80321EC0`
(5.4 MB); small data at `80888B00`.

`__init_registers` (`800041A8`) sets r13 = `80890B00` and r2 =
`80896440`; `tools/look.py` uses them.

### The SDK

RVL SDK `0x4199_60831`, the builds of mid and late 2008:

| Library | Build |
|---|---|
| AI, AX, DSP, DVD, EXI, SC, SI, THP | Jul 30 2008 |
| MP, MPDS, NCD, NWC24, SO, SOCKET, REX-PPC (RevoEX-2.2) | Aug 6 2008 |
| VI, GX, NAND, WPAD, KPAD | Sep 11 2008 |
| HBM | Sep 24 2008 |
| OS | Oct 2 2008 |
| RFL (Miis) | Nov 11 2008 |
| NHTTP, SSL, DWC (Nintendo Wi-Fi Connection) | Mar-Jul 2008 |

NW4R's sound (`NW4R - SND`, Oct 6 2008). The game's own code is in
namespace `mk::` (its debug windows: `mk::CFWDBW...`).

**MP and MPDS** are the RVL SDK's libraries for talking to DS consoles over
the Wii's wireless (`/dev/net/wd/command`): the DS's MP protocol, and data
sharing over it, with the NitroSDK's WM states (`WM_STATECODE_*`) and the
NitroSDK's `wh.c` wireless helper on top (`WH_StateOutStartChildMP :
WM_StartDataSharing OK`). This is how the Wii game played with the DS
game; see `07-next-session.md`.

### The names

1 760 names (`tools/names.py` -> `build/names.tsv`):

- **1 709 by kin** (`tools/kinmatch.py`). No other port has this SDK's
  builds, but six have named DOLs: a function here whose words hash as one
  there (Dolphin's checksum, immediates and branch targets masked) takes
  its name (Castlevania Judgment 719, Crystal Bearers 645, Conduit 2 101,
  Monster Hunter Tri 41, ...); then by place; then, new in this port, **by
  order**: between two such matches that follow each other in both DOLs,
  with the same number of functions between them on each side, the
  functions pair in order where their instructions are alike (opcodes
  only, 80 % or more). That names libraries built again with small
  changes: 379 functions, the 2008 WPAD among them.
- 30 by signature (Dolphin's `totaldb.dsy`, Victorious's ELF), 4 by debug
  string.
- 17 by hand (`tools/names-manual.tsv`), each with its evidence: WPAD's
  thunks and callback setters, KPAD's entry points.

Every runtime hook the game reaches resolves. The others are not in this
executable (the 2009-10 SDKs' `WPADSetAutoSleepTime`, `KPADReadEx`) or are
never called (KPAD's parameter setters; `KPADRead` is replaced whole, so
its insides do not matter).

### KPAD

This KPAD (Sep 11 2008) is laid out as Crystal Bearers' (June 2009), from
`calc_acc` (`8020250C`) to `KPADSetConnectCallback` (`80205830`), but its
`KPADiRead` is larger (0x908 bytes against 0x72C).

- `KPADRead` (`8020495C`): `li r6,0; li r7,0; b KPADiRead`.
- `KPADInit` (`80205270`): `li r3,0; li r4,0; b KPADInitEx`.
- `KPADSetConnectCallback` (`80205830`): stores the callback at +0x550 of
  the channel's 0x5C0-byte state; `KPADiConnectCallback` calls it.
- `KPADEnableStickCrossClamp` (`802060F0`): a flag `read_kpad_ext` reads
  to clamp the Nunchuk's stick to a cross.

## The input

Set up at `80173118`: `WPADRegisterAllocator`, `KPADInit`,
`KPADEnableStickCrossClamp`, and `KPADSetConnectCallback(chan, 80173100)`
for the four channels. That callback disconnects every Remote but the
first: **one player a console**. The others play on their own DS (or
online).

Read each frame at `801731E0`: `WPADProbe` and `KPADRead(chan, 8 + chan *
0xB00, 16)` for the four channels: `KPADStatus` is **0xB0** bytes, as in
Crystal Bearers.

The game then makes a DS's key state from the Wii's buttons (`801078C0`),
active low like the DS's `KEYINPUT`:

| Wii | DS |
|---|---|
| A | A |
| B | B |
| Z | Y |
| C | L |
| 1 | START |
| 2 | SELECT |
| the Nunchuk's stick past ±0.6 | the cross |
| the Remote's cross (in one of two modes, `800F1674`) | the cross |

The pointer is the touch screen. `tools/eot-keys.txt` lays these out on the
keyboard and the mouse.

## The NAND's /tmp

At boot the game copies `coolresn.rsb`, `sound/music.sdat` and
`sound/se.brstm` (41 MB) from the disc to the NAND's `/tmp`
(`cdevSoundMemoryNandArchive.cpp`), and reads them from there, so that the
disc stays free for the rest. IOS empties `/tmp` when it starts a title;
wiikit did not, and at the second boot the game found the last run's copies
there and stopped, all its threads asleep, three frames in. wiikit now
empties it at boot (`10-wiikit.md`).
