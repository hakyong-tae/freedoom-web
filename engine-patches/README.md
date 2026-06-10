# Engine patches (GPL-2.0 source disclosure)

`public/index.js`, `public/index.wasm`, and `public/index.data` are built from
[GMH-Code/Dwasm](https://github.com/GMH-Code/Dwasm) at commit
`ddf0347a4fc115b11ffb1c5710768b7c47c46698` with the patch in this folder applied.

## 0001-verse8-rewarded-revive.patch

Adds rewarded-ad revive support for the Verse8 platform:

- `src/p_inter.c` — when the console player dies (`P_KillMobj`), calls
  `Module.onPlayerDeath()` on the page so it can offer an ad-based revive.
  Skipped during demo playback and netgames.
- `src/p_user.c` — two `EMSCRIPTEN_KEEPALIVE` exports:
  - `JS_PlayerIsDead()` — lets the page check whether the revive offer still applies.
  - `JS_RevivePlayer()` — resurrects the console player in place (restores
    health, collision flags, state, view height, and weapon sprites).

## Rebuilding

```bash
git clone https://github.com/GMH-Code/Dwasm.git
cd Dwasm
git checkout ddf0347a4fc115b11ffb1c5710768b7c47c46698
git apply ../engine-patches/0001-verse8-rewarded-revive.patch
# place prboomx.wad into wasm/fs/ (see Dwasm README "PrBoomX WAD")
mkdir build && cd build
emcmake cmake .. -DCMAKE_BUILD_TYPE=Release
make
# outputs: index.js / index.wasm / index.data (+ shell index.html, unused here)
```

Built with emsdk 6.0.0, without GL4ES (software renderer only).
