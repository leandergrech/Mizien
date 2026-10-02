# Archive

If an authority edits or deletes a statement, this folder is how the record of what was said survives.

`manifest.csv` lists every claim source with:

- a Wayback Machine snapshot URL (`archived_url`),
- the SHA-256 of the page as fetched (`sha256`) and when (`retrieved_utc`).

## Fill it in

```
pip install -r scripts/requirements.txt
python scripts/archive_sources.py            # fetch, hash, look up or request Wayback snapshots
python scripts/archive_sources.py --no-save  # look up existing snapshots only
```

The script is polite (one request every few seconds) and respects `robots.txt`. Sources that block automation are
marked `robots_disallowed`: open them in a browser, save a snapshot at https://web.archive.org/save/ and paste the
resulting URL into the manifest by hand.

Do not commit paywalled PDFs or full copies of articles. Links and hashes are enough.

The manifest starts with every row `pending`. Run the script once after the repository is created.
