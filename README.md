# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/dudukuyz/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/dudukuyz/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world's news of Friday, 20 November 2026 — drawn
as a newspaper front page. The lead story is the first-ever Trump–Xi–Putin
trilateral meeting in Shenzhen and the peace declaration it produced, with
Cyclone Akvan bearing down on India, Russian strikes damaging embassies in
Kyiv, a migrant boat sinking off Senegal, and the APEC leaders' summit, plus
the day's other headlines (a record $190.4m Van Gogh, Nicholls' unbeaten
century, Anthropic's reported $1.5 trillion valuation, and Modi meeting the
Prince and Princess of Wales).

`render_poster.py` draws the poster with Pillow (standard fonts, no network)
and writes `entry.png` (1024×1024, about 140 KB). `main.py` is the entry
program: it checks the image is a whole PNG within the 1024×1024 and 1 MiB
gates, then copies it to `/output/entry.png` — deterministic, so both grading
runs write the same bytes. `poster.html` is the design the Pillow renderer
follows.

## Run it

```sh
python3 render_poster.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=t32jh3bx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
