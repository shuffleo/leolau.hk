---
name: writing-artwork-descriptions
description: >-
  Write concept-led, artist-voiced artwork descriptions for website display.
  Use when the user provides notes, drafts, or conversations about an artwork
  and wants a polished description, or says "write description", "artwork text",
  "work description", "website text for this piece", or "describe this work".
  Also use when writing or fixing a work's medium line, caption, label metadata,
  or alternative versions of a description.
---

# Writing Artwork Descriptions

Turn raw notes, drafts, and conversations into website-ready artwork descriptions.

## Default Voice & Balance

- Show, then tell: the physical encounter first, then the concept it carries
- Artist voice — not curator, not institution (applies to the body text; the metadata block follows institutional label conventions, see Output Format)
- 70% accessible, 30% theoretical
- Clear, layered, open-ended
- Hint of artist statement, but still a website text
- Leave room for interpretation

## Output Format

### Metadata Block (Label Conventions)

Two kinds of text sit on a work page, and they follow different rules:

- **Conventional fields** (title, year, medium line, dimensions, duration, credit, alt text, captions) follow the institutional convention for that field. Imitate how a museum registrar or collection database writes it. Do not compose them as prose or in the artist's voice.
- **Composed text** (the description body) follows the voice rules in this skill.

When unsure of a field's convention, check an authoritative style guide (Art Institute of Chicago, Philadelphia Museum of Art, Getty, MoMA, Tate, Whitney) rather than improvising. Test: *could this line sit unedited in a collection database or loan form?* If not, rewrite it.

Fields: Title, Year, then the medium line (materials, then dimensions or duration).

On this site's Work pages these are `# Title`, `Year:`, and `Type:`. `Type:` holds the medium line plus dimensions or duration. Keep the key name and change only the content. Mirror the same string in the `works/content.md` table row.

**Medium line rules:**

1. **Noun phrases only.** Materials and, where defining, technique. No verbs, no sentences, no commentary, no trailing full stop.
2. **Descending prominence.** Name what the object mostly is first, like an ingredient list. Secondary components follow. Where the logic is process, use order of application.
3. **"on" for applied medium and support** (*oil on canvas*). **"with"** for a secondary or found component (*cast resin, with salvaged steel frame*). A sculpture without a support is a plain list of media.
4. **Technique only when it defines the work** (3D-printed, cast, generative, hand-woven). Never craft-praise or subjective adjectives (*hand-crafted, delicate, striking*). Use age words like "vintage" only when they are specific (give a date, *c. 1960*); otherwise omit.
5. **No category lead-in** ("sculpture, …", "installation made from …") and no meaning. The body text carries both.
6. **Spell out materials and abbreviations on first mention**, abbreviation in parentheses: *polylactic acid (PLA)*.
7. **Capitalise only the first word.** Use commas, with "and" before the last item in a long list.
8. **Dimensions after the materials**, height × width × depth, in cm (add inches only if the audience expects them). Use "Dimensions variable" for site-specific or reconfigurable work. Time-based work: format, colour/sound, running time (mm:ss).
9. **Never invent a fact** (dimensions, date, edition, age or origin of a found object, number of channels). If it is missing, leave it out and ask for it in the post-draft note.
10. **Check sibling pages, then follow the convention.** If existing entries diverge from the convention, follow the convention for the new entry and flag the mismatch. Do not silently copy the weaker pattern.

Illustrative shapes only; never reuse for a real work:

| Work type | Medium line shape |
| :--- | :--- |
| Sculpture | Cast aluminium, enamel paint, and steel, 40 × 30 × 30 cm |
| Applied medium on support | Gouache on cotton paper, 50 × 70 cm |
| Installation | Plywood, fluorescent tubes, and speakers. Dimensions variable |
| Video | Single-channel video, colour, sound, 12:30 min |
| Audio | Stereo sound, 3:24 min |

### Length Tiers

Default to **Standard** unless the user asks otherwise.

| Tier | Words | Shape |
| :--- | :--- | :--- |
| Short / wall label | 50–75 | One paragraph: encounter + thesis |
| **Standard / web text (default)** | 120–180 | Two short paragraphs |
| Extended / catalog | 200–250 | Full arc, including series / practice context |

