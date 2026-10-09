import cmitLogoWhite from '../assets/cmit-logo-white.png'

export default function Footer() {
  return (
    <footer className="border-t border-white/10 bg-navy-deep">
      <div className="mx-auto grid max-w-content gap-10 px-6 py-16 sm:grid-cols-[1.5fr_1fr_1fr]">
        <div>
          <img src={cmitLogoWhite} alt="CMIT Solutions®" className="h-10 w-auto" />
          <p className="mt-4 max-w-xs text-sm text-light-blue">
            Your Technology Team — enterprise-class IT and cybersecurity,
            delivered locally.
          </p>
        </div>
        <div>
          <h4 className="text-sm font-semibold uppercase tracking-wide text-cmit-gray">
            Services
          </h4>
          <ul className="mt-4 space-y-2 text-sm text-light-blue">
            <li><a href="#" className="transition-colors hover:text-fg">Managed IT</a></li>
            <li><a href="#" className="transition-colors hover:text-fg">Cybersecurity</a></li>
            <li><a href="#" className="transition-colors hover:text-fg">Cloud</a></li>
            <li><a href="#" className="transition-colors hover:text-fg">Compliance</a></li>
          </ul>
        </div>
        <div>
          <h4 className="text-sm font-semibold uppercase tracking-wide text-cmit-gray">
            Company
          </h4>
          <ul className="mt-4 space-y-2 text-sm text-light-blue">
            <li><a href="/about" className="transition-colors hover:text-fg">About</a></li>
            <li><a href="#" className="transition-colors hover:text-fg">Contact</a></li>
            <li><a href="#" className="transition-colors hover:text-fg">Careers</a></li>
          </ul>
        </div>
      </div>
      <div className="border-t border-white/10 px-6 py-6 text-center text-xs text-light-blue">
        © {new Date().getFullYear()} CMIT Solutions®, LLC. All rights reserved.
      </div>
    </footer>
  )
}
