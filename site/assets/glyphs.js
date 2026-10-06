/* Miżien glyphs: one vocabulary of small line-art pictures for everything the site groups, links and maps.

   The idea is the one a game designer uses to curate map icons, for attention and discovery:
   - every KIND of thing has a silhouette of its own, so it can be told from the others before a word is read;
   - the SAME kind of thing has the SAME glyph in every view (claims web, map, timeline, filters, claim pages);
   - things that are the same idea share on purpose (a theme that is the pattern "Selective metric" uses that pattern's
     glyph), and the places where that happens are listed in ALIAS below and on the glyph key page (/about/glyphs/).
   Bodies (government, agencies, parties, NGOs ...) share the glyph of their kind, never an emblem of their own.

   Each glyph is a single SVG path in a 24 x 24 box, stroke only, to be drawn with stroke-width 1.8, round caps and joins,
   no fill. Keys: display names for topics, subtopics, verdicts, patterns, stages and kinds of body; "pledge:<label>";
   "theme:T<n>"; "place:<key>" (the key is `icon` in a claim's `location`); "mode:<grouping>"; "person".
   To add a glyph, add it to the right group below. site/_data/glyphkey.js checks at build time that no two different
   things share a path (unless listed in ALIAS) and warns about topics, subtopics, labels, themes or places in the claim
   records that have no glyph. scripts/validate_claims.py reads the place keys from this file.
   Used by assets/map/map.js and assets/lens.js in the browser, and by the glyph shortcode and key page in Eleventy
   (eleventy.config.js loads this same file). */
