import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import api from '../api/client'
import GlassPanel from '../components/GlassPanel'

export default function Settings() {
  const queryClient = useQueryClient()
  const [token, setToken] = useState('')

  const { data: user } = useQuery({
    queryKey: ['user'],
    queryFn: () => api.get('/users/me').then((r) => r.data.user),
  })

  const linkYandex = useMutation({
    mutationFn: (t: string) => api.post('/users/link-yandex', { token: t }),
    onSuccess: () => {
      setToken('')
      queryClient.invalidateQueries({ queryKey: ['user'] })
    },
  })

  const updateQuality = useMutation({
    mutationFn: (q: string) => api.put('/users/settings', { preferred_quality: q }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['user'] }),
  })

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">Settings</h1>

      <GlassPanel className="space-y-3">
        <h2 className="font-semibold text-sm">Yandex Music Account</h2>
        {user?.has_yandex ? (
          <p className="text-green-400 text-sm">Connected</p>
        ) : (
          <div className="space-y-2">
            <input
              type="text"
              placeholder="Yandex OAuth token"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              className="w-full bg-white/5 rounded-lg px-3 py-2 text-sm outline-none placeholder-white/30"
            />
            <button
              onClick={() => token && linkYandex.mutate(token)}
              disabled={!token || linkYandex.isPending}
              className="w-full py-2 rounded-lg bg-accent text-black text-sm font-semibold disabled:opacity-50"
            >
              Link Account
            </button>
          </div>
        )}
      </GlassPanel>

      <GlassPanel className="space-y-3">
        <h2 className="font-semibold text-sm">Download Quality</h2>
        <div className="flex gap-2">
          {['mp3', 'flac'].map((q) => (
            <button
              key={q}
              onClick={() => updateQuality.mutate(q)}
              className={`flex-1 py-2 rounded-lg text-sm uppercase ${
                user?.preferred_quality === q
                  ? 'bg-accent text-black font-semibold'
                  : 'bg-white/10 text-white/60'
              }`}
            >
              {q}
            </button>
          ))}
        </div>
      </GlassPanel>
    </div>
  )
}
