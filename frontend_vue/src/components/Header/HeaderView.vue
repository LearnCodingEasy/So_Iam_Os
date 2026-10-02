<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

import Avatar from 'primevue/avatar'
import Badge from 'primevue/badge'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Divider from 'primevue/divider'
import InputText from 'primevue/inputtext'
import Menu from 'primevue/menu'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const sidebarOpen = ref(true)
const mobileMenuOpen = ref(false)
const profileMenu = ref(null)
const searchQuery = ref('')

const menuItems = [
  { label: 'Dashboard', icon: 'pi pi-home', route: '/dashboard/' },
  { label: 'Projects', icon: 'pi pi-folder', route: '/projects', unavailable: true },
  { label: 'Tasks', icon: 'pi pi-check-square', route: '/tasks' },
  { label: "Today's Tasks", icon: 'pi pi-calendar', route: '/tasks/today' },
  { label: 'Goals', icon: 'pi pi-bullseye', route: '/goals' },
  { label: 'Progress', icon: 'pi pi-chart-line', route: '/progress' },
  { label: 'Learning', icon: 'pi pi-book', route: '/learning' },
  { label: 'Knowledge', icon: 'pi pi-database', route: '/knowledge' },
  { label: 'Memory', icon: 'pi pi-history', route: '/memory', unavailable: true },
  { label: 'Social', icon: 'pi pi-users', route: '/social' },
  { label: 'Jobs', icon: 'pi pi-briefcase', route: '/jobs' },
  { label: 'AI Assistant', icon: 'pi pi-sparkles', route: '/ai' },
  { label: 'Codex', icon: 'pi pi-code', route: '/codex' },
  { label: 'automation', icon: 'pi pi-code', route: '/automation_Dashboard' },
  { label: 'Notifications', icon: 'pi pi-bell', route: '/notifications' },
]

const secondaryItems = [
  { label: 'Settings', icon: 'pi pi-cog', route: '/settings' },
  { label: 'Profile', icon: 'pi pi-user', route: userProfileRoute },
  { label: 'About', icon: 'pi pi-info-circle', route: '/About' },
]

const userName = computed(() => {
  return userStore.fullName || userStore.user?.full_name || userStore.user?.email || 'User'
})

const userEmail = computed(() => userStore.user?.email || '')

const userInitials = computed(() => {
  const name = userName.value.trim()
  if (!name) return 'U'

  return name
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join('')
})

const avatarUrl = computed(() => userStore.user?.avatar_url || null)

const currentRouteLabel = computed(() => {
  const item = [...menuItems, ...secondaryItems].find((entry) => {
    if (typeof entry.route !== 'string') return false
    return route.path === entry.route || route.path.startsWith(`${entry.route}/`)
  })

  return item?.label || 'So Iam OS'
})

const profileRoute = computed(() => {
  const id = userStore.user?.id
  return id ? `/profile/${id}` : '/settings'
})

const profileMenuItems = computed(() => [
  {
    label: 'Profile',
    icon: 'pi pi-user',
    command: () => router.push(profileRoute.value),
  },
  {
    label: 'Settings',
    icon: 'pi pi-cog',
    command: () => router.push('/settings'),
  },
  { separator: true },
  {
    label: 'Logout',
    icon: 'pi pi-sign-out',
    command: logout,
  },
])

function userProfileRoute() {
  return profileRoute.value
}

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

function closeSidebarOnMobile() {
  if (window.innerWidth <= 900) {
    sidebarOpen.value = false
    mobileMenuOpen.value = false
  }
}

function toggleProfileMenu(event) {
  profileMenu.value?.toggle(event)
}

function submitSearch() {
  const query = searchQuery.value.trim()
  if (!query) return

  router.push({
    path: '/codex',
    query: { q: query },
  })
}

function logout() {
  return userStore.logout().finally(() => {
    router.push('/login')
  })
}

function handleKeydown(event) {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault()
    document.querySelector('#global-header-search')?.focus()
  }
}

