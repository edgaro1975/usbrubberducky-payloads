import { Routes, Route } from 'react-router-dom'
import { useSmoothScroll } from './hooks/useSmoothScroll'
import Nav from './components/Nav'
import PageTransition from './components/PageTransition'
import Home from './pages/Home'
import About from './pages/About'

export default function App() {
  // Lenis smooth scroll + GSAP sync for the whole app, set up once.
  useSmoothScroll()

  return (
    <>
      <Nav />
      <PageTransition />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </>
  )
}
