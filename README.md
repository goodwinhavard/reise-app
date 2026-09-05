# reise-app

A travel journal. The public site is a single static page, [index.html](index.html),
that reads [travel_data.json](travel_data.json) and the [photos/](photos/) folder and
renders a map, per-trip cards and photo galleries. No build step, no server code.

## Editing content

Edit `travel_data.json` by hand (or keep using the Streamlit app in `app.py` /
`pages/` locally to edit, then commit the updated JSON). Each entry:

```json
{
  "name": "Skopje",
  "country": "North Macedonia",
  "start_date": "2025-10-03",
  "end_date": "2025-10-07",
  "text": "Free-text notes, shown as-is.",
  "locations": [{ "cname": "Skopje", "x_coord": 41.99, "y_coord": 21.43 }],
  "photos": ["photos\\Skopje\\IMG_4261.JPEG"]
}
```

- `x_coord` = latitude, `y_coord` = longitude. Locations outside ±90 / ±180 are
  skipped on the map (e.g. the `999` placeholder).
- Photo paths may use `\\` or `/`; put the files under `photos/<folder>/`.
- If `country` isn't in the flag list in `index.html` (`ISO2`), add its two-letter
  code there to get a flag.

## Viewing locally

Browsers block `fetch` from `file://`, so run a tiny server from the repo root:

```
python -m http.server
```

then open <http://localhost:8000>.

## Publishing (Netlify or Vercel)

The repo root is the site — nothing to build.

**Netlify:** drag the project folder onto <https://app.netlify.com/drop>, or
"Add new site" → import from Git and leave build command empty, publish directory `.`.

**Vercel:** "Add New Project" → import the repo → Framework Preset **Other** →
leave build & output settings empty → Deploy.

Every push to the default branch redeploys. The `photos/` folder (~145 MB) is
served as-is; if pages feel slow, downscale the largest JPEGs.
