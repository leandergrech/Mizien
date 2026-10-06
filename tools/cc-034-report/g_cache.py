"""Claim Check 034: download (and cache) Malta's attainment reports (Air Quality e-Reporting dataflow G) from the
Eionet Central Data Repository. Each file states, per pollutant and objective, the value before and after the
deduction of natural sources (Saharan dust, sea salt) and whether the limit was exceeded. Cached in out/cache/G/."""
import pathlib
import time
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "out" / "cache" / "G"
BASE = "https://cdr.eionet.europa.eu/mt/eu/aqd/g/"
UA = {"User-Agent": "Mozilla/5.0 (Mizien-factcheck/1.0; +https://github.com/leandergrech/Mizien)"}
# year -> envelope/file (the latest accepted or final-feedback resubmission for each year, as listed on 6 Oct 2026)
FILES = {
    2015: "envwfdfa/MT_DataFlow_G_Attainment_2015_retro_1_.xml",
    2016: "envwlxxnw/MT_DataFlow_G_Attainment_2016_retro.xml",
    2017: "envxaqeq/DataFlow_G_Attainment_2017_retro.xml",
    2018: "envytfadw/DataFlow_G_Attainment_2018_retro_V2.xml",
    2019: "envytfloa/DataFlow_G_Attainment_2019_retro_V2.xml",
    2020: "envyvfpkw/MT_DataFlow_G_Attainment_2020_retro_V1.xml",
    2021: "envyzwbyq/DataFlow_G_Attainment_2021_retro_V1.xml",
    2022: "envzrp2pw/DataFlow_G_Attainment_2022_retro_V3.xml",
    2023: "envzvrqaw/DataFlow_G_Attainment_2023_retro_V4.xml",
    2024: "envajbxaq/DataFlow_G_Attainment_2024_retro_V4.xml",
    2025: "envanrlvw/DataFlow_G_Attainment_2025_retro_V2.xml",
}


def fetch(refresh=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    out = {}
    for y, f in FILES.items():
        local = CACHE / f"G_{y}.xml"
        if refresh or not local.exists():
            for i in range(4):
                try:
                    req = urllib.request.Request(BASE + f, headers=UA)
                    local.write_bytes(urllib.request.urlopen(req, timeout=180).read())
                    break
                except OSError:
                    time.sleep(5 * (i + 1))
        out[y] = (BASE + f, local)
        print(y, local.stat().st_size)
    return out


if __name__ == "__main__":
    fetch()
