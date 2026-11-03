"""Claim Check 153 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 12 March 2026 the European Commission announced letters of formal notice to 19 Member States, Malta among them, "
        "because they <b>“failed to submit their draft National Building Renovation Plan (NBRP) to the Commission by the "
        "deadline of 31 December 2025.”</b> We checked each part of that statement against the Commission’s own pages and "
        "the Directive. It stands. What it does not tell us is whether Malta has submitted a draft since.", lead)]
S.append(key_points([
    ("The notice exists as described.",
     "The Commission’s item of 12 March 2026 lists Malta as INFR(2026)2027, with 18 other Member States, and says they have "
     "two months to respond [1]."),
    ("The deadline comes from the Directive.",
     "Article 3 of Directive (EU) 2024/1275 requires the first draft plan by 31 December 2025 [2]."),
    ("Malta has no entry on the Commission’s plan page.",
     "On 3 November 2026 the page lists 18 Member States and the Walloon Region; Malta is not among them [3]. The page may "
     "lag behind submissions, so this is not proof that nothing was sent."),
    ("A first step, not a ruling.",
     "A letter of formal notice states the Commission’s view; it can end with a reasoned opinion and later a court case. "
     "The claim is about a reporting deadline, not about how many buildings Malta has renovated."),
    ("Verdict: supported (high confidence for the claim as worded).",
     "Every element of the statement is confirmed by the Commission’s own text."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("19", ORANGE, "Member States sent letters of formal notice, 12 March 2026"),
             ("31 Dec 2025", GREEN, "deadline for the first draft plan (Directive 2024/1275, Article 3)"),
             ("2 months", GREEN, "period to respond, as stated by the Commission"),
             ("0", RED, "entries for Malta on the Commission’s plan page, 3 Nov 2026")]),
      Spacer(1, 4 * mm),
      up_down("Nothing: Supported is the top of the scale.",
              "A Commission or Maltese government document showing that Malta had submitted a draft before 31 December 2025 "
              "(the notice would then be wrong), or the Commission closing the case."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the documents show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is the Commission’s own announcement, published on its Representation in Malta website under the title "
           "“March infringements package”, dated 12 March 2026 [1]. We read the whole item. It is the Commission’s text; "
           "the quotation marks below are its words. The record’s first source, an EU Reporter re-publication, refused our "
           "download and was not used."))
S.append(std_table([
    [C("What the Commission says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“The European Commission decided to open infringement procedures by sending a letter of formal notice to Belgium "
       "(INFR(2026)2014), Czechia (INFR(2026)2016), Germany (INFR(2026)2017) … Malta (INFR(2026)2027) … as they failed to "
       "submit their draft National Building Renovation Plan (NBRP) to the Commission by the deadline of 31 December 2025.” "
       "(19 Member States are named; we abbreviate the list.)"), C("[1]"), C("Read in full")],
    [C("“These Member States have two months to respond to the letters of formal notice. In the absence of a satisfactory "
       "response, the Commission may decide to issue a reasoned opinion.”"), C("[1]"), C("Read in full")],
], [108 * mm, 22 * mm, 40 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("We test the four facts in the statement: the notice, Malta’s case number, the deadline and the response period. "
                 "We do not rate whether the Commission’s view is right on the merits; that is for Malta to answer and, ultimately, "
                 "for the Court of Justice. The claim is about a reporting deadline, not about renovation itself.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is the Commission’s statement consistent with its own register of plans and with the law that sets the deadline?"))
S.append(P("<b>Evidence.</b> The Commission’s news item [1]; Article 3(3) of Directive (EU) 2024/1275 (the German text, read at "
           "gesetze.legal, because EUR-Lex refused our requests; the Commission’s energy site and REHVA give the same 31 December "
           "2025 date) [2]; the Commission’s “National Building Renovation Plans” page, read in full on 3 November 2026, which "
           "lists every draft plan received [3]; and the Commission’s first assessment of 14 July 2026 [4]. The counts are "
           "recomputed by <i>tools/cc-153-report/calc.py</i> from <i>data/cc-153/</i>. There is no peer-reviewed literature on "
           "this question; the evidence is official documents (grade C). The search log is in <i>literature/CC-153/notes.md</i>."))
S.append(P("<b>Grades.</b> Official documents are grade C. <b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the documents show"))
S.append(P("The notice and the deadline", h2))
S.append(P("The 12 March item names 19 Member States and their case numbers; Malta’s is INFR(2026)2027 [1]. Article 3(3) of the "
           "Directive says Member States submit the first draft of the plan to the Commission by 31 December 2025 [2]. The "
           "notice came 71 days after the deadline."))
S.append(P("What the Commission’s plan page shows", h2))
S.append(fig(FIG / "fig1_timeline.png"))
S.append(P("Figure 1. Every draft plan listed on the Commission’s page, by the date printed beside it. Malta has no entry. "
           "Six entries are dated on or before 31 December 2025; thirteen are later, ten of them after the 12 March notice.", cap))
S.append(P("Of the 19 notified States, 11 now have an entry (some under their own name, Belgium only for the Walloon Region); "
           "eight do not: Czechia, Hungary, Ireland, Italy, Luxembourg, Malta, Poland and Slovakia [3]. The Commission’s July "
           "assessment says 15 EU countries and the Walloon Region submitted between December 2025 and May 2026 [4]; "
           "later entries on the page (Estonia, Greece, Latvia) came after that. The page does not say whether each printed "
           "date is the submission or the date of the English translation."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Has Malta still not submitted?", "NOT SHOWN EITHER WAY", AMBER,
    "Malta has no entry on the Commission’s plan page on 3 November 2026, and we found no Commission or Maltese government "
    "statement that a draft was submitted.",
    "The page may lag behind submissions, and the infringement register entry for INFR(2026)2027 (its current stage) could not "
    "be read. A LinkedIn post and a legal-news summary mention an escalation in October 2026 ◆ (second-hand, not verified).",
    "<b>For this claim:</b> not needed. The claim concerns the deadline and the March notice, which are documented; it does not "
    "say Malta has not submitted since."))
S.append(contested(
    "Q2  Does missing the draft deadline mean Malta is not renovating?", "DIFFERENT QUESTION", AMBER,
    "The plans are the Directive’s tool for renovation pipelines; a missing draft delays the Commission’s assessment [1].",
    "Malta has a renovation strategy and grant schemes (a search found the Irrinova Darek scheme, aligned by MaltaToday with the "
    "Long-term Renovation Strategy 2050; not read in full). Those do not replace the plan, and the notice does not rate them.",
    "<b>For this claim:</b> the statement is limited to the deadline; we do not rate renovation performance."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta, with 18 other Member States, received a letter of formal notice (INFR(2026)2027) in March 2026"),
     C("The Commission’s item of 12 March 2026 names 19 States; Malta is INFR(2026)2027 [1]."), verd("SUPPORTED", GREEN)],
    [C("<b>B.</b> The notice was for not submitting the draft National Building Renovation Plan, due by 31 December 2025"),
     C("The Commission’s text says so; Article 3 of Directive 2024/1275 sets the date [1][2]."), verd("SUPPORTED", GREEN)],
    [C("<b>C.</b> Malta has two months to respond"),
     C("Stated in the Commission’s item [1]. Whether Malta has responded is not documented."), verd("SUPPORTED", GREEN)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Supported", "Every element of the statement is confirmed by the Commission’s own text and the Directive. "
                  "Confidence: high for the claim as worded."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The Commission’s item contains the quoted statement. (2) The Directive sets the 31 December 2025 date. "
           "(3) Malta’s absence from the Commission’s plan page on 3 November 2026 is consistent with the notice, though not proof "
           "of the current state."))
S.append(P("<b>What this verdict does not say.</b> It does not say that Malta’s buildings are poorly renovated, that the Commission’s "
           "view is final, or that anyone acted in any particular way. A letter of formal notice is a first procedural step."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "Whether Malta submitted a draft NBRP, and when.",
    "The current stage of INFR(2026)2027 in the Commission’s infringement decisions register.",
    "Whether and when a public consultation on Malta’s draft was held (Article 3(4) of the Directive).",
]))

S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["EUR-Lex refused our requests; the Directive’s Article 3 was read in the German text at gesetze.legal, and the date was "
          "cross-checked on the Commission’s energy site, REHVA and Build-Up. We did not read the English official text.",
          "The Commission’s plan page may lag behind submissions and prints a date whose meaning (submission or translation) is not stated.",
          "The Commission’s infringement register entry could not be read; later stages of the case are unverified.",
          "We did not search Maltese parliamentary or ministry records exhaustively (see the notes for what was searched).",
          "The statement concerns a reporting obligation, not renovation performance."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission, Representation in Malta (12 March 2026). March infringements package: Commission calls on Member States "
          "to submit their draft National Building Renovation Plans.",
     "https://malta.representation.ec.europa.eu/news/march-infringements-package-2026-03-12_en"),
    ("2", "Directive (EU) 2024/1275 of 24 April 2024 on the energy performance of buildings (recast), Article 3(3). German text read at "
          "gesetze.legal; date cross-checked at the Commission’s energy site.",
     "https://gesetze.legal/eu/rl_2024_1275_eu/3"),
    ("3", "European Commission, DG Energy. National Building Renovation Plans (page read 3 Nov 2026).",
     "https://energy.ec.europa.eu/topics/energy-efficiency/energy-performance-buildings/national-building-renovation-plans_en"),
    ("4", "European Commission, DG Energy (14 July 2026). National Building Renovation Plans: the Commission’s first assessment.",
     "https://energy.ec.europa.eu/news/national-building-renovation-plans-commissions-first-assessment-2026-07-14_en"),
    ("5", "Miżien. Data and calculations: data/cc-153/; tools/cc-153-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "3 Nov 2026", "First issue. Verdict: Supported; no right of reply needed.")])

build_report(Report(
    number="153", out=str(FIG / "report.pdf"), kicker="Planning and housing",
    title_lines=["Did Malta miss the", "renovation-plan", "deadline?"],
    subtitle_lines=["Testing the Commission’s March 2026 infringement notice on",
                    "National Building Renovation Plans"],
    quote_lines=["“…Malta (INFR(2026)2027)… failed to submit their draft", "National Building Renovation Plan… by the deadline of 31 December 2025”"], quote_size=16,
    attribution="European Commission, March infringements package, 12 March 2026.",
    context="Malta and 18 other Member States were given two months to respond.",
    verdict="Supported", verdict_note="Notice, case number, deadline and period all confirmed",
    footer_lines=["Version 1.0  ·  3 November 2026", "Status: draft · no right of reply needed",
                  "Prepared from public documents.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Building renovation plan – Malta", version="1.0", date="3 November 2026",
    pdf_title="Did Malta miss the renovation-plan deadline? Claim Check 153",
    pdf_subject="Tests the Commission's March 2026 infringement notice to Malta on its draft National Building Renovation Plan",
    story=S))
