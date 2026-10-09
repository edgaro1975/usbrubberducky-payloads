import { NavLink } from 'react-router-dom'

const linkClass = ({ isActive }) =>
  `transition-colors hover:text-fg ${isActive ? 'text-fg' : 'text-muted'}`

export default function Nav() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 backdrop-blur-md bg-bg/60 border-b border-white/5">
      <nav className="mx-auto flex max-w-content items-center justify-between px-6 py-4">
        <NavLink to="/" className="text-lg font-bold tracking-tight">
          ◆ Studio
        </NavLink>
        <div className="flex items-center gap-6 text-sm">
          <NavLink to="/" className={linkClass} end>
            Home
          </NavLink>
          <NavLink to="/about" className={linkClass}>
            About
          </NavLink>
          <a
            href="#"
            className="rounded-full bg-fg px-4 py-1.5 font-medium text-bg transition-transform hover:scale-105"
          >
            Get started
          </a>
        </div>
      </nav>
    </header>
  )
}
