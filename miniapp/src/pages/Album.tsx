import { useParams } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import api from '../api/client'
import GlassPanel from '../components/GlassPanel'
import TrackCard from '../components/TrackCard'

export default function Album() {
  const { id } = useParams<{ id: string }>()

  const { data } = useQuery({
    queryKey: ['album', id],
    queryFn: () => api.get(`/albums/${id}`).then((r) => r.data.album),
  })

  const download = useMutation({
    mutationFn: () => api.post(`/albums/${id}/download`, { quality: 'mp3' }),
  })

  const album = data

  return (
    <div className="p-4 space-y-4">
      {album && (
        <>
          <div className="flex gap-4 items-end">
            <div className="w-32 h-32 rounded-xl bg-white/10 overflow-hidden flex-shrink-0">
              {album.cover_url && (
                <img src={album.cover_url} alt="" className="w-full h-full object-cover" />
              )}
            </div>
            <div>
              <h1 className="text-lg font-bold">{album.title}</h1>
              <p className="text-sm text-white/50">{album.artist}</p>
              {album.year && <p className="text-xs text-white/30">{album.year}</p>}
            </div>
          </div>

          <button
            onClick={() => download.mutate()}
            disabled={download.isPending}
            className="w-full py-2 rounded-xl bg-accent text-black font-semibold text-sm disabled:opacity-50"
          >
            {download.isPending ? 'Downloading...' : 'Download Album'}
          </button>

          <GlassPanel>
            {album.tracks?.map((t: any, i: number) => (
              <div key={t.id} className="flex items-center gap-2">
                <span className="text-xs text-white/30 w-6 text-right">{i + 1}</span>
                <div className="flex-1">
                  <TrackCard
                    id={t.id}
                    title={t.title}
                    artist={t.artist}
                    duration={t.duration_sec}
                  />
                </div>
              </div>
            ))}
          </GlassPanel>
        </>
      )}
    </div>
  )
}
