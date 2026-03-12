import { useParams } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import api from '../api/client'
import GlassPanel from '../components/GlassPanel'
import { useTelegram } from '../hooks/useTelegram'

export default function Track() {
  const { id } = useParams<{ id: string }>()
  const { haptic } = useTelegram()
  const [quality, setQuality] = useState<'mp3' | 'flac'>('mp3')

  const { data } = useQuery({
    queryKey: ['track', id],
    queryFn: () => api.get(`/tracks/${id}`).then((r) => r.data.track),
  })

  const download = useMutation({
    mutationFn: () => api.post(`/tracks/${id}/download`, { quality }),
    onSuccess: () => haptic('medium'),
  })

  const track = data

  return (
    <div className="p-4 space-y-6">
      {track && (
        <>
          <div className="flex flex-col items-center gap-4">
            <div className="w-64 h-64 rounded-2xl bg-white/10 overflow-hidden">
              {track.cover_url && (
                <img src={track.cover_url} alt="" className="w-full h-full object-cover" />
              )}
            </div>
            <div className="text-center">
              <h1 className="text-xl font-bold">{track.title}</h1>
              <p className="text-white/50">{track.artist}</p>
            </div>
          </div>

          <GlassPanel className="flex items-center justify-between">
            <span className="text-sm text-white/60">Quality</span>
            <div className="flex gap-2">
              {(['mp3', 'flac'] as const).map((q) => (
                <button
                  key={q}
                  onClick={() => setQuality(q)}
                  className={`px-3 py-1 rounded-full text-xs uppercase ${
                    quality === q ? 'bg-accent text-black' : 'bg-white/10 text-white/60'
                  }`}
                >
                  {q}
                </button>
              ))}
            </div>
          </GlassPanel>

          <button
            onClick={() => download.mutate()}
            disabled={download.isPending}
            className="w-full py-3 rounded-2xl bg-accent text-black font-semibold disabled:opacity-50"
          >
            {download.isPending ? 'Downloading...' : 'Download'}
          </button>
        </>
      )}
    </div>
  )
}
