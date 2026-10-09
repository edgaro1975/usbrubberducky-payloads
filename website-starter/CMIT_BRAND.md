# CMIT Solutions® Brand — Applied to This Starter

This starter is pre-themed to the official **CMIT Solutions Brand Guide (v2.1,
2025)**. Build CMIT landing pages on top of it and the colors, fonts, logo, and
messaging are already correct. This doc is the quick reference; keep assets on
brand with the checklist at the bottom.

## Colors (Tailwind tokens in `tailwind.config.js`)

| Token | Hex | Role |
|-------|-----|------|
| `navy` / `bg` | `#002F44` | Primary brand blue · default dark background |
| `navy-deep` / `surface` | `#001B28` | Deep background variation · cards |
| `red` / `accent` | `#EF3F37` | Logo accent · primary highlight · CTAs |
| `bright-blue` / `accent2` | `#3291DB` | Emphasis, CTAs, backgrounds |
| `royal-purple` | `#7035FF` | High-impact headers / highlights |
| `orange` | `#EF9637` | Accent highlight |
| `teal` | `#25B17E` | Green/teal — specific purposes only |
| `light-blue` / `muted` | `#B0D3E4` | Backgrounds · muted text on navy |
| `cmit-gray` | `#D0DADF` | Interactive / hover states |

**Color rules (enforced by the brand guide):**
- **Blue must be present before any secondary color is used.** Navy is the base
  everywhere here, so you're covered.
- Red should **not** be paired with only green and yellow.
- Yellow and green only appear **after** red is already in the asset.
- Stay inside the palette (illustration-internal complementary colors aside).

## Gradients — **linear only** (radial is not approved)

Use the preset Tailwind backgrounds: `bg-cmit-blue-purple`, `bg-cmit-navy-blue`,
`bg-cmit-red-blue`, `bg-cmit-navy-green`. Approved pairs: Red→Yellow, Blue→Green,
Blue→Purple, Purple→Green, Dark Blue→Green, Dark Blue→Blue, Red→Blue. Gradients
should subtly highlight sections — never overpower text, logos, or icons.

## Typography — Avenir (Arial fallback)

Font stack is set to `Avenir Next, Avenir, Arial, system-ui`. Hierarchy:
- **Pre-header:** ALL CAPS, loose letter spacing (`uppercase tracking-[0.25em]`),
  ≥25% of header size. Light/Medium weight.
- **Header:** sentence case. Use **Black weight only for 1–3 word headers**;
  headers of **3+ words use sentence case, not bold** (`font-semibold` here).
- **Subheader:** Title Case, ~25% larger than paragraph.
- **Paragraph:** sentence case, ≥10pt, short lines. Space paragraphs ≥1.5× line height.

## Logo

- Files: `src/assets/cmit-logo.png` (light backgrounds) and
  `src/assets/cmit-logo-white.png` (dark backgrounds). This starter is dark
  navy, so the **white** logo is used in the nav and footer.
- Always write **CMIT Solutions®** with the ® symbol.
- Tagline: **"Your Technology Team."**
- Never distort, recolor, crowd, or shrink the logo below its minimum size.
  Keep clear space around it.

## Voice & messaging

**Tone:** professional, confident, trustworthy, innovative, inclusive — wit when
appropriate, always professional.

**Positioning:** "CMIT Solutions delivers locally-owned, nationally-supported
enterprise-class IT solutions to proactively protect your growing business and
outpace the competition."

**Three value propositions** (used on the Home page):
1. **Enterprise-class IT for everyone**
2. **Local owners, national strength**
3. **Strategic advisors**

**Promise:** "Safeguard your assets, work smarter, and serve more customers with
CMIT's enterprise-class IT solutions and services."

**Values — CRISP:** Community & Collaboration · Respect & Selflessness ·
Integrity & Honesty · Service Excellence · Passion & Enthusiasm.

## Imagery

Bold, dramatic, professional, cool-toned. Diverse, inclusive representation.
Prefer real franchisee photos over stock. Always license properly — Google
Image search "for commercial use" is prohibited.

## Where the brand is wired in

| Element | File |
|---------|------|
| Palette + fonts + gradients | `tailwind.config.js` |
| Logo (nav) | `src/components/Nav.jsx` |
| Logo + CRISP + footer | `src/components/Footer.jsx`, `src/pages/About.jsx` |
| Value props + positioning | `src/pages/Home.jsx`, `src/components/ParallaxHero.jsx` |
| Services | `src/components/PinnedGallery.jsx` |

## On-brand checklist (run before shipping)

1. **Colors** — all from the palette? Blue present before secondaries? Ratio rules kept?
2. **Typography** — Avenir/Arial? Hierarchy sizes right? Headers in correct case?
3. **Logo** — correct variant for the background? Clear space? ® present?
4. **Messaging** — aligns with the 3 value props? Professional yet approachable?
5. **Imagery** — dramatic, cool-toned, diverse, licensed?
6. **Gradients** — linear, from the approved list, not overpowering?
7. **Layout** — balanced, medium white space, clean and modern?
