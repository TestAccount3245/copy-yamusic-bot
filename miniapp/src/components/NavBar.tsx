import { useNavigate, useLocation } from 'react-router-dom'

const tabs = [
  { path: '/', label: 'Home', icon: '🏠' },
  { path: '/search', label: 'Search', icon: '🔍' },
  { path: '/downloads', label: 'Library', icon: '📚' },
  { path: '/settings', label: 'Settings', icon: '⚙️' },
]

export default function NavBar() {
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <nav className="fixed bottom-0 left-0 right-0 glass-panel-strong rounded-none border-x-0 border-b-0 px-2 py-2 flex justify-around items-center z-50">
      {tabs.map((tab) => {
        const active = location.pathname === tab.path
        return (
          <button
            key={tab.path}
            onClick={() => navigate(tab.path)}
            className={`flex flex-col items-center gap-0.5 px-4 py-1 rounded-xl transition-colors ${
              active ? 'text-accent' : 'text-white/50'
            }`}
          >
            <span className="text-xl">{tab.icon}</span>
            <span className="text-[10px]">{tab.label}</span>
          </button>
        )
      })}
    </nav>
  )
}
