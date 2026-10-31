if (lid_t >= 0 && world_active()) {
    lid_t += 1;
    lid = min(1, lid_t / 28);   // lid stop aligned to snd_chest_open (~0.468 s)
    if (lid >= 1) lid_t = -1;
}