### Structure (Show-Then-Tell — follow this order)

1. **Visual & material encounter:** what the work physically or visually is (medium, scale, spatial form, light, weight)
2. **Conceptual thesis:** the underlying inquiry or tension it embodies
3. **Material mechanics:** how specific processes and tools build or mirror that meaning
4. **Open inquiry:** end without resolving the ambiguity

Lead with what the work *is*, not how it was set up. Technical process belongs in step 3, and only where it carries meaning.

### Sentence 1 Formula

`[Physical object / medium] + [active verb] + [central tension or inquiry]`

> *A wall-mounted array of 3D-printed tiles maps the structural overlap between cerebral folds and algorithmically generated networks.*

Do not open with an abstract theme ("This work explores…"), a tool credit, or a slow poetic lead-in.

## Writing Rules

**Prefer:**

- Clear opening sentence following the formula above
- Concrete language
- Active verbs (see the matrix below)
- Specific tensions, conditions, relations
- Grounded abstraction
- Locating presence, risk, and judgment — where the artist's hand actually is
- Tactile and spatial specifics: scale, lighting, weight, spatial presence (monolithic, fragile, wall-mounted, suspended, hand-finished)

**Avoid:**

- Press-release tone
- Curatorial jargon
- Generic phrases: "explores the intersection of", "challenges perceptions", "invites viewers to reflect", "blurs boundaries"
- Overexplaining
- Sounding too academic or too promotional
- Performative depth — text that signals substance without delivering it
- The "tool narrative" — reducing a medium to "made with X" or "created using Y"
- Descriptions that read as purely digital or theoretical, with no sense of a body, a room, or a surface

### Material Mechanics Rule

Never list a material or tool in isolation. Tie its physical property to its conceptual meaning in the same sentence.

- ❌ *"cast resin and copper"*
- ✅ *"translucent cast resin that traps suspended copper dust, holding decay mid-air"*

Only name a material if you can say what it does for the idea. If you can't, cut it.

### Vocabulary & Verb Matrix

| Replace generic terms | Use active alternatives |
| :--- | :--- |
| *explores / investigates* | *dissects, maps, confronts, destabilizes, tests the limits of* |
| *blurs boundaries / juxtaposes* | *collides, layers, intertwines, forces into tension* |
| *invites the viewer to reflect* | *frames, exposes, positions the audience within* |
| *created using [tool]* | *manipulates [tool] to…, pushes [tool] until it fails, redirects [tool]* |

Use these as defaults, not a checklist. Don't stack several in one text, and don't force a verb the work doesn't earn.

### Exemplars

The examples below are illustrative only. Never reuse their wording or details for a real work.

❌ **Avoid (curatorial jargon and tool credit):**

> This work explores the intersection of nature and artificial intelligence. Created using a custom 3D printer and machine learning algorithms, it invites viewers to reflect on post-human aesthetics.

✅ **Prefer (show-then-tell and material mechanics):**

> A dense lattice of 3D-printed PLA, hand-polished until it reads as bone and neural pathways, rests beneath a single focused beam of light. By running procedural generation scripts past their error limits, the sculpture yields organic structural flaws — framing machine failure as a biological state.

## When the Work Uses AI or Computational Processes

- Describe what the system *does* to the work (its biases, defaults, tendencies) — not just that it was used.
- Foreground what the artist chose, kept, refused, or redirected.
- Don't flatten to "made with AI" or "created using [tool]."
- If multiple agencies are at play (artist, model, dataset, culture), let the description hold that — don't reduce it to a credit line.
- If the work sits between human control and machine tendency, let the text sit there too.

## Extracting from Raw Materials

When the user gives notes or drafts, identify:

1. What the work physically is (medium, scale, space, light)
2. Core concept and central tension
3. Material / process — and the artist's relationship to it
4. Viewer experience
5. Larger stakes
6. Whether this is a single work, part of a series, or part of an ongoing practice
7. Where human presence, risk, and judgment enter the process

