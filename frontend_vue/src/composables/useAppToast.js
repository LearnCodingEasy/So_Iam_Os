import { useToast } from 'primevue/usetoast'
import { getApiErrorMessage } from '@/utils/apiError'

export function useAppToast() {
  const toast = useToast()

  const success = (detail, summary = 'Success') =>
    toast.add({ severity: 'success', summary, detail, life: 3200 })

  const info = (detail, summary = 'Info') =>
    toast.add({ severity: 'info', summary, detail, life: 3200 })

  const warn = (detail, summary = 'Attention') =>
    toast.add({ severity: 'warn', summary, detail, life: 3600 })

  const error = (value, summary = 'Error') =>
    toast.add({
      severity: 'error',
      summary,
      detail: typeof value === 'string' ? value : getApiErrorMessage(value),
      life: 4500,
    })

  return { success, info, warn, error }
}
