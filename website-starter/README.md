# Website Starter — GSAP · Lenis · ReactBits

A ready-to-use base for building modern, animated websites. Everything is
pre-wired so you can start on the actual site instead of plumbing.

| Tool | What it gives you | Docs |
|------|-------------------|------|
| **GSAP** + ScrollTrigger | The animation engine — timelines, tweens, scroll-triggered motion | https://gsap.com |
| **Lenis** | Smooth, inertial scrolling | https://lenis.dev |
| **ReactBits** | Copy-paste animated React components | https://reactbits.dev |
| **Vite** + **React** | Fast dev server and build | https://vitejs.dev |

## Getting started

```bash
cd website-starter
npm install      # already run once; re-run after cloning fresh
npm run dev      # start the dev server (usually http://localhost:5173)
npm run build    # production build into dist/
npm run preview  # preview the production build locally
```

## How the pieces fit together

- **`src/hooks/useSmoothScroll.js`** — starts Lenis and syncs it with GSAP's
  ScrollTrigger so the two share one clock. Call `useSmoothScroll()` once near
  the root of your app (already done in `src/App.jsx`). This is the part people
  usually get wrong — it's done for you here.
- **`src/App.jsx`** — the demo page. Shows a scroll-scrubbed GSAP animation and
  the text-reveal component. Replace its contents with your own sections.
- **`src/components/SplitText.jsx`** — an example animated component in the
  ReactBits style: small, self-contained, and yours to edit.

## Adding ReactBits components

ReactBits isn't a package you import from — you bring each component into your
own code. Two ways:

1. **Copy-paste (always works):** open a component on https://reactbits.dev,
   copy its code into `src/components/`, and import it.
2. **CLI:** `npm run add:component` (runs `jsrepo add`) and follow the prompts,
   or use the exact command shown on the component's page on reactbits.dev.

Either way the component is plain React + GSAP, so it works with the smooth
scroll already set up here.

## Turning this into its own GitHub repo

This folder is self-contained. To lift it out into a standalone repo:

```bash
cp -r website-starter ../my-website && cd ../my-website
git init && git add -A && git commit -m "Initial website starter"
# then create a repo on GitHub and push
```