(function (root) {
  "use strict";
  var GROUPS = [], OWN = {};
  function group(id, title, note, entries) {
    var keys = Object.keys(entries);
    GROUPS.push({ id: id, title: title, note: note, keys: keys });
    keys.forEach(function (k) { OWN[k] = entries[k]; });
  }

  group("topic", "Topics",
    "The topics the checks are filed under. Each has its own colour and glyph.", {
    "Land & Trees": "M12 2.5 L5.5 11 H9 L5 16.5 H19 L15 11 H18.5 Z M12 16.5 V21.5",
    "Climate & Energy": "M13.5 2.5 L5 13.5 H11 L10 21.5 L19 10 H13 Z",
    "Waste": "M4 6.5 H20 M9.5 6.5 V4 H14.5 V6.5 M6 6.5 L7 20.5 H17 L18 6.5 M10 10 V17 M14 10 V17",
    "Water": "M12 2.5 C12 2.5 5.5 10 5.5 14.5 A6.5 6.5 0 0 0 18.5 14.5 C18.5 10 12 2.5 12 2.5 Z",
    "Nature & Wildlife": "M21.8 7.8 L18.8 9.3 C18.8 14 15.5 17 11 17 C8 17 5.5 16 2.5 14 L7.5 11 C8.5 7 11.5 4.5 15.5 4.5 C18 4.5 19 5.8 18.6 6.6 M16 8 V8.1 M10 17 V20.5 M13.5 17 V20.5 M8.5 13 Q11.5 13 13.5 11",
    "Air": "M3 8.5 H13 A3 3 0 1 0 10 5.5 M3 12.5 H18 A3 3 0 1 1 15 15.5 M3 16.5 H9",
    "Transport": "M3 13.5 L5.5 7.5 H18.5 L21 13.5 V18 H3 Z M3 13.5 H21 M6 18 V20 M18 18 V20 M7 15.8 H8.5 M15.5 15.8 H17",
    "Governance & Promises": "M2.5 11 H21.5 M4.5 11 V20.5 H19.5 V11 M8.5 11 V3.5 H15.5 V11 M10.3 7.2 L11.6 8.5 L13.8 5.8",
    "Planning & Housing": "M3 11 L12 3.5 L21 11 M5.5 9 V20.5 H18.5 V9 M10 20.5 V14.5 H14 V20.5",
    "Noise": "M3.5 9.5 H7.5 L12.5 5 V19 L7.5 14.5 H3.5 Z M16 9 C17.3 10.5 17.3 13.5 16 15 M18.8 6.5 C21.4 9.5 21.4 14.5 18.8 17.5",
    "Tourism & Population": "M2.63 14.93 A9.5 9.5 0 0 1 20.9 9.7 Q16.97 7.49 14.81 11.44 Q10.88 9.24 8.72 13.19 Q4.79 10.98 2.63 14.93 M11.76 12.31 L13.83 19.52 M5.5 21 H14",
    "Health & Safety": "M12 20.5 C12 20.5 3 15 3 8.8 C3 5.8 5.2 3.8 7.8 3.8 C9.7 3.8 11.2 4.8 12 6.3 C12.8 4.8 14.3 3.8 16.2 3.8 C18.8 3.8 21 5.8 21 8.8 C21 15 12 20.5 12 20.5 Z M12 8.5 V14 M9.25 11.25 H14.75",
  });

  group("subtopic", "Subtopics",
    "Every subtopic has a glyph of its own, so a subgroup can be recognised before it is read. A topic with no named subtopics (Noise) keeps the topic's glyph.", {
    "Air quality & health": "M12 3 V9 M12 9 C12 11.5 10.5 12.5 8.2 13.2 M12 9 C12 11.5 13.5 12.5 15.8 13.2 M9 7.5 C5.5 8 3 13 3 17.5 C3 19.8 4.5 21 6.5 21 C8 21 9 20 9 18.5 Z M15 7.5 C18.5 8 21 13 21 17.5 C21 19.8 19.5 21 17.5 21 C16 21 15 20 15 18.5 Z",
    "Port & power emissions": "M5 21.5 L6.8 10 H11.8 L13.6 21.5 Z M5.9 15.8 H12.7 M11.3 6.8 C9.5 6.8 9.2 4.2 11 3.6 C11.8 2.4 14 2.4 14.8 3.6 C16.2 2.9 18.2 3.6 18.2 5.2 C20.4 5.2 21 8.2 18.8 8.2 C16.3 8.2 13.8 6.8 11.3 6.8 Z",
    "Electricity & grid": "M12 2.5 V5.5 M7.5 21.5 L10 5.5 H14 L16.5 21.5 M3.5 11.5 V9 H20.5 V11.5 M6.5 14.5 H17.5",
    "Emissions & targets": "M7.6 12 A2.8 2.8 0 1 0 2 12 A2.8 2.8 0 1 0 7.6 12 M16.4 12 A4.4 4.4 0 1 0 7.6 12 A4.4 4.4 0 1 0 16.4 12 M22 12 A2.8 2.8 0 1 0 16.4 12 A2.8 2.8 0 1 0 22 12",
    "Renewables": "M12 10.5 V21.5 M8.5 21.5 H15.5 M12 10.5 L14.7 3 M12 10.5 L4.1 11.9 M12 10.5 L17.1 16.6",
    "Accountability": "M3.5 5.5 L5.3 7.3 L8.5 3.5 M11.5 5.5 H20.5 M3.5 12 L5.3 13.8 L8.5 10 M11.5 12 H20.5 M3.5 16 H8.5 V21 H3.5 Z M11.5 18.5 H20.5",
    "Manifestos & pledges": "M6.5 3.5 H19.5 V15 M19.5 15 A2.25 2.25 0 0 1 19.5 19.5 H6.5 V8 M6.5 8 A2.25 2.25 0 0 1 6.5 3.5 M10 10.5 H16 M10 14 H15",
    "Heat & health": "M10 13.5 V5 A2 2 0 0 1 14 5 V13.5 A4.5 4.5 0 1 1 10 13.5 Z M12 17.5 V9.5 M17.5 5.5 H20 M17.5 9 H20 M17.5 12.5 H20",
    "Workplace safety": "M4 17 C4 10.5 7.5 6.5 12 6.5 C16.5 6.5 20 10.5 20 17 M2.5 17.5 H21.5 V20 H2.5 Z M9.5 6.8 V4 H14.5 V6.8 M9.5 8 C8.8 10.5 8.5 13 8.5 17 M14.5 8 C15.2 10.5 15.5 13 15.5 17",
    "Land take & agriculture": "M12 21.5 V8 M12 8 C10.5 6.5 10.5 4 12 2.5 C13.5 4 13.5 6.5 12 8 M12 13 C9 13 7 11 6.5 8.5 C9.5 8.5 11.5 10 12 13 M12 13 C15 13 17 11 17.5 8.5 C14.5 8.5 12.5 10 12 13 M12 18.5 C9 18.5 7 16.5 6.5 14 C9.5 14 11.5 15.5 12 18.5 M12 18.5 C15 18.5 17 16.5 17.5 14 C14.5 14 12.5 15.5 12 18.5",
    "Open spaces & parks": "M5 20.5 V5.5 H19 V20.5 M5 9.5 H19 M2.5 15 H21.5 M2.5 11.8 H5 M19 11.8 H21.5",
    "Trees & planting": "M12 21.5 V11 M5 21.5 H19 M12 14 C7.5 14.5 4.5 11.5 4.5 7 C9 6.5 12 9 12 14 Z M12 11 C12 6 15 3 20 3 C20 8 17 11 12 11 Z",
    "Dark skies": "M21 12.8 A9 9 0 1 1 11.2 3 A7 7 0 0 0 21 12.8 Z M17.5 3.8 Q17.8 6.2 20.2 6.5 Q17.8 6.8 17.5 9.2 Q17.2 6.8 14.8 6.5 Q17.2 6.2 17.5 3.8 Z",
    "Hunting & birds": "M20.5 3.5 C12 3.5 6.5 8 6.5 15 L9.5 17.5 C12.5 17.5 15 16.5 16.8 15 L13.8 14.3 L18 11.8 L15.6 10.8 C19 9 20.7 6.5 20.5 3.5 Z M3.5 20.5 L16 8",
    "Marine protection": "M3 12 C6 5.5 12.5 5.5 16 12 C12.5 18.5 6 18.5 3 12 Z M16 12 L21.5 6.5 V17.5 Z M7 10.8 V10.9",
    "Development & construction": "M3 5 H21 V19 H3 Z M3 9.7 H21 V14.3 H3 M12 5 V9.7 H7.5 V14.3 H12 V19 M16.5 9.7 V14.3",
    "Heritage & character": "M3.5 21 H20.5 M5 21 V15.5 H19 V21 M7 15.5 A5 5 0 0 1 17 15.5 M12 10.5 V2.5 M10 4.7 H14 M10.5 21 V18.8 A1.5 1.5 0 0 1 13.5 18.8 V21",
    "Housing & affordability": "M3.5 17 A3.5 3.5 0 1 0 10.5 17 A3.5 3.5 0 1 0 3.5 17 M9.5 14.5 L20 4 M17 7 L18.8 8.8 M13.5 10.5 L15.3 12.3",
    "Permits & enforcement": "M9.5 11.5 V6 A2.5 2.5 0 0 1 14.5 6 V11.5 M5 11.5 H19 V16 H5 Z M3.5 20.5 H20.5",
    "Population & labour": "M12 4.5 A2.7 2.7 0 1 0 12.01 4.5 M7.5 20 C7.5 13.5 16.5 13.5 16.5 20 M5 9 A2 2 0 1 0 5.01 9 M3 19 C3 14.5 6 13 8 13.5 M19 9 A2 2 0 1 0 19.01 9 M21 19 C21 14.5 18 13 16 13.5",
    "Short lets & concessions": "M3 5 V20 M3 17 H21 V20 M11 17 V13 H18 A3 3 0 0 1 21 16 V17 M5.5 14.5 H8.5",
    "Tourism numbers & capacity": "M7.5 7 H16.5 A2.5 2.5 0 0 1 19 9.5 V17 A2.5 2.5 0 0 1 16.5 19.5 H7.5 A2.5 2.5 0 0 1 5 17 V9.5 A2.5 2.5 0 0 1 7.5 7 Z M9.5 7 V3.5 H14.5 V7 M9.5 10.5 V16 M14.5 10.5 V16 M8 19.5 V21.5 M16 19.5 V21.5",
    "Cars & traffic": "M8 2.5 H16 A2 2 0 0 1 18 4.5 V17 A2 2 0 0 1 16 19 H8 A2 2 0 0 1 6 17 V4.5 A2 2 0 0 1 8 2.5 Z M11.1 6.8 A0.9 0.9 0 1 0 12.9 6.8 A0.9 0.9 0 1 0 11.1 6.8 M11.1 10.8 A0.9 0.9 0 1 0 12.9 10.8 A0.9 0.9 0 1 0 11.1 10.8 M11.1 14.8 A0.9 0.9 0 1 0 12.9 14.8 A0.9 0.9 0 1 0 11.1 14.8 M12 19 V21.5",
    "Public transport": "M2.5 7 H5 V5 A1.5 1.5 0 0 1 6.5 3.5 H17.5 A1.5 1.5 0 0 1 19 5 V7 H21.5 M19 7 V18 H5 V7 M5 12 H19 M8.5 7.5 H15.5 M8.5 15 V15.1 M15.5 15 V15.1 M7.5 21 V18 H16.5 V21",
    "Roads & mass transit": "M2.5 21 L8.5 3.5 M21.5 21 L15.5 3.5 M12 5 V7.5 M12 11 V14 M12 17.5 V20.5",
    "Ferries & Gozo links": "M12 6.5 V20.5 M9 9.5 H15 M14 4.5 A2 2 0 1 1 10 4.5 A2 2 0 1 1 14 4.5 M3.5 13.5 C4 18 8 20.5 12 20.5 C16 20.5 20 18 20.5 13.5 M3.5 13.5 L2.5 11.5 M20.5 13.5 L21.5 11.5",
    "Construction waste": "M2.5 9 H14 V16 H2.5 Z M14 11 H18 L21.5 14 V16 H14 M6.5 19 A1.8 1.8 0 1 0 6.5 19.01 M17.5 19 A1.8 1.8 0 1 0 17.5 19.01 M4.5 9 L6.5 5.5 L9 7 L11 4 L12.5 9",
    "Landfill & treatment": "M2.5 20.5 C4 17 6 14.5 9 14 H15 C18 14.5 20 17 21.5 20.5 Z M3 8.5 Q5 3.5 8 7.5 Q11 3.5 13 8.5 M15.5 11.5 Q17 9 19 11 Q21 9 22 11.5",
    "Recycling & separation": "M4.48 9.26 A8 8 0 0 1 19.52 9.26 M19.52 9.26 L20.87 5.93 M19.52 9.26 L16.34 7.57 M19.52 14.74 A8 8 0 0 1 4.48 14.74 M4.48 14.74 L3.13 18.07 M4.48 14.74 L7.66 16.43",
    "Bathing water & sewage": "M2.5 6.5 Q5.5 3 8.5 6.5 Q11.5 10 14.5 6.5 Q17.5 3 21.5 6.5 M2.5 12.5 Q5.5 9 8.5 12.5 Q11.5 16 14.5 12.5 Q17.5 9 21.5 12.5 M2.5 18.5 Q5.5 15 8.5 18.5 Q11.5 22 14.5 18.5 Q17.5 15 21.5 18.5",
    "Flood relief": "M7 14.5 H17 A3.5 3.5 0 0 0 17.5 7.7 A5.5 5.5 0 0 0 7.5 8.8 A3 3 0 0 0 7 14.5 Z M8 17.5 L7 20.5 M12.5 17.5 L11.5 20.5 M17 17.5 L16 20.5",
    "Water supply & groundwater": "M9 3.5 H15 M12 3.5 V7 M3 7 H15 C17.5 7 19.5 9 19.5 11.5 V12 H16 V11.5 C16 10.8 15.5 10.5 15 10.5 H3 Z M17.75 15.5 C17.75 15.5 15.5 18 15.5 19.2 A2.25 2.25 0 0 0 20 19.2 C20 18 17.75 15.5 17.75 15.5 Z",
  });

  group("verdict", "Verdicts",
    "The verdict scale, and claims not yet checked. The glyph repeats the colour, so a verdict can be read without colour.", {
    "Supported": "M5 12.5 L10 17.5 L19 7",
    "Largely supported": "M4 13 L8.5 17.5 L15.5 9 M12.5 17 L14 18.5 L21 10",
    "Not substantiated": "M8.8 9 A3.3 3.3 0 1 1 13.6 12 C12.4 12.6 12 13.3 12 14.6 M12 18 V18.1",
    "Misleading": "M12 3.5 L21.5 20 H2.5 Z M12 10 V14.5 M12 17 V17.1",
    "Contradicted": "M6 6 L18 18 M18 6 L6 18",
    "Not yet checked": "M5.5 12 V12.1 M12 12 V12.1 M18.5 12 V12.1",
  });

  group("pledge", "Pledge labels",
    "A pledge gets a label instead of, or as well as, a verdict. The flag means \"a pledge\"; each label has a shape of its own.", {
    "pledge": "M5 21 V4 M5 4.5 H16 L13.8 8.3 L16 12 H5",
    "pledge:Not measurable": "M2.5 8 H21.5 V16 H2.5 Z M6.5 8 V12 M10.5 8 V11 M14.5 8 V12 M18.5 8 V11",
    "pledge:Not yet due": "M7 3.5 H17 M7 20.5 H17 M8 3.5 C8 9 12 10 12 12 C12 14 8 15 8 20.5 M16 3.5 C16 9 12 10 12 12 C12 14 16 15 16 20.5",
    "pledge:On track": "M3 17 L9 11 L13 15 L20 8 M14.5 7.5 H20.5 V13.5",
    "pledge:Off track": "M3 7 L9 13 L13 9 L20 16 M14.5 16.5 H20.5 V10.5",
    "pledge:Met": "M12 2.5 A6.5 6.5 0 1 0 12.01 2.5 M9 9 L11.2 11.2 L15.2 6.8 M9 14.8 L7.5 21.5 L10.7 19.6 L12 21.8 L13.3 19.6 L16.5 21.5 L15 14.8",
    "pledge:Missed": "M8.5 2.5 H15.5 L21.5 8.5 V15.5 L15.5 21.5 H8.5 L2.5 15.5 V8.5 Z M8.5 8.5 L15.5 15.5 M15.5 8.5 L8.5 15.5",
  });

  group("pattern", "Patterns",
    "Recurring ways a claim can mislead (provisional until a report is finished).", {
    "Selective metric": "M10.5 4 A6.5 6.5 0 1 0 10.51 4 M15.2 15.2 L20.5 20.5",
    "Input-as-outcome": "M3.5 5 H20.5 L14 12.5 V19.5 L10 17.5 V12.5 Z",
    "Compliance-not-health": "M12 3 L19 6 V11 C19 15.5 16 19 12 21 C8 19 5 15.5 5 11 V6 Z M9 12 L11 14 L15 10",
    "Conditional-turned-unconditional": "M6 3.5 V20.5 M6 12 C11 12 12 6 18 6 M15 3 L18 6 L15 9",
    "Promise-without-baseline": "M10 3.5 V18 M10 3.5 L19 7.5 L10 11.5 M2.5 21 H7 M13 21 H21.5",
    "No pattern tag": "M12 8 A4 4 0 1 0 12.01 8",
  });

  group("stage", "Stages",
    "Where a check stands, from not started to published.", {
    "Not started": "M12 3 A9 9 0 1 0 12.01 3 M12 7 V12 L15.5 14",
    "In progress": "M4 12 H19 M13 6 L19 12 L13 18",
    "Drafted": "M4 20 L8.5 19 L19.5 8 L16 4.5 L5 15.5 Z M14 6.5 L17.5 10",
    "Right of reply": "M4 4.5 H20 V15 H10.5 L6.5 19.5 V15 H4 Z",
    "Published": "M3.5 5 H10.5 C11.4 5 12 5.6 12 6.5 V20 C12 19.2 11.4 18.6 10.5 18.6 H3.5 Z M20.5 5 H13.5 C12.6 5 12 5.6 12 6.5 V20 C12 19.2 12.6 18.6 13.5 18.6 H20.5 Z",
  });

  group("speaker", "Who said it",
    "The kinds of body, and people, that make claims. Every body shares the glyph of its kind, on purpose: the register is open-ended and neutral, and a glyph of its own could read as a logo or an endorsement.", {
    "Government & ministers": "M3 9 L12 4 L21 9 Z M5.5 9.5 V17.5 M10 9.5 V17.5 M14 9.5 V17.5 M18.5 9.5 V17.5 M3 20 H21",
    "Public agencies & companies": "M4 20.5 V8 L9 5 V20.5 M9 9 L15 6 V20.5 M15 10 L20 8 V20.5 M2.5 20.5 H21.5 M6 11 H7 M6 14 H7 M11.5 12 H12.5 M11.5 15 H12.5 M17 13 H18",
    "Regulators & authorities": "M8.5 3.5 H15.5 V6.5 H8.5 Z M6.5 5 H4.5 V21 H19.5 V5 H17.5 M8 11.5 H16 M8 15.5 H13",
    "Courts, tribunals & oversight": "M13.67 2.15 L21.45 9.93 L16.93 14.45 L9.15 6.67 Z M13 10.6 L5 18.6 M3 21 H12",
    "Political parties": "M4.5 10 H19.5 V20.5 H4.5 Z M8.5 10 L12 4 L15.5 10 M9 15 H15",
    "NGOs & unions": "M8 7.5 A2.8 2.8 0 1 0 8.01 7.5 M16 7.5 A2.8 2.8 0 1 0 16.01 7.5 M2.5 19.5 C2.5 15 13.5 15 13.5 19.5 M10.5 19.5 C10.5 15 21.5 15 21.5 19.5",
    "Business & industry": "M4 8 H20 V19.5 H4 Z M9 8 V5 H15 V8 M4 13 H20",
    "Media": "M4 5 H17 V19.5 H6 C4.9 19.5 4 18.6 4 17.5 Z M17 9 H20 V17.5 C20 18.6 19.1 19.5 18 19.5 M7 8.5 H14 M7 12 H14 M7 15.5 H11",
    "EU & international": "M12 3 A9 9 0 1 0 12.01 3 M3 12 H21 M12 3 C15.5 6.5 15.5 17.5 12 21 C8.5 17.5 8.5 6.5 12 3",
    "Research & statistics": "M5 20 V11 M10 20 V6 M15 20 V13 M20 20 V16 M3 20.5 H21.5",
    "person": "M12 11.5 A4 4 0 1 0 12.01 11.5 M4.5 21 C4.5 16.5 8 14.5 12 14.5 C16 14.5 19.5 16.5 19.5 21",
  });

  group("theme", "Themes",
    "Links between claims. A theme that is the same idea as a pattern, topic or subtopic shares that glyph.", {
    "theme:T1": "M2.5 3.5 H21.5 V8 H2.5 Z M12 8 V21 M5 14.5 L12 11 L19 14.5 M7.5 20 L12 11 L16.5 20",
    "theme:T2": "M2.5 10.5 A8 8 0 1 0 18.5 10.5 A8 8 0 1 0 2.5 10.5 M16.16 4.84 L18.66 7.34 A8 8 0 0 1 7.34 18.66 L4.84 16.16 M6.2 14 C5.2 9 8.2 6.5 13.5 7 C14 11.5 11.5 14.5 6.2 14 Z M6.2 14 L10 10",
    "theme:T3": "M3.54 8.92 A9 9 0 0 1 20.16 8.2 M21.04 4.91 L20.16 8.2 L17.08 6.76 M20.46 15.08 A9 9 0 0 1 3.84 15.8 M2.96 19.09 L3.84 15.8 L6.92 17.24 M12 7.5 C12 7.5 8.5 11 8.5 13.8 A3.5 3.5 0 0 0 15.5 13.8 C15.5 11 12 7.5 12 7.5 Z",
    "theme:T4": "M5.64 19.36 A9 9 0 1 1 18.36 19.36 M12 13.5 L16.2 8.8 M12 13.5 V13.6 M12 6.6 V7.4 M7.2 8.5 L7.8 9.1 M5.6 13 H6.4",
    "theme:T5": "M5 8.5 H20 L17 14 H8 Z M8.5 8.5 C8.5 5.5 11 4.5 13 5.5 C14.5 4 17.5 5 17.5 8.5 M8 14 L2.5 11 M10 14 L8.5 21.5 M17 14 L18.3 16 M18.5 18.7 A2.7 2.7 0 1 0 18.51 18.7",
    "theme:T7": "M11 3.5 A8.5 8.5 0 1 0 20.5 13 M11 8 A4 4 0 1 0 15 12 M11.5 12.5 L20 4 M16.5 3.5 H20.5 V7.5",
    "theme:T8": "M3 6 L12 3 L21 8 L19 20 L5 21 Z M7.5 17 V12.5 L11.5 9 L15.5 12.5 V17 Z",
    "theme:T11": "M6.5 10 A3.5 3.5 0 1 0 13.5 10 A3.5 3.5 0 1 0 6.5 10 M14.38 5.62 L15.66 4.34 M10 3.8 L10 2 M5.62 5.62 L4.34 4.34 M3.8 10 L2 10 M5.62 14.38 L4.34 15.66 M20.5 9.5 L14.5 17 H19 L16 22",
    "theme:T12": "M2.5 12 C5 7.5 8.5 5.5 12 5.5 C15.5 5.5 19 7.5 21.5 12 C19 16.5 15.5 18.5 12 18.5 C8.5 18.5 5 16.5 2.5 12 Z M9.5 12 A2.5 2.5 0 1 0 14.5 12 A2.5 2.5 0 1 0 9.5 12",
    "theme:T14": "M3 6 A4 1.8 0 1 0 11 6 A4 1.8 0 1 0 3 6 M3 6 V9.6 A4 1.8 0 0 0 11 9.6 V6 M3 9.6 V13.2 A4 1.8 0 0 0 11 13.2 V9.6 M3 13.2 V16.8 A4 1.8 0 0 0 11 16.8 V13.2 M13 9.6 A4 1.8 0 1 0 21 9.6 A4 1.8 0 1 0 13 9.6 M13 9.6 V13.2 A4 1.8 0 0 0 21 13.2 V9.6 M13 13.2 V16.8 A4 1.8 0 0 0 21 16.8 V13.2",
  });

  group("place", "Places",
    "Landmark emblems on the map. A place with an identity of its own has its own emblem; places that are the same kind of thing (two ferry terminals, two road works, two parks) share one.", {
    "place:parliament": "M2 20.5 H22 M4 20.5 V9.5 H11 V20.5 M13 20.5 V9.5 H20 V20.5 M3 9.5 H21 M6 12 V18 M8.5 12 V18 M15.5 12 V18 M18 12 V18 M4 7 H20",
    "place:castille": "M2 20.5 H22 M3 20.5 V10.5 H21 V20.5 M10 20.5 V16 A2 2 0 0 1 14 16 V20.5 M3 10.5 L12 6.5 L21 10.5 M12 6.5 V2.5 L15.5 3.5 L12 4.6 M6 13 V15.5 M18 13 V15.5",
    "place:citygate": "M2 21 H22 M4.5 21 V5.5 L8.5 4 V21 M15.5 21 V4 L19.5 5.5 V21 M8.5 21 H15.5 M10.5 9 H13.5 M10.5 13 H13.5",
    "place:barrakka": "M2 20.5 H22 M3 20.5 V11.5 A3 3 0 0 1 9 11.5 V20.5 M9 11.5 A3 3 0 0 1 15 11.5 V20.5 M15 11.5 A3 3 0 0 1 21 11.5 V20.5 M3 8.5 H21 M17 6 L21 4.5",
    "place:ravelin": "M12 2.5 L21.5 10 L18 20.5 H6 L2.5 10 Z M7.5 17.5 H16.5 M12 6.5 V11 M9.5 11 H14.5",
    "place:waterfront": "M2 20.5 H22 M3 20.5 V12 H21 V20.5 M5 20.5 V16 A1.5 1.5 0 0 1 8 16 V20.5 M10.5 20.5 V16 A1.5 1.5 0 0 1 13.5 16 V20.5 M16 20.5 V16 A1.5 1.5 0 0 1 19 16 V20.5 M3 12 L12 8 L21 12",
    "place:tower": "M8 19 V8.5 H15 V19 M7 8.5 H16 M8 5.5 H15 V8.5 M8 5.5 V4 M11.5 5.5 V4 M15 5.5 V4 M10.5 12 H12.5 M2 21.5 C5 20.5 7 22.5 10 21.5 C13 20.5 15 22.5 18 21.5 C19.5 21 20.5 21.2 22 21.5",
    "place:landfill": "M2 20.5 C5 13 9 10 13 12 C16 13.5 19 16.5 22 20.5 Z M15.5 9.5 V4 H17.5 V10.5 M7 17.5 L9.5 15 M12 17 L14 14.5",
    "place:flyover": "M2 18 C8 18 10 10 16 10 H22 M2 12 H8 C14 12 15 18 22 18 M6 18 V21.5 M18 10 V21.5 M12 13.5 V21.5",
    "place:ro_plant": "M6 21 V12.5 H18 V21 Z M6 16 H18 M9.5 12.5 V21 M14.5 12.5 V21 M12 2.5 C12 2.5 9 6.5 9 8.5 A3 3 0 0 0 15 8.5 C15 6.5 12 2.5 12 2.5 Z",
    "place:park": "M2 20.5 H22 M7 20.5 V13.5 M7 4 C3 6 3 12 7 13.5 C11 12 11 6 7 4 Z M13 15.5 H21 M14 15.5 L13 20.5 M20 15.5 L21 20.5 M14.5 13 H19.5",
    "place:crane": "M4.5 21 V5.5 H20.5 M4.5 5.5 L8.5 2.5 H18.5 L20.5 5.5 M15 5.5 V10.5 M12.5 10.5 H17.5 V13.5 H12.5 Z M9.5 21 V17 H21 V21 M2 21 H22",
    "place:ferry": "M3 15 H21 L19 19 H5 Z M6.5 15 V11.5 H16.5 V15 M8.5 11.5 V8.5 H13.5 V11.5 M17.5 8 V11.5 M2 21.5 C5 20.5 7 22.5 10 21.5 C13 20.5 15 22.5 18 21.5 C19.5 21 20.5 21.2 22 21.5",
    "place:pin": "M12 21 C12 21 5 14 5 9 A7 7 0 0 1 19 9 C19 14 12 21 12 21 Z M12 9 V9.1",
    "place:cross": "M8.8 2.5 L12 5.3 L15.2 2.5 L14 10 L21.5 8.8 L18.7 12 L21.5 15.2 L14 14 L15.2 21.5 L12 18.7 L8.8 21.5 L10 14 L2.5 15.2 L5.3 12 L2.5 8.8 L10 10 Z",
    "place:valletta": "M3 20.5 V16 H21 V20.5 M2 20.5 H22 M6 16 V13 A4 4 0 0 1 14 13 V16 M10 9 V6.5 M16.5 16 V10 L18 3 L19.5 10 V16",
    "place:era": "M2.5 21.5 H14.5 M4 21.5 V10.5 H13 V21.5 M7 14 V14.1 M10 14 V14.1 M8.5 21.5 V17.5 M13 10.5 C12 5.5 15.5 2.8 21 2.8 C21.5 8 18.5 10.5 13 10.5 Z",
    "place:cittadella": "M3 21.5 V14 H6.5 V16 H17.5 V14 H21 V21.5 M2 21.5 H22 M8.5 16 V12 A3.5 3.5 0 0 1 15.5 12 V16 M12 8.5 V5.5",
    "place:airport": "M12 2.5 C13.2 2.5 14 3.5 14 5 V9 L21.5 14 V16.5 L14 14 V18.5 L16.5 20.5 V22 L12 21 L7.5 22 V20.5 L10 18.5 V14 L2.5 16.5 V14 L10 9 V5 C10 3.5 10.8 2.5 12 2.5 Z",
    "place:tunnel": "M3 15 V5 H21 V15 M7.5 15 V11 A4.5 4.5 0 0 1 16.5 11 V15 M3 18 C6 16.5 8 19.5 12 18 C16 16.5 18 19.5 21 18 M3 21.5 C6 20 8 23 12 21.5 C16 20 18 23 21 21.5",
    "place:lagoon": "M12 3 V14 M12 3.5 L19.5 14 H12 M12 8 L6 14 M4 16.5 H20 L18 19 H6 Z M2 21.5 C5 20.5 7 22.5 10 21.5 C13 20.5 15 22.5 18 21.5 C19.5 21 20.5 21.2 22 21.5",
    "place:luzzu": "M2.5 11 C8 14 14 13.5 17.5 10.5 C19.5 8.5 20.5 6.5 21.5 3.5 C20.5 11 17.5 18.5 13 18.5 H8 C5 18.5 3 15.5 2.5 11 Z M17 13.2 V13.3 M2 21.5 C5 20.5 7 22.5 10 21.5 C13 20.5 15 22.5 18 21.5 C19.5 21 20.5 21.2 22 21.5",
    "place:hospital": "M2.5 21.5 V11 H6 V3.5 H18 V11 H21.5 V21.5 Z M12 8.5 V14.5 M9 11.5 H15",
    "place:sewage": "M5 7 A7 2.8 0 1 0 19 7 A7 2.8 0 1 0 5 7 M5 7 V18 A7 2.8 0 0 0 19 18 V7 M5 13 C7.5 11.5 9.5 14.5 12 13 C14.5 11.5 16.5 14.5 19 13",
    "place:cliffs": "M2.5 20 L4 8 L9 4.5 H15 L13.5 8.5 L16 12 L14 16 L15.5 20 M17.5 9.5 C18.8 8.3 20 10.5 21.5 9.3 M17.5 14.5 C18.8 13.3 20 15.5 21.5 14.3 M2.5 20.5 C5 19 7 22 10 20.5 C13 19 15 22 18 20.5 C19.5 19.8 20.5 20 21.5 20.5",
    "place:powerstation": "M2 21.5 H22 M3 21.5 V15 H21 V21.5 M6 15 L6.5 9 H9.5 L10 15 M14 15 L14.5 9 H17.5 L18 15 M8 6.5 C8 5 10 4.5 9.5 2.5 M16 6.5 C16 5 18 4.5 17.5 2.5",
    "place:fort": "M3 21 V6.5 H7 V9.5 H10 V6.5 H14 V9.5 H17 V6.5 H21 V21 M9.5 21 V16 A2.5 2.5 0 0 1 14.5 16 V21 M2 21 H22",
    "place:saltpans": "M3 4 L12 3 L11 8 L3.5 9 Z M14 5 L21 4 L20.5 9.5 L13.5 10.5 Z M3.5 11.5 L10 12.5 L9 16.5 L4 16 Z M12.5 13 L20 12.5 L21 16.5 L13 17 Z M2.5 20.5 C5 19 7 22 10 20.5 C13 19 15 22 18 20.5 C19.5 19.8 20.5 20 21.5 20.5",
    "place:bay": "M2.5 2.5 H18 C9 4.5 7 9 7 12 C7 15 9 19.5 18 21.5 H2.5 Z M13 9.5 C15 8 17 11 19 9.5 M13 15 C15 13.5 17 16.5 19 15",
    "place:temple": "M4.5 21 V11.5 H2.5 V8.5 L11 7.5 V11.5 H4.5 M9 11.5 V21 M15 21 V7 H13 V3.5 H21.5 V7 H15 M19.5 7 V21",
    "place:reeds": "M5.5 20.5 V13 A1.6 1.6 0 0 0 7.1 11.4 V7.6 A1.6 1.6 0 0 0 3.9 7.6 V11.4 A1.6 1.6 0 0 0 5.5 13 M11.5 20.5 V10.5 A1.6 1.6 0 0 0 13.1 8.9 V4.6 A1.6 1.6 0 0 0 9.9 4.6 V8.9 A1.6 1.6 0 0 0 11.5 10.5 M17.5 20.5 V14 A1.6 1.6 0 0 0 19.1 12.4 V8.6 A1.6 1.6 0 0 0 15.9 8.6 V12.4 A1.6 1.6 0 0 0 17.5 14 M2 21.5 H22",
    "place:gardjola": "M3 21.5 V17.5 H21 V21.5 Z M7 17.5 L8.5 15 V10.5 H15.5 V15 L17 17.5 M8.5 10.5 C8.5 6.5 10.5 5 12 5 C13.5 5 15.5 6.5 15.5 10.5 M12 5 V2.5 M12 13 V13.1",
  });

  group("mode", "Views and groupings",
    "The controls above the claims web.", {
    "mode:topic": "M12 3 A9 9 0 1 0 12.01 3 M7 9 A1.5 1.5 0 1 0 7.01 9 M16 8 A1.5 1.5 0 1 0 16.01 8 M11 16 A1.5 1.5 0 1 0 11.01 16",
    "mode:subtopic": "M12 3 A9 9 0 1 0 12.01 3 M12 7.5 A4.5 4.5 0 1 0 12.01 7.5 M12 3 V7.5 M12 16.5 V21 M3 12 H7.5 M16.5 12 H21",
    "mode:verdict": "M12 3 V20.5 M7.5 20.5 H16.5 M4.5 6.5 H19.5 M4.5 6.5 L2 12.5 H7 Z M19.5 6.5 L17 12.5 H22 Z",
    "mode:pattern": "M12 3 A9 9 0 1 0 12.01 3 M12 7 A5 5 0 1 0 12.01 7 M12 11 A1 1 0 1 0 12.01 11",
    "mode:status": "M3 12 H21 M5 12 A1.5 1.5 0 1 0 5.01 12 M12 12 A1.5 1.5 0 1 0 12.01 12 M19 12 A1.5 1.5 0 1 0 19.01 12",
    "mode:speaker": "M8.5 6 A3.5 3.5 0 0 1 15.5 6 V10.5 A3.5 3.5 0 0 1 8.5 10.5 Z M5 10.5 A7 7 0 0 0 19 10.5 M12 17.5 V21 M8.5 21 H15.5",
    "mode:year": "M4 6.5 H20 V20 H4 Z M4 10.5 H20 M8 4 V8 M16 4 V8 M7.5 14 H9 M11.25 14 H12.75 M15 14 H16.5 M7.5 17 H9 M11.25 17 H12.75",
    "mode:network": "M5 6 A2 2 0 1 0 5.01 6 M19 7 A2 2 0 1 0 19.01 7 M12 18 A2 2 0 1 0 12.01 18 M6.5 7.5 L11 16 M17.5 8.5 L13 16 M7 6.2 L17 6.8",
  });

  // Shared on purpose: the same idea, so the same glyph. [name] -> [the name whose glyph it uses]
  var ALIAS = {
    "theme:T6": "Selective metric",
    "theme:T9": "Compliance-not-health",
    "theme:T10": "Tourism & Population",
    "theme:T13": "Noise",
    "theme:T15": "Heritage & character",
    "place:bus": "Public transport",
    "place:pylon": "Electricity & grid",
    "mode:pledges": "pledge"
  };

  // Every name that has a glyph, own or shared, as one flat table.
  var PATHS = {};
  Object.keys(OWN).forEach(function (k) { PATHS[k] = OWN[k]; });
  Object.keys(ALIAS).forEach(function (k) { PATHS[k] = OWN[ALIAS[k]]; });
  // Place emblems by `icon` key (without the "place:" prefix); "pin" is the fallback.
  var PLACES = {};
  Object.keys(PATHS).forEach(function (k) { if (k.indexOf("place:") === 0) PLACES[k.slice(6)] = PATHS[k]; });

  function path(name) { return PATHS[name] || null; }
  // An <svg> string; size in px (or "1em" when omitted). Style it with .gl (assets/theme.css).
  function svg(name, o) {
    var d = path(name); if (!d) return "";
    o = o || {};
    var size = o.size ? ' width="' + o.size + '" height="' + o.size + '"' : "";
    return '<svg class="gl' + (o.cls ? " " + o.cls : "") + '"' + size + ' viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>';
  }

  root.MizienGlyphs = { groups: GROUPS, own: OWN, alias: ALIAS, paths: PATHS, places: PLACES, path: path, svg: svg };
})(typeof window !== "undefined" ? window : this);
