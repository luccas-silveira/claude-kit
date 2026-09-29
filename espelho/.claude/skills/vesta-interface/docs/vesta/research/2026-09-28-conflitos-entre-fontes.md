I read the spec, all four main skill files, the core hallmark references, the impeccable references and its detector rule catalog, the ui-ux-pro-max `pro-rules.md` and `quick-reference.md`, and the three taste variants (minimalist, soft, brutalist).

**Path legend** (all cites below are `prefix:line`):
- **H** = `__HOME__/.claude/skills/hallmark/` (SKILL.md unless a file is named)
- **T** = `__HOME__/Code/ux-lab/vendor/taste-skill/skills/taste-skill/SKILL.md`
- **Tm / Ts / Tb** = `__HOME__/Code/ux-lab/vendor/taste-skill/skills/{minimalist-skill,soft-skill,brutalist-skill}/SKILL.md`
- **I** = `__HOME__/Code/ux-lab/vendor/impeccable/.claude/skills/impeccable/` (SKILL.md or `reference/*.md`)
- **IJ** = `__HOME__/Code/ux-lab/vendor/impeccable/crates/live/assets/antipatterns.json`. This is the detector's rule catalog; it has no useful line numbers, so I cite it by rule id.
- **U** = `__HOME__/Code/ux-lab/vendor/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/` (SKILL.md, `references/quick-reference.md` = **Uq**, `references/pro-rules.md` = **Up**)

---

## 1. Contradictions between sources

### Fonts
| Topic | Side A | Side B |
|---|---|---|
| Inter | H bans it outright: `typography.md:40,236` | T only discourages it as a default and allows it for neutral, Linear-style or public-sector briefs: `T:169-170`. Tb recommends Inter Extra Bold: `Tb:28` |
| Geist | H makes it the default body face: `typography.md:89`. T recommends it: `T:169`. Tm and Ts use it | The IJ rule `overused-font` flags Geist next to Inter, Roboto, Fraunces, Plus Jakarta Sans and Space Grotesk |
| Fraunces / Instrument Serif | H lists both as display faces and uses Fraunces in its sample token: `typography.md:21,58,60`. Lumen theme uses Instrument Serif: `H:277`. Tm recommends Instrument Serif: `Tm:27` | T bans both as defaults: `T:180`. I calls Fraunces a "stopped looking" default: `I new-work.md:67`, and IJ `overused-font` flags it |
| Space Grotesk / Plus Jakarta Sans / Outfit | H uses Space Grotesk (Cobalt) and Plus Jakarta Sans (Hum): `H:277`. T recommends Outfit: `T:169`. Ts recommends Plus Jakarta Sans: `Ts:15` | I lists all three as training-data defaults: `I new-work.md:67`. H bans Outfit as a default: `typography.md:75` |
| Serif as default | H's default genre is editorial with a serif display: `H:230`, `typography.md:117` | T says serif is "VERY DISCOURAGED" as a default and should be sans unless the brief is genuinely editorial or luxury: `T:173-178` |
| System stack | H bans a system stack as the only stack: `typography.md:40,236` | I says Operate and Read surfaces are "well served by system stacks": `I new-work.md:67` |
| Number of families | H requires a pairing (minimum 2, ceiling 3) and bans single-font pages: `typography.md:7,15,238` | I says "One font family": `I distill.md:52`, and for Operate "a single well-tuned family": `I typeset.md:8` |
| Size scale | H uses a ratio scale (1.25) and at most 5 sizes: `typography.md:9,173,205`. IJ `flat-type-hierarchy` flags steps under 1.25× | U uses an additive scale 12/14/16/18/24/32 (16→18 is 1.125×): `Uq:119`. I says 3–4 sizes: `I distill.md:52` |
| Heading weight | H requires at least 300 units of contrast with body; 500/600 headings are banned: `typography.md:210` | U says headings 600–700 and labels 500: `Uq:122` |
| Italic in headings | H bans italic headers and italic emphasis words: `H:56` | T says emphasis should use "italic or bold of the SAME font" and adds descender-clearance rules for italic display: `T:179,183` |
| Display tracking and leading | H: display leading 1.05–1.2 and an all-caps floor of 1.0 (gate 55): `typography.md:10,224`. I: tracking floor −0.04em: `I craft-floor.md:12` | T uses `tracking-tighter leading-none` (−0.05em / 1.0): `T:166`. Tb uses leading 0.85–0.95 and tracking to −0.06em: `Tb:31-32` |
| Display maximum size | H ≤5.5rem, 6rem cap: `typography.md:190`. I 6rem max: `I craft-floor.md:12` | Tb `clamp(4rem,10vw,15rem)`: `Tb:30` |
| Minimum text size | H: body ≥16px, nothing under 10px: `typography.md:223,240`. IJ `undersized-ui-text` flags UI text under 11px | Tb sets navigation and metadata at 10–14px, uppercase: `Tb:39-42`. T's eyebrow examples use 10.5–11px: `T:253` |
| Light text on dark | H: reduce body weight by 50: `color.md:68` | I: one step more weight, plus more leading and tracking: `I typeset.md:48` |