onMounted(() => window.addEventListener('keydown', handleKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', handleKeydown))
</script>

<template>
  <div class="header-layout" :class="{ 'sidebar-collapsed': !sidebarOpen }">
    <div
      v-if="sidebarOpen && mobileMenuOpen"
      class="sidebar-overlay"
      @click="mobileMenuOpen = false"
    />

    <aside class="app-sidebar" :class="{ collapsed: !sidebarOpen, 'mobile-open': mobileMenuOpen }">
      <div class="brand-row">
        <RouterLink to="/" class="brand-link" @click="closeSidebarOnMobile">
          <div class="brand-logo">
            <i class="pi pi-sparkles" />
          </div>
          <div v-if="sidebarOpen" class="brand-copy">
            <strong>So Iam OS</strong>
            <span>Your Personal AI OS</span>
          </div>
        </RouterLink>

        <Button
          v-if="sidebarOpen"
          text
          rounded
          severity="secondary"
          icon="pi pi-angle-left"
          aria-label="Collapse sidebar"
          class="sidebar-toggle"
          @click="toggleSidebar"
        />
      </div>

      <div v-if="!sidebarOpen" class="collapsed-toggle">
        <Button
          text
          rounded
          severity="secondary"
          icon="pi pi-angle-right"
          aria-label="Expand sidebar"
          @click="toggleSidebar"
        />
      </div>

      <Divider />

      <nav class="main-navigation" aria-label="Main navigation">
        <div v-if="sidebarOpen" class="nav-section-title">MAIN NAVIGATION</div>

        <template v-for="item in menuItems" :key="item.label">
          <RouterLink
            v-if="!item.unavailable"
            :to="item.route"
            class="nav-item"
            :class="{
              active: route.path === item.route || route.path.startsWith(`${item.route}/`),
            }"
            @click="closeSidebarOnMobile"
          >
            <i :class="item.icon" class="nav-icon" />
            <span v-if="sidebarOpen" class="nav-label">{{ item.label }}</span>
          </RouterLink>

          <div
            v-else
            class="nav-item nav-item-disabled"
            :title="`${item.label} route is not registered yet`"
          >
            <i :class="item.icon" class="nav-icon" />
            <span v-if="sidebarOpen" class="nav-label">{{ item.label }}</span>
            <Badge v-if="sidebarOpen" value="Soon" severity="secondary" />
          </div>
        </template>

        <Divider v-if="sidebarOpen" />

        <div v-if="sidebarOpen" class="nav-section-title">SYSTEM</div>

        <RouterLink
          v-for="item in secondaryItems"
          :key="item.label"
          :to="typeof item.route === 'function' ? item.route() : item.route"
          class="nav-item"
          :class="{ active: currentRouteLabel === item.label }"
          @click="closeSidebarOnMobile"
        >
          <i :class="item.icon" class="nav-icon" />
          <span v-if="sidebarOpen" class="nav-label">{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <Card class="status-card">
          <template #content>
            <div class="status-content">
              <span class="status-dot" />
              <div v-if="sidebarOpen">
                <strong>System Online</strong>
                <span>All services operational</span>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </aside>

    <section class="app-shell">
      <header class="top-header">
        <div class="top-header-left">
          <Button
            text
            rounded
            icon="pi pi-bars"
            aria-label="Open navigation"
            class="mobile-menu-button"
            @click="mobileMenuOpen = !mobileMenuOpen"
          />

          <div class="breadcrumb-area">
            <span class="breadcrumb-home"><i class="pi pi-home" /></span>
            <i class="pi pi-angle-right breadcrumb-separator" />
            <strong>{{ currentRouteLabel }}</strong>
          </div>
        </div>

        <div class="global-search">
          <i class="pi pi-search" />
          <InputText
            id="global-header-search"
            v-model="searchQuery"
            placeholder="Search Codex, files, features, APIs..."
            @keyup.enter="submitSearch"
          />
          <kbd>Ctrl K</kbd>
        </div>

        <div class="top-header-actions">
          <RouterLink to="/notifications" class="header-action-link" aria-label="Notifications">
            <i class="pi pi-bell" />
            <Badge value="" severity="danger" class="notification-dot" />
          </RouterLink>

          <ThemeSwitcher />

          <Button text class="user-trigger" @click="toggleProfileMenu">
            <Avatar v-if="avatarUrl" :image="avatarUrl" shape="circle" size="normal" />
            <Avatar v-else :label="userInitials" shape="circle" size="normal" />
            <span class="user-summary">
              <strong>{{ userName }}</strong>
              <small>{{ userEmail }}</small>
            </span>
            <i class="pi pi-angle-down" />
          </Button>
          <Menu ref="profileMenu" :model="profileMenuItems" popup />
        </div>
      </header>

      <div class="page-context-bar">
        <div>
          <span>SO_IAM_OS</span>
          <strong>{{ currentRouteLabel }}</strong>
        </div>
        <RouterLink v-if="route.path !== '/codex'" to="/codex" class="codex-shortcut">
          <i class="pi pi-code" />
          Open Codex
        </RouterLink>
      </div>

      <main class="page-content">
        <slot />
      </main>
    </section>
  </div>
</template>

<style scoped lang="scss">
.header-layout {
  --sidebar-width: 280px;
  --sidebar-collapsed-width: 76px;
  --header-height: 72px;
  min-height: 100vh;
  display: flex;
  background: var(--surface-ground, #f8fafc);
  color: var(--text-color, #0f172a);
}

.app-sidebar {
  width: var(--sidebar-width);
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 1100;
  display: flex;
  flex-direction: column;
  padding: 16px;
  background: var(--surface-card, #ffffff);
  border-right: 1px solid var(--surface-border, #e2e8f0);
  transition:
    width 0.2s ease,
    transform 0.2s ease;
  overflow: hidden;
}

.app-sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
  padding-inline: 10px;
}

.brand-row {
  min-height: 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
  color: inherit;
  text-decoration: none;
  min-width: 0;
}

.brand-logo {
  width: 40px;
  height: 40px;
  flex: 0 0 40px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: white;
  font-size: 18px;
}

.brand-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.brand-copy strong {
  font-size: 15px;
}

.brand-copy span {
  color: var(--text-color-secondary, #64748b);
  font-size: 10px;
  white-space: nowrap;
}

.collapsed-toggle {
  display: flex;
  justify-content: center;
  padding-top: 4px;
}

.main-navigation {
  flex: 1;
  overflow-y: auto;
  padding-top: 4px;
}

.nav-section-title {
  margin: 12px 8px 8px;
  color: var(--text-color-secondary, #64748b);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.09em;
}

.nav-item {
  min-height: 42px;
  margin: 3px 0;
  padding: 0 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-radius: 10px;
  color: var(--text-color, #334155);
  text-decoration: none;
  transition:
    background 0.15s ease,
    color 0.15s ease;
}

.nav-item:hover,
.nav-item.active {
  background: color-mix(in srgb, var(--primary-color, #3b82f6) 10%, transparent);
  color: var(--primary-color, #2563eb);
}

.nav-item-disabled {
  color: var(--text-color-secondary, #94a3b8);
  cursor: not-allowed;
}

.nav-icon {
  width: 20px;
  text-align: center;
  flex: 0 0 20px;
}

.nav-label {
  flex: 1;
  font-size: 13px;
  font-weight: 500;
}

.sidebar-footer {
  padding-top: 10px;
}

.status-card :deep(.p-card-body),
.status-card :deep(.p-card-content) {
  padding: 10px;
}

.status-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22c55e;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12);
}

.status-content div {
  display: flex;
  flex-direction: column;
}

.status-content strong {
  font-size: 11px;
}

.status-content span {
  font-size: 9px;
  color: var(--text-color-secondary, #64748b);
}

.app-shell {
  width: calc(100% - var(--sidebar-width));
  margin-left: var(--sidebar-width);
  min-width: 0;
  transition:
    width 0.2s ease,
    margin-left 0.2s ease;
}

.sidebar-collapsed .app-shell {
  width: calc(100% - var(--sidebar-collapsed-width));
  margin-left: var(--sidebar-collapsed-width);
}

.top-header {
  min-height: var(--header-height);
  position: sticky;
  top: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 10px 22px;
  background: color-mix(in srgb, var(--surface-card, #fff) 92%, transparent);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--surface-border, #e2e8f0);
}

.top-header-left {
  display: flex;
  align-items: center;
  flex: 0 0 auto;
}

.mobile-menu-button {
  display: none;
}

.breadcrumb-area {
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  font-size: 13px;
}

.breadcrumb-home {
  color: var(--text-color-secondary, #64748b);
}

.breadcrumb-separator {
  color: var(--text-color-secondary, #94a3b8);
  font-size: 10px;
}

.global-search {
  position: relative;
  max-width: 600px;
  flex: 1;
  margin: 0 auto;
}

.global-search > i {
  position: absolute;
  z-index: 2;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-color-secondary, #64748b);
}

.global-search :deep(.p-inputtext) {
  width: 100%;
  padding-left: 40px;
  padding-right: 70px;
  border-radius: 10px;
  background: var(--surface-ground, #f8fafc);
}

.global-search kbd {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  padding: 3px 6px;
  border: 1px solid var(--surface-border, #e2e8f0);
  border-radius: 5px;
  color: var(--text-color-secondary, #64748b);
  font-size: 10px;
}

.top-header-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.header-action-link {
  width: 38px;
  height: 38px;
  position: relative;
  display: grid;
  place-items: center;
  color: inherit;
  border-radius: 50%;
  text-decoration: none;
}

.header-action-link:hover {
  background: var(--surface-hover, #f1f5f9);
}

.notification-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 7px;
  min-width: 7px;
  height: 7px;
  padding: 0;
}

.user-trigger {
  display: flex !important;
  align-items: center;
  gap: 8px;
  color: inherit !important;
}

.user-summary {
  display: flex;
  flex-direction: column;
  text-align: left;
  line-height: 1.2;
}

.user-summary strong {
  font-size: 12px;
}

.user-summary small {
  color: var(--text-color-secondary, #64748b);
  font-size: 9px;
}

.page-context-bar {
  min-height: 48px;
  padding: 10px 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--surface-border, #e2e8f0);
  background: var(--surface-card, #fff);
}

.page-context-bar > div {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-context-bar span {
  color: var(--text-color-secondary, #64748b);
  font-size: 11px;
}

.page-context-bar strong {
  font-size: 13px;
}

.codex-shortcut {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--primary-color, #2563eb);
  text-decoration: none;
  font-size: 12px;
  font-weight: 600;
}

.page-content {
  min-height: calc(100vh - var(--header-height));
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  z-index: 1090;
  background: rgba(15, 23, 42, 0.45);
}

@media (max-width: 1100px) {
  .user-summary,
  .user-trigger > i {
    display: none;
  }
}

@media (max-width: 900px) {
  .app-sidebar {
    transform: translateX(-100%);
    width: min(280px, 86vw);
  }

  .app-sidebar.mobile-open {
    transform: translateX(0);
  }

  .app-sidebar.collapsed {
    width: min(280px, 86vw);
  }

  .app-shell,
  .sidebar-collapsed .app-shell {
    width: 100%;
    margin-left: 0;
  }

  .mobile-menu-button {
    display: inline-flex;
  }

  .breadcrumb-area {
    display: none;
  }

  .top-header {
    padding: 8px 12px;
    gap: 8px;
  }

  .global-search {
    min-width: 0;
  }

  .global-search kbd {
    display: none;
  }

  .top-header-actions .user-trigger {
    padding-inline: 4px;
  }
}

@media (max-width: 640px) {
  .global-search {
    display: none;
  }

  .top-header {
    justify-content: space-between;
  }

  .page-context-bar {
    padding-inline: 14px;
  }

  .page-context-bar > div {
    gap: 6px;
  }

  .page-context-bar span {
    display: none;
  }
}
</style>
