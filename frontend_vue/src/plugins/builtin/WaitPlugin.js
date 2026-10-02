// ============================================================
//  WaitPlugin.js
//  src/plugins/builtin/WaitPlugin.js
//
//  الـ Action: wait
//  الـ Backend يعمل إيه؟
//    1. بياخد الـ seconds من الـ payload
//    2. بيعمل time.sleep(seconds) في الـ Python worker
//    3. بيكمل للـ Action التالية
//
//  الـ payload:
//    { seconds: 2 }
//
//  متى تستخدمه؟
//    - بعد فتح برنامج: انتظر لحد ما يكمّل التحميل
//    - بين خطوتين عشان البرنامج يتجاوب
//    - قبل الـ screenshot عشان الـ UI يظهر
//
//  مثال:
//    Action: { action_type: "wait", payload: { seconds: 3 } }
//    Django: time.sleep(3)
// ============================================================

import { definePlugin } from '../PluginSDK'

export default definePlugin({
  id:          'wait',
  label:       'Wait',
  icon:        'pi pi-stopwatch',
  color:       '#f59e0b',
  description: 'استنى عدد ثواني معين قبل الخطوة الجاية',
  category:    'timing',

  // ─── Default Payload ──────────────────────────────────────
  defaultPayload: {
    seconds: 2,   // ثانيتين افتراضياً
  },

  // ─── buildPayload ─────────────────────────────────────────
  buildPayload: (formData = {}) => ({
    seconds: Number(formData.seconds ?? 2),
  }),

  // ─── validate ─────────────────────────────────────────────
  validate: (formData = {}) => {
    const sec = Number(formData.seconds)
    if (isNaN(sec) || sec < 0)  return 'عدد الثواني لازم يكون رقم موجب'
    if (sec > 300)               return 'الحد الأقصى 300 ثانية (5 دقائق)'
    return null
  },

  // ─── Metadata ─────────────────────────────────────────────
  author:  'builtin',
  version: '1.0.0',
  tags:    ['wait', 'delay', 'sleep', 'timing', 'pause'],
})
