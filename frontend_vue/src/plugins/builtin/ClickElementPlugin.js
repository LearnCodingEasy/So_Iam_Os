// ============================================================
//  ClickElementPlugin.js
//  src/plugins/builtin/ClickElementPlugin.js
//
//  الـ Action: click_element
//  الـ Backend يعمل إيه؟
//    1. بياخد الـ element_id من الـ payload
//    2. بيجيب الـ ProgramElement من الـ DB
//    3. حسب الـ selector_type:
//       - "image"  → pyautogui.locateCenterOnScreen(image, confidence)
//       - "coords" → pyautogui.click(x, y)
//       - "ui"     → pywinauto.find_element(xpath).click()
//    4. قبل الـ click بيعمل focus على الـ program window
//
//  الـ payload:
//    { element_id: "uuid-of-program-element" }
//
//  مثال:
//    Action: { action_type: "click_element", payload: { element_id: "btn-build-uuid" } }
//    Django: _click_element("btn-build-uuid") → pyautogui.click(x, y)
// ============================================================

import { definePlugin } from '../PluginSDK'

export default definePlugin({
  id:          'click_element',
  label:       'Click Element',
  icon:        'pi pi-mouse',
  color:       '#0ea5e9',
  description: 'اضغط على عنصر محدد في الشاشة (زرار، input، menu...)',
  category:    'input',

  // ─── Default Payload ──────────────────────────────────────
  defaultPayload: {
    element_id: null,   // UUID بتاع الـ ProgramElement
  },

  // ─── buildPayload ─────────────────────────────────────────
  // formData.element_id = الـ UUID اللي اختاره المستخدم من الـ dropdown
  buildPayload: (formData = {}) => ({
    element_id: formData.element_id ?? null,
  }),

  // ─── validate ─────────────────────────────────────────────
  validate: (formData = {}) => {
    if (!formData.element_id) return 'لازم تختار العنصر اللي هتضغط عليه'
    return null
  },

  // ─── Metadata ─────────────────────────────────────────────
  author:  'builtin',
  version: '1.0.0',
  tags:    ['click', 'mouse', 'element', 'button', 'ui'],
})
