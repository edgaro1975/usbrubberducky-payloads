import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { useSmoothScroll } from './hooks/useSmoothScroll'
import SplitText from './components/SplitText'

gsap.registerPlugin(ScrollTrigger)

export default function App() {
  // Turn on Lenis smooth scroll + GSAP sync for the whole app.
  useSmoothScroll()

  const boxRef = useRef(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      // A simple scroll-scrubbed animation to prove GSAP + Lenis are in sync.
      gsap.to(boxRef.current, {
        rotation: 360,
        scale: 1.4,
        ease: 'none',
        scrollTrigger: {
          trigger: boxRef.current,
          start: 'top 80%',
          end: 'bottom 20%',
          scrub: true,
        },
      })
    })
    return () => ctx.revert()
  }, [])

  return (
    <main>
      <section className="hero">
        <SplitText text="Build beautiful websites" />
        <p className="subtitle">
          GSAP animations · Lenis smooth scroll · ReactBits components — all wired up.
        </p>
        <span className="scroll-hint">Scroll ↓</span>
      </section>

      <section className="panel">
        <div ref={boxRef} className="box" />
        <SplitText as="h2" text="Scroll-synced GSAP animation" className="h2" />
        <p className="body">
          The square rotates as you scroll because ScrollTrigger reads its
          position from Lenis. Edit <code>src/App.jsx</code> to build your own.
        </p>
      </section>

      <section className="panel alt">
        <SplitText as="h2" text="Add components from ReactBits" className="h2" />
        <p className="body">
          Copy any component from reactbits.dev into <code>src/components</code>,
          or run <code>npm run add:component</code>. They are plain React + GSAP,
          so they drop straight in.
        </p>
      </section>
    </main>
  )
}
