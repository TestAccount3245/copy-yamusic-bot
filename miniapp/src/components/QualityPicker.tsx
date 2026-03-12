interface Props {
  value: 'mp3' | 'flac'
  onChange: (quality: 'mp3' | 'flac') => void
}

export default function QualityPicker({ value, onChange }: Props) {
  return (
    <div className="flex gap-2">
      {(['mp3', 'flac'] as const).map((q) => (
        <button
          key={q}
          onClick={() => onChange(q)}
          className={`px-4 py-1.5 rounded-full text-xs uppercase font-medium transition-colors ${
            value === q
              ? 'bg-accent text-black'
              : 'bg-white/10 text-white/60 hover:bg-white/15'
          }`}
        >
          {q}
        </button>
      ))}
    </div>
  )
}
