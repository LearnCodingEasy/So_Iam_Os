/**
 * src/services/mcpService.js
 *
 * API client for the MCP Server dashboard endpoints.
 * These are REST management endpoints (not the MCP protocol itself).
 */

import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true,
})

// ── Sessions ──────────────────────────────────────────────

export const mcpService = {
  /** GET /api/mcp/sessions/ — all active sessions + tool stats */
  async getSessions() {
    const { data } = await api.get('/api/mcp/sessions/')
    return data
  },

  /** GET /api/mcp/tools/ — all tools with enable state */
  async getTools() {
    const { data } = await api.get('/api/mcp/tools/')
    return data
  },

  /** POST /api/mcp/tools/{name}/ — toggle tool enabled/disabled */
  async setToolEnabled(toolName, enabled) {
    const { data } = await api.post(`/api/mcp/tools/${toolName}/`, { enabled })
    return data
  },

  /** POST /api/mcp/token/ — generate new API token */
  async createToken(name = 'API Token', expiresDays = 30) {
    const { data } = await api.post('/api/mcp/token/', {
      name,
      expires_days: expiresDays,
    })
    return data
  },

  /** DELETE /api/mcp/token/ — revoke a token */
  async revokeToken(token) {
    const { data } = await api.delete('/api/mcp/token/', { data: { token } })
    return data
  },

  /** GET /api/mcp/logs/ — recent tool call logs */
  async getLogs(limit = 50) {
    const { data } = await api.get('/api/mcp/logs/', { params: { limit } })
    return data
  },
}

export default mcpService
