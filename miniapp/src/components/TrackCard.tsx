import { useNavigate } from 'react-router-dom'

interface Props {
  id: string
  title: string
  artist: string
  coverUrl?: string
  duration?: number
}

export default function TrackCard({ id, title, artist, coverUrl, duration }: Props) {
  const navigate = useNavigate()

  const formatDuration = (sec?: number) => {
    if (!sec) return ''
    const m = Math.floor(sec / 60)
    const s = sec % 60
    return `${m}:${s.toString().padStart(2, '0')}`
  }

  return (
    <button
      onClick={() => navigate(`/track/${id}`)}
      className="flex items-center gap-3 w-full p-2 rounded-xl hover:bg-white/5 transition-colors text-left"
    >
      <div className="w-12 h-12 rounded-lg bg-white/10 flex-shrink-0 overflow-hidden">
        {coverUrl && <img src={coverUrl} alt="" className="w-full h-full object-cover" />}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">{title}</p>
        <p className="text-xs text-white/50 truncate">{artist}</p>
      </div>
      {duration && <span className="text-xs text-white/30">{formatDuration(duration)}</span>}
    </button>
  )
}
