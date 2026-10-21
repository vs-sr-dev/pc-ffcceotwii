# Next session

The game plays with the keyboard and the mouse (`00-sessions.md`, session
1). Two kinds of work are ahead: the whole game played through, and the
link with the DS edition.

## 1. Play further

- A longer game: the first dungeon, a boss, a save and a load, the movies
  (Mobiclip DS, `movie/*.mods`, decoded by the game's own code: check
  their picture and sound, and their speed).
- The menus and the touch screen's parts with the pointer: the magic ring,
  the inventory, the forge, the mail.
- The sound: SDAT sequences played by the game on AX (`music.sdat`,
  `se.sdat`, copied to `/tmp`); listen for gaps at loads.
- A gamepad as the Remote and the Nunchuk (`10-wiikit.md`), if the
  keyboard is not enough.

## 2. The DS link (wiikit and ndskit)

The two editions played together: up to four players, Wii and DS mixed,
over the DS's own wireless (MP), locally, and over Nintendo Wi-Fi
Connection. The Wii speaks MP through the RVL SDK's MP library (Aug 6
2008) and MPDS (data sharing over MP), on IOS's `/dev/net/wd/command`;
the game's code above them is the NitroSDK's `wh.c` (`WH_*`, `WM_*`
states), the DS edition's own.

What is known (`03-executable.md`):

- MP opens `/dev/net/wd/command` at `80206FC0`; `802067FC(ioctl, n_in,
  n_out, vectors)` sends ioctlv to it. Seen: 0x1000 (from `80207074`),
  0x1002, 0x1004, 0x1006, 0x1007, 0x1008, 0x100E, 0x1010, and two more
  whose number is in a register.
- MP spans `80206FC0`-`8020AC74`, MPDS follows at `8020AC74`.
- The game's menus for it: `mk::CFWDBWWireless{Top,Parent,Child,ChildWait}`
  and `mk::CFWDBWWiFi*`.

Steps:

1. **Name MP and MPDS** (their debug strings, their order; the RVL SDK's
   MP API: `MPStartup`, `MPOpenPort`, `MPSend`...). Find what the game asks
   of them: parent only (the Wii hosts, the DS joins), as the RVL SDK's MP
   allows?
2. **WD in wiikit** (`ios.cpp`): the device and its ioctlv, each one's
   vectors, from the library's code (Dolphin's `IOS/Network/WD` names a
   few). First answer as a Wii with nobody near: the game's local mode
   must fail as on a console alone.
3. **A virtual MP on UDP**, shared by wiikit and ndskit: beacons with the
   GGID and the game's info, a child's association, the MP frames
   (parent's send, children's replies) at the DS's cadence, the data
   sharing's rounds. The Wii's WD on one side, the DS's WM (the ARM7's
   wireless, HLE in ndskit) on the other.
4. **Two Wii ports first**: two wiiboot on one PC, one hosting: does the
   other edition's absence matter? (The Wii game may host only DS
   children: then a DS port is needed, `ffcceotds` on ndskit.)
5. **ffcceotds on ndskit**, then the two together.

Online (DWC) is a separate road: Nintendo Wi-Fi Connection closed in 2014;
the community's replacement servers speak its protocol.

## 3. Smaller things

- `ios: open /dev/net/kd/request: no such device` and
  `/dev/net/ncd/manage`: WiiConnect24 and the network config, as in the
  other ports; harmless so far.
- "Failed to register network shutdown function. -29" (NWC24): the same.
