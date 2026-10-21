# wiikit: what this port asks of it

The port takes wiikit as a submodule at `wiikit/`, pinned first at
ce8560e, the other ports' commit, then at baa481a, this session's fix (checked on
the nine other ports), then at 241ab87, whose README names this port.

The game boots, plays and reaches its menus on wiikit as it was. Its layer
(`tools/eot.cpp`) asks only for what wiikit already offers:
`wpad_set_kpad_status_size(0xB0)` (Crystal Bearers' size, for an SDK a
year older) and `wpad_set_nunchuk(true)`.

Session 1 added one thing, game-agnostic:

**The NAND's /tmp is empty at boot** (ios.cpp). IOS deletes `/tmp` when it
launches a title; games may keep there what lives for one run. This one
copies three disc files there (41 MB) and reads its sound and resources
from the copies; wiikit kept the folder across runs, and with the last
run's copies in place the game stopped at its next boot. `ios_init` now
removes the NAND's `/tmp` (only when a NAND folder is given) before making
its folders.

What this port brought that may move into wiikit:

- **Names by order** (`tools/kinmatch.py`): with names by kin (Castlevania
  Judgment's) and Crystal Bearers' `tools/sigmatch.py`, for wiikit's
  planned `sig` (layer 3, "names by signature in stripped executables").
  It names a library built again with small changes, from any named DOL
  with a close build.
- **The DS link**: `/dev/net/wd/command`, the IOS device under the RVL
  SDK's MP and MPDS libraries, is game-agnostic. Every Wii game that
  talks to a DS (Download Play from the Wii, DS-linked modes) goes through
  it, so its emulation belongs in wiikit's `ios`, and its wire format,
  shared with ndskit, in both kits (`07-next-session.md`).
- **A gamepad as the Remote and the Nunchuk**: the left stick as the
  Nunchuk's, the buttons as A, B, C, Z, 1 and 2; the pointer stays on the
  mouse (or the right stick). wiikit has the gamepad only as the Classic.
