import { NavLink } from 'react-router-dom'
import cmitLogoWhite from '../assets/cmit-logo-white.png'

const linkClass = ({ isActive }) =>
  `transition-colors hover:text-fg ${isActive ? 'text-fg' : 'text-muted'}`

export default function Nav() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/10 bg-navy/70 backdrop-blur-md">
      <nav className="mx-auto flex max-w-content items-center justify-between px-6 py-4">
        {/* White logo variant for dark navy backgrounds (CMIT brand rule) */}
        <NavLink to="/" aria-label="CMIT Solutions home" className="flex items-center">
          <img src={cmitLogoWhite} alt="CMIT Solutions®" className="h-9 w-auto" />
        </NavLink>
        <div className="flex items-center gap-6 text-sm">
          <NavLink to="/" className={linkClass} end>
            Home
          </NavLink>
          <NavLink to="/about" className={linkClass}>
            About
          </NavLink>
          {/* Red is the CMIT primary highlight for CTAs */}
          <a
            href="#"
            className="rounded-full bg-red px-5 py-2 font-medium text-white transition-transform hover:scale-105"
          >
            Get a consultation
          </a>
        </div>
      </nav>
    </header>
  )
}
