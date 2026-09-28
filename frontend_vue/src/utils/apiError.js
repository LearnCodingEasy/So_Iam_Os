export function getApiErrorMessage(error, fallback = 'Something went wrong.') {
  const data = error?.response?.data
  if (typeof data === 'string' && data.trim()) return data
  if (data?.detail) return String(data.detail)
  if (data?.message) return String(data.message)
  if (data?.error) return String(data.error)
  if (data && typeof data === 'object') {
    const first = Object.values(data).flat?.()[0]
    if (first) return String(first)
  }
  if (error?.message) return error.message
  return fallback
}

export function isAuthError(error) {
  return error?.response?.status === 401
}
