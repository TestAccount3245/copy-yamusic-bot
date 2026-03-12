import { ReactNode } from 'react'

interface Props {
  children: ReactNode
  className?: string
  strong?: boolean
}

export default function GlassPanel({ children, className = '', strong = false }: Props) {
  return (
    <div className={`${strong ? 'glass-panel-strong' : 'glass-panel'} p-4 ${className}`}>
      {children}
    </div>
  )
}
