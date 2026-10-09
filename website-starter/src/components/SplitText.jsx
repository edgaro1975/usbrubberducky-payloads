import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

/**
 * A ReactBits-style animated text component.
 *
 * This is the pattern ReactBits uses: a small, self-contained, copy-paste
 * component you own and can tweak. It splits text into words and reveals them
 * on scroll using GSAP. Swap or add components from https://reactbits.dev the
 * same way — either copy them into src/components or run `npm run add:component`.
 */
export default function SplitText({ text, className = '', as: Tag = 'h1' }) {
  const ref = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    const words = el.querySelectorAll('.split-word')

    const ctx = gsap.context(() => {
      gsap.from(words, {
        yPercent: 120,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out',
        stagger: 0.08,
        scrollTrigger: {
          trigger: el,
          start: 'top 85%',
        },
      })
    }, el)

    return () => ctx.revert()
  }, [text])

  return (
    <Tag ref={ref} className={className} aria-label={text}>
      {text.split(' ').map((word, i) => (
        <span key={i} className="split-word-wrap">
          <span className="split-word">{word}</span>
          {i < text.split(' ').length - 1 ? ' ' : ''}
        </span>
      ))}
    </Tag>
  )
}
