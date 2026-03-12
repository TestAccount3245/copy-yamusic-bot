import { useNavigate } from 'react-router-dom'

interface Props {
  id: string
  name: string
  coverUrl?: string
}

export default function ArtistCard({ id, name, coverUrl }: Props) {
  const navigate = useNavigate()

  return (
    <button
      onClick={() => navigate(`/artist/${id}`)}
      className="flex items-center gap-3 w-full p-2 rounded-xl hover:bg-white/5 transition-colors text-left"
    >
      <div className="w-12 h-12 rounded-full bg-white/10 flex-shrink-0 overflow-hidden">
        {coverUrl && <img src={coverUrl} alt="" className="w-full h-full object-cover" />}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">{name}</p>
        <p className="text-xs text-white/50">Artist</p>
      </div>
    </button>
  )
}
