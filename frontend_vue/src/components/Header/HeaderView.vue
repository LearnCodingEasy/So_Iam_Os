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

  { label: 'Projects', icon: 'pi pi-folder', route: '/projects' },

  { label: 'Tasks', icon: 'pi pi-check-square', route: '/tasks' },

  { label: "Today's Tasks", icon: 'pi pi-calendar-check', route: '/tasks/today' },

  { label: 'Goals', icon: 'pi pi-bullseye', route: '/goals' },

  { label: 'Progress', icon: 'pi pi-chart-line', route: '/progress' },

  { label: 'Learning', icon: 'pi pi-book', route: '/learning' },

  { label: 'Knowledge', icon: 'pi pi-database', route: '/knowledge' },

  { label: 'Memory', icon: 'pi pi-history', route: '/memory' },

  { label: 'Memory', icon: 'pi pi-history', route: '/memory', unavailable: true },

  { label: 'Social', icon: 'pi pi-users', route: '/social' },

  { label: 'Jobs', icon: 'pi pi-briefcase', route: '/jobs' },
  { label: 'Scraper', icon: 'pi pi-briefcase', route: '/scraper' },

  { label: 'AI Assistant', icon: 'pi pi-sparkles', route: '/ai' },

  { label: 'Codex', icon: 'pi pi-code', route: '/codex' },

  { label: 'Automation', icon: 'pi pi-cog', route: '/automation' },

  { label: 'Challenges', icon: 'pi pi-bolt', route: '/challenges' },

  { label: 'Finance', icon: 'pi pi-wallet', route: '/finance' },

  { label: 'Memory', icon: 'pi pi-history', route: '/memory' },

  { label: 'AI Agents', icon: 'pi pi-users', route: '/ai/agents' },

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
  <div class="header_layout" :class="{ 'sidebar-collapsed': !sidebarOpen }">
    <div
      v-if="sidebarOpen && mobileMenuOpen"
      class="sidebar_overlay"
      @click="mobileMenuOpen = false"
    />

    <aside class="app_sidebar" :class="{ collapsed: !sidebarOpen, 'mobile-open': mobileMenuOpen }">
      <div class="brand_row">
        <RouterLink to="/" class="brand_link" @click="closeSidebarOnMobile">
          <div class="brand_logo">
            <i class="pi pi-sparkles" />
          </div>
          <div v-if="sidebarOpen" class="brand_copy">
            <strong>So Iam OS</strong>
            <span>Your Personal AI OS</span>
          </div>
        </RouterLink>

        <prime_button
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

      <div v-if="!sidebarOpen" class="collapsed_toggle">
        <prime_button
          text
          rounded
          icon="pi pi-angle-right"
          severity="secondary"
          aria-label="Expand sidebar"
          @click="toggleSidebar"
          class="class_name"
        />
      </div>

      <Divider />

      <nav class="main_navigation" aria-label="Main navigation">
        <div v-if="sidebarOpen" class="nav_section_title">MAIN NAVIGATION</div>

        <template v-for="item in menuItems" :key="item.label">
          <RouterLink
            v-if="!item.unavailable"
            :to="item.route"
            class="nav_item"
            :class="{
              active: route.path === item.route || route.path.startsWith(`${item.route}/`),
            }"
            @click="closeSidebarOnMobile"
          >
            <i :class="item.icon" class="nav_icon" />
            <span v-if="sidebarOpen" class="nav_label">{{ item.label }}</span>
          </RouterLink>

          <div
            v-else
            class="nav_item nav_item_disabled"
            :title="`${item.label} route is not registered yet`"
          >
            <i :class="item.icon" class="nav_icon" />
            <span v-if="sidebarOpen" class="nav_label">{{ item.label }}</span>
            <prime_badge v-if="sidebarOpen" value="Soon" severity="secondary" />
          </div>
        </template>

        <prime_badge v-if="sidebarOpen" />

        <div v-if="sidebarOpen" class="nav_section_title">SYSTEM</div>

        <RouterLink
          v-for="item in secondaryItems"
          :key="item.label"
          :to="typeof item.route === 'function' ? item.route() : item.route"
          class="nav_item"
          :class="{ active: currentRouteLabel === item.label }"
          @click="closeSidebarOnMobile"
        >
          <i :class="item.icon" class="nav_icon" />
          <span v-if="sidebarOpen" class="nav_label">{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="sidebar_footer">
        <Card class="status_card">
          <template #content>
            <div class="status_content">
              <span class="status_dot" />
              <div v-if="sidebarOpen">
                <strong>System Online</strong>
                <span>All services operational</span>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </aside>

    <section class="app_shell">
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
