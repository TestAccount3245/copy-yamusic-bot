import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
import TrackCard from '../components/TrackCard'

const TYPES = ['all', 'track', 'album', 'artist'] as const

export default function Search() {
  const [query, setQuery] = useState('')
  const [type, setType] = useState<string>('all')

  const { data, isFetching } = useQuery({
    queryKey: ['search', query, type],
    queryFn: () => api.get('/search', { params: { q: query, type } }).then((r) => r.data.results),
    enabled: query.length >= 2,
  })

  return (
    <div className="p-4 space-y-4">
      <input
        type="text"
        placeholder="Search music..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full glass-panel px-4 py-3 bg-transparent text-white placeholder-white/30 outline-none"
      />

      <div className="flex gap-2">
        {TYPES.map((t) => (
          <button
            key={t}
            onClick={() => setType(t)}
            className={`px-3 py-1 rounded-full text-xs transition-colors ${
              type === t ? 'bg-accent text-black' : 'glass-panel text-white/60'
            }`}
          >
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      <div>
        {isFetching && <p className="text-white/30 text-sm">Searching...</p>}
        {data?.tracks?.map((t: any) => (
          <TrackCard
            key={t.id}
            id={t.id}
            title={t.title}
            artist={t.artist}
            coverUrl={t.cover_url}
            duration={t.duration_sec}
          />
        ))}
      </div>
    </div>
  )
}
