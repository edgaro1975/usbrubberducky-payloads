import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import ParallaxHero from '../components/ParallaxHero'
import PinnedGallery from '../components/PinnedGallery'
import SplitText from '../components/SplitText'

gsap.registerPlugin(ScrollTrigger)

export default function Home() {
  const featuresRef = useRef(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from('.feature-card', {
        y: 40,
        opacity: 0,
        duration: 0.7,
        ease: 'power3.out',
        stagger: 0.12,
        scrollTrigger: { trigger: featuresRef.current, start: 'top 75%' },
      })
    }, featuresRef)
    return () => ctx.revert()
  }, [])

  return (
    <>
      <ParallaxHero />
      <PinnedGallery />

      <section ref={featuresRef} className="mx-auto max-w-content px-6 py-32">
        <SplitText
          as="h2"
          text="Everything wired up for you"
          className="text-center text-4xl font-bold tracking-tight sm:text-5xl"
        />
        <div className="mt-14 grid gap-6 sm:grid-cols-3">
          {[
            ['Smooth scroll', 'Lenis + GSAP share one clock — no jitter.'],
            ['Scroll motion', 'ScrollTrigger pins, parallax, and reveals.'],
            ['Routing + transitions', 'React Router with a GSAP wipe between pages.'],
          ].map(([title, body]) => (
            <div
              key={title}
              className="feature-card rounded-2xl border border-white/10 bg-surface p-7"
            >
              <h3 className="text-xl font-semibold">{title}</h3>
              <p className="mt-2 text-muted">{body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-content px-6 pb-40 text-center">
        <SplitText
          as="h2"
          text="Start building your landing page"
          className="text-4xl font-bold tracking-tight sm:text-5xl"
        />
        <p className="mx-auto mt-5 max-w-lg text-muted">
          Replace these sections with your own. See DESIGN_REFERENCE.md for
          layout and style patterns to follow.
        </p>
      </section>
    </>
  )
}
