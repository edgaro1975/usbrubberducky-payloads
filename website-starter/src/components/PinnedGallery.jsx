import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const CARDS = [
  { title: 'Managed IT services', body: 'Proactive monitoring, support, and management of your entire IT environment.', tag: '01' },
  { title: 'Cybersecurity', body: 'Multi-layered protection to keep your data, people, and business safe.', tag: '02' },
  { title: 'Cloud services', body: 'Secure cloud migration, hosting, and productivity tools that scale with you.', tag: '03' },
  { title: 'Data backup & recovery', body: 'Business continuity so you bounce back fast from any disruption.', tag: '04' },
  { title: 'Compliance', body: 'Meet industry and regulatory requirements with expert guidance.', tag: '05' },
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
          <h2 className="max-w-sm text-4xl font-semibold leading-tight sm:text-5xl">
            What we do for you
            <span className="mt-3 block text-lg font-normal text-light-blue">
              Keep scrolling — the section pins while our services move past.
            </span>
          </h2>
        </div>
        {CARDS.map((c) => (
          <div key={c.tag} className="panel-card flex h-full shrink-0 items-center">
            <div className="panel-inner flex h-[60vh] w-[70vw] max-w-md flex-col justify-between rounded-3xl border border-white/10 bg-surface p-8 sm:w-[32vw]">
              <span className="font-semibold text-red">{c.tag}</span>
              <div>
                <h3 className="text-3xl font-semibold">{c.title}</h3>
                <p className="mt-2 text-light-blue">{c.body}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
