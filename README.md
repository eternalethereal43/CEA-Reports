# CEA Daily Coal Stock — dashboard

A single-page dashboard for the Central Electricity Authority's daily coal stock
reports. Drop the workbooks into the repository, push, and the site shows the
all-India position, plant-wise detail, trends over any period and a comparison
between any two dates.

Everything runs in the browser. There is no server, no build step and no upload —
the workbooks are read on the reader's own machine.

---

## Putting it on GitHub

1. Create a repository and copy these files into it.
2. Put your reports **in the root of the repository, beside `index.html`**, named
   by their date: `26-08-2026.xlsx`, `25-08-2026.xls`, and so on. Both CEA
   exports are read and may be mixed.
3. Push.
4. In **Settings → Pages**, set *Source* to **Deploy from a branch**, branch
   `main`, folder `/ (root)`. Your dashboard appears at
   `https://<user>.github.io/<repo>/`.

Adding a report later is just a matter of dropping the file in and pushing. The
included GitHub Action rebuilds `manifest.json`, which is how the page knows what
is there. If you would rather not use Actions, run `python tools/make_manifest.py`
before committing — or delete the manifest entirely and let the page fall back to
the GitHub contents API, which lists the repository without any manifest at all.

```
your-repo/
├── index.html                    the whole dashboard, one file
├── 26-08-2026.xlsx               your daily reports, in the root
├── 25-08-2026.xls
├── manifest.json                 generated; lists what is there
├── tools/make_manifest.py        regenerates the manifest
├── .github/workflows/build-manifest.yml
├── .nojekyll                     publish the files as they are
└── README.md
```

Reports may also be kept in a sub-folder — `CEA Reports`, `Reports` or `data` are
all checked, and on GitHub the whole repository listing is read, so any folder
works. The root is simply what it looks at first.

### If a newly added report doesn't appear

Press **Check for new reports** in the top bar — it re-reads the folder without a
page reload. If it is still missing:

- The page merges every source it can see, and also asks directly for the last
  twelve dates, so a `manifest.json` that was not regenerated cannot hide a
  recent file. An older report added long after the fact does need the manifest
  rebuilt: run `python tools/make_manifest.py`, or let the Action do it.
- GitHub Pages takes a minute or two to publish, and its CDN may hold the old
  copy briefly. A hard refresh (Ctrl+Shift+R, or Cmd+Shift+R) clears it.
- Check the file name is exactly `DD-MM-YYYY.xlsx` or `.xls`.

### If the site loads but shows no reports

The page says so plainly and lists every location it tried — open **What it
tried** on the message. The usual causes:

- **The files are not named by date.** They must be `DD-MM-YYYY.xlsx` or `.xls`.
  A name like `26-08-2026 (1).xlsx` or `DailyCoalReport.xlsx` is skipped.
- **Pages has not finished publishing.** Check the Actions tab; a push takes a
  minute or two to appear.
- **GitHub API rate limit.** The listing call is limited to 60 an hour per
  address. Running `python tools/make_manifest.py` and committing the result
  removes that call entirely.

### Keeping the repository private

GitHub Pages needs a paid plan to serve a private repository. If your data
shouldn't be public, keep the repository private and open `index.html` straight
from your own disk instead — see below.

## Running it without GitHub

- **Straight off your disk.** Open `index.html` in Chrome or Edge and point it at
  the folder when asked. The browser remembers the folder, so afterwards it opens
  directly into the dashboard.
- **From a local server.** Run `python -m http.server 8000` in the folder and open
  `http://localhost:8000/`.
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
- To search a different folder, edit `DATA_DIRS` near the top of the script in
  `index.html`.
