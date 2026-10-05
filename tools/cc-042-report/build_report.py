"""Claim Check 042 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

LG = colors.HexColor("#8DB36B")
FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 1 July 2025 the Nationalist Party (PN) said that “the same government that boasts about the ‘quality’ of "
        "our beaches ends up having to close them within days”, after Fajtata Bay in Marsaskala was closed to "
        "bathers two days after the government announced 13 Blue Flag beaches. We checked the dates, the causes of "
        "the closures and what the EU bathing-water data say.", lead)]
S.append(key_points([
    ("The sequence is as the PN described it.",
     "The 13 Blue Flags, Fajtata Bay among them, were announced on Saturday 28 June 2025. The Environmental Health "
     "Directorate (EHD) advised against bathing at Fajtata on Monday 30 June because foul water overflowed near the "
     "public toilets, and lifted the warning on 2 July after repeated sampling."),
    ("Closures for sewage did happen that season, but they were short and local.",
     "Qui-si-Sana (Sliema) was closed 18–24 June after a private establishment’s drain failed. Fajtata was closed "
     "for about two days. Xlendi, which the PN also listed, was closed for run-off after rain, which the Water "
     "Services Corporation said was not sewage."),
    ("The national picture is much better than ‘Red Alert’ suggests.",
     "In the EEA’s 2025 classification, 77 of Malta’s 87 bathing waters are Excellent (88.5%), none is Poor, and "
     "Fajtata has been Excellent every season since 2015. The share of Excellent sites has fallen from 92% in 2024."),
    ("Verdict: largely supported (moderate confidence).",
     "The facts the PN cited are accurate. Its wider inference, a failure of infrastructure over years, is an "
     "opinion that a single toilet overflow cannot test, and we do not rate it."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("2 days", GREENC, "From the Blue Flag announcement to the Fajtata warning"),
             ("2 days", LG, "Length of the Fajtata closure (30 Jun to 2 Jul)"),
             ("77 of 87", GREY, "Bathing waters rated Excellent by the EEA for 2025 (92% in 2024)"),
             ("0", GREY, "Sites rated Poor in 2025")]),
      Spacer(1, 4 * mm),
      up_down("Not applicable: Supported is the top of the scale. Largely supported rather than Supported because "
              "the systemic reading is an opinion and the closures were brief.",
              "Evidence that Fajtata’s closure had no sewage cause, or that the government’s statement was not what "
              "the PN reported."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the record shows"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The PN issued the statement on 1 July 2025; it is reported in full by the Malta Independent [1] and by "
           "MaltaToday [2]. We could not find it on the party’s own site, and the quotations below are the outlets’ "
           "English rendering of a statement that may have been issued in Maltese. The sentence recorded for this "
           "check, “the government celebrates Blue Flag beaches while bathing sites close for sewage "
           "contamination”, is the headline sense of that statement."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>PN statement</b>, 1 Jul 2025, in MaltaToday [2]"),
     C("“The same government that boasts about the ‘quality’ of our beaches ends up having to close them within "
       "days.” Also: “This is yet another structural failure that reveals how the Government has done nothing for "
       "years to protect and maintain the country’s infrastructure.”"),
     C("Read in full (Internet Archive copy)."), C("<b>The claim</b>")],
    [C("<b>EHD notice</b>, 30 Jun 2025, in MaltaToday, Newsbook, TVMnews [3]"),
     C("“Bathing is not recommended due to an overflow of foul water in the vicinity of the public toilets.”"),
     C("Read via the outlets; EHD site refuses automated access."), C("<b>Primary notice, second-hand</b>")],
    [C("<b>Government announcement</b>, 28 Jun 2025 [4]"),
     C("Ten beaches in Malta and three in Gozo, Fajtata Bay among them, awarded the Blue Flag; announced by the "
       "Minister for Foreign Affairs and Tourism."),
     C("Lovin Malta read; press release itself not retrievable ◆."), C("Context")],
    [C("<b>EEA</b> bathing-water data [5]"), C("Class of each of Malta’s 87 sites, 2015–2025."),
     C("Downloaded 5 Oct 2026 (data/cc-005)."), C("<b>Primary data</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Did the events the PN described happen as it said, and do they bear out the impression that "
           "Malta’s bathing sites are being closed for sewage?"))
S.append(P("<b>Evidence.</b> We split the statement into sub-claims (Section 5), dated each event from news reports of "
           "the EHD’s notices (<i>data/cc-042/events_2025.csv</i>), and took the EU-standard classification of every "
           "Maltese bathing water from the European Environment Agency (EEA), reusing the data gathered for "
           "Claim Check 005 (<i>tools/cc-042-report/calc.py</i>). The EHD’s own closure reports could not be "
           "downloaded, so every closure cause is second-hand (◆)."))
S.append(P("<b>Grades.</b> EEA data are grade C (official statistics); the notices are official but reached us through "
           "news reports (C, second-hand). The PN’s inference about infrastructure is an assertion (D). "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(85 * mm))
S.append(SectionHeading(3, "What the record shows"))
S.append(KeepTogether([fig(FIG / "fig1_events.png", width=CW * 0.98),
                       P("Figure 1. Left: three warnings around the Blue Flag announcement, with dates from news reports of "
                         "EHD notices. Right: EEA class of Malta’s 87 bathing waters by season (the number is 2025’s "
                         "Excellent sites).", cap)]))
S.append(P("<b>Timeline.</b> The Blue Flags were announced on Saturday 28 June; MaltaToday’s report of the Fajtata notice "
           "is timed 12:45 on Monday 30 June, about two days later; the warning was lifted on 2 July after “repeated "
           "sampling of seawater”, so it lasted about two days. A summary of the EHD’s official record that we saw "
           "gives 28 June to 2 July for the same event ◆; if so, the closure began on the day the flags were "
           "announced, which would make the PN’s ‘48 hours’ slightly generous to the government, not to the PN."))
S.append(P("<b>Causes.</b> At Fajtata the EHD named an overflow of foul water near the public toilets; the Labour Party "
           "called it “a problem with a public convenience” [1], and the EHD later said the irregularity in the "
           "“sewage system of the public lavatory” had been rectified [6]. That is sewage contamination of a "
           "bathing site, from a local fault. At Qui-si-Sana, the EHD traced the leak to a private establishment’s "
           "drainage ◆. At Xlendi the closure followed rain: the EHD report speaks of run-off from fields and the "
           "Water Services Corporation said no sewage was involved ◆; the PN’s list of ‘sewage spills’ "
           "(as MaltaToday paraphrases it) includes Xlendi, which overstates it."))
S.append(P("<b>The wider data.</b> In the EEA’s classification, which rests on four seasons of samples, 77 of the 87 "
           "sites are Excellent for 2025, 8 Good, 2 Sufficient and none Poor. This is lower than 2024 (80 Excellent, "
           "92%), and the share of Excellent sites has slipped from 98.9% in 2018, but it is far from a ‘red "
           "alert’. Fajtata (site A07, Triq il-Qaliet) has been Excellent in every season from 2015 to 2025. The EEA "
           "dataset also counts samples taken during short-term pollution events: 3 in 2022, 9 in 2023 and 11 in "
           "2024 (the 2025 count was not yet published). The Labour Party’s reply cited the EU report’s “over 92%” "
           "Excellent figure [1]; that is the 2024 figure, not 2025’s 88.5%."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Do the closures show a failing system, or isolated faults?", "OPEN", AMBER,
                   "Several warnings in the weeks before the statement (Qui-si-Sana, Fond Għadir, St Thomas Bay, "
                   "Fajtata) involve drainage or stormwater. Malta was found, as the PN notes, to have breached EU environmental law on sewage "
                   "discharges, and the share of Excellent sites has drifted "
                   "down since 2018.",
                   "Each cause reported by the EHD is local: a public toilet, a private establishment’s drain, "
                   "field run-off. The warnings were lifted within days after sampling, no site is rated Poor, and "
                   "Fajtata itself is Excellent in every season. The Labour Party says the PN made a national issue "
                   "of a public-convenience fault [1].",
                   "Both are partly right. The sequence the PN reported is accurate and closures for sewage did "
                   "occur; whether they reveal a structural failure over years needs an analysis of all closures "
                   "and their causes, which the EHD’s reports could support but which we could not read.",
                   label_a="FOR THE PN’S INFERENCE", label_b="AGAINST"))

S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The government celebrated 13 Blue Flag beaches, Fajtata among them, on 28 June 2025"),
     C("PN [1]"), C("The Minister for Tourism announced ten Maltese and three Gozitan Blue Flags at Golden Bay, "
                    "Fajtata Bay included [4] ◆. The Blue Flag itself is awarded by Nature Trust–FEE Malta."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Fajtata was closed to bathers within days (‘48 hours’) of the announcement"), C("PN [1]"),
     C("EHD notice 30 June; lifted 2 July [3][6]. Possibly 28 June per a summary of the EHD record ◆."),
     verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Bathing sites close because of sewage contamination in 2025"), C("PN [1]"),
     C("True for Fajtata and Qui-si-Sana. Xlendi was run-off, not sewage ◆. Closures were short; 77 of 87 sites "
       "are Excellent for 2025 and none is Poor."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>D.</b> This reflects years of government neglect of infrastructure"), C("PN [1]"),
     C("An opinion about causes and responsibility; a single public-toilet overflow cannot test it."),
     verd("NOT RATED", GREY)],
], [42 * mm, 14 * mm, 80 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict"),
      verdict_box("Largely supported", "The facts cited are accurate; the inference of systemic failure is an opinion "
                  "the data neither confirm nor refute. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Our scale rates a claim <i>Largely supported</i> when the evidence backs the substance with "
           "only minor caveats. The Blue Flag announcement, the Fajtata closure for foul water and its timing, and "
           "the occurrence of sewage-related closures that season are all documented. The caveats are that "
           "Xlendi was not sewage, that the closures were brief, and that Malta’s bathing waters remain "
           "overwhelmingly rated Excellent. Confidence is moderate because the causes come from news reports of the "
           "EHD’s notices, not the EHD’s own reports."))
S.append(P("<b>What this verdict does not say.</b> It does not say that Malta’s sewage infrastructure is adequate, "
           "or that it is not; Section 4 sets out why that needs a separate analysis. A fairer summary of the "
           "evidence: <i>“Two days after the Blue Flag announcement, Fajtata Bay was closed for about two days "
           "because of a public-toilet overflow; other sewage closures occurred that June, but Malta’s bathing "
           "waters remain mostly Excellent.”</i> The PN and the Labour Party were each right about part of this."))
S.append(callout([P("RIGHT OF REPLY", tag),
                  P("Not needed: the verdict is Largely supported.", small)], bg=PALE, bar=GREEN))
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The EHD’s closure reports and notices refuse automated access and are not archived; causes and dates are "
          "from news reports (second-hand, ◆). A maintainer can add the PDFs.",
          "We did not read the PN’s statement in Maltese or on its own site; the quotations are the outlets’ English text.",
          "The Blue Flag press release was not retrievable; the list of beaches is from Lovin Malta and a search summary ◆.",
          "We did not count every 2025 closure; the PN’s own list of nine EHD closure reports is a lead, not evidence.",
          "The EEA 2025 class is the in-season update; the EEA’s final 2025 report may differ slightly."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "The Malta Independent (1 Jul 2025). Marsascala beach goes from Blue Flag to Red Alert in 48 hours, PN says; "
          "PL responds.",
     "https://www.independent.com.mt/articles/2025-07-01/local-news/Marsascala-beach-goes-from-Blue-Flag-to-Red-Alert-in-48-hours-PN-says-6736271331"),
    ("2", "MaltaToday (1 Jul 2025). ‘From Blue Flag to Red Alert’: PN slams government over beach closures.",
     "https://www.maltatoday.com.mt/news/national/135722/from_blue_flag_to_red_alert_pn_slams_government_over_beach_closures"),
    ("3", "MaltaToday (30 Jun 2025). Fajtata Bay closed to bathers after public toilet overflow spills into sea; "
          "Newsbook; TVMnews (EHD notice).",
     "https://www.maltatoday.com.mt/news/national/135697/fajtata_bay_closed_to_bathers_after_public_toilet_overflow_spills_into_sea_"),
    ("4", "Lovin Malta (Jun 2025). Fajtata Beach Closed Due To Sewage Leak Days After Earning Blue Flag Status; "
          "Office of the Deputy Prime Minister press release, 28 Jun 2025 ◆.",
     "https://lovinmalta.com/lifestyle/announcements/fajtata-beach-closed-due-to-sewage-leak-days-after-earning-blue-flag-status/"),
    ("5", "European Environment Agency. Bathing Water Directive data (DiscoMap, DiscoData), retrieved 5 Oct 2026.",
     "https://www.eea.europa.eu/en/topics/in-depth/bathing-water"),
    ("6", "MaltaToday (Jul 2025). Fajtata Bay open to swimmers again.",
     "https://www.maltatoday.com.mt/news/national/135753/fajtata_bay_open_to_swimmers_again"),
    ("7", "MiŻien. Data and script: data/cc-042/; tools/cc-042-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="042", out=str(FIG / "report.pdf"), kicker="Water and bathing sites",
    title_lines=["From Blue Flag", "to Red Alert?"],
    subtitle_lines=["Fajtata Bay, the 2025 closures and what the", "EU bathing-water data show"],
    quote_lines=["“The same government that boasts about the ‘quality’ of", "our beaches ends up having to close them within days.”"],
    quote_size=14,
    attribution="Nationalist Party (PN), statement of 1 July 2025, as reported by MaltaToday.",
    context="After Fajtata Bay was closed two days after 13 Blue Flags were announced.",
    verdict="Largely supported", verdict_note="Sequence accurate; ‘systemic failure’ is an opinion",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and EEA data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="From Blue Flag to Red Alert – PN statement, 1 July 2025", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="From Blue Flag to Red Alert? Claim Check 042",
    pdf_subject="Tests the PN's statement on Fajtata Bay and 2025 bathing-site closures",
    story=S))
