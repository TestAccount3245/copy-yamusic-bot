import GlassPanel from '../components/GlassPanel'

export default function Downloads() {
  // TODO: fetch download history from /api/users/me/downloads
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">Library</h1>

      <div className="flex gap-3">
        <button className="flex-1 glass-panel py-3 text-center text-sm font-medium">
          Downloads
        </button>
        <button
          className="flex-1 glass-panel py-3 text-center text-sm font-medium text-white/50"
          onClick={() => window.location.href = '/upload'}
        >
          Upload
        </button>
      </div>

      <GlassPanel>
        <p className="text-white/40 text-sm text-center">Your download history will appear here</p>
      </GlassPanel>
    </div>
  )
}
