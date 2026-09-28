import { onMounted, ref } from 'vue'

const THEME_KEY = 'so_iam_os.theme'

export function useTheme() {
  const isDark = ref(false)

  const apply = (dark) => {
    isDark.value = Boolean(dark)
    document.documentElement.classList.toggle('p-dark', isDark.value)
    document.documentElement.dataset.theme = isDark.value ? 'dark' : 'light'
    localStorage.setItem(THEME_KEY, isDark.value ? 'dark' : 'light')
  }

  const toggle = () => apply(!isDark.value)

  onMounted(() => {
    const saved = localStorage.getItem(THEME_KEY)
    apply(saved ? saved === 'dark' : window.matchMedia?.('(prefers-color-scheme: dark)').matches)
  })

  return { isDark, apply, toggle }
}
