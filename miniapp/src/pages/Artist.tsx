import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
import GlassPanel from '../components/GlassPanel'
import TrackCard from '../components/TrackCard'

export default function Artist() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { data } = useQuery({
    queryKey: ['artist', id],
    queryFn: () => api.get(`/artists/${id}`).then((r) => r.data.artist),
  })

  const artist = data

  return (
    <div className="p-4 space-y-6">
      {artist && (
        <>
          <div className="flex flex-col items-center gap-3">
            <div className="w-32 h-32 rounded-full bg-white/10 overflow-hidden">
              {artist.cover_url && (
                <img src={artist.cover_url} alt="" className="w-full h-full object-cover" />
              )}
            </div>
            <h1 className="text-xl font-bold">{artist.name}</h1>
          </div>

          <section>
            <h2 className="text-base font-semibold mb-2">Top Tracks</h2>
            <GlassPanel>
              {artist.top_tracks?.map((t: any) => (
                <TrackCard
                  key={t.id}
                  id={t.id}
                  title={t.title}
                  artist={artist.name}
                  coverUrl={t.cover_url}
                  duration={t.duration_sec}
                />
              ))}
            </GlassPanel>
          </section>

          {artist.albums?.length > 0 && (
            <section>
              <h2 className="text-base font-semibold mb-2">Albums</h2>
              <div className="grid grid-cols-2 gap-3">
                {artist.albums.map((a: any) => (
                  <button
                    key={a.id}
                    onClick={() => navigate(`/album/${a.id}`)}
                    className="glass-panel p-2 text-left"
                  >
                    <div className="w-full aspect-square rounded-lg bg-white/10 overflow-hidden mb-2">
                      {a.cover_url && (
                        <img src={a.cover_url} alt="" className="w-full h-full object-cover" />
                      )}
                    </div>
                    <p className="text-xs font-medium truncate">{a.title}</p>
                    <p className="text-[10px] text-white/40">{a.year}</p>
                  </button>
                ))}
              </div>
            </section>
          )}
        </>
      )}
    </div>
  )
}
