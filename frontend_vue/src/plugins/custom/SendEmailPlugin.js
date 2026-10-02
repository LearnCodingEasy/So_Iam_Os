// src/plugins/custom/SendEmailPlugin.js
import { definePlugin } from '@/plugins/PluginSDK'

export default definePlugin({
  id:          'send_email',
  label:       'Send Email',
  icon:        'pi pi-envelope',
  color:       '#0ea5e9',
  category:    'custom',
  defaultPayload: { to: '', subject: '', body: '' },
  buildPayload: (form) => ({ to: form.to, subject: form.subject, body: form.body }),
  validate: (form) => !form.to ? 'البريد الإلكتروني مطلوب' : null,
})
