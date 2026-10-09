import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const CARDS = [
  { title: 'Hero', body: 'Layered parallax with scroll-synced depth.', tag: '01' },
  { title: 'Pin', body: 'This section is pinned while the track scrolls sideways.', tag: '02' },
  { title: 'Reveal', body: 'Text and images animate in as they enter the viewport.', tag: '03' },
  { title: 'Transition', body: 'A wipe overlay plays between routes.', tag: '04' },
]

/**
 * A pinned, horizontally-scrolling section — one of the most recognisable
 * scroll patterns on modern landing pages. The section pins to the viewport
 * and the inner track moves left as the user scrolls down.
 */
export default function PinnedGallery() {
  const root = useRef(null)
  const track = useRef(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      const panels = gsap.utils.toArray('.panel-card', track.current)
      // Distance the track must travel = its overflow width.
      const getScrollAmount = () => track.current.scrollWidth - window.innerWidth

      const scrollTween = gsap.to(track.current, {
        x: () => -getScrollAmount(),
        ease: 'none',
        scrollTrigger: {
          trigger: root.current,
          start: 'top top',
          end: () => `+=${getScrollAmount()}`,
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
          anticipatePin: 1,
        },
      })

      // Subtle entrance for each card, tied to the horizontal track movement.
      panels.forEach((p) => {
        const inner = p.querySelector('.panel-inner')
        if (!inner) return
        gsap.from(inner, {
          opacity: 0.3,
          scale: 0.92,
          scrollTrigger: {
            trigger: p,
            containerAnimation: scrollTween,
            start: 'left center',
            end: 'center center',
            scrub: true,
          },
        })
      })
    }, root)
    return () => ctx.revert()
  }, [])

  return (
    <section id="work" ref={root} className="relative h-screen overflow-hidden">
      <div ref={track} className="flex h-full w-max items-center gap-8 px-[10vw]">
        <div className="panel-card flex h-full shrink-0 items-center">
          <h2 className="max-w-sm text-4xl font-bold leading-tight sm:text-5xl">
            Pinned horizontal scroll
            <span className="mt-3 block text-lg font-normal text-muted">
              Scroll down — the section pins and these panels move sideways.
            </span>
          </h2>
        </div>
        {CARDS.map((c) => (
          <div key={c.tag} className="panel-card flex h-full shrink-0 items-center">
            <div className="panel-inner flex h-[60vh] w-[70vw] max-w-md flex-col justify-between rounded-3xl border border-white/10 bg-surface p-8 sm:w-[32vw]">
              <span className="text-sm text-muted">{c.tag}</span>
              <div>
                <h3 className="text-3xl font-semibold">{c.title}</h3>
                <p className="mt-2 text-muted">{c.body}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
