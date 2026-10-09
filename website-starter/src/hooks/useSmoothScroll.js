import { useEffect } from 'react'
import Lenis from 'lenis'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

/**
 * Sets up Lenis smooth scrolling and wires it into GSAP's ScrollTrigger so the
 * two stay perfectly in sync. Call this once, near the root of your app.
 *
 * Why this matters: Lenis takes over the scroll position, and ScrollTrigger
 * needs to be told whenever that position changes. We also drive Lenis's
 * animation frame from GSAP's ticker so there is a single clock for everything.
 */
export function useSmoothScroll() {
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    })

    // Tell ScrollTrigger to recalculate on every Lenis scroll event.
    lenis.on('scroll', ScrollTrigger.update)

    // Drive Lenis from GSAP's ticker (one clock, no jitter).
    const raf = (time) => lenis.raf(time * 1000)
    gsap.ticker.add(raf)
    gsap.ticker.lagSmoothing(0)

    return () => {
      gsap.ticker.remove(raf)
      lenis.destroy()
    }
  }, [])
}
