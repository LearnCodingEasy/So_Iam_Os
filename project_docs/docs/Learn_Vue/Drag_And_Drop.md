# Drag And Drop

<div dir="rtl">

Vue Flow علشان نعمل مخطط Nodes متوصلة ببعض (زي Workflow أو Automation Diagram).
<br/>
يعني عندك:
<br/>

🟡 Start
<br/>
⬇️
<br/>
🟡 End
<br/>

وخط بينهم 🔗

</div>

## Install

```cmd
  npm install @vue-flow/core
  npm install @vue-flow/background
  npm install @vue-flow/controls
  npm install @vue-flow/minimap
  npm install lodash
  npm install @dagrejs/dagre
  npm install vuedraggable@next
  npm install dagre nanoid
```

```cmd
  npm install @vue-flow/core @vue-flow/background @vue-flow/controls @vue-flow/minimap vuedraggable@next lodash @dagrejs/dagre nanoid dagre
```

## First Graph

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow v-model:nodes="nodes" v-model:edges="edges"> </VueFlow>
  </div>
</template>
```

```js
<script setup>
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>
```

```css
<style>
  /* Style For Explain */
  .VueFlow_Component_Name {
    height: 93vh;
    width: 90%;
    overflow: hidden;
    margin: auto;
  }
</style>
```

![This is an image](automation\first-graph.png)

## CSS Style

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow v-model:nodes="nodes" v-model:edges="edges"> </VueFlow>
  </div>
</template>
```

```js
<script setup>
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>
```

```css
<style lang="scss">
  // Style For Explain
  .VueFlow_Component_Name {
    height: 93vh;
    width: 90%;
    overflow: hidden;
    margin: auto;
  }

  // Style For VueFlow
  // Node Style
  .vue-flow__node,
  .vue-flow__node-custom {
    background: #ffeaa7;
    color: white;
    box-shadow: 0 0 0 1px #ffeaa7;
    padding: 8px;
    border: 1px solid #ffeaa7;
    border-radius: 4px;
    font-size: 15px;
  }

  // Parent Single Node
  .vue-flow__node {
    border: 1px solid #ffeaa7;
    outline: none;
    &:focus-visible {
      border: 1px solid #ffeaa7;
    }
  }

  .vue-flow__node-default.selected,
  .vue-flow__node-default:focus,
  .vue-flow__node-default:focus-visible {
    border: 1px solid #ffeaa7;
  }

  // Edge
  .vue-flow__node-default .vue-flow__handle,
  .vue-flow__node-input .vue-flow__handle,
  .vue-flow__node-output .vue-flow__handle {
    width: 33px;
    height: 13px;
    border-radius: 10px;
    background-color: #fdcb6e;
    border: 1px solid transparent;
  }
</style>
```

![This is an image](automation\css_style.png)

## Background

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow v-model:nodes="nodes" v-model:edges="edges">
      <Background />
      <Background pattern-color="#aaa" :gap="8" />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>
```

![This is an image](automation\Background.png)

## MiniMap

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow v-model:nodes="nodes" v-model:edges="edges">
      <Background />
      <MiniMap />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>
```

![This is an image](automation\MiniMap.png)

## Controls

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow v-model:nodes="nodes" v-model:edges="edges">
      <Background />
      <Controls />
      <MiniMap />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 100, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>

```

![This is an image](automation\Controls.png)

## Zoom

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      :default-zoom="1.5"
      :min-zoom="0.2"
      :max-zoom="4"
    >
      <Background />
      <Controls />
      <MiniMap />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 100, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>
```

![This is an image](automation\Zoom.png)

## Zoom Control

```html
<button @click="zoomIn()">+</button>
<button @click="zoomOut()">-</button>
<button @click="fitView()">Fit</button>
```

```js
// It gives you control tools (Zoom / Fit)
import { useVueFlow } from "@vue-flow/core";
// VueFlow Controls
const { zoomIn, zoomOut, fitView } = useVueFlow();
```

## Node