### Punctuation, emoji and glyphs
| Topic | Side A | Side B |
|---|---|---|
| **Em dash** | H prescribes em dash for interruptions and en dash for ranges (`10–20`): `copy.md:59`, `typography.md:219`. It also uses `—` as the placeholder for a missing metric: `H:48`, and offers em dash as a footer separator: `component-cookbook.md:127` | T allows **zero** em or en dashes anywhere; ranges use a hyphen: `T:649,685-701,920`. I flags only saturation (8 or more at about 1 per 500 characters, advisory): IJ `em-dash-overuse` |
| Middle dot | H uses `·` heavily and offers it as a separator: `component-cookbook.md:127` | T rations it to one per line: `T:645` |
| Unicode glyphs as icons | H's own 8-state demo uses ⌛ ⚠ ✓: `H:111-113` | I bans "Unicode glyphs or emoji standing in for an icon system": `I craft-floor.md:40` |
| Emoji in text | H, U and I ban emoji only as icons: `assets.md:61`, `Uq:81`, `I craft-floor.md:40` | T discourages emoji anywhere: `T:148`. Tm bans them everywhere, including alt text: `Tm:20` |

### Icons
| Topic | Side A | Side B |
|---|---|---|
| Lucide | H makes Lucide the SaaS default: `anti-patterns.md:199`, `assets.md:49,394`. U names Heroicons and Lucide: `Uq:81`, `Up:13` | T discourages Lucide unless asked and puts Phosphor first: `T:141-142,623`. Tm bans Lucide, Feather and Heroicons: `Tm:15`. Ts bans Lucide, FontAwesome and Material: `Ts:16` |
| Hand-drawn SVG | H allows "build a custom SVG mark": `anti-patterns.md:223`. I allows "authored SVG": `I craft-floor.md:40` | T says NEVER hand-roll icon SVGs: `T:143` |

This matters for the spec: shadcn's default icon set is Lucide.

### Color
| Topic | Side A | Side B |
|---|---|---|
| Color space | H: OKLCH only, for every color: `color.md:7`, `H:451` | I: use the project's existing color space and prefer OKLCH for new palettes: `I colorize.md:38`. U uses semantic tokens with hex/Tailwind examples: `Uq:120,123`. T, Tm and Tb specify hex/Tailwind: `T:193-196`, `Tm:33-40`, `Tb:55-63` |
| Accent dosage | H: one accent (two at most), ≤3% of the viewport, never as big fills: `color.md:8,80,95`. T: max 1 accent: `T:186` | I's color strategies include "Committed" (30–60% of the surface) and "Drenched": `I new-work.md:65`. I also says there is "no fixed percentage rule": `I colorize.md:27` |
| Neutrals | H: neutrals must be tinted; zero-chroma gray is banned: `color.md:10,77` | I: "Neutral gray is valid when it serves the world": `I colorize.md:44` |
| Pure white | H: `#fff` is banned as a base surface: `color.md:76`. T: no pure `#000`/`#fff`: `T:585,601` | Tm uses a `#FFFFFF` canvas: `Tm:33`. H itself allows pure white in modern-minimal: `verbs/audit.md:16` |
| Cream / beige paper | H's example palette is warm oat paper: `color.md:25`. Ts's "Editorial Luxury" uses cream `#FDFBF7`: `Ts:26`. Tm uses bone `#F7F6F3`: `Tm:33` | T bans the beige family for premium-consumer briefs: `T:192-207`. I calls cream plus serif the AI rut: `I new-work.md:69-71`, and IJ has `cream-palette` |
| Gradients | H: two stops only: `color.md:83` | T allows a "brand-appropriate gradient" in bento cells: `T:259`. I calls gradients "the gap wearing chrome": `I new-work.md:128` |
| **Dark mode default** | T: design both modes, mandatory for consumer pages, default to `prefers-color-scheme`: `T:531-535,574,588`. U: design light and dark together and test both: `Uq:87`, `Up:72,96` | I: never a default; pick light or dark from the physical use scene: `I craft-floor.md:42`, `I new-work.md:65`. H: each theme is a single paper band and dark is optional: `export-formats.md:316`, `contract.md:22` |
| Brand accent in dark mode | H: reduce accent chroma by 0.02–0.04: `color.md:69`. U: desaturated tonal variants: `Uq:124` | T: "Don't desaturate the brand into a dark mode": `T:584` |
| Body contrast target | H, I and U: 4.5:1 minimum, 7:1 as a target or AAA option: `color.md:57`, `I colorize.md:59`, `Uq:125` | T: AAA for body text: `T:534` |

