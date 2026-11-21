// frontend_vue\src\services\nodeStorageService.js
// 🔑 مفتاح التخزين
const STORAGE_KEY = 'vueflow_graph'

/* =================================================
🧠 PRIVATE HELPERS
================================================= */

// 📖 READ ALL
function read() {
  const raw = localStorage.getItem(STORAGE_KEY)

  if (!raw) return { nodes: [], edges: [] }

  try {
    const parsed = JSON.parse(raw)
    return {
      nodes: Array.isArray(parsed.nodes) ? parsed.nodes : [],
      edges: Array.isArray(parsed.edges) ? parsed.edges : [],
    }
  } catch {
    return { nodes: [], edges: [] }
  }
}

// 💾 WRITE
function write(graph) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(graph))
}

/* =================================================
🚀 PUBLIC CRUD API
================================================= */

// 📚 READ ALL
export function getGraph() {
  return read()
}

// 🔍 READ ONE (Node)
export function getOne(id) {
  const graph = read()
  return graph.nodes.find((n) => n.id === id)
}

export function getEdge(id) {
  const graph = read()
  return graph.edges.find((e) => e.id === id)
}
// ➕ CREATE
export function createNode(node) {
  const graph = read()
  graph.nodes.push(node)
  write(graph)
}

// ✏️ UPDATE
export function updateNode(id, newData) {
  const graph = read()
  const index = graph.nodes.findIndex((n) => n.id === id)
  if (index === -1) return
  graph.nodes[index] = {
    ...graph.nodes[index],
    ...newData,
  }

  write(graph)
}

// 🗑 DELETE
export function removeNode(id) {
  const graph = read()
  graph.nodes = graph.nodes.filter((n) => n.id !== id)
  // 🔗 حذف أي Edge مرتبط
  graph.edges = graph.edges.filter((e) => e.source !== id && e.target !== id)
  write(graph)
}
export function removeEdge(id) {
  const graph = read()
  graph.edges = graph.edges.filter((n) => n.id !== id)
  write(graph)
}

// 💾 SAVE ALL (لما نستخدم Drag)
export function saveGraph(nodes, edges) {
  write({ nodes, edges })
}
