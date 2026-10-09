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
      <SplitText as="h1" text="About this starter" className="text-5xl font-extrabold tracking-tight sm:text-6xl" />
      <div className="mt-8 max-w-2xl space-y-4 text-lg text-muted">
        <p className="about-line">
          This is a second route — notice the wipe transition when you navigated
          here, and that smooth scroll still works.
        </p>
        <p className="about-line">
          Each page runs its own entrance animation on mount. Build your real
          pages the same way: drop sections in, animate with GSAP, and let the
          shared layout handle scroll and transitions.
        </p>
        <p className="about-line">
          Swap in components from ReactBits whenever you want a ready-made
          animated element.
        </p>
      </div>
    </section>
  )
}
