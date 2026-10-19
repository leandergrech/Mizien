"""Claim Check 126 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 22 June 2026 the Partit Nazzjonalista said that the Government “has signed an agreement for just nine months” with BP “without "
        "providing any details about the price”, and that “the Labour Government had promised that by this year Malta would have a pipeline "
        "for gas supply so that the country would no longer depend on the tanker in Marsaxlokk. But here too, it has failed.” "
        "<b>The contract facts hold; the pipeline is not built; but we could not find the dated promise.</b> The BP supply runs to the end "
        "of May 2027: 9.6 months from the expiry of the old contract, 11.3 from the announcement. No price was published, though Enemalta "
        "said it is linked to the TTF gas index. The pipeline is unbuilt, and its promoter’s own page gives 2030 as indicative "
        "commissioning. But we found no Labour statement promising it “by 2026”.", lead)]
S.append(key_points([
    ("“Just nine months” is a fair description.", "Supply is secured “till the end of May 2027” (Enemalta); SOCAR’s contract ends 13 Aug 2026: 291 days, 9.6 months. The start date of BP supply is not published."),
    ("No price was published.", "Enemalta’s release gives no price or volume; The Shift reports that neither Enemalta nor the Ministry disclosed the expected cost. The release does say the price is linked to the TTF index, a detail PN’s wording leaves out."),
    ("The pipeline is not built.", "The promoter’s page (updated Dec 2022) lists construction start 2028 and commissioning 2030 as indicative; Labour’s 2026 manifesto still speaks of studies and seeking EU funds."),
    ("“Promised by this year” is not shown.", "We found no Labour document or statement dating the pipeline to 2026. Dated targets we found second-hand were 2024 and 2025; the 2017 manifesto reportedly said “shortest time possible”."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("9.6 mo", GREEN, "From SOCAR expiry (13 Aug 2026) to end of May 2027; 11.3 months from the 21 Jun announcement"),
             ("0", AMBER, "Prices or volumes published for the BP contract (TTF link disclosed)"),
             ("2030", ORANGE, "Pipeline commissioning date on its promoter’s page (indicative; page updated Dec 2022)"),
             ("0", RED, "Labour statements found dating the pipeline to 2026")]),
      Spacer(1, 4 * mm),
      up_down("A Labour manifesto, ministerial or Enemalta statement that dates the pipeline to 2026 would move the pledge sub-claim to supported and the whole to Largely supported.",
              "Documents showing the pipeline was never promised, or was promised only for dates after 2026, would move it to Misleading."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the evidence shows"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The words are from a Partit Nazzjonalista statement of 22 June 2026, “Government must immediately publish the price and conditions of the "
           "gas supply agreement with BP”, English text as published by the party; we read it in full on 19 October 2026 [1]."))
S.append(callout([P("THE PARTY’S WORDS (22 JUNE 2026)", tag),
                  P("“Now, the Government has signed an agreement that will cover only nine months, without providing any details about the price at "
                    "which it will be purchasing gas.” … “The Labour Government had promised that by this year Malta would have a pipeline for gas "
                    "supply so that the country would no longer depend on the tanker in Marsaxlokk. But here too, it has failed.”", small)], bg=PALE, bar=GREEN))
S += [Spacer(1, 3 * mm), P("The statement also says the Government “has signed an agreement for just nine months” (in its sub-heading), speaks of "
        "“management by crisis” and of thousands of families starting summer “with candles and fans”. Those are opinion or context and are not rated.")]
S.append(std_table([
    [C("Source", cellh), C("What it gives", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Partit Nazzjonalista</b>, press release 22 Jun 2026 [1]"), C("The four statements above."), C("Read in full."), C("<b>The claim</b>")],
    [C("<b>Enemalta</b>, release 21 Jun 2026 [2]"), C("Supply “till the end of May 2027”; TTF-linked; seven bidders; no price."), C("Read in full."), C("<b>Primary</b>")],
    [C("<b>Italpress/MNA</b>, 22 Jun 2026 [3]"), C("Announcement by the PM; SOCAR contract expires 13 Aug; price not disclosed."), C("Read in full."), C("Outlet text")],
    [C("<b>The Shift</b>, 22 Jun 2026 [4]"), C("Neither Enemalta nor the Ministry disclosed the expected cost; no reply to its questions."), C("Read in full."), C("Outlet text")],
    [C("<b>Melita TransGas</b> (Interconnect Malta Ltd), project page [5]"), C("Pipeline description, milestones, indicative 2028 construction and 2030 commissioning."), C("Read in full; page last updated 22 Dec 2022."), C("<b>Primary</b> (state promoter)")],
    [C("<b>Labour</b> manifesto 2026, pledge 16.7 [6]"), C("Hydrogen-ready pipeline studies complete; will keep seeking EU funds."), C("Our own summary in data/manifesto_pledges.csv (6 Oct 2026); not re-opened."), C("Primary, via our summary")],
    [C("Labour’s <b>dated</b> pipeline promise"), C("The statement or document dating the pipeline to 2026."), C("Not found in any readable source."), C("Gap")],
], [44 * mm, 52 * mm, 50 * mm, 24 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The Opposition’s own 2022 programme also proposed a gas pipeline to Sicily to “end reliance on the Electrogas tanker” (our summary of "
                 "pledge MP-PN-2022-217 [7]); its 2026 programme proposes studying a hydrogen-ready pipeline. Government and Opposition statements on "
                 "energy are held to the same standard (CC-095, CC-113, CC-027).", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is the BP agreement as the party describes it (length, price disclosure), and is it true that a pipeline was promised by 2026 and has not been delivered?"))
S.append(P("<b>Evidence.</b> The contract facts come from Enemalta’s release and two outlets that read it (19 Oct 2026). The term arithmetic is in "
           "<i>tools/cc-126-report/calc.py</i> with outputs in <i>data/cc-126/checks.csv</i>. For the pipeline we read the promoter’s page, and searched for Labour’s "
           "promise (see the search log in <i>literature/CC-126/notes.md</i>). No peer-reviewed literature bears on a contract term or a political promise; "
           "we rely on official and promoter documents (grade C) and mark second-hand material ◆."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(P("The contract", h2))
S.append(P("Enemalta says the BP agreement “will secure LNG supply till the end of May 2027” and that the existing SOCAR contract expires on 13 August "
           "(Italpress [3]). The party’s “nine months” is the supply period after the old contract ends: 291 days, 9.6 months. Counted from the announcement "
           "of 21 June it is 344 days, 11.3 months. Enemalta did not publish the date supply under the BP agreement starts, so we cannot say which count the "
           "Government would use [2, 3]."))
S.append(fig(FIG / "fig_term.png"))
S.append(P("Figure 1. The BP supply period counted two ways.", cap))
S.append(P("On price, Enemalta’s release gives the mechanism (“linked to the Title Transfer Facility (TTF) index”) but no price, margin or volume [2]. "
           "Italpress says the Prime Minister “did not disclose the price agreed” [3] and The Shift reports that neither Enemalta nor the Energy Ministry disclosed "
           "the expected cost, with no reply to its questions [4]. A TTF link is a detail about the price; the statement that no “details about the price” were given "
           "is therefore a little stronger than the record: the formula’s reference was disclosed, the price was not."))
S.append(P("The pipeline", h2))
S.append(P("The promoter’s page describes the Melita TransGas pipeline as a project that “will end Malta’s isolation from the European gas network”, says "
           "the island “presently” depends on LNG by ship, and calls the current floating storage unit and regasification facility, introduced in January 2017, "
           "“an intermediate solution” [5]. Its “Next Steps” list 2028 for the indicative start of construction and 2030 for indicative commissioning (page last updated "
           "22 December 2022) [5]. In December 2025 the Prime Minister linked any future cut in electricity subsidies to completion of the pipeline, “years away” "
           "(Malta News Agency, outlet text) [8]. Labour’s 2026 manifesto, in our summary, says the hydrogen-ready pipeline studies are complete and EU funds will keep "
           "being sought [6]. A trade-press report of July 2026 describes the project as stalled and relays that EU ministers extended a derogation keeping it on the "
           "EU’s Projects of Common Interest list (relaying Times of Malta) ◆ [9]."))
S.append(fig(FIG / "fig_targets.png"))
S.append(P("Figure 2. Dated pipeline targets we found against the year in the party’s statement. ◆ the 2024 and 2025 targets are known only from Global Energy Monitor’s "
           "summary of earlier reports [10].", cap))
S.append(P("Was a pipeline “by this year” promised?", h2))
S.append(P("We found no Labour manifesto, ministerial or Enemalta statement that dates the pipeline to 2026. Global Energy Monitor’s summary reports a July 2019 expectation "
           "of completion by 2024 (MaltaToday) and a September 2020 promoter schedule of operations from 2025 ◆ [10]; a search summary of The Malta Independent’s report "
           "on Labour’s 2017 manifesto says the party pledged the pipeline in the “shortest time possible” ◆ [11]. The promoter’s own later page gives 2030 [5]. "
           "None of these is a 2026 date, and none was read in the original. This is a gap in our search, not proof that no such statement exists "
           "(search log: <i>literature/CC-126/notes.md</i>)."))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Was a gas pipeline “promised by this year”?", "NOT SHOWN", AMBER,
    "Labour has long backed the pipeline: the 2017 manifesto reportedly pledged it, the Government created a promoter company in 2018, and the 2026 manifesto still lists it ◆ [5, 6, 11]. "
    "Earlier targets of 2024 and 2025 were missed ◆ [10].",
    "No document we could read dates the pipeline to 2026; the promoter’s later page gives 2030 as indicative commissioning [5].",
    "<b>For this claim:</b> the pipeline is late against every date we found, but “by this year” is not shown. The gap makes the specific statement unsubstantiated even where the substance is plausible.",
    label_a="A PIPELINE WAS PROMISED AND IS LATE", label_b="NO 2026 DATE FOUND"))
S.append(contested(
    "Q2  “Without providing any details about the price”", "LARGELY HOLDS", GREENC,
    "No price, volume or margin was published; the Minister and Enemalta did not answer questions on cost [2, 4].",
    "Enemalta did disclose that the price is linked to TTF, and that seven bidders took part [2].",
    "<b>For this claim:</b> accurate on the price itself; omits the disclosed formula reference.",
    label_a="NO PRICE PUBLISHED", label_b="MECHANISM DISCLOSED"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The Government “has signed an agreement for just nine months”"), C("PN, 22 Jun 2026 [1]"),
     C("Supply to end of May 2027: 9.6 months from SOCAR’s expiry, 11.3 from the announcement [2, 3]; start date unpublished."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> “without providing any details about the price”"), C("PN [1]"),
     C("No price published; TTF link disclosed [2, 3, 4]."), verd("LARGELY ACCURATE", GREENC)],
    [C("<b>C.</b> “The Labour Government had promised that by this year Malta would have a pipeline for gas supply so that the country would no longer depend on the tanker in Marsaxlokk”"), C("PN [1]"),
     C("No statement dating the pipeline to 2026 found; second-hand targets 2024 and 2025 ◆; promoter: 2030 [5, 10, 11]."), verd("NOT SHOWN", AMBER)],
    [C("<b>D.</b> “But here too, it has failed” (no pipeline in place)"), C("PN [1]"),
     C("Pipeline not built; construction not started; promoter lists indicative 2030 [5, 8]."), verd("SUPPORTED", GREENC)],
], [44 * mm, 24 * mm, 66 * mm, 36 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "The contract facts and the unbuilt pipeline hold; the dated promise “by this year” is not shown. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Two of the four parts reproduce (the term, and the absence of a published price, with the TTF link omitted), and the pipeline is not in place. The "
           "central charge, that Labour promised the pipeline for 2026 and failed to keep it, rests on a date we could not find in any statement. Our scale gives "
           "<i>Not substantiated</i> where a claim is stated more strongly than the evidence available allows; the pipeline is late against every date we did find, "
           "so this is not a finding that the promise was never made. Confidence is moderate because our search for the promise was partial: Labour’s earlier "
           "manifestos and Government statements were not opened (search log in notes)."))
S.append(P("<b>What this does not say.</b> It does not assess the BP contract’s price, the Government’s energy policy, or the 21 June power cuts. It says nothing about motive."))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "The Labour manifesto (2013, 2017 or 2022) or Government statement that dated the pipeline to 2026 or earlier, with the exact wording.",
    "Whether the Government considers the pipeline’s delivery date to be 2030, as the promoter’s page says, and when that page was last confirmed.",
    "The start date of BP supply and any price the Government is willing to publish.",
])]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Status: pending right of reply (Partit Nazzjonalista). No reply has been sought by this run; the maintainer decides when and how. A comment "
                 "or document from the party would be appended.", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We did not read Labour’s 2013, 2017 or 2022 manifestos or any Government pipeline announcement in the original. The 2017 pledge and the 2024 and 2025 targets are second-hand ◆.",
          "The promoter’s page was last updated on 22 December 2022; its 2028 and 2030 dates may have been revised since.",
          "Enemalta did not publish the start date of BP supply; “nine months” depends on it.",
          "Labour’s 2026 manifesto is cited from our own summary of 6 October 2026, not re-read in this run.",
          "The contract itself was not published; we rely on Enemalta’s release and outlets reading it.",
          "Hosts refused to scripts (MaltaToday, The Malta Independent, gov.mt, meae.gov.mt) and the Wayback Machine (connection reset) could not be read."]:
    S.append(P("• " + l, bul))

S += [CondPageBreak(70 * mm), Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Partit Nazzjonalista (22 Jun 2026). Government must immediately publish the price and conditions of the gas supply agreement with BP. Read 19 Oct 2026.", "https://pn.org.mt/en/?p=29003"),
    ("2", "Enemalta (21 Jun 2026). Enemalta secures new LNG supply agreement. Read 19 Oct 2026.", "https://enemalta.com.mt/2026/06/21/enemalta-secures-new-lng-supply-agreement/"),
    ("3", "Italpress/MNA (22 Jun 2026). Malta secures LNG supply deal with BP until May 2027. Read 19 Oct 2026.", "https://www.italpress.com/?p=703189"),
    ("4", "The Shift News (22 Jun 2026). Dalli silent on LNG costs as BP deal raises questions over pricing and duration. Read 19 Oct 2026.",
     "https://theshiftnews.com/2026/06/22/dalli-silent-on-lng-costs-as-bp-deal-raises-questions-over-pricing-and-duration/"),
    ("5", "Melita TransGas Company Ltd / Interconnect Malta Ltd. Melita TransGas hydrogen-ready pipeline (project page; website last updated 22 Dec 2022). Read 19 Oct 2026.", "https://melitatransgas.com.mt/"),
    ("6", "Partit Laburista (2026). Int Malta: Manifest Elettorali 2026, chapter 16, pledge 16.7 (summary in data/manifesto_pledges.csv, 6 Oct 2026).", "https://partitlaburista.org/wp-content/uploads/2026/08/Manifest_Elettorali_INT_MALTA_2026.pdf"),
    ("7", "Partit Nazzjonalista (2022). Viżjoni Għal Malta 2030 +1, pledge 217 (summary in data/manifesto_pledges.csv, 6 Oct 2026).", ""),
    ("8", "Malta News Agency / Italpress (15 Dec 2025). Malta subsidies may end after €300m Sicily gas pipeline, PM says (outlet text of an interview). Read 19 Oct 2026.",
     "https://www.maltanewsagency.com/2025/12/malta-subsidies-may-end-after-e300m-sicily-gas-pipeline-pm-says/"),
    ("9", "◆ Pipeline Technology Journal (Jul 2026), relaying Times of Malta. Malta secures key EU backing for stalled mainland hydrogen-ready pipeline project. Second-hand.",
     "https://www.pipeline-journal.net/news/malta-secures-key-eu-backing-stalled-mainland-hydrogen-ready-pipeline-project"),
    ("10", "◆ Global Energy Monitor. Malta-Italy Gas Pipeline (wiki), citing MaltaToday (26 Jul 2019) and the Sept 2020 promoter schedule. Second-hand.", "https://www.gem.wiki/Malta-Italy_Gas_Pipeline"),
    ("11", "◆ The Malta Independent (19 May 2017). PL manifesto: gas pipeline to Sicily. Seen only as a search summary (403 to scripts); second-hand.",
     "https://www.independent.com.mt/articles/2017-05-19/local-news/PL-Manifesto-Gas-pipeline-to-Sicily-transparency-register-16-year-olds-to-be-given-right-to-vote-6736174459"),
    ("12", "Miżien. Calculation script and outputs: tools/cc-126-report/calc.py; data/cc-126/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "19 Oct 2026", "First issue. Pending right of reply.")])

build_report(Report(
    number="126", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["PN on the BP gas", "deal and the", "missing pipeline"],
    subtitle_lines=["Testing the Opposition’s statement of 22 June 2026", "against Enemalta and the pipeline’s promoter"],
    quote_lines=["“The Labour Government had promised that by this year", "Malta would have a pipeline for gas supply … it has failed.”"], quote_size=15,
    attribution="Partit Nazzjonalista, statement, 22 June 2026.",
    context="The BP deal “covers only nine months”, with no price details given.",
    verdict="Not substantiated", verdict_note="Contract facts hold; dated promise not shown",
    footer_lines=["Version 1.0  ·  19 October 2026", "Status: pending right of reply",
                  "Prepared from public sources.", "Repository: github.com/leandergrech/Mizien"],
    running_head="PN on the BP gas deal", version="1.0", date="19 October 2026",
    pdf_title="PN on the BP gas deal and the missing pipeline. Claim Check 126",
    pdf_subject="Tests a Partit Nazzjonalista statement on the BP LNG agreement and the gas pipeline pledge",
    story=S))
