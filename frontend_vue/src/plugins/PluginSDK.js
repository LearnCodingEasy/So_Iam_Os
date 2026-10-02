// ============================================================
//  PluginSDK.js
//  src/plugins/PluginSDK.js
//
//  الـ Contract اللي كل Plugin لازم يلتزم بيه.
//
//  الفكرة:
//   كل action_type في الـ Dashboard = Plugin مستقل.
//   كل Plugin بيتعرّف على نفسه بـ metadata ويقدّم:
//     - UI component (بيظهر في الـ ActionPanel)
//     - buildPayload() (بيبني الـ payload قبل الـ API call)
//     - validate()     (بيتأكد من البيانات قبل الحفظ)
//     - icon + color   (بيظهر في الـ NodeMarketplace)
//
//  طريقة الاستخدام:
//    import { definePlugin } from '@/plugins/PluginSDK'
//    export default definePlugin({ ... })
// ============================================================

/**
 * definePlugin — بيتحقق إن الـ plugin complete وبيرجعه
 *
 * @param {Object} config
 * @param {string}   config.id          - معرّف فريد  e.g. 'open_program'
 * @param {string}   config.label       - اسم يظهر للمستخدم e.g. 'Open Program'
 * @param {string}   config.icon        - PrimeIcons class e.g. 'pi pi-desktop'
 * @param {string}   config.color       - hex color للبطاقة e.g. '#16a34a'
 * @param {string}   config.description - وصف قصير
 * @param {string}   config.category    - 'programs' | 'input' | 'timing' | 'ai' | 'custom'
 * @param {Object}   config.defaultPayload - الـ payload الافتراضي
 * @param {Function} config.buildPayload   - (formData) => payload object
 * @param {Function} config.validate       - (formData) => null | errorString
 * @param {Object}   [config.component]   - Vue component للـ ActionPanel
 * @returns {Object} plugin definition
 */
export function definePlugin(config) {
  // ─── Required fields validation ───────────────────────────
  const required = ['id', 'label', 'icon', 'color', 'category', 'buildPayload']
  for (const field of required) {
    if (!config[field]) {
      console.error(`[PluginSDK] ❌ Plugin missing required field: "${field}"`)
    }
  }

  return {
    // ─── Identity ─────────────────────────────────────────
    id:           config.id,
    label:        config.label,
    icon:         config.icon,
    color:        config.color,
    description:  config.description  ?? '',
    category:     config.category     ?? 'custom',

    // ─── Defaults ─────────────────────────────────────────
    defaultPayload: config.defaultPayload ?? {},

    // ─── Core Methods ─────────────────────────────────────

    /**
     * buildPayload — بيبني الـ payload اللي هيتبعت للـ Django
     * @param {Object} formData - البيانات من الـ ActionPanel UI
     * @returns {Object} payload
     */
    buildPayload: config.buildPayload,

    /**
     * validate — بيتأكد إن البيانات صح قبل الحفظ
     * @param {Object} formData
     * @returns {string|null} null = valid, string = error message
     */
    validate: config.validate ?? (() => null),

    /**
     * component — Vue component بيظهر في الـ ActionPanel
     * لو مفيش → بيظهر الـ DefaultActionForm
     */
    component: config.component ?? null,

    // ─── Metadata for NodeMarketplace ─────────────────────
    meta: {
      isPremium:    config.isPremium    ?? false,
      isExperimental: config.isExperimental ?? false,
      author:       config.author       ?? 'builtin',
      version:      config.version      ?? '1.0.0',
      tags:         config.tags         ?? [],
    },
  }
}

/**
 * PLUGIN_CATEGORIES — فئات الـ plugins للعرض في الـ Marketplace
 */
export const PLUGIN_CATEGORIES = {
  programs: { label: 'Programs',    icon: 'pi pi-desktop',     color: '#16a34a' },
  input:    { label: 'Input',       icon: 'pi pi-keyboard',    color: '#0ea5e9' },
  timing:   { label: 'Timing',      icon: 'pi pi-stopwatch',   color: '#f59e0b' },
  ai:       { label: 'AI Actions',  icon: 'pi pi-sparkles',    color: '#8b5cf6' },
  custom:   { label: 'Custom',      icon: 'pi pi-code',        color: '#64748b' },
}
