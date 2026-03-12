import { create } from 'zustand'

interface TrackInfo {
  id: string
  title: string
  artist: string
  coverUrl?: string
  previewUrl?: string
}

interface PlayerState {
  currentTrack: TrackInfo | null
  isPlaying: boolean
  setTrack: (track: TrackInfo) => void
  play: () => void
  pause: () => void
  toggle: () => void
  clear: () => void
}

export const usePlayerStore = create<PlayerState>((set) => ({
  currentTrack: null,
  isPlaying: false,
  setTrack: (track) => set({ currentTrack: track, isPlaying: true }),
  play: () => set({ isPlaying: true }),
  pause: () => set({ isPlaying: false }),
  toggle: () => set((state) => ({ isPlaying: !state.isPlaying })),
  clear: () => set({ currentTrack: null, isPlaying: false }),
}))
