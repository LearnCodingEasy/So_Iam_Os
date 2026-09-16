<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import LiveDebugConsole from '@/components/Debug/LiveDebugConsole.vue'

const userStore = useUserStore()

const isDropdownOpen = ref(false)

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const closeDropdown = () => {
  isDropdownOpen.value = false
}

const logout = async () => {
  try {
    await userStore.logout()
  } finally {
    closeDropdown()
  }
}
</script>
<template>
  <div class="wrapper_page_app">
    <div class="header_wrapper sticky top-0 left-0 right-0">
      <div class="container mx-auto">
        <div class="header_inner">
          <prime_card class="header_card px-2" v-if="userStore.isLoggedIn">
            <template #content>
              <header class="header_header">
                <nav class="header_nav">
                  <div class="header_content">
                    <div class="header_content_inner relative flex items-center justify-between">
                      <div
                        class="header_mobile_menu_button absolute inset-y-0 left-0 flex items-center sm:hidden"
                      >
                        <button
                          type="button"
                          class="relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-blue-600 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                          aria-controls="mobile-menu"
                          aria-expanded="false"
                        >
                          <span class="absolute -inset-0.5"></span>
                          <span class="sr-only">Open main menu</span>

                          <svg
                            class="block h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            aria-hidden="true"
                            data-slot="icon"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
                            />
                          </svg>

                          <svg
                            class="hidden h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            aria-hidden="true"
                            data-slot="icon"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              d="M6 18 18 6M6 6l12 12"
                            />
                          </svg>
                        </button>
                      </div>
                      <div
                        class="header_wrapper_links flex flex-1 items-center justify-center sm:items-stretch sm:justify-start"
                      >
                        <!-- <div class="header_logo_link flex flex-shrink-0 items-center">
                          <RouterLink to="/" class="logo flex">
                            <span class=""> Logo </span>
                          </RouterLink>
                        </div> -->
                        <div class="header_left_section flex items-center space-x-1 basis-1/4">
                          <!-- Logo -->
                          <RouterLink to="/" class="logo">
                            <!-- <i class="fab fa-facebook fa-fw"></i> -->
                            <!-- <fa :icon="['fab', 'facebook']" /> -->
                            <svg
                              fill="#0866ff"
                              version="1.1"
                              id="Capa_1"
                              xmlns="http://www.w3.org/2000/svg"
                              xmlns:xlink="http://www.w3.org/1999/xlink"
                              width="254px"
                              height="254px"
                              viewBox="-12.4 -12.4 148.80 148.80"
                              xml:space="preserve"
                              stroke="#0866ff"
                              stroke-width="4.216"
                            >
                              <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                              <g
                                id="SVGRepo_tracerCarrier"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke="#CCCCCC"
                                stroke-width="0.744"
                              ></g>
                              <g id="SVGRepo_iconCarrier">
                                <g>
                                  <path
                                    d="M121.4,89.5H2.6c-1.4,0-2.6,1.2-2.6,2.6v9.801c0,1.399,1.2,2.6,2.6,2.6h118.8c1.399,0,2.6-1.2,2.6-2.6V92.1 C124,90.7,122.8,89.5,121.4,89.5z"
                                  ></path>
                                  <path
                                    d="M2.7,77.5h11.9c1.7,0,3.4-1.7,3.4-3.4V56.7c0-1.7,1-3.2,2.7-3.2h13.6c1.7,0,2.8,1.5,2.8,3.2v17.5 c0,1.7,1.6,3.399,3.3,3.399h12c1.7,0,2.7-1.699,2.7-3.399V22c0-1.7-1-2.5-2.7-2.5h-12c-1.7,0-3.3,0.9-3.3,2.5v14.3 c0,1.7-1.1,3.2-2.8,3.2H20.7C19,39.5,18,38,18,36.3V22c0-1.7-1.7-2.5-3.4-2.5H2.7C1,19.5,0,20.4,0,22v52.1C0,75.8,1,77.5,2.7,77.5z "
                                  ></path>
                                  <path
                                    d="M109.9,50.3c0.899-0.3,1.6-0.7,2.3-1.1c2.399-1.5,4.3-3.4,5.7-5.7c1.399-2.3,2.1-5.1,2.1-8.3c0-3.7-0.9-6.8-2.7-9.4 c-1.8-2.6-4.2-4.1-7.1-5.1c-2.9-1-7.2-1.2-12.7-1.2H69.1c-0.899,0-2.1,0.2-2.1,1.1v55c0,0.9,1.2,1.9,2.1,1.9H84 c0.9,0,2.1-1,2.1-1.9V55.1c0-0.9,0.5-1.6,1.301-1.6c1.6,0,3,0.4,4.3,1.3c1,0.7,2,2.2,3.2,4.5l9.1,17.2c0.3,0.5,0.8,1,1.4,1h16.8 c1.2,0,2-1.4,1.399-2.5c-2.6-5.1-4.899-10.5-8.199-15.3c-1.301-1.9-2.7-4.1-4.4-5.6C109.9,53.2,107.7,51.2,109.9,50.3z M101,39.6 c-0.9,1.2-2.3,2-3.8,2.4c-3.2,0.9-6.601,0.6-9.9,0.6C86.4,42.6,86,41.9,86,41v-8.7c0-0.9,0.2-1.8,1.1-1.8H93.4 c2.8,0,5.8,0.2,7.6,2.8C102.3,35.1,102.3,37.8,101,39.6z"
                                  ></path>
                                </g>
                              </g>
                            </svg>
                          </RouterLink>
                          <!-- Search Bar -->
                          <div class="search_bar w-full">
                            <span class="icon">
                              <!-- <i class="fas fa-search fa-fw"></i> -->
                              <fa :icon="['fas', 'search']" />
                            </span>
                            <input
                              type="text"
                              class="w-full p-2 rounded-full focus:outline-none"
                              placeholder="Search"
                            />
                          </div>
                        </div>
                        <div class="header_main_links hidden sm:ml-6 sm:block">
                          <div class="header_main_link flex space-x-4">
                            <RouterLink
                              to="/knowledge"
                              class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition hover:bg-slate-100 dark:hover:bg-slate-800"
                              active-class="bg-indigo-50 text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400"
                            >
                              <FontAwesomeIcon :icon="faBrain" />
                              <span>Knowledge</span>
                            </RouterLink>
                            <RouterLink to="/dashboard" class="rounded-md px-3 py-2 text-md"
                              >Dashboard
                            </RouterLink>
                            <RouterLink to="/automation" class="rounded-md px-3 py-2 text-md"
                              >automation
                            </RouterLink>
                            <RouterLink to="/mcp" class="rounded-md px-3 py-2 text-md">
                              <span><i class="pi pi-server"></i> MCP Server</span>
                            </RouterLink>

                            <RouterLink
                              to="/Vendors"
                              class="rounded-md px-3 py-2 text-md"
                              aria-current="page"
                            >
                              Vendors</RouterLink
                            >
                            <RouterLink to="/About" class="rounded-md px-3 py-2 text-md"
                              >About
                            </RouterLink>
                            <RouterLink to="/explains" class="rounded-md px-3 py-2 text-md"
                              >Explain
                            </RouterLink>
                            <RouterLink to="/products" class="rounded-md px-3 py-2 text-md"
                              >Products
                            </RouterLink>
                          </div>
                        </div>
                      </div>
                      <div
                        class="header_wrapper_profile_search absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0"
                      >
                        <button
                          type="button"
                          class="relative rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                        >
                          <span class="absolute -inset-1.5"></span>
                          <span class="sr-only">View notifications</span>
                          <svg
                            class="h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            aria-hidden="true"
                            data-slot="icon"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0"
                            />
                          </svg>
                        </button>
                        <div class="relative ml-3">
                          <div>
                            <button
                              type="button"
                              class="relative flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                              id="user-menu-button"
                              aria-expanded="false"
                              aria-haspopup="true"
                              @click="toggleDropdown"
                            >
                              <span class="absolute -inset-1.5"></span>
                              <span class="sr-only">Open user menu</span>
                              <img
                                v-if="userStore.user.get_avatar !== 'undefined'"
                                :src="userStore.user.get_avatar"
                                class="h-8 w-8 rounded-full"
                                alt=""
                              />
                              <img
                                v-else
                                class="h-8 w-8 rounded-full"
                                src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                                alt=""
                              />
                            </button>
                          </div>
                          <!-- dropdown -->
                          <div
                            v-if="isDropdownOpen"
                            class="border absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                            role="menu"
                            aria-orientation="vertical"
                            aria-labelledby="user-menu-button"
                            tabindex="-1"
                          >
                            <!-- User Profile -->
                            <div class="div_wrapper_profile flex py-1 items-center cursor-pointer">
                              <div
                                class="icon_div_wrapper_profile flex justify-center items-center"
                              >
                                <RouterLink
                                  class="flex justify-center items-center"
                                  v-if="userStore.user.id"
                                  :to="{
                                    name: 'profile',
                                    params: { id: userStore.user.id },
                                  }"
                                  @click="closeDropdown"
                                >
                                  <!-- If Image -->
                                  <div class="mr-1">
                                    <span
                                      class="user_img"
                                      v-if="userStore.user.get_avatar !== 'undefined'"
                                    >
                                      <img
                                        :src="userStore.user.get_avatar"
                                        class="rounded-full w-8 h-8"
                                        alt=""
                                      />
                                    </span>
                                    <span class="user_icon" v-else>
                                      <i class="pi pi-user px-2" shape="circle"></i>
                                    </span>
                                  </div>
                                  <!-- If Name -->
                                  <div class="">
                                    <span class="user_name" v-if="userStore.user.name">{{
                                      userStore.user.name
                                    }}</span>
                                    <span class="user_name" v-else>Your Profile</span>
                                  </div>
                                </RouterLink>
                              </div>
                            </div>
                            <!-- Settings -->
                            <div class="div_wrapper_logout flex py-1 items-center cursor-pointer">
                              <div
                                class="icon_logout flex justify-center items-center"
                                @click="closeDropdown"
                              >
                                <i class="pi pi-cog px-2" shape="circle"></i>
                                <button class="">Settings</button>
                              </div>
                            </div>
                            <!-- Sign Out -->
                            <div
                              class="div_wrapper_logout flex py-1 items-center cursor-pointer"
                              @click="logout"
                            >
                              <div
                                class="icon_logout flex justify-center items-center"
                                @click="closeDropdown"
                              >
                                <i class="pi pi-sign-out px-2" shape="circle"></i>
                                <button class="">Sign out</button>
                              </div>
                            </div>
                            <!-- Toggle Theme -->
                            <div
                              class="flex div_wrapper_toggle_theme cursor-pointer"
                              @click="closeDropdown"
                            >
                              <ThemeSwitcher />
                              <span class="mb-2">Toggle theme</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="sm:hidden" id="mobile-menu">
                    <div class="space-y-1 px-2 pb-3 pt-2">
                      <RouterLink
                        to="/knowledge"
                        class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition hover:bg-slate-100 dark:hover:bg-slate-800"
                        active-class="bg-indigo-50 text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400"
                      >
                        <FontAwesomeIcon :icon="faBrain" />
                        <span>Knowledge</span>
                      </RouterLink>
                      <a
                        href="#"
                        class="block rounded-md bg-gray-900 px-3 py-2 text-base font-medium text-white"
                        aria-current="page"
                        >Dashboard</a
                      >
                      <a
                        href="#"
                        class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
                        >Team</a
                      >
                      <a
                        href="#"
                        class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
                        >Projects</a
                      >
                      <a
                        href="#"
                        class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
                        >Calendar</a
                      >
                    </div>
                  </div>
                </nav>
              </header>
            </template>
          </prime_card>
        </div>
      </div>
    </div>
    <prime_toast />
    <prime_confirm_dialog />
    <LiveDebugConsole />

    <RouterView />
  </div>
</template>

<script>
export default {
  mounted() {
    document.title = 'Home'
  },
}
</script>

<style lang="scss">
.header_right_section {
  a,
  RouterLink {
    margin: 0 0.5rem;
  }
}

.wrapper_page_app {
  .header_wrapper {
    border-bottom: 1px solid #99999985;
    z-index: 7;
    .container {
      .header_inner {
        .header_card {
          border-radius: 0;
          box-shadow: none;

          > div {
            padding: 0;

            header.header_header {
              nav.header_nav {
                .header_content {
                  .header_content_inner {
                    .header_mobile_menu_button {
                      button {
                        border: 0.1rem solid #085dd8;
                      }
                    }

                    .header_wrapper_links {
                      .header_logo_link {
                        .logo {
                          i {
                          }
                        }
                      }

                      .header_main_links {
                        .header_main_link {
                          a {
                          }

                          button {
                            background-color: #085dd8;
                            border: 0;
                            color: white;
                          }
                        }
                      }
                    }

                    .header_wrapper_profile_search {
                      .header_input_search {
                        margin: 0 0.5rem;
                        height: 30px;

                        input {
                          border-radius: 3px;
                          height: 100%;
                          box-shadow: none;
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
</style>