### Layout, spacing, cards, radius
| Topic | Side A | Side B |
|---|---|---|
| Centered layouts | H: a hero with everything centered auto-fails; at most two centered elements: `slop-test.md:35`, `layout-and-space.md:74` | U's `--variance` low setting deliberately produces "Centered / minimal": `U:121`. T allows centered when DESIGN_VARIANCE ≤4 or for editorial/manifesto briefs: `T:210-211` |
| Eyebrows / kickers | I: banned outright, "no brief earns it back": `I craft-floor.md:27`. H: off by default, 1–2 per page, only for ordinal content: `anti-patterns.md:149-151` | T: up to 1 per 3 sections, hero may have one: `T:240,253-257`. Ts **requires** pill eyebrows above H1 and H2: `Ts:52` |
| Section numbers (01/02) | H: allowed in Long Document, Manifesto or Catalogue when the content is ordinal: `H:450`. I: allowed when the sequence carries information: `I craft-floor.md:28` | T: banned outright: `T:639` |
| Nested cards | H bans card-in-card: `layout-and-space.md:76`. I: "nested cards are always wrong": `I craft-floor.md:25` | Ts **requires** the "Double-Bezel" nested shell plus core for all major cards: `Ts:41-44,90` |
| Border radius | T: one radius system per page: `T:217`. H: per-theme `--radius-card/pill/input` tokens: `export-formats.md:40` | Ts: `rounded-[2rem]` and pill primary buttons required: `Ts:43,47,82`. Tm: no pill primary buttons, cards ≤12px, buttons 4–6px: `Tm:19,46,50`. Tb: radius 0: `Tb:71` |
| Spacing scale | H: 2/4/8/12/16/24/40/64/96/144: `layout-and-space.md:15-29` | U: tiers 16/24/32/48: `Up:58`, density presets 24–96, 16–64, 8–32: `U:123`. T: Tailwind `py-16`…`py-48` by density: `T:566-567`. Ts: `py-24`–`py-40`, "double your padding": `Ts:51` |
| Breakpoints | H: content-driven, in `rem`; fixed px breakpoints are banned: `responsive.md:22,35,137`. Verify at 320/375/414/768: `H:54` | T: Tailwind 640/768/1024/1280/1536: `T:151`. U: 375/768/1024/1440: `Uq:97`. I captures 1440 and 390: `I new-work.md:118` |
| Z-index scale | H: 1/10/100/200/400/500/600: `layout-and-space.md:60-69` | U: 0/10/20/40/100/1000: `Uq:104` |
| Shadows | H: depth comes from weight, not shadow; only "whisper" or a zero-offset hairline: `layout-and-space.md:53-57` | I: shadows need an offset and blur, and a zero-offset colored halo is decoration: `I craft-floor.md:10`. Ts: heavy diffuse shadows: `Ts:27` |
| Faux browser/OS chrome | H forbids it: `H:52`, gate 47. T bans div-based fake screenshots: `T:290,655` | Tm prescribes a faux-OS window with three gray dots: `Tm:60-61` |
| Hero text | H: headline ≤7 words and ≤50 characters; lede about 2 lines, ≤60ch: `H:449`, `slop-test.md:136` | T: subtext ≤20 words and 3–4 lines; `text-7xl` only for 3–5 words: `T:236-237` |
| Navigation | H bans the standard sticky full-width nav and rotates archetypes: `anti-patterns.md:77`, `H:294` | U: every nav item needs icon plus label, and nav placement stays the same across pages: `Uq:204,217`. Ts bans an edge-to-edge sticky nav: `Ts:18` |
| Imagery | H: the default is typography-only, with CSS art and hand-built SVG preferred over generated images: `H:395-401` | T: use an image-generation tool first, a text-only page is "incomplete", hand-rolled decorative SVG strongly discouraged: `T:267-274,285`. I: anything drawn beyond icon size must be a generated plate: `I new-work.md:110`, and IJ `shape-assembled-illustration` |
| Invented content | H: no fabricated metrics or logos: `H:48`. I: claims can't be invented: `I new-work.md:59` | T says to invent an SVG mark for invented brands: `T:279`, and to "use organic, messy data (47.2%)": `T:618`. That contradicts T's own ban on fake-precise numbers at `T:327-330` |

