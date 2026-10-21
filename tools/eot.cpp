// Final Fantasy Crystal Chronicles: Echoes of Time — the port's own layer
// over the wiikit runtime.
//
// Linked into wiiboot by eot.cmake; the functions it replaces are listed in
// eot-hooks.txt, which the recompiler takes with --hooks. What belongs here
// is what only this game needs.
#include "rt.h"

namespace {

void install() {
    // This KPAD (Sep 11 2008) has a KPADStatus of 0xB0 bytes: the game reads
    // 16 of them a channel at that stride (801731E0, channels 0xB00 apart).
    wpad_set_kpad_status_size(0xB0);
    // Played with the Remote and the Nunchuk: the stick walks
    // (KPADEnableStickCrossClamp at the input set-up).
    wpad_set_nunchuk(true);
}

RtGameLayer layer("Final Fantasy Crystal Chronicles: Echoes of Time", install);

}  // namespace
