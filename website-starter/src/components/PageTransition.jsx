import { useEffect, useRef } from 'react'
import { useLocation } from 'react-router-dom'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

/**
 * A route-change "wipe" transition. On every navigation it slides a full-screen
 * panel up to cover the page, then slides it away to reveal the new page.
 *
 * This approach is robust because it doesn't depend on keeping the outgoing
 * page mounted — the overlay plays independently, so transitions never break
 * even on fast navigation. It also resets scroll and refreshes ScrollTrigger
 * so scroll animations measure the new page correctly.
 */
export default function PageTransition() {
  const overlay = useRef(null)
  const location = useLocation()
  const first = useRef(true)

  useEffect(() => {
    // Skip the wipe on first load so the landing page isn't hidden on arrival.
    if (first.current) {
      first.current = false
      return
    }

    const el = overlay.current
    const tl = gsap.timeline()

    tl.set(el, { display: 'block', transformOrigin: 'bottom', scaleY: 0 })
      .to(el, { scaleY: 1, duration: 0.45, ease: 'power3.inOut' })
      .add(() => {
        window.scrollTo(0, 0)
        ScrollTrigger.refresh()
      })
      .set(el, { transformOrigin: 'top' })
      .to(el, { scaleY: 0, duration: 0.45, ease: 'power3.inOut' })
      .set(el, { display: 'none' })

    return () => tl.kill()
  }, [location.pathname])

  return (
    <div
      ref={overlay}
      aria-hidden="true"
      className="fixed inset-0 z-[9999] hidden bg-gradient-to-br from-accent to-accent2"
    />
  )
}
