import { useState, useRef } from 'react'
import { useMutation } from '@tanstack/react-query'
import api from '../api/client'
import GlassPanel from '../components/GlassPanel'

export default function Upload() {
  const fileRef = useRef<HTMLInputElement>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const upload = useMutation({
    mutationFn: async (file: File) => {
      const form = new FormData()
      form.append('file', file)
      return api.post('/uploads', form).then((r) => r.data.track)
    },
    onSuccess: () => setSelectedFile(null),
  })

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">Upload Track</h1>

      <GlassPanel className="text-center space-y-3">
        <input
          ref={fileRef}
          type="file"
          accept="audio/*"
          className="hidden"
          onChange={(e) => setSelectedFile(e.target.files?.[0] ?? null)}
        />
        <button
          onClick={() => fileRef.current?.click()}
          className="w-full py-8 border-2 border-dashed border-white/20 rounded-xl text-white/40 hover:border-accent/50 hover:text-accent/50 transition-colors"
        >
          {selectedFile ? selectedFile.name : 'Tap to select audio file'}
        </button>

        {selectedFile && (
          <>
            <div className="text-xs text-white/40">
              {(selectedFile.size / 1024 / 1024).toFixed(1)} MB
            </div>
            <button
              onClick={() => upload.mutate(selectedFile)}
              disabled={upload.isPending}
              className="w-full py-3 rounded-xl bg-accent text-black font-semibold disabled:opacity-50"
            >
              {upload.isPending ? 'Uploading...' : 'Upload'}
            </button>
          </>
        )}

        {upload.isSuccess && (
          <p className="text-green-400 text-sm">Track uploaded successfully!</p>
        )}
        {upload.isError && (
          <p className="text-red-400 text-sm">Upload failed. Please try again.</p>
        )}
      </GlassPanel>
    </div>
  )
}