### Motion
| Topic | Side A | Side B |
|---|---|---|
| Animated properties | H, T and U: transform and opacity only: `motion.md:9`, `T:522`, `Uq:137` | I: "Reach past transform and opacity: blur, backdrop-filter, clip-path, mask, shadow": `I craft-floor.md:13`, `I animate.md:38-43` |
| Durations | H: 120/220/420ms, all within 100–500ms: `motion.md:10,31-36` | I allows a 500–800ms focal entrance: `I animate.md:59`. T reveals at 600ms: `T:494`. Tm uses 600ms: `Tm:71`. Ts uses 700ms and 800ms+: `Ts:55,69` |
| Easing | H: three named cubic-beziers, no overshoot on UI: `motion.md:15-27,103`. I: exponential ease-out: `I animate.md:61` | U prefers springs over cubic-bezier: `Uq:145`. T uses a spring (stiffness 100, damping 20) for perpetual motion: `T:358`. Ts bans `ease-in-out`, which H keeps as the `--ease-in-out` token: `Ts:19` vs `motion.md:23` |
| Scroll reveals | H: one orchestrated entrance, no further on-scroll animation: `microinteractions.md:196`. I: one authored moment, and content visible by default: `I craft-floor.md:13`, `I animate.md:71`, IJ `content-hidden-at-rest` | T: if MOTION >4, key sections must scroll-reveal: `T:359`. Tm: animate all major blocks: `Tm:83`. Ts: "elements never appear statically": `Ts:69,94` |
| Stagger step | U: 30–50ms: `Uq:147`. H: 60ms: `motion.md:61` | H also says 100ms: `microinteractions.md:32`. T: 100ms: `T:515`. Tm: 80ms: `Tm:73` |
| Reduced motion | H: collapse to an opacity crossfade of ≤150ms: `motion.md:13`. I: fewer and gentler, keep meaningful feedback: `I animate.md:77` | T: collapse to static or instant: `T:529` |
| Parallax | H bans it: `motion.md:106` | U allows it sparingly: `Uq:144`. T allows it at MOTION 8–10: `T:563` |
| Marquee | IJ `marquee` flags it as slop | T allows 1 per page: `T:361`. H ships marquee archetypes (40–60s infinite): `microinteractions.md:31` |
| Instant (0ms) changes | H: "0 ms is the right answer surprisingly often"; focus rings never animate: `microinteractions.md:65,218` | U lists "Instant state changes (0ms)" as an anti-pattern: `U:23`, and "state changes should animate smoothly": `Uq:142` |
| Scroll handlers | H and T: never use a scroll listener: `motion.md:72`, `T:511,563` | U and I allow debounced or throttled handlers: `Uq:73`, `I optimize.md:137` |

