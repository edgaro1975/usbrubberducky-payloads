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
        <p className="text-center text-sm uppercase tracking-[0.25em] text-light-blue">
          Why CMIT Solutions
        </p>
        <SplitText
          as="h2"
          text="Enterprise strength, delivered locally"
          className="mt-3 text-center text-4xl font-semibold tracking-tight sm:text-5xl"
        />
        {/* CMIT's three value propositions */}
        <div className="mt-14 grid gap-6 sm:grid-cols-3">
          {[
            [
              'Enterprise-class IT for everyone',
              'Enterprise-grade IT and cybersecurity at a price that meets your business where it is.',
            ],
            [
              'Local owners, national strength',
              'Local support backed by a powerful national network of the brightest minds in IT.',
            ],
            [
              'Strategic advisors',
              'A local CMIT professional who understands your needs and guides you toward growth.',
            ],
          ].map(([title, body]) => (
            <div
              key={title}
              className="feature-card rounded-2xl border border-white/10 bg-surface p-7"
            >
              {/* Thin red top-accent keeps the brand highlight present on cards */}
              <div className="mb-5 h-1 w-10 rounded-full bg-red" />
              <h3 className="text-xl font-semibold">{title}</h3>
              <p className="mt-2 text-light-blue">{body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-content px-6 pb-40 text-center">
        <SplitText
          as="h2"
          text="Let's build your technology roadmap"
          className="text-4xl font-semibold tracking-tight sm:text-5xl"
        />
        <p className="mx-auto mt-5 max-w-xl text-light-blue">
          Safeguard your assets, work smarter, and serve more customers with
          CMIT's enterprise-class IT solutions and services.
        </p>
        <a
          href="#"
          className="mt-8 inline-block rounded-full bg-red px-7 py-3 font-medium text-white transition-transform hover:scale-105"
        >
          Get a consultation
        </a>
      </section>
    </>
  )
}
