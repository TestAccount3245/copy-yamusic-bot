import { useQuery, useMutation } from '@tanstack/react-query'
import api from '../api/client'

export function useSearch(query: string, type: string) {
  return useQuery({
    queryKey: ['search', query, type],
    queryFn: () => api.get('/search', { params: { q: query, type } }).then((r) => r.data.results),
    enabled: query.length >= 2,
  })
}

export function useTrack(id: string) {
  return useQuery({
    queryKey: ['track', id],
    queryFn: () => api.get(`/tracks/${id}`).then((r) => r.data.track),
  })
}

export function useAlbum(id: string) {
  return useQuery({
    queryKey: ['album', id],
    queryFn: () => api.get(`/albums/${id}`).then((r) => r.data.album),
  })
}

export function useArtist(id: string) {
  return useQuery({
    queryKey: ['artist', id],
    queryFn: () => api.get(`/artists/${id}`).then((r) => r.data.artist),
  })
}

export function useWave() {
  return useQuery({
    queryKey: ['wave'],
    queryFn: () => api.get('/wave').then((r) => r.data.tracks),
  })
}

export function useUser() {
  return useQuery({
    queryKey: ['user'],
    queryFn: () => api.get('/users/me').then((r) => r.data.user),
  })
}

export function useDownloadTrack() {
  return useMutation({
    mutationFn: ({ trackId, quality }: { trackId: string; quality: string }) =>
      api.post(`/tracks/${trackId}/download`, { quality }),
  })
}

export function useUploadTrack() {
  return useMutation({
    mutationFn: (file: File) => {
      const form = new FormData()
      form.append('file', file)
      return api.post('/uploads', form)
    },
  })
}
