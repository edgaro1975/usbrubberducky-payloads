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
      {/* Parallax background layers — CMIT palette (blue present + red accent) */}
      <div
        data-speed="slow"
        className="pointer-events-none absolute -left-20 top-10 h-72 w-72 rounded-full bg-bright-blue/25 blur-3xl"
      />
      <div
        data-speed="mid"
        className="pointer-events-none absolute right-0 top-40 h-96 w-96 rounded-full bg-royal-purple/20 blur-3xl"
      />
      <div
        data-speed="fast"
        className="pointer-events-none absolute bottom-0 left-1/3 h-64 w-64 rounded-full bg-red/20 blur-3xl"
      />

      {/* Foreground content */}
      <div data-hero-content className="relative z-10 max-w-content px-6 text-center">
        {/* Pre-header: ALL CAPS, loose letter spacing (brand typography rule) */}
        <p className="mb-5 text-sm uppercase tracking-[0.25em] text-light-blue">
          Your Technology Team
        </p>
        {/* 3+ word header → sentence case, not black weight (brand rule) */}
        <SplitText
          text="Enterprise-class IT for everyone"
          className="text-5xl font-semibold leading-[1.08] tracking-tight sm:text-7xl"
        />
        <p className="mx-auto mt-6 max-w-2xl text-lg text-light-blue">
          Locally-owned, nationally-supported IT and cybersecurity that
          proactively protects your growing business and helps you outpace the
          competition.
        </p>
        <div className="mt-8 flex items-center justify-center gap-4">
          <a className="rounded-full bg-red px-6 py-3 font-medium text-white transition-transform hover:scale-105" href="#work">
            Get a consultation
          </a>
          <a className="rounded-full border border-white/20 px-6 py-3 font-medium transition-colors hover:bg-white/5" href="#work">
            Explore services
          </a>
        </div>
      </div>

      <span className="absolute bottom-8 text-xs uppercase tracking-[0.2em] text-muted">
        Scroll ↓
      </span>
    </section>
  )
}
