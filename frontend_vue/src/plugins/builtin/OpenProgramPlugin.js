// ============================================================
//  OpenProgramPlugin.js
//  src/plugins/builtin/OpenProgramPlugin.js
//
//  الـ Action: open_program
//  الـ Backend يعمل إيه؟
//    1. بياخد الـ executable_path من الـ Program المربوط بالـ Node
//    2. بيشغّله عبر subprocess.Popen(executable_path)
//    3. بيستنى لحد ما يتأكد إن البرنامج اشتغل (psutil check)
//    4. لو ما اشتغلش في 20 ثانية → error
//
//  الـ payload:
//    {} ← فارغ لأن الـ Node نفسه محمّل program FK
//
//  مثال:
//    Node: { program: "vscode-uuid", node_type: "program" }
//    Action: { action_type: "open_program", payload: {} }
//    Django: _open_program(node.program) → subprocess.Popen(...)
// ============================================================

import { definePlugin } from '../PluginSDK'

export default definePlugin({
  id:          'open_program',
  label:       'Open Program',
  icon:        'pi pi-desktop',
  color:       '#16a34a',
  description: 'افتح البرنامج المحدد (VSCode, Chrome, OBS...)',
  category:    'programs',

  // ─── Default Payload ──────────────────────────────────────
  // فارغ لأن الـ Django بياخد المعلومات من الـ Node.program FK
  defaultPayload: {},

  // ─── buildPayload ─────────────────────────────────────────
  // مش محتاجين نبعت حاجة — الـ backend بيعرف البرنامج من الـ node
  buildPayload: () => ({}),

  // ─── validate ─────────────────────────────────────────────
  // الـ validation بيتعمل على مستوى الـ Node مش الـ Action
  // (يعني لازم الـ Node يكون عنده program FK)
  validate: () => null,

  // ─── Metadata ─────────────────────────────────────────────
  author:  'builtin',
  version: '1.0.0',
  tags:    ['program', 'open', 'launch', 'start'],
})
