import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import SplitText from '../components/SplitText'

export default function About() {
  const ref = useRef(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from('.about-line', {
        y: 30,
        opacity: 0,
        duration: 0.6,
        ease: 'power3.out',
        stagger: 0.1,
        delay: 0.2,
      })
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="mx-auto flex min-h-screen max-w-content flex-col justify-center px-6 py-32">
      <p className="about-line text-sm uppercase tracking-[0.25em] text-light-blue">
        About CMIT Solutions®
      </p>
      <SplitText as="h1" text="Local owners, national strength" className="mt-3 text-5xl font-semibold tracking-tight sm:text-6xl" />
      <div className="mt-8 max-w-2xl space-y-4 text-lg text-light-blue">
        <p className="about-line">
          CMIT Solutions delivers locally-owned, nationally-supported
          enterprise-class IT solutions to proactively protect your growing
          business and help you outpace the competition.
        </p>
        <p className="about-line">
          Your local CMIT professional understands your unique business needs
          and guides you toward the right technology for growth — backed by a
          national network of IT experts.
        </p>
      </div>
      {/* CRISP brand values */}
      <div className="about-line mt-10 grid max-w-3xl gap-4 sm:grid-cols-5">
        {[
          ['C', 'Community & Collaboration'],
          ['R', 'Respect & Selflessness'],
          ['I', 'Integrity & Honesty'],
          ['S', 'Service Excellence'],
          ['P', 'Passion & Enthusiasm'],
        ].map(([letter, label]) => (
          <div key={letter} className="rounded-xl border border-white/10 bg-surface p-4">
            <div className="text-2xl font-black text-red">{letter}</div>
            <div className="mt-1 text-sm text-light-blue">{label}</div>
          </div>
        ))}
      </div>
    </section>
  )
}
