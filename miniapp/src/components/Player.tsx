import { usePlayerStore } from '../store/playerStore'

export default function Player() {
  const { currentTrack, isPlaying, toggle } = usePlayerStore()

  if (!currentTrack) return null

  return (
    <div className="fixed bottom-16 left-2 right-2 glass-panel-strong p-3 flex items-center gap-3 z-40">
      <div className="w-10 h-10 rounded-lg bg-white/10 flex-shrink-0 overflow-hidden">
        {currentTrack.coverUrl && (
          <img src={currentTrack.coverUrl} alt="" className="w-full h-full object-cover" />
        )}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">{currentTrack.title}</p>
        <p className="text-xs text-white/50 truncate">{currentTrack.artist}</p>
      </div>
      <button
        onClick={toggle}
        className="w-10 h-10 flex items-center justify-center rounded-full bg-accent text-black"
      >
        {isPlaying ? '⏸' : '▶'}
      </button>
    </div>
  )
}
