# CEA Daily Coal Stock — dashboard

A single-page dashboard for the Central Electricity Authority's daily coal stock
reports. Drop the workbooks into **`CEA Reports/`**, push, and the site shows the
all-India position, plant-wise detail, trends over any period and a comparison
between any two dates.

Everything runs in the browser. There is no server, no build step and no upload —
the workbooks are read on the reader's own machine.

---

## Putting it on GitHub

1. Create a repository and copy these files into it, keeping the layout below.
2. Put your reports in `CEA Reports/`, named by their date: `26-08-2026.xlsx`,
   `25-08-2026.xls`, and so on. Both CEA exports are read and may be mixed.
3. Push.
4. In **Settings → Pages**, set *Source* to **Deploy from a branch**, branch
   `main`, folder `/ (root)`. Your dashboard appears at
   `https://<user>.github.io/<repo>/`.

Adding a report later is just a matter of dropping the file into
`CEA Reports/` and pushing. The included GitHub Action rebuilds
`CEA Reports/manifest.json`, which is how the page knows what is in the folder.
If you would rather not use Actions, run `python tools/make_manifest.py` before
committing — or delete the manifest entirely and let the page fall back to the
GitHub contents API, which lists the folder without any manifest at all.

```
your-repo/
├── index.html                        the whole dashboard, one file
├── CEA Reports/
│   ├── 26-08-2026.xlsx               your daily reports
│   ├── 25-08-2026.xls
│   └── manifest.json                 generated; lists what is in the folder
├── tools/make_manifest.py            regenerates the manifest
├── .github/workflows/build-manifest.yml
└── README.md
```

### Keeping the repository private

GitHub Pages needs a paid plan to serve a private repository. If your data
shouldn't be public, keep the repository private and open `index.html` straight
from your own disk instead — see below.

## Running it without GitHub

- **Straight off your disk.** Open `index.html` in Chrome or Edge and point it at
  the folder when asked. The browser remembers the folder, so afterwards it opens
  directly into the dashboard. Choosing the repository root is fine; it looks
  inside `CEA Reports/` on its own.
- **From a local server.** Run `python -m http.server 8000` in the repository and
  open `http://localhost:8000/`.
- Firefox and Safari can read the folder but cannot remember it, so you pick it
  each time. Dragging files onto the page works in every browser.

---

## What it shows

| View | What it answers |
|---|---|
| All-India position | Headline stock, days of stock, critical plants, day-on-day change, and splits by state, mode, sector and category |
| Power plants | Every plant, sortable on any column, exportable to CSV |
| Trend over a period | Any metric across any date range, daily or averaged weekly or monthly, optionally split by state, sector, mode, genco or plant |
| Compare two dates | Movers charts and a plant-by-plant delta table between any two reports |

Filters in the left panel apply to all four views: state, mode of transport,
coal source, days of stock, sector, report category, genco, the CEA critical
flag, and free-text search.

**What changed** on the front page lists, against the previous report: plants
that fell below the critical threshold, plants CEA newly flagged critical,
plants that recovered, and the largest falls in days of stock.

**Print daily brief** produces a one-page summary and opens the print dialogue —
print to PDF to circulate it.

## How the numbers are worked out

- **Days of stock = total stock ÷ daily requirement at 85% PLF**, both taken from
  the report. Group figures use total stock ÷ total requirement for the group,
  not an average of the plants' days.
- Stock is in thousand tonnes (TT); capacity in MW.
- *Critical* is CEA's own flag: stock below 25% of normative stock. The colour
  bands (under 4 days / 4–7 / 7–15 / 15 and over) are separate and yours to
  change — edit **Band thresholds** in the left panel and every chart, table,
  alert and the brief follow. The setting is remembered.
- Plants on more than one mode (`RAIL-Sea-ROAD`) count under each mode, so
  mode-wise plant counts add to more than the total.
- Category C (plants not in operation) is left out by default, because zero stock
  at zero PLF distorts the averages. Switch it on under **Report category**.
- Columns are found by their headings rather than their position, so the modern
  `.xlsx` and the older JasperReports `.xls` both read correctly, and percentages
  written as `73%` are handled alongside decimals.
- Spelling variants in the source (Uttar Pardesh, Chhatisgarh, West Bangal, the
  RAIIL typo) are normalised so filters don't split a state in two.
- Reports are matched plant by plant on the station name, because CEA sometimes
  moves a plant between states between editions. Where one export leaves the
  owner blank for categories B, C and D, the name is filled in from any other
  loaded report.

## Notes

- The newest report is parsed first so the dashboard opens straight away; older
  files load behind it, with progress shown in the top bar.
- Parsed reports are cached in the browser, so a folder holding a year of files
  is read only once. **Clear cache and start over** forces a re-read.
- To use a different folder name, change `DATA_DIR` near the top of the script in
  `index.html` and the path in `tools/make_manifest.py`.
