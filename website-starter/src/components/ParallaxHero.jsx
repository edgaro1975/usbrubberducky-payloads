import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SplitText from './SplitText'

gsap.registerPlugin(ScrollTrigger)

/**
 * A layered parallax hero. Each decorative layer moves at a different speed as
 * you scroll (driven by Lenis via ScrollTrigger), creating depth. The headline
 * and content sit on top and drift up slightly.
 */
export default function ParallaxHero() {
  const root = useRef(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Different `yPercent` values = different parallax speeds = depth.
      gsap.to('[data-speed="slow"]', {
        yPercent: 18,
        ease: 'none',
        scrollTrigger: { trigger: root.current, start: 'top top', end: 'bottom top', scrub: true },
      })
      gsap.to('[data-speed="mid"]', {
        yPercent: 40,
        ease: 'none',
        scrollTrigger: { trigger: root.current, start: 'top top', end: 'bottom top', scrub: true },
      })
      gsap.to('[data-speed="fast"]', {
        yPercent: 70,
        ease: 'none',
        scrollTrigger: { trigger: root.current, start: 'top top', end: 'bottom top', scrub: true },
      })
      // Fade the whole hero content out as it leaves.
      gsap.to('[data-hero-content]', {
        opacity: 0,
        yPercent: -20,
        ease: 'none',
        scrollTrigger: { trigger: root.current, start: 'center top', end: 'bottom top', scrub: true },
      })
    }, root)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={root}
      className="relative flex h-screen items-center justify-center overflow-hidden"
    >
      {/* Parallax background layers */}
      <div
        data-speed="slow"
        className="pointer-events-none absolute -left-20 top-10 h-72 w-72 rounded-full bg-accent/30 blur-3xl"
      />
      <div
        data-speed="mid"
        className="pointer-events-none absolute right-0 top-40 h-96 w-96 rounded-full bg-accent2/30 blur-3xl"
      />
      <div
        data-speed="fast"
        className="pointer-events-none absolute bottom-0 left-1/3 h-64 w-64 rounded-full bg-indigo-400/20 blur-3xl"
      />

      {/* Foreground content */}
      <div data-hero-content className="relative z-10 max-w-content px-6 text-center">
        <p className="mb-5 inline-block rounded-full border border-white/10 px-4 py-1 text-sm text-muted">
          GSAP · Lenis · ReactBits · Tailwind
        </p>
        <SplitText
          text="Design-grade websites, fast"
          className="text-5xl font-extrabold leading-[1.05] tracking-tight sm:text-7xl"
        />
        <p className="mx-auto mt-6 max-w-xl text-lg text-muted">
          A pre-wired foundation for building animated landing pages — smooth
          scroll, scroll-synced motion, routing, and page transitions included.
        </p>
        <div className="mt-8 flex items-center justify-center gap-4">
          <a className="rounded-full bg-fg px-6 py-3 font-medium text-bg transition-transform hover:scale-105" href="#work">
            See it in action
          </a>
          <a className="rounded-full border border-white/15 px-6 py-3 font-medium transition-colors hover:bg-white/5" href="#">
            Docs
          </a>
        </div>
      </div>

      <span className="absolute bottom-8 text-xs uppercase tracking-[0.2em] text-muted">
        Scroll ↓
      </span>
    </section>
  )
}
