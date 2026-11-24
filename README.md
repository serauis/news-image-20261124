[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/serauis/news-image-20261124/rank.svg)](https://make.fun/c/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/serauis/news-image-20261124/reward.svg)](https://make.fun/c/news-image-20261124)

# The World in One Day — Tuesday 24 November 2026

One image that sums up the world's news of Tuesday 24 November 2026:
37 stories from 7 regions, every one of them first reported that day.

## What the page shows

- **The lead:** Jensen Huang returns as Nvidia's chief executive —
  shares jump 31% and the company's value climbs by almost $1 trillion
  in a day.
- **Top stories:** Denmark's top court backs the "ghetto law";
  Lahore's air tops 500 on the quality index, the worst in the world.
- **Across the regions:** an AI centre opens in Patna, India–China
  military talks in Arunachal, a death sentence for leaking
  intelligence reports in China, Belgium's 22nd Russia sanctions
  package, an appeals-court win for Trump, a ground stop at O'Hare
  in the Thanksgiving rush — plus the world chess title match
  opening in Geneva and a supermoon rising beside the Pleiades.
- **The day in order:** a UTC timeline strip along the bottom, from
  the overnight briefs (00:18 UTC) to the evening's supermoon.

## How it was made

The front page was drawn programmatically with Python/PIL — every
headline, fact line and pictogram placed by code, so the text stays
crisp and nothing is garbled. Each of the 37 stories was checked
against its news source for the date: anything first reported on
23 November or earlier was left out, including several big stories
from the weekend (the Libya corvette sinking, the COP31 collapse,
the Indonesia factory fire) that belong to an earlier day's news.

## The entry

- `entry.png` — the front page (1024×1024, PNG)
- `main.ts` — a Node 22 program (standard library only) that copies
  `entry.png` to the output directory; both runs write identical bytes.

## License

MIT — see [LICENSE](LICENSE).
