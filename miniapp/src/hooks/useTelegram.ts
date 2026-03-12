import { useCallback, useEffect, useMemo } from 'react'

interface TelegramWebApp {
  initData: string
  initDataUnsafe: {
    user?: {
      id: number
      first_name: string
      last_name?: string
      username?: string
      language_code?: string
    }
  }
  colorScheme: 'light' | 'dark'
  themeParams: Record<string, string>
  MainButton: {
    text: string
    show(): void
    hide(): void
    onClick(fn: () => void): void
    offClick(fn: () => void): void
    setText(text: string): void
    enable(): void
    disable(): void
  }
  BackButton: {
    show(): void
    hide(): void
    onClick(fn: () => void): void
    offClick(fn: () => void): void
  }
  HapticFeedback: {
    impactOccurred(style: 'light' | 'medium' | 'heavy'): void
    notificationOccurred(type: 'error' | 'success' | 'warning'): void
  }
  ready(): void
  expand(): void
  close(): void
}

declare global {
  interface Window {
    Telegram: {
      WebApp: TelegramWebApp
    }
  }
}

export function useTelegram() {
  const tg = useMemo(() => window.Telegram?.WebApp, [])

  useEffect(() => {
    tg?.ready()
    tg?.expand()
  }, [tg])

  const haptic = useCallback(
    (style: 'light' | 'medium' | 'heavy' = 'light') => {
      tg?.HapticFeedback?.impactOccurred(style)
    },
    [tg],
  )

  return {
    tg,
    user: tg?.initDataUnsafe?.user,
    initData: tg?.initData ?? '',
    colorScheme: tg?.colorScheme ?? 'dark',
    haptic,
  }
}
