import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
import TrackCard from '../components/TrackCard'

export default function Wave() {
  const { data } = useQuery({
    queryKey: ['wave'],
    queryFn: () => api.get('/wave').then((r) => r.data.tracks),
  })

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">My Wave</h1>
      <p className="text-sm text-white/40">Personalized for you</p>

      <div>
        {data?.map((t: any) => (
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