### Single

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      @node-click="onNodeClick"
    >
      <Background pattern-color="#aaa" :gap="8" />
      <MiniMap />
      <Controls />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 📦 Drag and drop tools for the user interface
  // import vuedraggable from 'vuedraggable'
  // 🟣 Definition of Nodes
  const nodes = ref([
    {
      id: '1', position: { x: 100, y: 80 }, data: {
        label: "Start",
        type: "trigger",
        color: "green",
        apiUrl: "/start-process"
      }
    },
    { id: '2', position: { x: 100, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
  // 🖱️ Clicking Node | print data in console.
  function onNodeClick(e) {
    console.log('Node Click:', e.node)
  }
</script>
```

### Add

```html
<template>
  <div class="VueFlow_Component_Name">
    <div class="">
      <button type="button" @click="addNode">Add Node</button>
    </div>
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      :default-zoom="1.5"
      :min-zoom="0.2"
      :max-zoom="5"
      @node-click="onNodeClick"
    >
      <Background pattern-color="#aaa" :gap="8" />
      <MiniMap />
      <Controls />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 🟣 Definition of Nodes
  const nodes = ref([
    {
      id: '1', position: { x: 100, y: 80 }, data: {
        label: "Start",
        type: "trigger",
        color: "green",
        apiUrl: "/start-process",
        ui: {
          theme: {
            background: '#0f172a',
            border: '#334155',
            shadow: '#334155'
          },
          layout: {
            width: 260,
            height: 240,
            rounded: true
          }
        },
        inputs: [
          { key: 'text', label: 'Text', type: 'string', value: '' },
          { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
          { key: 'color', label: 'Background Color', type: 'color', value: '#0f172a' }
        ],
        ai: {
          enabled: false,
          context: {},
          memory: [],
          suggestions: []
        }
      }
    },
    { id: '2', position: { x: 100, y: 150 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
  // 🖱️ Clicking Node | print data in console.
  function feature1() {
    console.log("Feature 1 Activated 🎯")
  }
  function onNodeClick(e) {
    feature1()
    console.log("Node Click:", e.node)
  }
  // ➕ Add Node
  function addNode() {
    nodes.value.push({
      id: Date.now().toString(),
      position: { x: 100, y: 220 },
      data: { label: 'Dynamic Node 🚀' }
    })
  }
</script>
```

![This is an image](automation\Zoom.png)

### Update

```html
<template>
  <div class="VueFlow_Component_Name">
    <div class="">
      <button type="button" @click="addNode">Add Node</button>
      <button type="button" @click="updateLabel">Update Node Label</button>
    </div>
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      :default-zoom="1.5"
      :min-zoom="0.2"
      :max-zoom="5"
      @node-click="onNodeClick"
    >
      <Background pattern-color="#aaa" :gap="8" />
      <MiniMap />
      <Controls />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 🟣 Definition of Nodes
  const nodes = ref([
    {
      id: '1', position: { x: 100, y: 80 }, data: {
        label: "Start",
        type: "trigger",
        color: "green",
        apiUrl: "/start-process",
        ui: {
          theme: {
            background: '#0f172a',
            border: '#334155',
            shadow: '#334155'
          },
          layout: {
            width: 260,
            height: 240,
            rounded: true
          }
        },
        inputs: [
          { key: 'text', label: 'Text', type: 'string', value: '' },
          { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
          { key: 'color', label: 'Background Color', type: 'color', value: '#0f172a' }
        ],
        ai: {
          enabled: false,
          context: {},
          memory: [],
          suggestions: []
        }
      }
    },
    { id: '2', position: { x: 100, y: 150 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
  // 🖱️ Clicking Node | print data in console.
  function feature1() {
    console.log("Feature 1 Activated 🎯")
  }
  function onNodeClick(e) {
    feature1()
    console.log("Node Click:", e.node)
  }
  // ➕ Add Node
  function addNode() {
    nodes.value.push({
      id: Date.now().toString(),
      position: { x: 100, y: 220 },
      data: { label: 'Dynamic Node 🚀' }
    })
  }
  // ♻️ Update Node
  function updateLabel() {
    nodes.value[0].data.label = "Updated ✨"
  }
</script>
```

![This is an image](automation\Zoom.png)

### Delete

```html
<template>
  <div class="VueFlow_Component_Name">
    <div class="">
      <button type="button" @click="addNode">Add Node</button>
      <button type="button" @click="updateLabel">Update Node Label</button>
      <button type="button" @click="deleteLastNode">Delete Node</button>
    </div>
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      :default-zoom="1.5"
      :min-zoom="0.2"
      :max-zoom="5"
      @node-click="onNodeClick"
    >
      <Background pattern-color="#aaa" :gap="8" />
      <MiniMap />
      <Controls />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 🟣 Definition of Nodes
  const nodes = ref([
    {
      id: '1', position: { x: 100, y: 80 }, data: {
        label: "Start",
        type: "trigger",
        color: "green",
        apiUrl: "/start-process",
        ui: {
          theme: {
            background: '#0f172a',
            border: '#334155',
            shadow: '#334155'
          },
          layout: {
            width: 260,
            height: 240,
            rounded: true
          }
        },
        inputs: [
          { key: 'text', label: 'Text', type: 'string', value: '' },
          { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
          { key: 'color', label: 'Background Color', type: 'color', value: '#0f172a' }
        ],
        ai: {
          enabled: false,
          context: {},
          memory: [],
          suggestions: []
        }
      }
    },
    { id: '2', position: { x: 100, y: 150 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
  // 🖱️ Clicking Node | print data in console.
  function feature1() {
    console.log("Feature 1 Activated 🎯")
  }
  function onNodeClick(e) {
    feature1()
    console.log("Node Click:", e.node)
  }
  // ➕ Add Node
  function addNode() {
    nodes.value.push({
      id: Date.now().toString(),
      position: { x: 100, y: 220 },
      data: { label: 'Dynamic Node 🚀' }
    })
  }
  // ♻️ Update Node
  function updateLabel() {
    nodes.value[0].data.label = "Updated ✨"
  }
  // 🗑️ Delete Node
  function deleteLastNode() {
    nodes.value.pop()
  }
</script>
```

![This is an image](automation\Zoom.png)

## Local Storage

### Storage Service

<div dir="rtl" style="font-size: 20px;">
  <div class=""></div>
</div>
  
<div dir="rtl" style="font-size: 20px;">
  <div class="">🔹 Read All  بيرجع كل البيانات</div>
  <div class="">🔹 Read One بيرجع عنصر واحد</div>
  <div class="">🔹 Create بيضيف عنصر جديد داخل Array</div>
  <div class="">🔹 Update  بيعدل عنصر موجود</div>
  <div class="">🔹 Delete  بيحذف العنصر + الروابط المرتبطة</div>
</div>

```js
  // frontend_vue\src\services\nodeStorageService.js
  // 🔑 مفتاح التخزين
  const STORAGE_KEY = "vueflow_graph";

  /_ =================================================
  🧠 PRIVATE HELPERS
  ================================================= _/

  // 📖 READ ALL
  function read() {
  const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return { nodes: [], edges: [] };
      try {
        const parsed = JSON.parse(raw);
        return {
          nodes: Array.isArray(parsed.nodes) ? parsed.nodes : [],
          edges: Array.isArray(parsed.edges) ? parsed.edges : [],
        };
      } catch {
        return { nodes: [], edges: [] };
      }
  }

  // 💾 WRITE
  function write(graph) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(graph));
  }

  /_ =================================================
  🚀 PUBLIC CRUD API
  ================================================= _/

  // 📚 READ ALL
  export function getGraph() {
  return read();
  }

  // 🔍 READ ONE (Node)
  export function getOne(id) {
  const graph = read();
  return graph.nodes.find((n) => n.id === id);
  }

  export function getEdge(id) {
  const graph = read();
  return graph.edges.find((e) => e.id === id);
  }
  // ➕ CREATE
  export function createNode(node) {
  const graph = read();
  graph.nodes.push(node);
  write(graph);
  }

  // ✏️ UPDATE
  export function updateNode(id, newData) {
  const graph = read();
  const index = graph.nodes.findIndex((n) => n.id === id);
  if (index === -1) return;
  graph.nodes[index] = {
  ...graph.nodes[index],
  ...newData,
  };
      write(graph);
  }

  // 🗑 DELETE
  export function removeNode(id) {
  const graph = read();
  graph.nodes = graph.nodes.filter((n) => n.id !== id);
  // 🔗 حذف أي Edge مرتبط
  graph.edges = graph.edges.filter((e) => e.source !== id && e.target !== id);
  write(graph);
  }
  export function removeEdge(id) {
    const graph = read()
    graph.edges = graph.edges.filter((n) => n.id !== id)
    write(graph)
  }
  // 💾 SAVE ALL (لما نستخدم Drag)
  export function saveGraph(nodes, edges) {
  write({ nodes, edges });
  }
```

### 1️⃣ Import Library

```js
// ==================================================
// 📦 1️⃣ Imports (المكتبات المستخدمة)
// ==================================================
// 🧠 Vue Composition API
import { ref, onMounted, watch } from "vue";
// 🔗 VueFlow (المكتبة الأساسية للرسم والـ Drag & Drop)
import { VueFlow } from "@vue-flow/core";
// 🎨 خلفية الشبكة (Grid Background)
import { Background } from "@vue-flow/background";
// 🗺️ MiniMap (خريطة مصغرة للمخطط)
import { MiniMap } from "@vue-flow/minimap";
// 🎛️ Controls (Zoom / Fit / Lock)
import { Controls } from "@vue-flow/controls";
// 📦 Panel (لو عايز تضيف أزرار مخصصة داخل VueFlow)
import { Panel } from "@vue-flow/core";
// 🆔 إنشاء ID فريد لكل Node أو Edge
import { nanoid } from "nanoid";
// ⏳ Debounce (يمنع الحفظ كل مرة يحصل تغيير سريع)
import debounce from "lodash/debounce";
```

### 1️⃣ Import Storage Service

```js
// 💾 Service مسؤول عن التخزين في LocalStorage
import { getGraph, saveGraph } from "@/services/nodeStorageService";
```

### 2️⃣ Static Variables

```js
// ==================================================
// 📍 2️⃣ State (البيانات التفاعلية)
// ==================================================
// 📦 كل الـ Nodes الموجودة في الرسم
const nodes = ref([]);
// 🔗 كل الـ Edges (الروابط بين الـ Nodes)
const edges = ref([]);
```

### 3️⃣ Lifecycle

```js
// ==================================================
// 🚀 3️⃣ Lifecycle (تشغيل أول ما الصفحة تفتح)
// ==================================================
// 👂 لما الكمبوننت يتركب
onMounted(initGraph);
// 🔄 تهيئة الجراف
function initGraph() {
  loadGraph();
}
```

### 4️⃣ LOAD GRAPH

```js
// ==================================================
// 📖 4️⃣ LOAD GRAPH (تحميل البيانات)
// ==================================================
function loadGraph() {
  // 📥 نقرأ البيانات من LocalStorage
  const graph = getGraph();
  // 🧠 لو فيه بيانات محفوظة
  if (graph.nodes.length) {
    nodes.value = graph.nodes;
    edges.value = graph.edges;
  } else {
    // 🆕 لو مفيش بيانات → ننشئ جراف افتراضي
    createDefaultGraph();
  }
}
```

### 5️⃣ Create Default Graph

```js
// ==================================================
// 🆕 5️⃣ Create Default Graph (أول تشغيل)
// ==================================================
function createDefaultGraph() {
  // 🆔 إنشاء ID فريد
  const startId = nanoid();
  const endId = nanoid();
  // 📦 إنشاء Nodes
  nodes.value = [
    {
      id: startId,
      position: { x: 100, y: 80 },
      data: { label: "Start 🚀" },
    },
    {
      id: endId,
      position: { x: 300, y: 200 },
      data: { label: "End 🏁" },
    },
  ];
  // 🔗 ربط Start → End
  edges.value = [
    {
      id: nanoid(),
      source: startId,
      target: endId,
    },
  ];
}
```

### 6️⃣ Auto Save

```js
// ==================================================
// 💾 6️⃣ Auto Save (حفظ تلقائي)
// ==================================================
// ⏳ Debounce: يمنع الحفظ كل جزء من الثانية
// بدل ما يحفظ كل حركة Drag
const debouncedSave = debounce(() => {
  // 💾 احفظ الجراف بالكامل
  saveGraph(nodes.value, edges.value);
}, 500); // بعد 500ms من آخر تغيير

// 👀 مراقبة أي تغيير في nodes أو edges
watch(
  [nodes, edges], // 👈 نراقب الاتنين
  debouncedSave, // 👈 لما يحصل تغيير ننفذ الحفظ
  { deep: true } // 👈 نراقب التغييرات الداخلية
);
```

```html
<template>
  <main class="h-screen p-4 grid grid-cols-12 gap-4 ">
    <section class="col-span-12  border rounded">
      <div class="VueFlow_Component_Name">
        <!-- eslint-disable vue/no-v-model-argument -->
        <VueFlow
          v-model:nodes="nodes"
          v-model:edges="edges"
          :default-zoom="1.5"
          :min-zoom="0.2"
          :max-zoom="5"
          @node-click="getSingleNode"
          @edge-click="getSingleEdge"
          @connect="addEdge"
          @selection-change="onSelectionChange"
          :class="{ layouting: isLayouting }"
          :snap-to-grid="true"
          :snap-grid="[20, 20]"
        >
          <Background pattern-color="#aaa" :gap="8" />
          <MiniMap />
          <Controls />
          <Panel
            position="top-right"
            style="display:flex; gap:5px;"
            class="wrapper_control_panel"
          >
            <button @click="zoomIn()">+</button>
            <button @click="zoomOut()">-</button>
            <button @click="fitView()">Fit</button>
          </Panel>
        </VueFlow>
      </div>
    </section>
  </main>
</template>
```

### 📖 READ ALL

![This is an image](automation\READ_ALL_Local_Storage.png)

### 📖 READ Single

```html
<template>
  <main class="h-screen p-4 grid grid-cols-12 gap-4">
    <aside class="col-span-3 border rounded p-4 overflow-auto space-y-6">
      <h2 class="aside_title m-auto text-3xl">Controls</h2>
      <div class="wrapper_control">
        <div class="wrapper_control_node_data">
          <div v-if="selectedNode" class="node_data">
            <h3>Node Settings ⚙️</h3>
            <input v-model="selectedNode.data.label" />
          </div>
          <div v-if="selectedEdge" class="edge_data">
            <h3>Edge Settings 🔗</h3>
            <p>From: {{ selectedEdge.source }}</p>
            <p>To: {{ selectedEdge.target }}</p>
          </div>
        </div>
      </div>
    </aside>
    <section class="col-span-9 border rounded">
      <div class="VueFlow_Component_Name">
        <!-- eslint-disable vue/no-v-model-argument -->
        <VueFlow
          v-model:nodes="nodes"
          v-model:edges="edges"
          :default-zoom="1.5"
          :min-zoom="0.2"
          :max-zoom="5"
          @node-click="getSingleNode"
          @edge-click="getSingleEdge"
          @connect="addEdge"
          @selection-change="onSelectionChange"
          :class="{ layouting: isLayouting }"
          :snap-to-grid="true"
          :snap-grid="[20, 20]"
        >
          <Background pattern-color="#aaa" :gap="8" />
          <MiniMap />
          <Controls />
          <Panel
            position="top-right"
            style="display:flex; gap:5px;"
            class="wrapper_control_panel"
          >
            <button @click="zoomIn()">+</button>
            <button @click="zoomOut()">-</button>
            <button @click="fitView()">Fit</button>
          </Panel>
        </VueFlow>
      </div>
    </section>
  </main>
</template>
```

```js
// 💾 Service مسؤول عن التخزين في LocalStorage
import {
  getGraph,
  getOne,
  getEdge,
  saveGraph,
} from "@/services/nodeStorageService";
```

```js
// 📌 Selection
const selectedNode = ref(null);
const selectedEdge = ref([]);
```

```js
/* ==================================================
🔍 4️⃣ READ
================================================== */
/**
 * 🧩 getSingleNode(e)
 * 🎯 وظيفتها: جلب Node واحدة من التخزين عند الضغط عليها
 * 🧠 الفكرة:
 * VueFlow بيبعت لنا Event فيه بيانات العقدة
 * لكن إحنا بنرجع نجيبها من Storage علشان يكون المصدر واحد (Source of Truth)
 */
function getSingleNode(e) {
  // 🆔 استخراج الـ ID من الحدث
  const nodeId = e.node.id;
  // 📦 جلب العقدة من التخزين باستخدام Service
  const node = getOne(nodeId);
  // 🎯 تخزين العقدة المختارة لعرضها في الـ Side Panel
  selectedNode.value = node;
  // ❌ إلغاء تحديد أي Edge
  selectedEdge.value = null;
  // 🖥️ طباعة في الكونسول للتأكد
  console.log("📦 Node From Storage:", node);
}
/**
 * 🔗 getSingleEdge(e)
 * 🎯 وظيفتها: جلب Edge واحدة عند الضغط عليها
 * 🧠 نفس الفكرة بالظبط لكن مع الروابط
 */
function getSingleEdge(e) {
  // 🆔 استخراج ID الرابط
  const edgeId = e.edge.id;
  // 📦 جلب الرابط من التخزين
  const edge = getEdge(edgeId);
  // 🎯 تخزين الرابط المختار
  selectedEdge.value = edge;
  // ❌ إلغاء تحديد أي Node
  selectedNode.value = null;
  // 🖥️ طباعة للتأكد
  console.log("🔗 Edge From Storage:", edge);
}
```

![This is an image](automation\READ_ALL_Local_Storage.png)

### ➕ CREATE

```html
<template>
  <main class="h-screen p-4 grid grid-cols-12 gap-4">
    <aside class="col-span-3 border rounded p-4 overflow-auto space-y-6">
      <h2 class="aside_title m-auto text-3xl">Controls</h2>
      <div class="wrapper_control">
        <div class="wrapper_control_node">
          <button type="button" @click="addNode">➕ Add Node</button>
        </div>
      </div>
    </aside>

    <section class="col-span-9 border rounded">
      <div class="VueFlow_Component_Name">
        <!-- eslint-disable vue/no-v-model-argument -->
        <VueFlow
          v-model:nodes="nodes"
          v-model:edges="edges"
          :default-zoom="1.5"
          :min-zoom="0.2"
          :max-zoom="5"
          @node-click="getSingleNode"
          @edge-click="getSingleEdge"
          @connect="addEdge"
          @selection-change="onSelectionChange"
          :class="{ layouting: isLayouting }"
          :snap-to-grid="true"
          :snap-grid="[20, 20]"
        >
          <Background pattern-color="#aaa" :gap="8" />
          <MiniMap />
          <Controls />
          <Panel
            position="top-right"
            style="display:flex; gap:5px;"
            class="wrapper_control_panel"
          >
            <button @click="zoomIn()">+</button>
            <button @click="zoomOut()">-</button>
            <button @click="fitView()">Fit</button>
          </Panel>
        </VueFlow>
      </div>
    </section>
  </main>
</template>
```

```js
// 💾 Service مسؤول عن التخزين في LocalStorage
import { getGraph, createNode, saveGraph } from "@/services/nodeStorageService";
```

```js
/* ==================================================
➕ 3️⃣ CREATE
================================================== */
/**
 * ➕ addNode()
 * 🎯 وظيفتها: إنشاء Node جديدة داخل النظام
 * 🧠 الفكرة:
 * 1- ننشئ كائن يمثل العقدة
 * 2- نحفظه في الـ Storage
 * 3- نعمل Sync مع Vue علشان يحصل Re-render
 */
function addNode() {
  // 🆔 إنشاء ID فريد لكل Node
  const newNode = {
    id: nanoid(), // 🔑 ID فريد باستخدام مكتبة nanoid
    position: { x: 100, y: 220 }, // 📍 مكان الظهور على الشاشة
    data: { label: "Dynamic Node 🚀" }, // 🏷️ البيانات الخاصة بالعقدة
  };
  // 💾 حفظ العقدة داخل Storage Service
  createNode(newNode);
  // 🔄 تحديث حالة Vue بالبيانات الجديدة
  syncGraph();
}
/**
 * 🔄 syncGraph()
 * 🎯 وظيفتها: مزامنة البيانات بين Storage و Vue State
 * 🧠 ليه بنعملها؟
 * لأننا بنخلي المصدر الأساسي للبيانات هو الـ Storage
 * وبعد أي تعديل نرجع نقرأ منه ونعكسه على Vue
 */
function syncGraph() {
  // 📦 جلب كل البيانات من التخزين
  const graph = getGraph();
  // 🧩 تحديث العقد
  nodes.value = graph.node;
  // 🔗 تحديث الروابط
  edges.value = graph.edges;
}
/**
 * 🔗 addEdge()
 * 🎯 وظيفتها: إنشاء رابط بين عقدتين
 * 🧠 params بتيجي من VueFlow event (@connect)
 */
function addEdge(params) {
  edges.value.push({
    ...params, // 📥 بيانات المصدر والهدف
    id: nanoid(), // 🆔 إنشاء ID فريد للرابط
  });
}
```

![This is an image](automation\Create_Local_Storage.png)

### ✍️ UPDATE

```html
<template>
  <main class="h-screen p-4 grid grid-cols-12 gap-4">
    <aside class="col-span-3 border rounded p-4 overflow-auto space-y-6">
      <h2 class="aside_title m-auto text-3xl">Controls</h2>
      <div class="wrapper_control">
        <div class="wrapper_control_node">
          <button type="button" @click="addNode">➕ Add Node</button>
          <button type="button" @click="updateFirstNode">
            Update First Node Label
          </button>
        </div>
        <div class="wrapper_control_node_data">
          <div v-if="selectedNode" class="node_data">
            <h3>Node Settings ⚙️</h3>
            <div class="node_update_data">
              <input v-model="selectedNode.data.label" />
              <button type="button" @click="updateNodeById(selectedNode.id)">
                Update Node
              </button>
            </div>
          </div>
          <div v-if="selectedEdge" class="edge_data">
            <h3>Edge Settings 🔗</h3>
            <p>From: {{ selectedEdge.source }}</p>
            <p>To: {{ selectedEdge.target }}</p>
          </div>
        </div>
      </div>
    </aside>
    <section class="col-span-9 border rounded">
      <div class="VueFlow_Component_Name">
        <!-- eslint-disable vue/no-v-model-argument -->
        <VueFlow
          v-model:nodes="nodes"
          v-model:edges="edges"
          :default-zoom="1.5"
          :min-zoom="0.2"
          :max-zoom="5"
          @node-click="getSingleNode"
          @edge-click="getSingleEdge"
          @connect="addEdge"
          @selection-change="onSelectionChange"
          :class="{ layouting: isLayouting }"
          :snap-to-grid="true"
          :snap-grid="[20, 20]"
        >
          <Background pattern-color="#aaa" :gap="8" />
          <MiniMap />
          <Controls />
          <Panel
            position="top-right"
            style="display:flex; gap:5px;"
            class="wrapper_control_panel"
          >
            <button @click="zoomIn()">+</button>
            <button @click="zoomOut()">-</button>
            <button @click="fitView()">Fit</button>
          </Panel>
        </VueFlow>
      </div>
    </section>
  </main>
</template>
```

```js
<script setup>
// ==================================================
// 📦 1️⃣ Imports (المكتبات المستخدمة)
// ==================================================
// 🧠 Vue Composition API
import { ref, onMounted, watch } from 'vue'
// 🔗 VueFlow (المكتبة الأساسية للرسم والـ Drag & Drop)
import { VueFlow } from "@vue-flow/core"
// 🎨 خلفية الشبكة (Grid Background)
import { Background } from '@vue-flow/background'
// 🗺️ MiniMap (خريطة مصغرة للمخطط)
import { MiniMap } from '@vue-flow/minimap'
// 🎛️ Controls (Zoom / Fit / Lock)
import { Controls } from '@vue-flow/controls'
// 📦 Panel (لو عايز تضيف أزرار مخصصة داخل VueFlow)
import { Panel } from '@vue-flow/core'
// 🆔 إنشاء ID فريد لكل Node أو Edge
import { nanoid } from 'nanoid'
// ⏳ Debounce (يمنع الحفظ كل مرة يحصل تغيير سريع)
import debounce from 'lodash/debounce'
// 💾 Service مسؤول عن التخزين في LocalStorage
import {
  getGraph,
  getOne,
  getEdge,
  createNode,
  updateNode,
  saveGraph
} from "@/services/nodeStorageService"
// ==================================================
// 📍 2️⃣ State (البيانات التفاعلية)
// ==================================================
// 📦 كل الـ Nodes الموجودة في الرسم
const nodes = ref([])
// 🔗 كل الـ Edges (الروابط بين الـ Nodes)
const edges = ref([])
// 📌 Selection
const selectedNode = ref(null)
const selectedEdge = ref([])

// ==================================================
// 🚀 3️⃣ Lifecycle (تشغيل أول ما الصفحة تفتح)
// ==================================================
// 👂 لما الكمبوننت يتركب
onMounted(initGraph)
// 🔄 تهيئة الجراف
function initGraph() {
  loadGraph()
}
// ==================================================
// 📖 4️⃣ LOAD GRAPH (تحميل البيانات)
// ==================================================
function loadGraph() {
  // 📥 نقرأ البيانات من LocalStorage
  const graph = getGraph()
  // 🧠 لو فيه بيانات محفوظة
  if (graph.nodes.length) {
    nodes.value = graph.nodes
    edges.value = graph.edges
  } else {
    // 🆕 لو مفيش بيانات → ننشئ جراف افتراضي
    createDefaultGraph()
  }
}
// ==================================================
// 🆕 5️⃣ Create Default Graph (أول تشغيل)
// ==================================================
function createDefaultGraph() {
  // 🆔 إنشاء ID فريد
  const startId = nanoid()
  const endId = nanoid()
  // 📦 إنشاء Nodes
  nodes.value = [
    {
      id: startId,
      position: { x: 100, y: 80 },
      data: { label: "Start 🚀" }
    },
    {
      id: endId,
      position: { x: 300, y: 200 },
      data: { label: "End 🏁" }
    }
  ]
  // 🔗 ربط Start → End
  edges.value = [
    {
      id: nanoid(),
      source: startId,
      target: endId
    }
  ]
}
/* ==================================================
🔍 4️⃣ READ
================================================== */

/**
 * 🧩 getSingleNode(e)
 * 🎯 وظيفتها: جلب Node واحدة من التخزين عند الضغط عليها
 * 🧠 الفكرة:
 * VueFlow بيبعت لنا Event فيه بيانات العقدة
 * لكن إحنا بنرجع نجيبها من Storage علشان يكون المصدر واحد (Source of Truth)
 */
function getSingleNode(e) {

  // 🆔 استخراج الـ ID من الحدث
  const nodeId = e.node.id

  // 📦 جلب العقدة من التخزين باستخدام Service
  const node = getOne(nodeId)

  // 🎯 تخزين العقدة المختارة لعرضها في الـ Side Panel
  selectedNode.value = node

  // ❌ إلغاء تحديد أي Edge
  selectedEdge.value = null

  // 🖥️ طباعة في الكونسول للتأكد
  console.log("📦 Node From Storage:", node)
}



/**
 * 🔗 getSingleEdge(e)
 * 🎯 وظيفتها: جلب Edge واحدة عند الضغط عليها
 * 🧠 نفس الفكرة بالظبط لكن مع الروابط
 */
function getSingleEdge(e) {

  // 🆔 استخراج ID الرابط
  const edgeId = e.edge.id

  // 📦 جلب الرابط من التخزين
  const edge = getEdge(edgeId)

  // 🎯 تخزين الرابط المختار
  selectedEdge.value = edge

  // ❌ إلغاء تحديد أي Node
  selectedNode.value = null

  // 🖥️ طباعة للتأكد
  console.log("🔗 Edge From Storage:", edge)
}

/* ==================================================
➕ 3️⃣ CREATE
================================================== */

/**
 * ➕ addNode()
 * 🎯 وظيفتها: إنشاء Node جديدة داخل النظام
 * 🧠 الفكرة:
 * 1- ننشئ كائن يمثل العقدة
 * 2- نحفظه في الـ Storage
 * 3- نعمل Sync مع Vue علشان يحصل Re-render
 */
function addNode() {
  // 🆔 إنشاء ID فريد لكل Node
  const newNode = {
    id: nanoid(), // 🔑 ID فريد باستخدام مكتبة nanoid
    position: { x: 100, y: 220 }, // 📍 مكان الظهور على الشاشة
    data: { label: "Dynamic Node 🚀" } // 🏷️ البيانات الخاصة بالعقدة
  }
  // 💾 حفظ العقدة داخل Storage Service
  createNode(newNode)
  // 🔄 تحديث حالة Vue بالبيانات الجديدة
  syncGraph()
}
/**
 * 🔄 syncGraph()
 * 🎯 وظيفتها: مزامنة البيانات بين Storage و Vue State
 * 🧠 ليه بنعملها؟
 * لأننا بنخلي المصدر الأساسي للبيانات هو الـ Storage
 * وبعد أي تعديل نرجع نقرأ منه ونعكسه على Vue
 */
function syncGraph() {
  // 📦 جلب كل البيانات من التخزين
  const graph = getGraph()
  // 🧩 تحديث العقد
  nodes.value = graph.nodes
  // 🔗 تحديث الروابط
  edges.value = graph.edges
}
/**
 * 🔗 addEdge()
 * 🎯 وظيفتها: إنشاء رابط بين عقدتين
 * 🧠 params بتيجي من VueFlow event (@connect)
 */
function addEdge(params) {
  edges.value.push({
    ...params,       // 📥 بيانات المصدر والهدف
    id: nanoid()     // 🆔 إنشاء ID فريد للرابط
  })
}

/* ==================================================
✏️ 5️⃣ UPDATE
================================================== */

/*
🎯 updateFirstNode()
📌 الهدف: تحديث أول Node موجود في الجراف
*/
function updateFirstNode() {
  if (!nodes.value.length) return // 🚫 لو مفيش Nodes اخرج

  updateNode(nodes.value[0].id, {   // 🆔 نجيب أول Node
    data: { label: "Updated ✨" }   // ✨ نعدل البيانات
  })

  syncGraph() // 🔄 نعمل مزامنة مع Vue State
}


/*
🎯 updateNodeById(id)
📌 الهدف: تحديث Node معين باستخدام الـ id
🆔 id → هو المعرف الفريد للـ Node
*/
function updateNodeById(id) {

  if (!id) return // 🚫 تأكد إن في id

  updateNode(id, {                  // 🆔 نستخدم الـ id مباشرة
    data: {
      label: selectedNode.value.data.label // ✍️ ناخد القيمة من input
    }
  })

  syncGraph() // 🔄 تحديث الحالة بعد التعديل
}

// ==================================================
// 💾 6️⃣ Auto Save (حفظ تلقائي)
// ==================================================
// ⏳ Debounce: يمنع الحفظ كل جزء من الثانية
// بدل ما يحفظ كل حركة Drag
const debouncedSave = debounce(() => {
  // 💾 احفظ الجراف بالكامل
  saveGraph(nodes.value, edges.value)
}, 500) // بعد 500ms من آخر تغيير
// 👀 مراقبة أي تغيير في nodes أو edges
watch(
  [nodes, edges],     // 👈 نراقب الاتنين
  debouncedSave,      // 👈 لما يحصل تغيير ننفذ الحفظ
  { deep: true }      // 👈 نراقب التغييرات الداخلية
)
</script>
```

![This is an image](automation\Update_Node.png)

### 🗑️ Delete

```html
<button type="button" @click="clearStorage">🧹 clear Storage</button>
<div v-if="selectedNode" class="node_data">
  <h3>Node Settings ⚙️</h3>
  <div class="node_update_data">
    <input v-model="selectedNode.data.label" />
    <button type="button" @click="updateNodeById(selectedNode.id)">
      Update Node
    </button>
    <button type="button" @click="removeNodeById(selectedNode.id)">
      DELETE Node By Id
    </button>
  </div>
</div>
<div v-if="selectedEdge" class="edge_data">
  <h3>Edge Settings 🔗</h3>
  <button type="button" @click="removeEdgeById(selectedEdge.id)">
    DELETE Node By Id
  </button>
  <p>From: {{ selectedEdge.source }}</p>
  <p>To: {{ selectedEdge.target }}</p>
</div>
```

```js
// 💾 Service مسؤول عن التخزين في LocalStorage
import {
  getGraph,
  getOne,
  getEdge,
  createNode,
  updateNode,
  removeNode,
  removeEdge,
  saveGraph,
} from "@/services/nodeStorageService";
```

```js
/* ===================================================
🗑 6️⃣ DELETE
=================================================== */

/*
🎯 removeNodeById(id)
🧩 الهدف: حذف Node من التخزين + تحديث الجراف
*/
function removeNodeById(id) {
  if (!id) return; // 🚫 تأكد إن فيه ID

  removeNode(id); // 💾 حذف من Storage (Service Layer)
  syncGraph(); // 🔄 تحديث Vue State بعد الحذف
}

/*
🎯 removeEdgeById(id)
🔗 الهدف: حذف Edge من التخزين + تحديث الجراف
*/
function removeEdgeById(id) {
  if (!id) return; // 🚫 حماية من الأخطاء

  removeEdge(id); // 💾 حذف من Storage
  syncGraph(); // 🔄 تحديث Vue State
}

/*
🎯 clearStorage()
🧹 الهدف: مسح كل الجراف نهائيًا من LocalStorage
⚠️ يستخدم في Reset أو Debug
*/
function clearStorage() {
  localStorage.removeItem("vueflow_graph"); // 🗂 حذف البيانات المخزنة

  nodes.value = []; // 🧩 تفريغ الـ Nodes
  edges.value = []; // 🔗 تفريغ الـ Edges
}
```

![This is an image](automation\Delete_Node.png)

### 📐 AUTO LAYOUT

```html
<div class="wrapper_control_node_layout_buttons layout-buttons">
  <h4 class="aside_subtitle  text-2xl">📐 Auto Layout Node</h4>
  <div class="inner_control_node_layout_buttons">
    <button @click="autoLayout('LR')">LR 📐</button>
    <button @click="autoLayout('RL')">RL 📐</button>
    <button @click="autoLayout('TB')">TB 📐</button>
    <button @click="autoLayout('BT')">BT 📐</button>
  </div>
</div>
```

```js
// Contract arrangement automatically
import dagre from "dagre";
```

```js
// 📌 Layout Flag
const isLayouting = ref(false);
```

```js
/* ===================================================
📐 7️⃣ AUTO LAYOUT (Dagre)
=================================================== */

/*
🎯 autoLayout(dir)
📐 الهدف: ترتيب الـ Nodes تلقائيًا باستخدام Dagre
🧭 dir:
   'TB' = Top ➝ Bottom ⬇️
   'LR' = Left ➝ Right ➡️
*/
function autoLayout(dir = "TB") {
  // 🚦 تفعيل حالة الـ Layout (لإضافة Animation مثلاً)
  isLayouting.value = true;

  // 🧠 إنشاء جراف جديد في Dagre
  const g = new dagre.graphlib.Graph();

  // ⚙️ إعدادات الجراف
  g.setGraph({
    rankdir: dir, // 🧭 اتجاه الترتيب
    nodesep: 50, // ↔️ مسافة بين الـ Nodes أفقيًا
    ranksep: 80, // ↕️ مسافة بين الصفوف
  });

  // 🔗 إعداد افتراضي للـ Edges
  g.setDefaultEdgeLabel(() => ({}));

  // 🧩 إضافة الـ Nodes إلى Dagre مع أبعاد ثابتة
  nodes.value.forEach((node) => {
    g.setNode(node.id, {
      width: 180, // 📏 عرض العقدة
      height: 60, // 📐 ارتفاع العقدة
    });
  });

  // 🔗 إضافة الـ Edges إلى Dagre
  edges.value.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  // 🚀 تشغيل خوارزمية الترتيب
  dagre.layout(g);

  // 🔄 تحديث مواقع الـ Nodes في VueFlow
  nodes.value = nodes.value.map((node) => {
    const pos = g.node(node.id); // 📍 الموقع الجديد من Dagre

    return {
      ...node,
      position: {
        x: pos.x - 90, // 🧮 تصحيح المنتصف (width / 2)
        y: pos.y - 30, // 🧮 تصحيح المنتصف (height / 2)
      },
    };
  });

  // ⏳ إنهاء حالة الـ Layout بعد الأنيميشن
  setTimeout(() => {
    isLayouting.value = false;
  }, 400);
}
```

![This is an image](automation\Auto_Layout_Node.png)

### 🚫 Isolated

```html
<button type="button" @click="findIsolatedNodes">find Isolated Nodes</button>
```

```js
/*
🔎 findIsolatedNodes()
🎯 اكتشاف العقد المعزولة
*/
function findIsolatedNodes() {
  const connected = new Set();

  // 🧠 تجميع كل النود المتوصلة
  edges.value.forEach((e) => {
    connected.add(e.source);
    connected.add(e.target);
  });

  // 🎯 تحديد المعزولين فقط
  const isolatedIds = nodes.value
    .filter((n) => !connected.has(n.id))
    .map((n) => n.id);

  // 🚨 إضافة الكلاس
  nodes.value = nodes.value.map((n) => ({
    ...n,
    class: isolatedIds.includes(n.id) ? "isolated-node" : "",
  }));

  // ⏳ بعد مدة → إزالة الكلاس تلقائيًا
  setTimeout(() => {
    nodes.value = nodes.value.map((n) => ({
      ...n,
      class: "",
    }));
  }, 2000); // 👈 المدة 2 ثانية (غيرها براحتك)
}
```

```css
.isolated-node {
  border: 2px solid red !important;
  box-shadow: 0 0 20px red !important;
  animation: pulse-shadow 0.8s ease-in-out infinite alternate;
}

@keyframes pulse-shadow {
  from {
    box-shadow: 0 0 5px red;
  }
  to {
    box-shadow: 0 0 25px red;
  }
}
```

![This is an image](automation\findIsolatedNodes.png)
