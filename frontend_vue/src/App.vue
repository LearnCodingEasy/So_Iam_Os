<script setup>
import { RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import LiveDebugConsole from '@/components/Debug/LiveDebugConsole.vue'
import HeaderView from '@/components/Header/HeaderView.vue'

const userStore = useUserStore()
</script>
<template>
  <div class="wrapper_page_app">
    <HeaderView v-if="userStore.isLoggedIn">
      <RouterView />
    </HeaderView>

    <RouterView v-else />

    <prime_toast />
    <prime_confirm_dialog />
    <LiveDebugConsole />
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
