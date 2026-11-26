/**
 * Deprecated compatibility shim.
 *
 * All application HTTP requests must use the canonical JWT-authenticated
 * client in `./api.js` (`user.access` / `user.refresh` with token rotation).
 */
export { default, getValidAccessToken } from './api'
