// // ============================================================
// //  useApiTracker.js  — Vue 3 Composable
// //  الصق الملف ده في مجلد composables/ في أي مشروع Vue
// //  الاستخدام: شوف README في آخر الملف
// // ============================================================

// import { ref, reactive } from 'vue'
// import axios from 'axios'

// // ── Stage definitions ────────────────────────────────────────
// const STAGES_TEMPLATE = [
//   { id: 'init',     label: 'تجهيز الطلب',      icon: '🔧', layer: 'Vue'     },
//   { id: 'auth',     label: 'التحقق من الهوية',  icon: '🔐', layer: 'Vue'     },
//   { id: 'send',     label: 'إرسال الـ Request', icon: '📡', layer: 'Network' },
//   { id: 'server',   label: 'السيرفر يعالج',     icon: '⚙️', layer: 'Django'  },
//   { id: 'response', label: 'استقبال الـ Response', icon: '📥', layer: 'Network' },
//   { id: 'parse',    label: 'قراءة البيانات',    icon: '📦', layer: 'Vue'     },
//   { id: 'done',     label: 'اكتمل',             icon: '✅', layer: 'Vue'     },
// ]

// // ── Create fresh stages array ────────────────────────────────
// function freshStages() {
//   return STAGES_TEMPLATE.map(s => ({
//     ...s,
//     status: 'idle',   // idle | active | pass | fail | skip
//     detail: null,
//     timing: null,
//   }))
// }

// // ── Main composable ──────────────────────────────────────────
// export function useApiTracker() {

//   const stages   = reactive(freshStages())
//   const isLoading = ref(false)
//   const result    = ref(null)
//   const error     = ref(null)
//   const meta      = reactive({
//     method: null, url: null, status: null,
//     requestBody: null, responseBody: null,
//     duration: null, startedAt: null,
//   })

//   // helper: set a stage status + detail
//   function setStage(id, status, detail = null) {
//     const s = stages.find(x => x.id === id)
//     if (!s) return
//     s.status = status
//     if (detail) s.detail = detail
//     if (status === 'active') s.timing = Date.now()
//     if ((status === 'pass' || status === 'fail') && s.timing) {
//       s.timing = Date.now() - s.timing
//     }
//   }

//   function resetAll() {
//     stages.forEach((s, i) => {
//       Object.assign(stages[i], freshStages()[i])
//     })
//     result.value  = null
//     error.value   = null
//     Object.assign(meta, {
//       method: null, url: null, status: null,
//       requestBody: null, responseBody: null,
//       duration: null, startedAt: null,
//     })
//   }

//   // ── execute: wraps any axios call ───────────────────────────
//   // options: { url, method, data, params, headers, label }
//   async function execute(options = {}) {
//     const {
//       serviceFn,
//       url,
//       method = 'GET',
//       data   = null,
//       params = null,
//       headers = {},
//       label  = null,
//     } = options

//     resetAll()
//     isLoading.value = true
//     const globalStart = Date.now()

//     meta.startedAt = new Date().toLocaleTimeString('ar-EG')
//     meta.method    = method.toUpperCase()
//     meta.url       = url
//     meta.requestBody = data ? JSON.stringify(data, null, 2) : null

//     // ── Stage 1: INIT ────────────────────────────────────────
//     setStage('init', 'active')
//     await tick()
//     const initDetail = `Method: ${method.toUpperCase()} | URL: ${url}`
//       + (data   ? `\nBody: ${JSON.stringify(data)}` : '')
//       + (params ? `\nParams: ${JSON.stringify(params)}` : '')
//     setStage('init', 'pass', initDetail)

//     // ── Stage 2: AUTH ────────────────────────────────────────
//     setStage('auth', 'active')
//     await tick()
//     const token = getToken()
//     if (token) {
//       headers['Authorization'] = headers['Authorization'] || `Token ${token}`
//       setStage('auth', 'pass', `Token موجود ✓`)
//     } else {
//       // not a fail unless endpoint requires auth — mark as info
//       setStage('auth', 'skip', 'مفيش token (public endpoint)')
//     }

//     // ── Stage 3: SEND ────────────────────────────────────────
//     setStage('send', 'active')
//     await tick()

//     let response
//     try {
//       response = await axios({
//         url, method,
//         data:   data   || undefined,
//         params: params || undefined,
//         headers: {
//           'Content-Type': 'application/json',
//           ...headers,
//         },
//       })

//       // ── Stage 4: SERVER (inferred) ─────────────────────────
//       setStage('send',   'pass', `Request أُرسل`)
//       setStage('server', 'active')
//       await tick(80)
//       setStage('server', 'pass', `Django استجاب`)

