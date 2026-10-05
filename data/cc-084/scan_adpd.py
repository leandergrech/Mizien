"""Scan ADPD's WordPress posts since 1 Feb 2026 for the 'tripled' wording (CC-084)."""
import urllib.request, json, re, html
for p in range(1, 8):
    try:
        u = f"https://adpd.mt/wp-json/wp/v2/posts?per_page=50&page={p}&after=2026-02-01T00:00:00&_fields=date,link,content"
        r = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        j = json.load(urllib.request.urlopen(r, timeout=40))
    except Exception as e:
        print("page", p, e)
        break
    print("page", p, len(j), "posts")
    for x in j:
        t = html.unescape(re.sub(r'<[^>]+>', ' ', x['content']['rendered']))
        for m in re.finditer(r'(?i)(tripl|three times|tliet darbiet|tlett darbiet|15-il sena|15 years|15 il-sena|1,338,841|1\.3 million)', t):
            print(x['date'], x['link'], t[max(0, m.start()-200):m.end()+200].replace('\n', ' '))
            print('--')
