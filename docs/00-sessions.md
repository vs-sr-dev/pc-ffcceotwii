# Session log

## Session 1 — set up, named, recompiled, played

Goal: the port set up on wiikit, the executable named and recompiled, and
as far as it would go.

Results:

* **The port set up** on wiikit (submodule, pinned at ce8560e, the other
  ports' commit). The disc (RVZ, European) extracted by `wiikit.disc` in
  about a minute: 97 files, 2.4 GB.
* **The executable** (`03-executable.md`): RFFP, stripped, the RVL SDK of
  2008, NW4R's sound, DWC, and the MP and MPDS libraries that spoke to the
  DS. The disc is the DS game's: SDAT sound, Mobiclip DS movies, the
  NitroSDK's wireless helper in the code; the Pollux Engine draws the DS's
  two screens side by side.
* **Names by kin, now by order too.** No port has this SDK's builds. Six
  have named DOLs: by hash and by place they give 1 336 names; a new pass
  in `tools/kinmatch.py` pairs, between two certain matches, functions
  alike in the same order (379 more, the 2008 WPAD among them). With 30
  signatures, 4 strings and 17 by hand (WPAD's thunks and setters, KPAD's
  entry points, each with its evidence): 1 760 names, every hook the game
  reaches.
* **Recompiled at the first try**: 16 174 units, 692 403 instructions, 171
  switch tables (4 not resolved), no bad target. Built in 39 s.
* **Booted at the first try**, on wiikit as it was, with only the port's
  layer (`tools/eot.cpp`: `KPADStatus` of 0xB0, the Nunchuk): the strap
  screen, the Square Enix and Pollux Engine logos, the title, at 30 frames
  a second.
* **The NAND's /tmp** (wiikit). The second boot stopped three frames in,
  every thread asleep. The game copies three files of the disc (41 MB) to
  the NAND's `/tmp` at boot and reads them from there; IOS empties `/tmp`
  when it starts a title, and wiikit kept the last run's copies, which the
  game did not expect. wiikit now empties it at boot: boots in a row reach
  the title every time.
* **The input** (`03-executable.md`). One player a console: the game's
  connect callback disconnects every Remote but the first. It turns the
  Wii's buttons into a DS's key state (A, B; Z as Y, C as L, 1 as START,
  2 as SELECT; the stick as the cross) and the pointer into the touch
  screen. `tools/eot-keys.txt` lays them out.
* **Scripted runs** reach "Create Your Hero" and the name entry by
  themselves.
* **Played by the user**, keyboard and mouse: "everything seems to work".
* **The DS link**, studied: the RVL SDK's MP library opens
  `/dev/net/wd/command` and speaks to it in ioctlv 0x1000-0x1010
  (`802067FC`); the plan is in `07-next-session.md`.
* **Published**: playable until proven otherwise. wiikit's README names
  the port; the nine other ports moved to the new wiikit.