//       // ── Stage 5: RESPONSE ──────────────────────────────────
//       setStage('response', 'active')
//       await tick(60)
//       meta.status = response.status
//       meta.responseBody = JSON.stringify(response.data, null, 2)
//       setStage('response', 'pass',
//         `Status: ${response.status} | Size: ${roughSize(response.data)}`)

//       // ── Stage 6: PARSE ─────────────────────────────────────
//       setStage('parse', 'active')
//       await tick(60)
//       const shape = describeShape(response.data)
//       setStage('parse', 'pass', `شكل البيانات: ${shape}`)

//       // ── Stage 7: DONE ──────────────────────────────────────
//       setStage('done', 'active')
//       await tick(40)
//       meta.duration = Date.now() - globalStart
//       setStage('done', 'pass', `اكتمل في ${meta.duration}ms`)

//       result.value    = response.data
//       isLoading.value = false
//       return response.data

//     } catch (err) {
//       // ── Error path ──────────────────────────────────────────
//       const st = err.response?.status

//       // mark send stage
//       setStage('send', err.response ? 'pass' : 'fail',
//         err.response ? 'Request وصل' : 'Network Error — السيرفر مش شغال أو URL غلط')

//       if (err.response) {
//         setStage('server', 'active')
//         await tick(60)

//         const errDetail = buildErrorDetail(st, err.response.data)
//         setStage('server', 'fail', `Django رجع ${st}`)
//         setStage('response', 'fail',
//           `Status: ${st} | ${errDetail.short}`)
//         setStage('parse', 'skip', 'لم يتم — الـ request فشل')
//         setStage('done',  'fail', errDetail.short)

//         meta.status = st
//         meta.responseBody = JSON.stringify(err.response.data, null, 2)
//         error.value = { status: st, data: err.response.data, detail: errDetail }
//       } else {
//         // no response at all
//         setStage('server',   'skip', 'لم يصل')
//         setStage('response', 'skip', 'لم يصل')
//         setStage('parse',    'skip', 'لم يصل')
//         setStage('done', 'fail', 'Network Error')
//         error.value = { status: null, data: null, detail: { short: err.message, fix: networkFix(url) } }
//       }

//       meta.duration   = Date.now() - globalStart
//       isLoading.value = false
//       throw err
//     }
//   }

//   return { execute, stages, isLoading, result, error, meta, reset: resetAll }
// }

// // ── Helpers ──────────────────────────────────────────────────

// function tick(ms = 120) {
//   return new Promise(r => setTimeout(r, ms))
// }

// function getToken() {
//   return (
//     localStorage.getItem('token') ||
//     localStorage.getItem('access_token') ||
//     localStorage.getItem('authToken') ||
//     null
//   )
// }

// function roughSize(data) {
//   try {
//     const s = JSON.stringify(data).length
//     return s > 1024 ? `${(s/1024).toFixed(1)}KB` : `${s}B`
//   } catch { return 'unknown' }
// }

// function describeShape(data) {
//   if (data === null)         return 'null (204 No Content)'
//   if (Array.isArray(data))   return `Array [ ${data.length} عنصر ]`
//   if (typeof data === 'object') {
//     const keys = Object.keys(data)
//     if (keys.includes('results') && keys.includes('count'))
//       return `Paginated { count: ${data.count}, results: ${data.results?.length} }`
//     return `Object { ${keys.slice(0,4).join(', ')}${keys.length > 4 ? '…' : ''} }`
//   }
//   return typeof data
// }

// function buildErrorDetail(status, body) {
//   const fixes = {
//     400: {
//       short: 'Validation Error — البيانات غلط',
//       fix: `راجع الـ Serializer fields. شوف: error.data لكل field فيه مشكلة.\nالـ errors: ${JSON.stringify(body).slice(0,200)}`,
//     },
//     401: {
//       short: 'Unauthorized — مفيش أو Token منتهي',
//       fix: 'تأكد إن الـ token موجود في localStorage وبيتبعت في Authorization header. لو JWT افحص الـ expiry.',
//     },
//     403: {
//       short: 'Forbidden — مش عنده صلاحية',
//       fix: 'الـ user مسجل بس مش عنده permission. راجع permission_classes في الـ Django View.',
//     },
//     404: {
//       short: 'Not Found — مش موجود',
//       fix: 'الـ URL غلط أو الـ ID مش موجود في الـ Database. افحص الـ urlpatterns في urls.py.',
//     },
//     405: {
//       short: 'Method Not Allowed',
//       fix: 'الـ View مش بيقبل الـ HTTP method دي. راجع http_method_names أو allowed_methods.',
//     },
//     409: {
//       short: 'Conflict — بيانات مكررة',
//       fix: 'في unique constraint انتهك — مثلاً email مكرر. راجع الـ unique_together في الـ Model.',
//     },
//     500: {
//       short: 'Server Error — Django وقع',
//       fix: 'افتح Django terminal وشوف الـ Traceback. أو فعّل DEBUG=True مؤقتاً.',
//     },
//   }
//   return fixes[status] || { short: `HTTP ${status}`, fix: 'راجع Django logs.' }
// }