### UX and feedback
| Topic | Side A | Side B |
|---|---|---|
| Destructive actions | H: optimistic update plus Undo, no confirmation dialogs: `microinteractions.md:215`, `H:459` | U: "Confirm before destructive actions": `Uq:170` |
| Success feedback | H: silent success, no "Done!" toast: `microinteractions.md:10,214` | U: confirm with a checkmark, toast or color flash: `Uq:179` |
| Toast dwell | H: 4–6s: `microinteractions.md:128` | U: 3–5s: `Uq:169` |
| Loading indicator | T: skeletons, not generic spinners: `T:221` | U: a spinner in the button during async work: `Uq:40` |
| Web touch target | H: 44 CSS px: `interaction-and-states.md:42`. I: 44pt: `I critique.md:762` | U: 24×24 CSS px for web (WCAG 2.2), 44pt/48dp for native: `Uq:28,37` |
| Press scale | H and T: 0.98: `microinteractions.md:106`, `T:224` | U: 0.95–1.05: `Uq:152` |

### Process
| Topic | Side A | Side B |
|---|---|---|
| Clarifying questions | H: always ask 3 questions, no exceptions: `H:211-228` | T: don't ask when you can infer, and ask exactly one question only when ambiguous: `T:33-36`. I: ask 2–3 through the structured question tool: `I new-work.md:20` |
| Verification loop | H: fix until every gate passes: `H:474`. T: "not done" until every box is ticked: `T:979`. The spec's step 5 says "corrige e verifica de novo" | I: bounded, at most 2 inspection rounds: `I SKILL.md:15`, `I new-work.md:138` |
| Metadata in code | H stamps CSS comments (macrostructure and critique scores) into the output: `H:46,461` | I: never put direction or contract info in source, including CSS or HTML comments: `I new-work.md:77` |
| User overriding bans | I: "The brief wins": `I SKILL.md:27`. H: "If the user insists, do it": `typography.md:44` | H: the eyebrow ban can't be bypassed by parity instructions: `anti-patterns.md:155`. I contradicts itself on eyebrows: `craft-floor.md:27` |
| Design system choice | Spec step 4: shadcn for every React project | T: use the official system when the brief implies one (Fluent, Carbon, GOV.UK…), and never mix shadcn with Material: `T:86-104`. T also says never ship shadcn in its default state: `T:627` |

### Contradictions inside a single source
The "tie goes to hallmark" rule doesn't settle these, so each needs its own decision:
- **Hallmark:**
  - OKLCH-only (`color.md:7`) vs a hex accent in its own example (`color.md:31,46`).
  - Chrome is forbidden (`H:52`) vs the H8 component, which draws traffic-light dots (`components/h8-mockup-split-browser-framed.md:13-22`).
  - Italic headers are banned (`H:56`) vs "use weight or italic" (`anti-patterns.md:39`).
  - Infinite loops are banned (`motion.md:109`) vs the infinite marquee (`microinteractions.md:31`).
  - Transform-only (`motion.md:9`) vs a tab underline "width transition" (`microinteractions.md:144`).
  - Two stops only (`color.md:83`) vs 2–3 stops (`assets.md:319`, `custom-craft.md:79`).
  - System-ui is banned (`typography.md:40`) vs the Austere tone using system-ui (`typography.md:129`).
- **Taste:**
  - The split-header ban (`T:258`) vs "a clean 2-column header" (`T:674`).
  - Fake numbers are banned (`T:327`) vs "47.2%" as an example to follow (`T:618`).
  - Tm says "no gradients" (`Tm:18`) vs radial light spots and a drifting blob (`Tm:67,74`).

---

## 2. Where the skills depend on their own names or tools

**Hallmark**
- The 21 themes' token values live in `../../site/css/tokens.css` (`H:282`). **That file isn't in the installed skill**; only 5 theme files exist (`references/themes/`: carnival, cobalt, grid, hum, lumen).
- It expects "The Future" font "(in repo)" (`typography.md:90`) and `../../docs/recipes.md` (`H:390`).
- It writes state files: `.hallmark/log.json`, `.hallmark/preflight.json`, CSS stamps and `tokens.css` (`H:177,462,464`).
- Study mode uses WebFetch (`H:508`). Image generation names Nanobanana and Recraft (`H:401`, `assets.md:142`).
- It reads `design.md` **or** `DESIGN.md` (`H:153`).
- It doesn't mention inspo anywhere.