### Critics, Quotes, and Theory in the Notes

- Treat interpretive material (critic responses, theory dialogues, intent tables) as input to absorb, not text to paste. Translate its ideas into plain prose. Name a thinker only when the idea can't be said without them.
- Never publish a quote attributed to a named real person unless the user confirms it is genuine and gives a source. Quotes that read as generated, or carry glitch text, are not usable. Say so.
- Attribute only what the thinker actually argued. Check each theoretical claim you keep.
- Clean glitch or placeholder strings out of pasted notes (repeated tokens, broken words). Do not carry them over.

## Workflow (Draft-First)

Do **not** front-load questions. Messy notes are normal, and the user should not have to reorganise them.

1. **Extract** the items above from the notes.
2. **Draft immediately** using the best interpretation and the default tier.
3. **Flag ambiguity and gaps after the draft.** If the notes left something open, append one short note offering alternative framings, for example:
   *"Option A foregrounds [concept X]; Option B foregrounds [process Y]. Let me know if you'd like to shift toward B."*
   Also name every assumed or missing fact (year, dimensions, duration, edition, who made which step) so the user can confirm or supply it.
4. **Revise** on request.

### When to Ask Before Drafting

Ask first **only** if the notes don't reveal what the work physically is or what its main idea is — there's nothing to draft from. In that case ask 2–3 short, high-yield questions, such as:

- "What does the viewer encounter first?"
- "What is the central tension in this work?"
- "Is this a standalone piece or part of a series?"
- "What part do you want to leave open rather than explain?"

Otherwise, resolve these through the post-draft options note:

- Single work, series, or ongoing practice?
- Does the process or technology need explaining?
- Tone: clearer, more reflective, or more minimal?
- Short, standard, or extended tier?

## Writing Alternative Versions

When asked for several versions, make them differ in *how the work is told*, not in the facts.

- Vary at least two axes: **point of view** (artist "I", impersonal, institutional third person, viewer "you"), **entry point** (the object, the viewer's body, the process, the idea), and **register** (plain, deadpan, formal, confessional).
- Keep the same facts and key ideas in every version. Each one carries the full conceptual load as fluent prose, not a list of themes.
- Each version still passes the Writing Rules and Red Flags. Register changes; standards do not.
- Do not invent biography, process details, or exhibition conditions to make a voice work (how long it took, whether visitors may touch it). If a voice needs a claim the notes don't support, rephrase it so it stays true, or flag it.
- Keep each version within about 1.5× the default tier unless asked otherwise.
- Label each version with its approach in one line. On a live page, keep unused versions inside an HTML comment so they never render, and tell the user to delete them before publishing (raw `content.md` is public once pushed).
- Close with a short note on what each version foregrounds and what it assumes.

## Revision Modes

Be ready to revise into:

- More accessible
- More precise
- More artist-voiced
- Less theoretical
- Shorter / longer (switch length tier)
- More open-ended
- More connected to series/practice
- More tactile / spatial

## Red Flags — Fix If the Draft…

- Opens with an abstract theme or with mechanism instead of the physical work
- Breaks the Sentence 1 formula
- Sounds like a curator wrote it
- Is too vague or could describe any artwork
- Explains too much
- Uses too much jargon, or leans on generic verbs from the left column of the matrix
- Lacks image, experience, or tension
- Performs authenticity — sounds deep but says nothing specific
- Reduces the medium to a tool credit
- Lists a material or tool without its conceptual meaning
- Has no sense of scale, surface, light, or space
- Resolves ambiguity the work deliberately keeps open
- Has a medium line that reads as prose, uses verbs or subjective adjectives, leads with a category word, or states an unverified fact
- Writes a conventional field (medium, dimensions, credit, caption) in the artist's voice
- Publishes quotes attributed to real people without a confirmed source
- Offers alternative versions that differ only in wording, not in point of view, entry point, or register

## Default Instruction

Write an artist-voiced website description that is clear, layered, balanced, and
open-ended. Open with the physical work and its central tension, state the
concept it carries, tie each material or process to meaning, and end without
closing the question. Draft first; refine through options, not interrogation.
