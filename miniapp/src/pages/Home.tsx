import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
import GlassPanel from '../components/GlassPanel'
import TrackCard from '../components/TrackCard'

export default function Home() {
  const { data: wave } = useQuery({
    queryKey: ['wave'],
    queryFn: () => api.get('/wave').then((r) => r.data.tracks),
  })

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold">YaMusic</h1>

      <section>
        <h2 className="text-lg font-semibold mb-3">My Wave</h2>
        <GlassPanel>
          {wave?.length ? (
            wave.slice(0, 10).map((t: any) => (
              <TrackCard
                key={t.id}
                id={t.id}
                title={t.title}
                artist={t.artist}
                coverUrl={t.cover_url}
                duration={t.duration_sec}
              />
            ))
          ) : (
            <p className="text-white/40 text-sm">Link your Yandex account to see personalized recommendations</p>
          )}
        </GlassPanel>
      </section>
    </div>
  )
}