**Impeccable**
- Almost everything goes through `scripts/impeccable`: context, detect, concept-seed, serve-question, surface-brief, build-phase, comp-spec, font-match, comp-diff, embed-prompt, generate-image, live, hooks, doctor, pin (`I SKILL.md:19,81-85`, `new-work.md:39-154`).
- **The launcher downloads a platform binary on first run** (`scripts/impeccable` header). There is no `bin/` in the vendor copy, and the detector is Rust (`crates/`). So "detector em `ferramentas/`" is not stdlib: you'd have to vendor per-OS binaries or build it.
- It expects PRODUCT.md, DESIGN.md and `.impeccable/` (config, mocks, review, live).
- It spawns shipped subagents (`.claude/agents/impeccable-{finish-reviewer,documenter,asset-producer,manual-edit-applier}.md`) and needs an image-generation tool.
- References hand off to each other by command name ("hand off to `/impeccable polish`": `animate.md:89`, `typeset.md:70`, `layout.md:74`).

**ui-ux-pro-max**
- Search runs at `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py` (`U:42`). That assumes the plugin-root environment variable, so the path must be rewritten.
- It reads CSVs under `data/`.
- `--persist` writes `design-system/<slug>/MASTER.md` (`U:97`).

**Taste**
- The block library `skills/taste-skill/blocks/` is empty ("implementations land iteratively": `T:835-841`).
- It relies on picsum.photos, the Simple Icons CDN and devicon (`T:269,277`), Lighthouse (`T:541`), and an image-generation tool (`T:267`).

**Name collision:** H's `design.md`, I's `DESIGN.md` and taste's stitch-skill `DESIGN.md` are three different schemas under names that collide on case-insensitive APFS. vesta-interface should own one file.

---

## 3. How each skill runs its workflow, and what the spec's 5 steps drop

**How each one is structured:**
- **Hallmark:**
  0. Pre-flight scan of the existing project
  1. Context gate (3 questions, genre, theme route)
  2. Macrostructure, nav and footer pick with diversification; 2.5 log memory; 2.6 theme dispatch
  3. Load rules
  4. Enrichment
  5. Preview block
  6. Build (stamp, log, `tokens.css`)
  7. 58-gate slop test

  Plus the verbs audit, redesign and study, and a component-scope flow.
- **Taste:**
  0. Brief inference and a one-line "Design Read"
  1. Three dials
  2. Map the brief to a design system
  3. Stack defaults

  Sections 4–10 hold the rules, 11 is the redesign protocol, and 14 is a pre-flight checklist of about 60 items.
- **Impeccable:** Setup (`context`) → route by mode and command → new-work:
  1. Decide what's already true
  2. Ask 2–3 questions
  3. Level of invention (concept-seed dice and a decision page)
  4. Commit the world
  5. Direction contract
  6. Build (comp-led gates or code-led)
  7. Inspect in at most 2 rounds, detector, fresh finish-reviewer subagent, documenter writes DESIGN.md
- **ui-ux-pro-max:**
  1. Analyze product, audience, style and stack
  2. `--design-system` (with `--persist` and the three dials)
  3. Domain searches
  4. `--stack` guidelines

  Then the pre-delivery checklist.

