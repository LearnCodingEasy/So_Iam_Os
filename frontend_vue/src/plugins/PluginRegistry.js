// ===================================================
//  PluginRegistry.js
//  src/plugins/PluginRegistry.js
//
//  المسؤولية:
//   - تسجيل كل الـ plugins (builtin + خارجية)
//   - توفير lookup بالـ action_type
//   - توفير قائمة كاملة للـ NodeMarketplace
//
//  طريقة الاستخدام:
//    import registry from '@/plugins/PluginRegistry'
//
//    // جيب plugin معين
//    const plugin = registry.get('open_program')
//
//    // جيب كل الـ plugins (للـ Marketplace)
//    const all = registry.getAll()
//
//    // جيب plugins بفئة معينة
//    const aiPlugins = registry.getByCategory('ai')
//
//    // سجّل plugin خارجي
//    registry.register(myCustomPlugin)
// ===================================================

import { definePlugin } from './PluginSDK'

// categories
export const PLUGIN_CATEGORIES = {
  programs: { label: 'Programs', icon: 'pi pi-desktop' },
  input: { label: 'Keyboard / Input', icon: 'pi pi-keyboard' },
  timing: { label: 'Timing', icon: 'pi pi-clock' },
  ai: { label: 'AI', icon: 'pi pi-sparkles' },
  custom: { label: 'Custom', icon: 'pi pi-cog' },
}
// ─── Builtin Plugins ──────────────────────────────
import OpenProgramPlugin from './builtin/OpenProgramPlugin'
import ClickElementPlugin from './builtin/ClickElementPlugin'
import WaitPlugin from './builtin/WaitPlugin'
import AIActionPlugin from './builtin/AIActionPlugin'

// ─── Press & Hotkey (بسيطة — معرّفة هنا مباشرة) ──────────
const PressPlugin = definePlugin({
  id: 'press',
  label: 'Press Key',
  icon: 'pi pi-arrow-right',
  color: '#64748b',
  description: 'اضغط على مفتاح واحد (Enter, Escape, Tab...)',
  category: 'input',
  defaultPayload: { key: 'Enter' },
  buildPayload: (form) => ({ key: form.key || 'Enter' }),
  validate: (form) => (!form.key?.trim() ? 'اسم المفتاح مطلوب' : null),
  tags: ['keyboard', 'key', 'press'],
})

const HotkeyPlugin = definePlugin({
  id: 'hotkey',
  label: 'Hotkey',
  icon: 'pi pi-bolt',
  color: '#f59e0b',
  description: 'اضغط مجموعة مفاتيح معاً (Ctrl+C, Ctrl+Shift+P...)',
  category: 'input',
  defaultPayload: { keys: ['ctrl', 'c'] },
  buildPayload: (form) => ({
    keys: Array.isArray(form.keys)
      ? form.keys
      : String(form.keys || '')
          .split('+')
          .map((k) => k.trim())
          .filter(Boolean),
  }),
  validate: (form) => (!form.keys?.length ? 'لازم تحدد مفاتيح' : null),
  tags: ['keyboard', 'shortcut', 'hotkey'],
})

const CloseProgram = definePlugin({
  id: 'close_program',
  label: 'Close Program',
  icon: 'pi pi-times-circle',
  color: '#dc2626',
  description: 'اقفل البرنامج المفتوح',
  category: 'programs',
  defaultPayload: {},
  buildPayload: () => ({}),
  tags: ['program', 'close'],
})

// ===================================================
//  Registry Class
// ===================================================
class PluginRegistry {
  constructor() {
    /** @type {Map<string, Object>} */
    this._plugins = new Map()
    this._initialized = false
  }

  // ─── Init — بيتشغل مرة واحدة عند بداية الـ App ───────────
  init() {
    if (this._initialized) return this
    this._initialized = true

    // ✅ سجّل كل الـ builtin plugins
    this.register(OpenProgramPlugin)
    this.register(ClickElementPlugin)
    this.register(WaitPlugin)
    this.register(AIActionPlugin)
    this.register(PressPlugin)
    this.register(HotkeyPlugin)
    this.register(CloseProgram)

    console.log(`[PluginRegistry] ✅ ${this._plugins.size} plugins registered`)
    return this
  }

  // ─── CRUD ─────────────────────────────────────────────────

  /**
   * سجّل plugin جديد
   * @param {Object} plugin - plugin definition من definePlugin()
   */
  register(plugin) {
    if (!plugin?.id) {
      console.warn('[PluginRegistry] ⚠️ Cannot register plugin without id')
      return this
    }
    if (this._plugins.has(plugin.id)) {
      console.warn(`[PluginRegistry] ⚠️ Plugin "${plugin.id}" already registered — overwriting`)
    }
    this._plugins.set(plugin.id, plugin)
    return this
  }

  /**
   * جيب plugin بالـ action_type
   * @param {string} actionType
   * @returns {Object|null}
   */
  get(actionType) {
    return this._plugins.get(actionType) ?? null
  }

  /**
   * جيب كل الـ plugins كـ array
   * @returns {Object[]}
   */
  getAll() {
    return Array.from(this._plugins.values())
  }

  /**
   * جيب plugins بفئة معينة
   * @param {string} category
   * @returns {Object[]}
   */
  getByCategory(category) {
    return this.getAll().filter((p) => p.category === category)
  }

  /**
   * ابني payload من الـ action_type والـ formData
   * لو مفيش plugin مسجّل → بيرجع {} فارغة
   * @param {string} actionType
   * @param {Object} formData
   * @returns {Object}
   */
  buildPayload(actionType, formData = {}) {
    const plugin = this.get(actionType)
    if (!plugin) {
      console.warn(`[PluginRegistry] ⚠️ No plugin for action_type: "${actionType}"`)
      return {}
    }
    return plugin.buildPayload(formData)
  }

  /**
   * validate الـ form قبل الحفظ
   * @param {string} actionType
   * @param {Object} formData
   * @returns {string|null}
   */
  validate(actionType, formData = {}) {
    const plugin = this.get(actionType)
    if (!plugin) return null
    return plugin.validate(formData)
  }

  /**
   * جيب الـ Vue component الخاص بالـ plugin
   * للاستخدام في الـ ActionPanel
   * @param {string} actionType
   * @returns {Object|null} Vue component
   */
  getComponent(actionType) {
    return this.get(actionType)?.component ?? null
  }

  /**
   * جيب default payload
   * @param {string} actionType
   * @returns {Object}
   */
  getDefaultPayload(actionType) {
    return this.get(actionType)?.defaultPayload ?? {}
  }

  // ─── Marketplace helpers ───────────────────────────────
  getMarketplaceItems() {
    return this.getAll().map((p) => ({
      id: p.id,
      label: p.label,
      icon: p.icon,
      color: p.color,
      description: p.description,
      category: p.category,
      tags: p.meta?.tags ?? [],
      isPremium: p.meta?.isPremium ?? false,
    }))
  }
}

import SendEmailPlugin from './custom/SendEmailPlugin'

// ─── Singleton Export ──────────────────────────────
const registry = new PluginRegistry()
registry.init()
registry.register(SendEmailPlugin)

export default registry
