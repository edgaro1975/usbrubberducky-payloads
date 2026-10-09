# Design Reference

Design cues for building landing pages with this starter.

> **Source:** The requested reference was the Kombai landing-pages gallery
> (https://kombai.com/gallery/web/landing-pages/). That site is blocked by this
> environment's network egress proxy, so it couldn't be fetched directly. Open
> it in your own browser for live visual examples. The patterns below distill
> the style that gallery curates — modern SaaS / startup / product landing
> pages — so you have a concrete reference to build against here.

## The anatomy of a modern landing page

Most high-end landing pages in this style follow the same vertical rhythm:

1. **Sticky nav** — slim, blurred/translucent, logo left, a few links + one
   high-contrast CTA button right. *(Implemented: `components/Nav.jsx`.)*
2. **Hero** — one bold claim, a one-line subhead, 1–2 CTAs, and an eyebrow tag.
   Often with motion/parallax or a product shot. *(Implemented: `ParallaxHero.jsx`.)*
3. **Logo cloud / social proof** — "trusted by" row of muted logos.
4. **Feature sections** — alternating text/visual blocks, often with a pinned or
   horizontally-scrolling showcase. *(Implemented: `PinnedGallery.jsx`.)*
5. **How it works / steps** — numbered, staggered reveal on scroll.
6. **Metrics / testimonials** — big numbers, quote cards.
7. **Pricing** — 3-tier cards, middle one highlighted.
8. **Final CTA** — large centered headline + button.
9. **Footer** — multi-column links, muted.

## Visual language

**Color.** Dark, near-black backgrounds (`#0b0b0f`) are dominant in this style,
with one or two saturated accent colors used sparingly (indigo → violet here)
for CTAs, gradients, and glow. Keep most of the page monochrome; let the accent
pop. Light-mode variants invert to off-white (`#f4f4f5`) with the same single
accent. The Tailwind theme in `tailwind.config.js` holds these tokens
(`bg`, `surface`, `fg`, `muted`, `accent`, `accent2`) — change them there to
rebrand the whole site at once.

**Typography.** Large, tight headlines (clamp from ~2.5rem up to ~7rem),
`font-extrabold`, negative letter-spacing (`tracking-tight`). Body copy stays
small, muted, and short (max ~48ch per line). One typeface is enough; vary
weight and size, not family.

**Space.** Generous. Big vertical padding between sections (`py-32`+), content
capped at ~72rem (`max-w-content`) and centered. Whitespace is the main tool
that makes a page feel premium.

**Depth.** Soft radial glows (blurred colored circles), subtle 1px white/low-
opacity borders (`border-white/10`), and gentle gradients. Avoid hard shadows;
prefer glow and layering.

**Shape.** Rounded everything — `rounded-2xl`/`rounded-3xl` cards, pill buttons
(`rounded-full`).

## Motion (what makes these pages feel alive)

- **Smooth scroll** sets the baseline feel — already on via Lenis.
- **Scroll-reveal:** content fades/slides up as it enters (85% threshold).
  See `SplitText.jsx` and the staggered feature cards in `pages/Home.jsx`.
- **Parallax:** background layers move slower than foreground for depth.
  See `ParallaxHero.jsx`.
- **Pinned / horizontal scroll:** a section locks while content moves sideways.
  See `PinnedGallery.jsx`.
- **Page transitions:** a quick wipe between routes. See `PageTransition.jsx`.
- **Micro-interactions:** buttons scale slightly on hover (`hover:scale-105`),
  links shift color. Keep these fast (150–250ms).

**Restraint is the rule.** Pick 2–3 signature motions per page. Animation should
guide attention, not compete for it. Respect `prefers-reduced-motion` for
accessibility when you ship real projects.

## Where to get ready-made pieces

- **ReactBits** (https://reactbits.dev) — animated headlines, backgrounds,
  cards. Copy into `src/components` or `npm run add:component`.
- **GSAP** (https://gsap.com) — the animation engine; ScrollTrigger for all
  scroll-driven motion.
- **Tailwind** (https://tailwindcss.com) — utility styling; tokens live in
  `tailwind.config.js`.