// function networkFix(url) {
//   if (!url?.startsWith('http'))
//     return 'الـ URL مش كامل — لازم يبدأ بـ http:// أو https://'
//   return 'تأكد إن Django server شغال وإن الـ baseURL صح في axios config.'
// }

// // ============================================================
// //  README — طريقة الاستخدام في أي مشروع
// // ============================================================
// //
// //  1. نسخ useApiTracker.js في مجلد src/composables/
// //  2. نسخ ApiFlowPanel.vue في مجلد src/components/
// //
// //  في أي Component:
// //  ─────────────────────────────────────────────────────────
// //  <script setup>
// //  import { useApiTracker } from '@/composables/useApiTracker'
// //  import ApiFlowPanel from '@/components/ApiFlowPanel.vue'
// //
// //  const { execute, stages, result, error, meta } = useApiTracker()
// //
// //  async function createProduct() {
// //    try {
// //      const data = await execute({
// //        url: '/api/products/',
// //        method: 'POST',
// //        data: { name: 'Laptop', price: 999 }
// //      })
// //      console.log('نجح:', data)
// //    } catch(e) {
// //      console.log('فشل:', error.value)
// //    }
// //  }
// //  </script>
// //
// //  <template>
// //    <button @click="createProduct">إضافة منتج</button>
// //    <ApiFlowPanel :stages="stages" :meta="meta" :error="error" />
// //  </template>
// //  ─────────────────────────────────────────────────────────
// ============================================================
//  useApiTracker.js — النسخة المحدثة لدعم الـ Service Functions
// ============================================================

import { ref, reactive } from 'vue'
import axios from 'axios'

const STAGES_TEMPLATE = [
  { id: 'init', label: 'تجهيز الطلب', icon: '🔧', layer: 'Vue' },
  { id: 'auth', label: 'التحقق من الهوية', icon: '🔐', layer: 'Vue' },
  { id: 'send', label: 'إرسال الـ Request', icon: '📡', layer: 'Network' },
  { id: 'server', label: 'السيرفر يعالج', icon: '⚙️', layer: 'Django' },
  { id: 'response', label: 'استقبال الـ Response', icon: '📥', layer: 'Network' },
  { id: 'parse', label: 'قراءة البيانات', icon: '📦', layer: 'Vue' },
  { id: 'done', label: 'اكتمل', icon: '✅', layer: 'Vue' },
]

function freshStages() {
  return STAGES_TEMPLATE.map((s) => ({
    ...s,
    status: 'idle',
    detail: null,
    timing: null,
  }))
}

