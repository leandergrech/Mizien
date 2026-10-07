"""Build sketch.html (the clickable graph) from page_template.html, graph.json and precheck.json.

    python sketch/fact-ledger/build.py && python sketch/fact-ledger/precheck.py && python sketch/fact-ledger/make_page.py
"""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
safe = lambda p: (HERE / p).read_text(encoding="utf-8").replace("</", "<\\/")
page = (HERE / "page_template.html").read_text(encoding="utf-8")
page = page.replace("__GRAPH__", safe("graph.json")).replace("__PRECHECK__", safe("precheck.json"))
head = '<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
(HERE / "sketch.html").write_text(head + page, encoding="utf-8")
print("wrote", HERE / "sketch.html")
