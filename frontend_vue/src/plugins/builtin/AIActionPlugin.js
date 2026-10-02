// ============================================================
//  AIActionPlugin.js
//  src/plugins/builtin/AIActionPlugin.js
//
//  الـ Action: ai_action
//  الفكرة:
//    بدل ما تحدد كل خطوة يدوياً، الـ AI بيقرر هو إيه الخطوة الجاية
//    بناءً على سياق الشاشة الحالية (screenshot + context)
//
//  الـ Backend يعمل إيه؟
//    1. بياخد screenshot للشاشة الحالية
//    2. بيبعتها مع الـ prompt للـ OpenAI Vision API
//    3. الـ AI بيرجع action (click x,y أو press key أو wait)
//    4. الـ Worker بينفّذ الـ action ده
//
//  الـ payload:
//    {
//      model:         "gpt-4o",
//      prompt:        "اضغط على زرار Build",
//      context:       "VSCode مفتوح",
//      max_steps:     3,      ← أقصى عدد خطوات يعملها الـ AI
//      screenshot:    true,   ← هل يبعت screenshot؟
//      fallback_action: "wait" ← لو الـ AI مش عارف يعمل إيه
//    }
//
//  ملاحظة:
//    ده Plugin تجريبي — الـ Backend لسه بيتبنى
//    isExperimental: true
// ============================================================

import { definePlugin } from '../PluginSDK'

export default definePlugin({
  id:          'ai_action',
  label:       'AI Action',
  icon:        'pi pi-sparkles',
  color:       '#8b5cf6',
  description: 'خلّي الـ AI يقرر الخطوة الجاية بناءً على حالة الشاشة',
  category:    'ai',

  // ─── Default Payload ──────────────────────────────────────
  defaultPayload: {
    model:           'gpt-4o',
    prompt:          '',
    context:         '',
    max_steps:       3,
    screenshot:      true,
    fallback_action: 'wait',
  },

  // ─── buildPayload ─────────────────────────────────────────
  buildPayload: (formData = {}) => ({
    model:           formData.model           ?? 'gpt-4o',
    prompt:          formData.prompt          ?? '',
    context:         formData.context         ?? '',
    max_steps:       Number(formData.max_steps ?? 3),
    screenshot:      formData.screenshot      ?? true,
    fallback_action: formData.fallback_action ?? 'wait',
  }),

  // ─── validate ─────────────────────────────────────────────
  validate: (formData = {}) => {
    if (!formData.prompt?.trim())  return 'لازم تكتب prompt للـ AI'
    if (formData.max_steps > 10)   return 'الحد الأقصى 10 خطوات'
    return null
  },

  // ─── Metadata ─────────────────────────────────────────────
  author:         'builtin',
  version:        '0.1.0',
  isExperimental: true,   // ← يظهر badge "Experimental" في الـ Marketplace
  isPremium:      false,
  tags:           ['ai', 'gpt', 'vision', 'smart', 'auto'],
})
