"""Claim Check 101 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 8 July 2026 the European Commission opened an infringement procedure against Malta (INFR(2026)2115). Its "
        "published summary says: <b>“Malta has failed to put in place a registration requirement for surface water "
        "abstraction and a prior authorisation regime to control the abstraction of surface and groundwater. In "
        "addition, Maltese law does not ensure a periodic review of the controls over the abstraction of surface and "
        "groundwater having a significant impact on water bodies.”</b> [1] We tested the facts it rests on against "
        "the law as published and Malta’s own documents; breach of EU law is for the Commission and the Court.",
        lead)]
S.append(key_points([
    ("What the Directive asks.",
     "Abstraction controls “including a register or registers of water abstractions and a requirement of prior "
     "authorisation”, reviewed periodically; insignificant abstractions may be exempted [3]."),
    ("Malta registers groundwater sources; the instruments read contain no permit to abstract.",
     "Sources had to be notified by November 2008 and drilling is under a moratorium with exceptions, but "
     "notification and drilling permits give no “right ... to draw water” [5, 6]."),
    ("Malta’s documents differ on what the control is.",
     "The Green Paper and 3rd plan treat an abstraction permit as still to be created [10, 11]; Malta’s April 2025 "
     "report to the Commission describes the register as the control [11]. We found no permit in force [21]."),
    ("Surface water: little of it, and no register found.",
     "Three short watercourses (3.4 km) and two tiny pools, none with abstraction as a significant pressure [17]; "
     "no rule to register its abstraction found."),
    ("Verdict: largely supported (moderate confidence).",
     "Facts match Maltese law as published; legal sufficiency and the review sentence not rated. It covers the "
     "Commission’s first sentence and the facts we could check. In 2019 Commission staff wrote of “a concession, "
     "authorisation and/or permitting regime to control groundwater and a register of groundwater use” [13]."),
]))
S += [Spacer(1, 1 * mm), VerdictMeter(1), Spacer(1, 1 * mm),
      tiles([("3,798", GREEN, "farm (3,553) and commercial (245) boreholes, Green Paper 2023"),
             ("62.9%", GREEN, "of 2024 groundwater abstraction outside public supply (taken as WSC; estimated)"),
             ("7 of 15", AMBER, "groundwater bodies with abstraction as a significant pressure"),
             ("3.4 km", GREY, "Malta’s three WFD watercourses in all; no abstraction pressure")]),
      Spacer(1, 2 * mm),
      up_down("The letter or Malta’s reply, if published, showing the facts are not in dispute (no permit to abstract "
              "water; no register of surface-water abstraction): <i>Supported</i>.",
              "A Maltese instrument in force that we missed, which grants a permit to abstract or requires registration "
              "of surface-water abstraction; or the Commission narrowing its sentence after Malta’s reply."),
      Spacer(1, 1 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the Directive asks, and Malta’s waters"),
          ("4", "What Maltese law contains"), ("5", "What Malta’s plans and reports say"),
          ("6", "Where the documents point different ways"), ("7", "Testing the claim"),
          ("8", "Verdict and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The speaker is the European Commission. The words are from its July 2026 infringements package, published "
           "in the Commission’s press corner (INF/26/1376) and on its Representation in Malta’s website, both dated "
           "8 July 2026 and identical [1, 2]. They summarise a letter of formal notice, which is not published. The "
           "same paragraph covers a letter to Spain (INFR(2026)2099), under the heading “Commission calls on Spain and "
           "Malta to ensure periodic review of water permits”, and says the two countries “now have two months to "
           "respond”."))
S.append(std_table([
    [C("Document", cellh), C("What it is", cellh), C("Access", cellh)],
    [C("INF/26/1376, July infringements package, 8 July 2026 [1]"), C("The Commission’s published summary; the claim"),
     C("Read in full (press corner print copy)")],
    [C("Representation in Malta page, 8 July 2026 [2]"), C("The same text"), C("Read in full")],
    [C("Letter of formal notice INFR(2026)2115"), C("The legal document the summary describes"), C("Not published")],
    [C("Infringement decisions register"), C("The case record"), C("Not reachable from our network (404)")],
    [C("Malta’s reply (due about two months after 8 July)"), C("The Government’s answer"), C("Not published; none found")],
], [64 * mm, 62 * mm, 44 * mm]))
S.append(P("Our record’s title, “EU: no registration or prior authorisation of water abstraction in Malta”, condenses "
           "the Commission’s first sentence and is not itself rated; we rate the Commission’s words quoted above. Malta "
           "does issue permits to <i>drill</i> boreholes [6]; in the instruments read we found no permit to "
           "<i>abstract</i> water (section 4)."))
S += [Spacer(1, 2 * mm),
      callout([P("FAIRNESS AND SCOPE", tag),
               P("A letter of formal notice is the first step of an infringement procedure, not a finding by a court. "
                 "We report what the Commission says, what Maltese law contains and what data exist; we offer no "
                 "opinion on whether Malta has transposed the Directive correctly. The verdict covers the Commission’s "
                 "first sentence (registration of surface-water abstraction; prior authorisation to control "
                 "abstraction) and the facts we could check; the second sentence (periodic review) and legal "
                 "sufficiency are not rated. Groundwater status, Water Services "
                 "Corporation (WSC) production and its “net-zero impact” aim are tested in CC-009, CC-039, CC-047 and "
                 "CC-108.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Does Maltese law, as published, contain (a) a requirement to register surface-water "
           "abstraction, (b) a permit to abstract surface water or groundwater, and (c) provisions for reviewing "
           "abstraction controls periodically? And what do Malta’s own documents and the EU’s data say about them?"))
S.append(P("<b>Evidence.</b> This is a documentary check. We read the Directive’s text [3] and the consolidated Maltese "
           "instruments on legislation.mt [4–9]. To look for any other abstraction instrument we searched, in its "
           "official sitemap, the titles of all 943 Legal Notices of 2024–2026, the full text of all 101 Acts of "
           "2024–2026 and the titles of 344 subsidiary instruments in the environment, energy-and-water and Water "
           "Services Corporation series [21]. We read Malta’s Green Paper on "
           "groundwater abstraction (2023) [10], its April 2025 report to the Commission on its programme of measures "
           "[11], its 2nd water plan [12], and the Commission’s assessments of Malta’s plans [13–15]. Data: Eurostat "
           "abstraction by source and sector [16] and Malta’s 2022 Water Framework Directive reporting in the EEA’s "
           "WISE system [17, 18]. Every number is recomputed by <i>tools/cc-101-report/calc.py</i> from "
           "<i>data/cc-101/</i>; Eurostat’s flags are kept. Each “not found” statement has a search log in "
           "<i>literature/CC-101/notes.md</i>. All documents were read on 6 October 2026."))
S.append(P("<b>Grades.</b> Legislation, official plans and reports and official statistics are grade C on our scale; "
           "there is no experimental or observational evidence to grade for a question of what a law says. News "
           "reports are used only to locate material and are marked ◆ where they report data we have not seen. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(40 * mm))
S.append(SectionHeading(3, "What the Directive asks, and Malta’s waters"))
S.append(P("Article 11 of the Water Framework Directive requires a programme of measures for each river basin "
           "district. Among its basic measures, Article 11(3)(e) requires “controls over the abstraction of fresh "
           "surface water and groundwater, and impoundment of fresh surface water, including a register or registers of "
           "water abstractions and a requirement of prior authorisation for abstraction and impoundment. These controls "
           "shall be periodically reviewed and, where necessary, updated. Member States can exempt from these controls, "
           "abstractions or impoundments which have no significant impact on water status” [3]. The Directive was to be "
           "transposed by 22 December 2003 (Article 24) and its measures made operational by 22 December 2012 "
           "(Article 11(7)). Article 11(5) separately asks for permits to be examined and reviewed where a water body "
           "is unlikely to reach its objectives [3]."))
S.append(P("Malta’s natural fresh water is almost all groundwater: 92.9% of the fresh water abstracted in 2024 [16]; "
           "desalinated seawater is not counted as abstraction. Its 2nd water plan says “there are no rivers in the Maltese "
           "islands” [12]. In its 2022 EU reporting Malta lists three river water bodies, the watercourses of Wied "
           "il-Baħrija, Wied il-Luq and Wied il-Lunzjata (1.5, 1.3 and 0.6 km), and two lake water bodies of at most "
           "0.001 km², besides coastal and transitional waters [17]. None of its surface water bodies lists abstraction "
           "as a significant pressure; seven of its 15 groundwater bodies do, and four groundwater bodies are in poor "
           "quantitative status [17, 18]. Malta told the Commission in 2019 that its only impoundments are small masonry "
           "dams in dry valleys holding less than 125,000 m³ in total [13]."))
S.append(P("Eurostat nevertheless records about 2.96 million m³ of “fresh surface water” abstraction a year in Malta "
           "(2019–2024), 7.1% of fresh water abstracted in 2024, split between households (1.71) and agriculture "
           "(1.25) [16]. The values are estimates (flag e) and are identical every year within 2010–2018 and within "
           "2019–2024, so they are not a metered series. Eurostat does not say what this water is. The Government’s "
           "Green Paper counts harvested rainwater as 8% of agricultural supply in 2022 [10], which may be part of it; "
           "that is our reading, not Eurostat’s."))
S.append(KeepTogether([fig(FIG / "fig1_abstraction.png"),
                       P("Figure 1. (a) Fresh water abstracted in Malta in 2024 by source and user. Groundwater: "
                         "38.46 million m³, of which agriculture 21.77 and the public supply 14.28; surface water 2.96 "
                         "[16]. All are Eurostat estimates. (b) Malta’s water bodies in its 2022 EU reporting: groundwater "
                         "bodies with abstraction as a significant pressure, groundwater bodies in poor quantitative status "
                         "(assessed 2021), and inland surface waters with abstraction as a significant pressure [17, 18]. "
                         "“Public water supply” is Eurostat’s category; we take it to be the Water Services Corporation "
                         "(WSC), the supplier the Green Paper would leave outside its framework [10]. That identification "
                         "is ours, not Eurostat’s.",
                         cap)]))

# ================================================================== 4
S.append(CondPageBreak(24 * mm))
S.append(SectionHeading(4, "What Maltese law contains"))
S.append(P("Malta’s groundwater rules date from 2008–2010 and were made under the Malta Resources Authority Act. In 2024 "
           "Act XVII moved them to the Environment Protection Act and to the Environment and Resources Authority (ERA), "
           "“until other provision is made” [9]. Together with the regulations that transpose the Directive, they are "
           "the instruments a reader would look to for registration, authorisation and review."))
S.append(std_table([
    [C("Instrument", cellh), C("What it does", cellh), C("Register?", cellh), C("Permit to abstract?", cellh),
     C("Review?", cellh)],
    [C("<b>S.L. 549.100</b> Water Policy Framework Regs (2015) [4]"),
     C("Reg. 12(3)(e) repeats Article 11(3)(e) almost word for word as a duty of the “competent authority”, including "
       "“These controls shall be periodically reviewed”. Reg. 12(5)(b) and (8): permits and authorisations are reviewed "
       "where objectives are at risk; programmes of measures every six years. Schedule VII: the plan summarises "
       "controls on abstraction “including reference to the registers”."),
     C("Duty stated"), C("Duty stated"), C("Duty stated")],
    [C("<b>S.L. 549.164</b> Notification of Groundwater Sources (2008) [5]"),
     C("Every groundwater source not registered under the 1997 rules had to be notified by 20 Nov 2008 (reg. 3); reg. 3A "
       "(2011) lets some old sources (dug before 1955; some shafts) be notified later, once ERA has decided. Reg. 6: "
       "notification “does not in any way give any right ... to draw water”; ERA may order closure “at any time”."),
     C("Yes: groundwater sources only"), C("No"), C("None in the text")],
    [C("<b>S.L. 549.165</b> Borehole Drilling (2008) [6]"),
     C("A permit is needed to drill into the saturated zone (reg. 4). Applications are barred for “a minimum period of "
       "twelve months ... or until such further period of time as the Authority may subsequently decide” (reg. 6(1)), "
       "with exceptions (reg. 6(2)): sea-wells, foundations, replacing a collapsed registered farm borehole and, from "
       "27 Dec 2024, research boreholes of public entities. Permits turn on “no significant impact on water "
       "resources” (reg. 7(3)), may carry a “term” (reg. 8(3)(a)) and can be suspended or revoked at any time (reg. 11). "
       "Reg. 9: no “right to draw water”. Reg. 10: ERA may order extraction stopped or reduced."),
     C("Drilling permits (reg. 12)"), C("No"), C("Term; may be suspended (regs 8, 11)")],
    [C("<b>S.L. 549.166</b> Metering (2010) [7]"),
     C("Registered and notified sources are to be metered by WSC; exemptions for sources without pumps, cultural "
       "property and domestic perched-aquifer sources under 1 m³ a day."), C("—"), C("No"), C("No")],
    [C("<b>S.L. 545.14</b> Water Supply and Sewerage Services (2004) [8]"),
     C("Licences for water suppliers, including tankers. “Supply of water” is defined to exclude “water "
       "abstraction”."), C("Licensed suppliers"), C("No"), C("Licence term")],
    [C("<b>S.L. 545.02</b> Control of Water Pumps and Wells Order (1946-47) [8]"),
     C("Declares the whole of Malta and of Gozo “a water-controlled area”. The text has no register, permit or review "
       "provision."), C("No"), C("No"), C("No")],
], [33 * mm, 79 * mm, 21 * mm, 17 * mm, 20 * mm]))
S.append(P("Also read: S.L. 549.168 (users of a source), S.L. 549.172 (environmental permits; no abstraction category), "
           "S.L. 549.21 (quality of surface water used for drinking water), S.L. 549.53 and 549.155 (groundwater "
           "pollution), and the WSC Act, whose licensing articles 43–45 are marked deleted (2000) [7, 9]. None registers "
           "surface-water abstraction or grants a permit to abstract.", cap))
S.append(P("So the instruments read contain a register of groundwater sources (notification was due by 20 November "
           "2008, with a later route for some old sources), a drilling-permit scheme with a moratorium and exceptions, "
           "metering rules, and powers to close a source or reduce its abstraction. We found in them no register of "
           "surface-water abstractions and no permit to abstract water. S.L. 549.100 states the Directive’s duty "
           "(reg. 12(3)(e)) in general terms, and we found in its text no provision that creates a register or a "
           "permit to abstract."))
S.append(KeepTogether([fig(FIG / "fig2_timeline.png"),
                       P("Figure 2. EU and Maltese steps on abstraction control, 1997–2026, one row each in date order "
                         "[1, 3–7, 10–14, 21].", cap)]))

# ================================================================== 5
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "What Malta’s plans and reports say"))
S.append(P("<b>The Government proposes the missing permit.</b> The November 2023 Green Paper, by the Energy and Water "
           "Agency (EWA) and ERA, lists the 2008–2010 regulations as the current framework and proposes a new one: "
           "“Following the enactment of the legal framework, no groundwater source will be utilized for the abstraction "
           "of groundwater unless an abstraction permit or clearance has been issued by the Environment and Resources "
           "Authority (ERA)”, with “permit conditions ... renewable for defined fixed term periods”, a public register "
           "of abstractors, quotas for farmers and tariffs for commercial and domestic users, “periodically reviewed” "
           "[10]. WSC’s own sources would be outside the framework, with its abstraction capped at 14 million m³ a year "
           "to 2030 [10]."))
S.append(P("<b>Malta’s report to the Commission.</b> Malta’s April 2025 interim report on its 3rd water plan (March "
           "2024) lists the proposal as Measure 053, “Development of a Groundwater Abstraction Licensing Framework” "
           "[11]. In that report, under Article 11(3)(e), Malta wrote that “National legislation requires all groundwater "
           "abstraction stations, regardless of yield, to be registered with the ERA. Only these registered sources are "
           "permitted to extract groundwater, and no new sources have been authorised since 2010, apart from seawater "
           "sources” [11]. The same report says the licensing framework is “close to being finalised. The next step "
           "will be for the proposed regulation to be issued for public consultation and eventually adopted by "
           "Government”, and that the resources to run it are “still being secured and configured” [11]. Its section on "
           "Article 11(3)(e) does not mention surface water."))
S.append(P("<b>Where things stand.</b> Of the 943 Legal Notices of 2024–2026 on legislation.mt, one title mentions "
           "groundwater, abstraction, boreholes, wells or water policy: L.N. 374 of 2024, which adds research boreholes by "
           "public entities to the exceptions from the drilling moratorium (read in full). We found no notice that "
           "creates an abstraction permit (titles only, apart from L.N. 374). Of the 101 Acts of 2024–2026 on the site, "
           "only Act XVII of 2024, which moved the groundwater regulations to ERA, mentions groundwater, abstraction or "
           "boreholes in its text, and the titles of 344 subsidiary instruments under S.L. 549, 423, 545, 355 and 427 "
           "turned up no abstraction instrument beyond those in section 4 [5–7, 21]. A news investigation reports that "
           "ERA said nothing had happened since the Green Paper beyond “internal discussions” ◆ [20]."))
S.append(KeepTogether([P("Registered and metered sources", h2), std_table([
    [C("What", cellh), C("Number", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Boreholes operated by agriculture"), C("3,553"), C("Green Paper, 2023 [10]"), grade_tag("C")],
    [C("Boreholes registered for commercial activities"), C("245"), C("Green Paper, 2023 [10]"), grade_tag("C")],
    [C("Registered low-yield sources (spieri), mostly without pumps, so not metered"), C("3,405"),
     C("Green Paper, 2023 [10]"), grade_tag("C")],
    [C("WSC boreholes (plus 12 pumping stations); abstraction “fully accounted for”"), C("110"),
     C("Green Paper, 2023 [10]"), grade_tag("C")],
    [C("Private sources metered"), C("“most” (2025); “more than 3 000” (2019)"),
     C("Malta, interim report [11]; Malta’s clarification in SWD(2019) 48, p. 124 n. 65 [13]"), grade_tag("C")],
    [C("Registered commercial boreholes reporting no abstraction data"), C("more than 63% ◆"),
     C("ERA data reported by Amphora Media, 2026 [20]"), grade_tag("D")],
], [78 * mm, 34 * mm, 46 * mm, 12 * mm]),
    P("We found no current count of metered sources. Malta told the Commission in 2019 that more than 3,000 private "
      "groundwater sources had been metered [13, p. 124 n. 65] (“practically all”, p. 84), and in 2025 that “most” "
      "registered sources have been [11]; a 2020 review by an Energy and Water Agency author describes agricultural "
      "use being managed “through the progressive metering of groundwater abstraction sources” [19, p. 30]. These are "
      "Malta’s statements, not counts we could check. The ◆ figure is second-hand (a news report of ERA records we "
      "have not seen) and is not used for any rating. Domestic boreholes (pools, gardens) have no count in the Green "
      "Paper.", cap)]))

# ================================================================== 6
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(6, "Where the documents point different ways"))
S.append(contested(
    "Q1  Does Malta’s register of groundwater sources amount to a “prior authorisation regime”?",
    "DOCUMENTS DIFFER; LEGAL QUESTION, NOT RATED", ORANGE,
    "Malta’s laws say notification and drilling permits give no right to draw water [5, 6], and we found no permit "
    "to abstract in the instruments read. The Government’s Green Paper treats an abstraction permit as new, to be "
    "created by “the enactment of the legal framework” [10], and Malta’s April 2025 interim report lists it as a "
    "measure still to be delivered [11]. In 2019 the Commission’s staff document says abstraction “should be "
    "included under cross compliance once the legislation on authorisations of abstraction is in place” [13, p. 125]. "
    "The Commission’s 2026 summary says Malta “failed to put in place” such a regime [1].",
    "Malta reports that “Only these registered sources are permitted to extract groundwater” and that no new "
    "sources have been authorised since 2010 apart from sea-wells [11]. In 2019 the Commission’s staff wrote that "
    "“in Malta there is a concession, authorisation and/or permitting regime to control groundwater and a register "
    "of groundwater use”, while noting that the plan gave no information on the procedures and resources in place to "
    "control abstractions [13, p. 121].",
    "<b>Why they differ:</b> the documents describe the same instruments in different terms. The 2019 staff document "
    "lists L.N. 254 and 255 of 2008 among the regulatory framework [13, p. 122], the instruments we read, and "
    "describes a regime; Malta’s 2023 Green Paper proposes an abstraction permit as new, while its April 2025 report "
    "describes the register as the control. Whether notification of existing sources meets the Directive’s wording is the legal "
    "question in the procedure, which we do not decide. <b>For this claim:</b> we rate the facts (C): the instruments "
    "read contain no permit to abstract water.",
    label_a="EVIDENCE FOR THE COMMISSION’S STATEMENT", label_b="EVIDENCE THAT POINTS THE OTHER WAY"))
S.append(contested(
    "Q2  Does Maltese law “ensure” periodic review?", "NOT RATED; LEGAL ASSESSMENT", GREY,
    "For a notified source, the operative instruments contain no term, expiry, renewal or review [5, 7]. S.L. 549.165 "
    "lets a drilling permit carry a “term” (reg. 8(3)(a)) and be suspended or revoked at any time on listed grounds "
    "(reg. 11), and its register of permits “shall be kept under review and up to date” (reg. 12(2)) [6]. The Green "
    "Paper proposes fixed-term abstraction permits and periodic review of quotas and tariffs [10].",
    "S.L. 549.100 reg. 12(3)(e) copies the Directive’s words: “These controls shall be periodically reviewed and, "
    "where necessary, updated” [4]. Its reg. 12(5)(b) says that where objectives are unlikely to be met “relevant "
    "permits and authorisations are examined and reviewed as appropriate”, and reg. 12(8) that programmes of measures "
    "are reviewed every six years [4]. ERA may also order a source closed or its abstraction reduced where it has a "
    "significant impact [5, 6].",
    "<b>Why they differ:</b> a duty written into law is not the same as a procedure that carries it out, but whether "
    "the first is enough is a question of EU law. <i>Context, not evidence on Malta:</i> across the Member States "
    "assessed the Commission found review periods “ranging from 6 years to several decades or even indefinite” and "
    "said it is enforcing the obligation to review permits [15]; Malta was not in that assessment [14]. "
    "<b>For this claim:</b> we show both and give no rating.",
    label_a="EVIDENCE FOR THE COMMISSION’S STATEMENT", label_b="EVIDENCE THAT POINTS THE OTHER WAY"))

# ================================================================== 7
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(7, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=32 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The Directive requires abstraction controls, with registers and prior authorisation, reviewed "
       "periodically (the Commission’s premise, not its words)"),
     C("Not rated as a statement of the speaker. For context, Article 11(3)(e) says so; abstractions with no "
       "significant impact on water status may be exempted [3]."),
     verd("PREMISE, NOT RATED", GREY)],
    [C("<b>B.</b> Malta has failed to put in place a registration requirement for surface water abstraction"),
     C("Rated on the facts: no instrument read requires registration of surface-water abstraction. Malta’s register "
       "covers groundwater sources only [5]; no surface-water provision in the instruments, Acts and titles searched "
       "[4–9, 21]; Malta’s 2nd plan notes a “lack of knowledge” of surface-water abstraction [12]. Surface water is "
       "small: three watercourses (3.4 km), two pools [17]; Eurostat estimates 2.96 million m³ a year [16]."),
     verd("ACCURATE (LAWS SEARCHED)", GREENC)],
    [C("<b>C.</b> Malta has failed to put in place a prior authorisation regime to control the abstraction of surface "
       "and groundwater"),
     C("Rated on the facts: no permit to abstract water in the instruments read. Notification and drilling permits give "
       "no right to draw water [5, 6]; the Green Paper and 3rd plan treat an abstraction permit as still to be created "
       "[10, 11], and we found none in force [21]. Caveat: the instruments do contain a register of groundwater "
       "sources, drilling permits judged on impact on water resources (reg. 7(3)), metering, and powers to close a "
       "source or reduce abstraction [5–7]; Malta’s 2025 report describes the register as the control [11]. Whether "
       "these are a “prior authorisation regime” is a legal question, not rated (section 6, Q1)."),
     verd("LARGELY ACCURATE (ON THE FACTS)", LG)],
    [C("<b>D.</b> Maltese law does not ensure a periodic review of the controls over the abstraction of surface and "
       "groundwater having a significant impact on water bodies"),
     C("S.L. 549.100 copies the Directive’s review duty (reg. 12(3)(e)) and provides for review of permits and "
       "authorisations where objectives are at risk (reg. 12(5)(b)) and of programmes every six years (reg. 12(8)) [4]; "
       "the instruments that run the controls set no term, renewal or review for a notified source, while drilling "
       "permits may carry a term and be suspended (regs 8(3)(a), 11) [5–7]; the Green Paper proposes fixed terms and "
       "periodic review [10]. Whether this “ensures” review is a legal question (section 6, Q2)."),
     verd("NOT RATED (LEGAL ASSESSMENT)", GREY)],
], [50 * mm, 88 * mm, 32 * mm], valign="MIDDLE"))
S.append(Spacer(1, 3 * mm))
S.append(P("<b>Why these ratings.</b> Sub-claim A is the Commission’s premise, not something it says about Malta, so it is "
           "not rated. Sub-claim B is “accurate” on a bounded search: we read every instrument a registration rule would "
           "sit in and searched the titles of recent Legal Notices, the text of recent Acts and the titles of related "
           "subsidiary instruments, but not every Chapter of the Laws of Malta. Sub-claim C is rated on what the "
           "instruments contain, not on the word “regime”: they contain no permit to abstract water (accurate on the same "
           "bounded search). It is “largely accurate” because the summary does not mention the controls that do exist: "
           "the register of groundwater sources, drilling permits judged on their impact, metering, and powers to close "
           "a source or reduce abstraction."))

# ================================================================== 8
S += [CondPageBreak(80 * mm), Spacer(1, 6 * mm), SectionHeading(8, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Facts match Maltese law as published; legal sufficiency and the review sentence "
                  "not rated. The verdict covers the Commission’s first sentence and the facts we could check. "
                  "Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The Directive asks for what the Commission’s sentences presuppose (A, a premise, not rated). "
           "(2) Malta’s registration rules cover groundwater sources only, and we found no requirement to register "
           "surface-water abstraction (B). (3) We found no permit to abstract water in the instruments read: the laws say "
           "notification and drilling permits give no right to draw water, and the Green Paper and 3rd plan treat an "
           "abstraction permit as still to be created; we found none in force on 6 October 2026 (C). (4) Caveats: Malta’s "
           "April 2025 report describes the register as the control; the register, drilling permits, moratorium, metering "
           "and closure powers are real, if partial, controls that the summary does not mention; and in 2019 Commission "
           "staff wrote of “a concession, authorisation and/or permitting regime to control groundwater and a register of "
           "groundwater use” [13]. (5) The review sentence turns on what “ensure” requires in EU law, so it is shown, not "
           "rated (D). Confidence is moderate: we read the Commission’s summary, not its letter; Malta’s reply and its 3rd "
           "plan itself were not available to us; and the absence of a provision is shown by a bounded search."))
S.append(P("<b>What this verdict does and does not say.</b> It covers the Commission’s first sentence, tested on the "
           "facts we could check. It does not rate the second sentence (periodic review) or whether Maltese law is "
           "sufficient under the Directive. It does not say that Malta is in breach of EU law, that anyone abstracts "
           "unlawfully, or how much over-abstraction there is. Groundwater status is covered in CC-009 and CC-047. A "
           "Largely supported verdict needs no right of reply."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The Commission: the letter of formal notice INFR(2026)2115, or its legal reasoning on Malta’s existing register.",
    "The Government (ERA, EWA): Malta’s reply to the letter, and the draft groundwater abstraction regulation under "
    "Measure 053 with its timetable for consultation and adoption.",
    "ERA: the current number of registered groundwater sources, how many are metered (Malta told the Commission in "
    "2019 that more than 3,000 private sources were) and how many report readings each year.",
    "EWA or the National Statistics Office: what Malta reports to Eurostat as fresh surface-water abstraction "
    "(2.96 million m³ a year), and how it is estimated.",
]))

# ================================================================== 9
S += [Spacer(1, 6 * mm), SectionHeading(9, "Limitations")]
for l in ["We read the Commission’s published summary [1, 2], not the letter of formal notice, which may set out more "
          "detail or different reasoning.",
          "Malta’s reply was due in about September 2026; we found none published.",
          "Malta’s 3rd water plan could not be read from our network (its host refuses scripts and the web archive was "
          "unreachable); its Programme of Measures is known here through Malta’s April 2025 interim report on it [11].",
          "“Not found” statements rest on the search recorded in the notes: the instruments listed in section 4, the "
          "titles of all Legal Notices of 2024–2026, the text of all Acts of 2024–2026 and the titles of S.L. 549, 423, "
          "545, 355 and 427 on legislation.mt [21]. A provision elsewhere in the Laws of Malta (including by-laws), a "
          "draft not yet published, or an instrument not yet on the site would not have been found.",
          "Eurostat’s abstraction figures for Malta are estimates; the surface-water series is flat within periods and "
          "unexplained.",
          "The 2nd water plan was read from a copy hosted outside ERA’s site (same title and content; hash in the notes).",
          "We give no legal opinion; the meaning of “prior authorisation” and “ensure ... periodic review” in the "
          "Directive is for the Commission and the Court of Justice."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (8 Jul 2026). July infringements package: key decisions. INF/26/1376, section 1, "
          "“Commission calls on Spain and Malta to ensure periodic review of water permits”. Read in full 6 Oct 2026.",
     "https://ec.europa.eu/commission/presscorner/detail/en/inf_26_1376"),
    ("2", "European Commission Representation in Malta (8 Jul 2026). July infringements package: key decisions. Read "
          "6 Oct 2026.", "https://malta.representation.ec.europa.eu/news/july-infringements-package-key-decisions-2026-07-08_en"),
    ("3", "Directive 2000/60/EC (Water Framework Directive), OJ L 327, 22.12.2000, p. 1: Articles 11(3)(e), 11(5), "
          "11(7), 24.", "https://data.europa.eu/eli/dir/2000/60/oj"),
    ("4", "Water Policy Framework Regulations, S.L. 549.100 (L.N. 345 of 2015, as amended), regs 12(3)(e), 12(5)(b), "
          "12(8) and Schedule VII.",
     "https://legislation.mt/eli/sl/549.100/eng"),
    ("5", "Notification of Groundwater Sources Regulations, S.L. 549.164 (L.N. 255 of 2008), regs 3, 3A, 6.",
     "https://legislation.mt/eli/sl/549.164/eng"),
    ("6", "Borehole Drilling and Excavation Works within the Saturated Zone Regulations, S.L. 549.165 (L.N. 254 of "
          "2008, as amended to L.N. 374 of 2024), regs 4, 6, 7, 8, 9, 10, 11, 12.", "https://legislation.mt/eli/sl/549.165/eng"),
    ("7", "Groundwater Abstraction (Metering) Regulations, S.L. 549.166 (L.N. 241 of 2010), regs 3, 8; Users of "
          "Groundwater Sources (Application) Regulations, S.L. 549.168.", "https://legislation.mt/eli/sl/549.166/eng"),
    ("8", "Water Supply and Sewerage Services Regulations, S.L. 545.14 (L.N. 525 of 2004), regs 2, 3, 6; Control of "
          "Water Pumps and Wells Order, S.L. 545.02 (Proclamations V of 1946 and II of 1947; ELI page sl/545.2).",
     "https://legislation.mt/eli/sl/545.14/eng"),
    ("9", "Environment Protection Act, Cap. 549, as amended by Act XVII of 2024 (transfer of the groundwater "
          "regulations to ERA); S.L. 549.172, 549.21, 549.53, 549.155; Water Services Corporation Act, Cap. 355.",
     "https://legislation.mt/eli/cap/549/eng"),
    ("10", "Energy and Water Agency and Environment and Resources Authority (Nov 2023). Green Paper on the Regulation "
           "of Groundwater Abstraction in the Maltese Islands. PDF pp. 3–7.",
     "https://energywateragency.gov.mt/wp-content/uploads/2023/11/GREEN-PAPER.pdf"),
    ("11", "Malta (Apr 2025). Interim reporting on the implementation of the Programme of Measures identified under "
           "the 3rd River Basin Management Plan. pp. 4, 13, 15, 22–23, 35.",
     "https://energywateragency.gov.mt/wp-content/uploads/2025/12/Interim-Report-2025-Final-Version.pdf"),
    ("12", "Sustainable Energy and Water Conservation Unit and ERA (2015). The 2nd Water Catchment Management Plan for "
           "the Malta Water Catchment District 2015–2021. pp. 1, 2, 15, 312, 339, 342, 373. Read from a copy on "
           "ampeid.org.",
     "https://era.org.mt/wp-content/uploads/2019/05/2nd_Water_Catchment_Management_Plan-Malta_Water_in_Maltese_Islands.pdf"),
    ("13", "European Commission (26 Feb 2019). Second River Basin Management Plans – Member State: Malta. SWD(2019) 48 "
           "final, pp. 84, 121–125.", "http://publications.europa.eu/resource/celex/52019SC0048"),
    ("14", "European Commission (4 Feb 2025). Report on the implementation of the Water Framework Directive and the "
           "Floods Directive. COM(2025) 2 final, pp. 3, 24.", "http://publications.europa.eu/resource/celex/52025DC0002"),
    ("15", "European Commission (4 Feb 2025). Staff Working Document, EU overview of the third river basin management "
           "plans. SWD(2025) 13 final, pp. 51–52.", "http://publications.europa.eu/resource/celex/52025SC0013"),
    ("16", "Eurostat. env_wat_abs Annual freshwater abstraction by source and sector; updated 16 Sep 2026, retrieved "
           "6 Oct 2026, with flags. doi:10.2908/ENV_WAT_ABS.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_wat_abs/default/table"),
    ("17", "European Environment Agency. WISE Water Framework Directive 2022 reporting: surface water bodies and "
           "significant pressures (surface water and groundwater), Malta. Retrieved 6 Oct 2026.",
     "https://water.discomap.eea.europa.eu/arcgis/rest/services/WISE_WFD"),
    ("18", "European Environment Agency. WISE Water Framework Directive 2022 reporting: groundwater bodies, "
           "quantitative status, Malta (assessed 2021). Retrieved 6 Oct 2026.",
     "https://water.discomap.eea.europa.eu/arcgis/rest/services/WISE_WFD/WFD2022_GroundWaterBody_WM/MapServer/0"),
    ("19", "Sapiano M. (2020). Integrated Water Resources Management in the Maltese Islands. <i>Acque Sotterranee</i> "
           "9(3):25–32 (pages as printed in the article). doi:10.7343/as-2020-477. Open access; context, p. 30.",
     "https://doi.org/10.7343/as-2020-477"),
    ("20", "◆ Amphora Media (Aug 2026). Profit In Every Drop: The Companies Pumping Malta’s Groundwater For Free. News "
           "report of ERA data we have not seen.", "https://www.amphora.media/2026/08/profit-in-every-drop-malta-groundwater"),
    ("21", "Miżien. data/cc-101/ and tools/cc-101-report/calc.py, including from legislation.mt’s ELI sitemap the "
           "titles of every Legal Notice and Act of 2024–2026 (with text-search counts for the Acts) and of S.L. 549, "
           "423, 545, 355 and 427.", ""),
])

S.append(CondPageBreak(95 * mm))
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance, official "
                "statistics, legislation or official reports · D assertion or anecdote. ◆ marks a source known only "
                "second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. No right of reply needed for a Largely supported verdict.")])

build_report(Report(
    number="101", out=str(FIG / "report.pdf"), kicker="EU law and the national record",
    title_lines=["EU: no registration or", "prior authorisation of", "water abstraction in Malta"],
    subtitle_lines=["Testing the Commission’s description of Malta’s", "abstraction controls against the law as published"],
    quote_lines=["“Malta has failed to put in place a registration requirement for",
                 "surface water abstraction and a prior authorisation regime to",
                 "control the abstraction of surface and groundwater.”"],
    quote_size=12.5,
    attribution="European Commission, July infringements package (INF/26/1376), 8 July 2026.",
    context="Summary of its letter of formal notice INFR(2026)2115; the letter itself is not published.",
    verdict="Largely supported", verdict_note="Facts match Maltese law as published; legal points not rated",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status:",
                  "Prepared from public documents and data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Water abstraction controls in Malta", version="1.0", date="6 October 2026",
    pdf_title="EU: no registration or prior authorisation of water abstraction in Malta. Claim Check 101",
    pdf_subject="Tests the facts behind the European Commission's statement that Malta has failed to put in place a "
                "registration requirement for surface water abstraction and a prior authorisation regime to control "
                "abstraction; periodic review and legal sufficiency are not rated",
    story=S))
