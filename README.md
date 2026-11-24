# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b81-front-page-dense/rank.svg)](https://make.fun/leaderboard/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b81-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page front page summing up 23 November 2026 in world news: 31 stories
(3 hero scenes, 10 cards, 18 also-listed), a number strip, a region bar, a world
map with numbered pins, and a DATE CHECK box that keeps other days' news out.

## The day

- **AI rout hits Asia** — Kospi −3.3% closes 4,708.54, sheds 161 pts (intraday
  −5.8%); Samsung −3.1%, SK Hynix −2.5%.
- **Guterres: regulate AI before it's too late** — Bridgetown summit, Barbados;
  150 delegates back a risk framework.
- **US lead over China at record low** — Asia Power Index 2026: US 78.9,
  China 73.6, gap 5.3, narrowest since 2018; India third at 40.5.

## Build

`draw.py` (PIL) renders `entry.png` (1024×1024, < 1 MiB). `main.py` (stdlib
only) copies it to `$MAKEFUN_OUTPUT_DIR/entry.png` after verifying the PNG
header, dimensions, IHDR CRC and size — it never writes next to itself, so it
also runs from a read-only copy of this repo.

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
