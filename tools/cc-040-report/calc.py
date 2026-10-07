"""CC-040: test 'per capita water consumption today stands at around 110 l/cap/day' (E&WA keynote, IWRA 2024).

Data (Eurostat dissemination API, retrieved 7 Oct 2026):
  env_wat_cat  wat_proc=PWS (public water supply), nace_r2=EP_HH (households), unit=MIO_M3
  demo_pjan    population on 1 January (total)
Per-capita figure = households' volume / mean of 1 Jan population of year Y and Y+1, in litres per day.
"""
import csv, json, subprocess, sys, datetime, pathlib
OUT = pathlib.Path(__file__).resolve().parents[2] / 'data' / 'cc-040'
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'
EU27 = 'AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK'.split()

def get(ds, q):
    j = json.loads(subprocess.check_output(['curl', '-sS', f'{BASE}{ds}?format=JSON&lang=EN&{q}']))
    dims, sizes = j['id'], j['size']
    idx = {d: list(j['dimension'][d]['category']['index']) for d in dims}
    for pos, v in j['value'].items():
        p = int(pos); c = []
        for s in reversed(sizes): c.append(p % s); p //= s
        c.reverse()
        r = {d: idx[d][i] for d, i in zip(dims, c)}
        r['v'] = v; r['flag'] = j.get('status', {}).get(pos, '')
        yield r

hh = {}
for r in get('env_wat_cat', 'wat_proc=PWS&nace_r2=EP_HH&unit=MIO_M3&sinceTimePeriod=2013'):
    hh[(r['geo'], int(r['time']))] = (r['v'], r['flag'])
pop = {}
for r in get('demo_pjan', 'age=TOTAL&sex=T&sinceTimePeriod=2013'):
    pop[(r['geo'], int(r['time']))] = r['v']

rows = []
for (g, y), (v, f) in sorted(hh.items()):
    if (g, y) in pop and (g, y + 1) in pop:
        p = (pop[(g, y)] + pop[(g, y + 1)]) / 2
        rows.append(dict(geo=g, year=y, hh_mio_m3=v, flag=f, pop_mean=round(p), l_cap_day=round(v * 1e6 * 1000 / p / 365, 1)))
with open(OUT / 'households_pws_per_capita.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]) + ['source', 'retrieved'])
    w.writeheader()
    for r in rows:
        w.writerow(r | dict(source='Eurostat env_wat_cat (PWS, EP_HH) / demo_pjan', retrieved='2026-10-07'))

mt = {r['year']: r for r in rows if r['geo'] == 'MT'}
print('Malta households, public water supply, l/cap/day')
for y in sorted(mt): print(y, mt[y]['hh_mio_m3'], mt[y]['flag'], mt[y]['l_cap_day'])
# latest year per EU-27 state, 2020 onwards
latest = {}
for r in rows:
    if r['geo'] in EU27 and r['year'] >= 2020:
        if r['geo'] not in latest or r['year'] > latest[r['geo']]['year']: latest[r['geo']] = r
rank = sorted(latest.values(), key=lambda r: r['l_cap_day'])
print('\nEU-27 latest (2020+), ascending')
for i, r in enumerate(rank, 1): print(i, r['geo'], r['year'], r['l_cap_day'])
vals = sorted(r['l_cap_day'] for r in rank)
n = len(vals); med = vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2
print('n', n, 'median', med, 'Malta rank (1=lowest)', [r['geo'] for r in rank].index('MT') + 1)
# common year 2022 comparison
c22 = sorted((r['l_cap_day'], r['geo']) for r in rows if r['year'] == 2022 and r['geo'] in EU27)
print('\n2022 common year', len(c22), c22)
json.dump(dict(malta=mt, n=n, median=med, rank=[(r['geo'], r['year'], r['l_cap_day']) for r in rank]), open(OUT / 'summary.json', 'w'), indent=1)

# Malta: all uses of public water supply (households + services incl. hotels + industry ...), l/cap/day, same population basis
tot = {}
for r in get('env_wat_cat', 'geo=MT&wat_proc=PWS&nace_r2=TOTAL_HH&nace_r2=G-U&unit=MIO_M3&sinceTimePeriod=2013'):
    tot[(r['nace_r2'], int(r['time']))] = r['v']
checks = []
for y in (2019, 2022, 2023, 2024):
    p = mt[y]['pop_mean']
    checks.append(('MT_all_uses_PWS_l_cap_day', y, round(tot[('TOTAL_HH', y)] * 1e9 / p / 365, 1)))
    checks.append(('MT_services_PWS_l_cap_day', y, round(tot[('G-U', y)] * 1e9 / p / 365, 1)))
    checks.append(('MT_households_PWS_l_cap_day', y, mt[y]['l_cap_day']))
checks.append(('MT_households_vs_110_pct_2024', 2024, round((mt[2024]['l_cap_day'] / 110 - 1) * 100, 1)))
checks.append(('EU27_median_l_cap_day_latest', 2024, med))
checks.append(('MT_rank_lowest_first_of_n', 2024, f"{[r['geo'] for r in rank].index('MT') + 1} of {n}"))
checks.append(('MT_vs_EU_median_pct', 2024, round((mt[2024]['l_cap_day'] / med - 1) * 100, 1)))
with open(OUT / 'checks.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['check', 'year', 'value', 'source', 'retrieved'])
    for c in checks: w.writerow(list(c) + ['Eurostat env_wat_cat, demo_pjan (tools/cc-040-report/calc.py)', '2026-10-07'])
for c in checks: print(c)