**Capabilities the spec's flow drops or doesn't mention:**
1. **Pre-flight scan of an existing project** (fonts, palette, motion libs, spacing, framework, with file:line): `H:147-201`, `I SKILL.md:20`, `I new-work.md` §1. Step 1 only covers the request.
2. **Structure pick and diversification.** Macrostructure, nav and footer archetypes and the log rotation (`H:264-331`) are hallmark's main differentiator. Step 3 lists only color, type, spacing and motion.
3. **Study from a URL or screenshot** into a DNA diagnosis and optional `design.md` (`H:28,490-552`, `study.md`). Step 2 only uses inspo, so a reference the user supplies has no path.
4. **Image-first work.** Taste's image-to-code skill (generate section images, analyze them, then code) and imagegen-frontend-web/mobile and brandkit (`taste-skill/skills/*`). Also impeccable's comp-led build with comp-spec, font-match and comp-diff gates (`I new-work.md:99-118`). No image-generation step anywhere in the spec.
5. **Live browser mode.** Impeccable `live` and `generate`: pick elements, hot-swap variants over HMR (`I SKILL.md:68-69`, `live.md`).
6. **Heuristic UX critique.** Nielsen's 10 heuristics scored, cognitive load, personas, run as two isolated assessments (`I critique.md:43-58`). Step 5 checks accessibility and states only.
7. **Directional refine modes** (bolder, quieter, distill, delight, overdrive, clarify, harden with i18n/RTL/emoji input, onboard, optimize). "Steps 3+5 only" doesn't express them.
8. **Persistent design system.** Impeccable init/document/extract (PRODUCT.md, DESIGN.md), U `--persist` MASTER.md with per-page overrides, H `design.md` plus exports to Tailwind v4 `@theme`, DTCG and shadcn CSS variables (`H:464-466`, `export-formats.md`). The shadcn export is directly useful for step 4.
9. **Component-scope flow with an 8-state preview file** (`H:60-141`).
10. **Preview block before code** (`H:405-441`) and the pre-emit 6-axis self-critique (`H:46`). The Vesta mockup may cover part of this.
11. **Modes Persuade / Operate / Read / Experience** (`I SKILL.md:31-40`). Several contradictions above resolve by mode (fonts, color dosage, motion).
12. **Design dials:** T's `T:47-79` and U's `U:111-127` are the same concept with different semantics.
13. **Redesign protocols** with IA, SEO and analytics preservation and delete-safety rails (`T:783-831`, `H:27,32-36`).
14. **Fresh-context finish reviewer and the detector hook after every edit** (`I new-work.md:144`, `hooks.md`).
15. **Native and mobile guidance:** `I ios.md`, `android.md`, `*.native.md`, plus U's 22 stacks and pro-rules.
16. **Charts domain** (U, 25 chart types) and U's stack guidelines, including `--stack shadcn`.
17. **The 58-gate slop test.** Most gates are judgment calls the impeccable detector doesn't encode (for example gates 6, 42, 44, 54). Spec step 5 relies on the detector alone.

---

## 4. Overlap: rules in 3 or more sources (candidates to state once)

Counts are H / T / I / U.
- **Slop:**
  - No gradient text (H, T, I)
  - No purple/blue AI gradients (H, T, IJ)
  - No emoji as icons (all 4)
  - One icon family with consistent stroke (all 4)
  - No 3 equal icon+heading+text cards (H, T, I)
  - No nested cards (H, I, T/image-to-code)
  - Eyebrows restricted (H, T, I; the strength differs)
  - Section numbers restricted (H, T, I)
  - No invented metrics or claims (H, I, T `4.9`)
  - Glass/blur only with purpose (all 4)
  - Buzzword ban (T, Tm, IJ)
- **Typography:**
  - Body ≥16px, leading about 1.5, measure 45–75ch (all 4)
  - No skipped heading levels (H, U, IJ)
  - Tabular figures for data (all 4)
  - `font-display: swap` and fallback metrics (all 4)
  - Avoid overused faces by default (H, T, I; the lists conflict)
- **Color:**
  - Contrast 4.5 / 3:1 (all 4)
  - Focus ring ≥3:1 (all 4)
  - Color is never the only signal (H, I, U)
  - Semantic tokens, no raw values in components (all 4)
  - No gray text on a colored surface (H, I, U)
  - Dark mode is not a mechanical inversion (H, I, U)
- **Layout:**
  - 4pt spacing base (H, I, U; T via Tailwind)
  - Named z-index scale (H, T, U)
  - No horizontal scroll, verify mobile (all 4)
  - Touch targets (H, I, U)
- **Motion:**
  - Transform/opacity only (H, T, U; I disagrees)
  - `prefers-reduced-motion` mandatory (all 4)
  - Motion must communicate something (all 4)
  - One orchestrated moment, 1–2 elements (H, I, U)
  - Exit about 60–75% of enter (H, I, U)
  - Ease-out `cubic-bezier(0.16,1,0.3,1)` (H, I, T, Tm)
- **UX:**
  - Full state set: hover, focus, active, disabled, loading, error, empty, success (all 4)
  - Visible label, error below the field, validate on blur (H, T, U)
  - Error = cause + fix (H, I, U)
  - One primary CTA / no duplicate intent (T, U, H)

That's roughly 40 rules in 3+ sources, about a third of the distinct rules. Most other rules are single-source: H's catalog and gates, T's hero/bento/copy tells, U's native, nav and chart rules, and I's process rules.
