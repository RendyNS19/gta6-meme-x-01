[![gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/RendyNS19/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/RendyNS19/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

# The biggest heist wasn't in the game

A WANTED poster for GTA VI's launch day: 24.6 million players paid an
estimated $2.36 billion in one day (Sensor Tower estimate) — the biggest
heist in Leonida happened at the checkout, not in the game. The make.fun
ghost (official press-kit mark) is the one holding the loot; the punchline
is that my AI agent did the work.

![The meme](meme.png)

`meme.png` (1600x900) is generated deterministically by `generate.py`
(Python + Pillow, no network, no randomness — re-running it produces
byte-identical output). The sunset scene, palms, skyline, money bag and
layout are all drawn by the script; the ghost is make.fun's official
press-kit mark (`assets/mark-1024.png`, https://make.fun/press).

## The post (to be posted by the account owner from @desyles1)

Attach `meme.png` as the first picture, with this caption:

> GTA VI made $2.36B in one day (est.). 24.6M players paid for the biggest heist in Leonida — and I wasn't even the one robbing the bank 😂
>
> My AI agent did the work on make.fun — and agents there earn real USDC for making stuff like this.
> Play code: makefun-latch-condor-planet
> @makefunai #GTA6 #GTAVI

`POST.json` holds the post's address once it is live; replace the
placeholder before submitting:

```json
{"url": "https://x.com/<handle>/status/<id>"}
```

## How the program works

`main.ts` (Node 22, standard library only) copies `POST.json` from the
repository root to the output directory, where the gate reads it. That is
all it has to do — the entry is the post itself; the house reads the post
from X (first picture, then text) and hands it to the judge.

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```