export function useApiTracker() {
  const stages = reactive(freshStages())
  const isLoading = ref(false)
  const result = ref(null)
  const error = ref(null)
  const meta = reactive({
    method: null,
    url: null,
    status: null,
    requestBody: null,
    responseBody: null,
    duration: null,
    startedAt: null,
  })

  function setStage(id, status, detail = null) {
    const s = stages.find((x) => x.id === id)
    if (!s) return
    s.status = status
    if (detail) s.detail = detail
    if (status === 'active') s.timing = Date.now()
    if ((status === 'pass' || status === 'fail') && s.timing) {
      s.timing = Date.now() - s.timing
    }
  }

  function resetAll() {
    stages.forEach((s, i) => Object.assign(stages[i], freshStages()[i]))
    result.value = null
    error.value = null
    Object.assign(meta, {
      method: null,
      url: null,
      status: null,
      requestBody: null,
      responseBody: null,
      duration: null,
      startedAt: null,
    })
  }

  async function execute(options = {}) {
    const {
      serviceFn, // الدالة من الـ AutomationService
      url,
      method = 'GET',
      data = null,
      params = null,
      headers = {},
    } = options

    resetAll()
    isLoading.value = true
    const globalStart = Date.now()
    meta.startedAt = new Date().toLocaleTimeString('ar-EG')

    // ── Stage 1: INIT ────────────────────────────────────────
    setStage('init', 'active')
    await tick(50)

    // تحديد البيانات الوصفية مبدئياً
    meta.method = method.toUpperCase()
    meta.url = url || 'دالة داخلية (Service)'
    meta.requestBody = data ? JSON.stringify(data, null, 2) : null

    setStage('init', 'pass', serviceFn ? 'تم تجهيز دالة الخدمة' : `Target: ${url}`)

    // ── Stage 2: AUTH ────────────────────────────────────────
    setStage('auth', 'active')
    const token = getToken()
    if (token) {
      headers['Authorization'] = headers['Authorization'] || `Token ${token}`
      setStage('auth', 'pass', `Token موجود ✓`)
    } else {
      setStage('auth', 'skip', 'لا يوجد Token')
    }

    // ── Stage 3: SEND ────────────────────────────────────────
    setStage('send', 'active')
    let response
    try {
      if (serviceFn) {
        // ✅ تنفيذ الدالة مباشرة (هذا يحل مشكلة الـ 404)
        response = await serviceFn()
      } else {
        // التنفيذ التقليدي عبر axios
        response = await axios({
          url,
          method,
          data,
          params,
          headers: { 'Content-Type': 'application/json', ...headers },
        })
      }

      // تحديث الـ Meta من الـ response الفعلي للسيرفر
      meta.url = response.config?.url || meta.url
      meta.method = response.config?.method?.toUpperCase() || meta.method

      // ── Stage 4: SERVER ─────────────────────────────────────
      setStage('send', 'pass', `تم الإرسال`)
      setStage('server', 'active')
      await tick(100)
      setStage('server', 'pass', `السيرفر استجاب بنجاح`)

      // ── Stage 5: RESPONSE ──────────────────────────────────
      setStage('response', 'active')
      meta.status = response.status
      meta.responseBody = JSON.stringify(response.data, null, 2)
      setStage('response', 'pass', `Status: ${response.status} | Size: ${roughSize(response.data)}`)

      // ── Stage 6: PARSE ─────────────────────────────────────
      setStage('parse', 'active')
      setStage('parse', 'pass', `شكل البيانات: ${describeShape(response.data)}`)

      // ── Stage 7: DONE ──────────────────────────────────────
      setStage('done', 'active')
      meta.duration = Date.now() - globalStart
      setStage('done', 'pass', `اكتمل في ${meta.duration}ms`)

      result.value = response.data
      return response.data
    } catch (err) {
      // ── Error Path ──────────────────────────────────────────
      const st = err.response?.status
      setStage('send', err.response ? 'pass' : 'fail', err.response ? 'وصل للسيرفر' : 'خطأ شبكة')

      if (err.response) {
        const errDetail = buildErrorDetail(st, err.response.data)
        setStage('server', 'fail', `خطأ من السيرفر: ${st}`)
        setStage('response', 'fail', errDetail.short)
        setStage('done', 'fail', 'فشل الطلب')

        meta.status = st
        meta.responseBody = JSON.stringify(err.response.data, null, 2)
        error.value = { status: st, data: err.response.data, detail: errDetail }
      } else {
        setStage('done', 'fail', 'Network Error')
        error.value = { status: null, detail: { short: err.message, fix: networkFix(url) } }
      }
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return { execute, stages, isLoading, result, error, meta, reset: resetAll }
}

// ── Helpers (نفس الـ Helpers اللي في كودك مع تحسينات بسيطة) ──
function tick(ms = 100) {
  return new Promise((r) => setTimeout(r, ms))
}

function getToken() {
  return localStorage.getItem('token') || localStorage.getItem('access_token')
}

function roughSize(data) {
  try {
    const s = JSON.stringify(data).length
    return s > 1024 ? `${(s / 1024).toFixed(1)}KB` : `${s}B`
  } catch {
    return '0B'
  }
}

function describeShape(data) {
  if (Array.isArray(data)) return `Array [${data.length}]`
  if (data && typeof data === 'object') return `Object {${Object.keys(data).length} keys}`
  return typeof data
}

function buildErrorDetail(status, body) {
  const fixes = {
    400: { short: 'بيانات غير صالحة', fix: 'راجع الحقول المرسلة' },
    401: { short: 'غير مصرح', fix: 'انتهت الجلسة، سجل دخول مجدداً' },
    404: { short: 'غير موجود', fix: 'الرابط غلط أو العنصر غير موجود في قاعدة البيانات' },
    500: { short: 'خطأ داخلي', fix: 'السيرفر تعطل، راجع الـ Terminal الخاص بـ Django' },
  }
  return fixes[status] || { short: `Error ${status}`, fix: 'فشل الطلب' }
}

function networkFix(url) {
  return url ? 'تأكد أن سيرفر Django يعمل' : 'الرابط غير محدد'
}
