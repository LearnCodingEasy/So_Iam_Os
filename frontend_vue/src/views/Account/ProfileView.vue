<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { usersAccountsAPI } from '@/services/usersAccounts'

import fallbackImage from '@/assets/Images/Page_Not_Found/404.jpg'

const route = useRoute()
const userStore = useUserStore()

// ==================================================
// 👤 Profile
// ==================================================

const user = ref(null)
const storeReady = ref(false)
const loadingProfile = ref(false)
const savingProfile = ref(false)

// ==================================================
// 🎨 UI
// ==================================================

const sidebar_open = ref(false)
const activeTab = ref('1')

// ==================================================
// 👤 Profile Status
// ==================================================

const can_send_friendship_request = ref(false)

// ==================================================
// 📝 Profile Form
// ==================================================

const formInfo = ref({
  id: '',
  name: '',
  surname: '',
  email: '',
  date_of_birth: '',
  gender: '',
  is_online: false,
  skills: [],
})

// ==================================================
// 🖼 Images
// ==================================================

const selectedImageAvatarFile = ref(null)
const selectedImageCoverFile = ref(null)

// ==================================================
// 🛠 Skills
// ==================================================

const tempSkill = ref('')

// ==================================================
// 📅 Date of Birth
// ==================================================

const day = ref(null)
const month = ref(null)
const year = ref(null)

// ==================================================
// 🔐 Password
// ==================================================

const formPassword = ref({
  old_password: '',
  new_password1: '',
  new_password2: '',
})

const errorsFormInfo = ref([])
const errorsFormPassword = ref([])

// ==================================================
// 👥 Friends
// ==================================================

const friendsAccepted = ref([])
const friendsWaiting = ref([])
const friendsNotSend = ref([])
const friendsSend = ref([])
const friendsSuggest = ref([])
const allFriends = ref([])

const isFriendsAccepted = ref(false)
const isFriendsWaiting = ref(false)
const isFriendsSend = ref(false)

// ==================================================
// 📊 Computed
// ==================================================

const currentUser = computed(() => userStore.user || null)

const isOwner = computed(() => {
  const currentId = userStore.user?.id
  const profileId = user.value?.id

  if (!currentId || !profileId) {
    return false
  }

  return String(currentId) === String(profileId)
})

const profileName = computed(() => {
  if (!user.value) {
    return ''
  }

  return user.value.full_name || [user.value.name, user.value.surname].filter(Boolean).join(' ')
})

const profileAvatar = computed(() => {
  return user.value?.avatar_url || fallbackImage
})

const profileCover = computed(() => {
  return user.value?.cover_url || fallbackImage
})

const profileSkills = computed(() => {
  return Array.isArray(user.value?.skills) ? user.value.skills : []
})

const ownerAvatar = computed(() => {
  return userStore.user?.avatar_url || fallbackImage
})

const ownerCover = computed(() => {
  return userStore.user?.cover_url || fallbackImage
})

const displayUser = computed(() => {
  return user.value || userStore.user || null
})

const friendsCount = computed(() => {
  return Number(displayUser.value?.friends_count || 0)
})

const taskCount = computed(() => {
  return Number(displayUser.value?.task_count || 0)
})

const lastLogin = computed(() => {
  return displayUser.value?.last_login_formatted || ''
})

// ==================================================
// 🚀 Initialize
// ==================================================

onMounted(async () => {
  document.title = 'Profile'

  try {
    await userStore.initStore()
  } catch (error) {
    console.error('❌ User store initialization failed:', error)
  }

  storeReady.value = true

  if (userStore.user?.id) {
    loadUserInfoFromStore()
  } else {
    console.warn('⚠️ No authenticated user')
  }

  await getProfile()
})

// ==================================================
// 👤 Load Current User From Store
// ==================================================

function loadUserInfoFromStore() {
  const current = userStore.user

  if (!current?.id) {
    console.warn('⚠️ User store is empty')
    return
  }

  formInfo.value = {
    ...formInfo.value,
    id: current.id,
    name: current.name ?? '',
    surname: current.surname ?? '',
    email: current.email ?? '',
    date_of_birth: current.date_of_birth ?? '',
    gender: current.gender ?? '',
    is_online: Boolean(current.is_online),
    skills: Array.isArray(current.skills) ? [...current.skills] : [],
  }

  initializeDateOfBirth(current.date_of_birth)
}

// ==================================================
// 📅 Initialize Date
// ==================================================

function initializeDateOfBirth(dateValue) {
  if (!dateValue) {
    day.value = null
    month.value = null
    year.value = null
    return
  }

  const date = new Date(dateValue)

  if (Number.isNaN(date.getTime())) {
    return
  }

  day.value = date
  month.value = date
  year.value = date
}

// ==================================================
// 👤 Get Profile
// ==================================================

async function getProfile() {
  const profileId = route.params.id

  if (!profileId) {
    console.warn('⚠️ Profile ID is missing')
    user.value = null
    return
  }

  loadingProfile.value = true

  try {
    const response = await usersAccountsAPI.profile(profileId)

    console.log('================================')
    console.log('👤 PROFILE FROM users_accounts')
    console.log('================================')
    console.log(response.data)

    /*
     * Support:
     *
     * {
     *   user: {...}
     * }
     *
     * or:
     *
     * {
     *   id: 1,
     *   name: ...
     * }
     */

    const profileData = response?.data?.user ?? response?.data ?? null

    if (!profileData || !profileData.id) {
      console.warn('⚠️ Invalid profile response')
      user.value = null
      return
    }

    user.value = profileData

    console.log('ID:', user.value?.id)
    console.log('Name:', user.value?.name)
    console.log('Surname:', user.value?.surname)
    console.log('Email:', user.value?.email)
    console.log('Avatar:', user.value?.avatar_url)
    console.log('Cover:', user.value?.cover_url)
    console.log('Skills:', user.value?.skills)
    console.log('================================')

    if (isOwner.value) {
      loadUserInfoFromStore()
    }
  } catch (error) {
    console.error('❌ Get profile failed:', error)
    console.error('Backend response:', error?.response?.data)

    user.value = null
  } finally {
    loadingProfile.value = false
  }
}

// ==================================================
// 🛠 Add Skill
// ==================================================

function addSkill(event) {
  if (event.key === ',' || event.key === 'Enter') {
    event.preventDefault()

    const skill = tempSkill.value.trim()

    if (skill && !formInfo.value.skills.includes(skill)) {
      formInfo.value.skills.push(skill)
    }

    tempSkill.value = ''
  }
}

// ==================================================
// 🗑 Delete Skill
// ==================================================

function deleteSkill(skill) {
  formInfo.value.skills = formInfo.value.skills.filter((item) => item !== skill)
}

// ==================================================
// 🖼 Avatar Upload
//===================================================

function handleAvatarFileUpload(event) {
  const file = event?.files?.[0] ?? null

  if (!file) {
    return
  }

  selectedImageAvatarFile.value = file

  console.log('🖼 Avatar selected:', file.name)
}

// ==================================================
// 🖼 Cover Upload
// ==================================================

function handleCoverFileUpload(event) {
  const file = event?.files?.[0] ?? null

  if (!file) {
    return
  }

  selectedImageCoverFile.value = file

  console.log('🖼 Cover selected:', file.name)
}

// ==================================================
// 📅 Build Date Of Birth
// ==================================================

function buildDateOfBirth() {
  const date = formInfo.value.date_of_birth

  if (date) {
    return date
  }

  /*
   * PrimeVue DatePicker can return Date objects.
   * We use the selected day/month/year safely.
   */

  const selectedDate = day.value || month.value || year.value

  if (!(selectedDate instanceof Date)) {
    return ''
  }

  const yyyy = selectedDate.getFullYear()

  const mm = String(selectedDate.getMonth() + 1).padStart(2, '0')

  const dd = String(selectedDate.getDate()).padStart(2, '0')

  return `${yyyy}-${mm}-${dd}`
}

// ==================================================
// 📝 Edit Profile
// ==================================================

async function formEditProfileInfo() {
  errorsFormInfo.value = []

  if (!userStore.user?.id) {
    errorsFormInfo.value.push('User is not authenticated.')
    return
  }

  savingProfile.value = true

  try {
    const formData = new FormData()

    formData.append('name', formInfo.value.name)

    formData.append('surname', formInfo.value.surname)

    formData.append('email', formInfo.value.email)

    const dateOfBirth = buildDateOfBirth()

    if (dateOfBirth) {
      formData.append('date_of_birth', dateOfBirth)
    }

    formData.append('gender', formInfo.value.gender || '')

    formData.append('is_online', formInfo.value.is_online ? 'true' : 'false')

    formData.append('skills', JSON.stringify(formInfo.value.skills))

    if (selectedImageAvatarFile.value) {
      formData.append('avatar', selectedImageAvatarFile.value)
    }

    if (selectedImageCoverFile.value) {
      formData.append('cover', selectedImageCoverFile.value)
    }

    const response = await usersAccountsAPI.editProfile(formData)

    console.log('✅ Profile updated:', response.data)

    const updatedUser = response?.data?.user ?? response?.data

    if (updatedUser) {
      userStore.setUserInfo(updatedUser)

      user.value = {
        ...(user.value || {}),
        ...updatedUser,
      }

      loadUserInfoFromStore()
    }

    selectedImageAvatarFile.value = null
    selectedImageCoverFile.value = null

    console.log('✅ Profile saved successfully')
  } catch (error) {
    console.error('❌ Profile update failed:', error)

    console.error('Backend response:', error?.response?.data)

    const backendErrors = error?.response?.data?.errors

    if (backendErrors) {
      Object.entries(backendErrors).forEach(([field, messages]) => {
        if (Array.isArray(messages)) {
          messages.forEach((message) => {
            errorsFormInfo.value.push(`${field}: ${String(message)}`)
          })
        } else {
          errorsFormInfo.value.push(`${field}: ${String(messages)}`)
        }
      })
    } else {
      errorsFormInfo.value.push('Profile update failed.')
    }
  } finally {
    savingProfile.value = false
  }
}

// ==================================================
// 🔐 Edit Password
// ==================================================

async function submitForm() {
  errorsFormPassword.value = []

  if (!userStore.user?.id) {
    errorsFormPassword.value.push('User is not authenticated.')
    return
  }

  try {
    await usersAccountsAPI.editPassword(formPassword.value)

    formPassword.value = {
      old_password: '',
      new_password1: '',
      new_password2: '',
    }

    console.log('✅ Password updated successfully')
  } catch (error) {
    console.error('❌ Password update failed:', error)

    console.error('Backend response:', error?.response?.data)

    const backendErrors = error?.response?.data?.errors

    if (backendErrors) {
      Object.entries(backendErrors).forEach(([field, messages]) => {
        if (Array.isArray(messages)) {
          messages.forEach((message) => {
            errorsFormPassword.value.push(`${field}: ${String(message)}`)
          })
        } else {
          errorsFormPassword.value.push(`${field}: ${String(messages)}`)
        }
      })
    } else {
      errorsFormPassword.value.push('Password update failed.')
    }
  }
}

// ==================================================
// 👥 Friends - Temporary
// ==================================================

function sendFriendshipRequest() {
  console.warn('⚠️ Friends API is not connected yet')
}

function sendFriendshipRequestById(userId) {
  console.warn('⚠️ Friends API is not connected yet:', userId)
}

function handleRequest(status, userId) {
  console.warn('⚠️ Friends API is not connected yet:', {
    status,
    userId,
  })
}

function sendDirectMessage() {
  console.warn('⚠️ Chat API is not connected yet')
}

// ==================================================
// 🎨 Sidebar
// ==================================================

function toggleSidebarOpen() {
  sidebar_open.value = !sidebar_open.value
}

// ==================================================
// 🔄 Route Change
// ==================================================

watch(
  () => route.params.id,
  async () => {
    if (!storeReady.value) {
      return
    }

    await getProfile()
  },
)
</script>

<template>
  <div class="wrapper_profile w-full">
    <div class="container mx-auto">
      <div class="inner_profile px-2">
        <!-- =================================== -->
        <!-- Loading -->

        <div v-if="loadingProfile" class="w-full flex justify-center items-center p-10">
          <div class="text-xl font-bold">Loading profile...</div>
        </div>

        <!-- ================================================= -->
        <!-- Profile Not Found -->
        <!-- ================================================= -->

        <div v-else-if="!displayUser" class="w-full p-10 text-center">
          <div class="text-2xl font-bold">Profile not found</div>

          <div class="mt-2 text-gray-500">We could not load this profile.</div>
        </div>

        <!-- ================================================= -->
        <!-- Main Profile -->
        <!-- ================================================= -->

        <template v-else>
          <!-- ================================================= -->
          <!-- Sidebar -->
          <!-- ================================================= -->

          <aside
            class="sidebar_profile flex-none"
            :class="{
              sidebar_open: sidebar_open,
            }"
          >
            <!-- Toggle -->
            <div class="aside_toggle" @click="toggleSidebarOpen">
              <i class="pi pi-angle-double-right"></i>
            </div>

            <!-- User -->
            <div
              class="user_image"
              @click="activeTab = '1'"
              :class="[activeTab === '1' ? 'activeView' : '']"
            >
              <div class="user_image_icon">
                <i class="pi pi-user"></i>
              </div>

              <div class="user_name_data">
                <div>
                  {{ currentUser?.name || displayUser?.name }}
                </div>

                <div>
                  {{ currentUser?.surname || displayUser?.surname }}
                </div>
              </div>
            </div>

            <!-- Password -->
            <div
              class="user_name"
              @click="activeTab = '2'"
              :class="[activeTab === '2' ? 'activeView' : '']"
              v-if="isOwner"
            >
              <div class="user_name_icon">
                <i class="pi pi-key"></i>
              </div>

              <div class="user_name_data">
                <div>******</div>
              </div>
            </div>

            <!-- Friends -->
            <div
              class="user_email"
              @click="activeTab = '3'"
              :class="[activeTab === '3' ? 'activeView' : '']"
            >
              <div class="user_email_icon">
                <fa :icon="['fas', 'users']" class="text-2xl" />
              </div>

              <div class="user_email_data">
                <div>
                  Friends All
                  {{ friendsAccepted.length }}
                </div>
              </div>
            </div>

            <!-- Suggestions -->
            <div
              class="user_Password"
              @click="activeTab = '4'"
              :class="[activeTab === '4' ? 'activeView' : '']"
            >
              <div class="user_Password_icon">
                <fa :icon="['fas', 'user-check']" class="text-2xl" />
              </div>

              <div class="user_Password_data">
                <div>Friends Suggest</div>
              </div>
            </div>

            <!-- Requests -->
            <div
              class="user_Password"
              @click="activeTab = '5'"
              :class="[activeTab === '5' ? 'activeView' : '']"
              v-if="isOwner"
            >
              <div class="user_Password_icon">
                <fa :icon="['fas', 'user-plus']" class="text-2xl" />
              </div>

              <div class="user_Password_data">
                <div>Friends Requests</div>
              </div>
            </div>

            <!-- Sent -->
            <div
              class="user_Password"
              @click="activeTab = '6'"
              :class="[activeTab === '6' ? 'activeView' : '']"
              v-if="isOwner"
            >
              <div class="user_Password_icon">
                <fa :icon="['fas', 'home']" class="text-2xl" />
              </div>

              <div class="user_Password_data">
                <div>User Tasks</div>
              </div>
            </div>

            <!-- Tasks -->
            <div
              class="user_Password"
              @click="activeTab = '7'"
              :class="[activeTab === '7' ? 'activeView' : '']"
            >
              <div class="user_Password_icon">
                <fa :icon="['fas', 'thumbtack']" class="text-2xl" />
              </div>

              <div class="user_Password_data">
                <div>User Tasks</div>
              </div>
            </div>
          </aside>

          <!-- ================================================= -->
          <!-- Profile Content -->
          <!-- ================================================= -->

          <div class="data_profile flex p-8">
            <!-- ================================================= -->
            <!-- TAB 1 - PROFILE -->
            <!-- ================================================= -->

            <div
              class="wrapper_info_data w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12 gap_20"
              v-if="activeTab === '1'"
            >
              <!-- ================================================= -->
              <!-- Old Data -->
              <!-- ================================================= -->

              <div
                class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_6 desktop_item_6 desktop_lg_item_6"
              >
                <div class="wrapper_old_data w-full">
                  <div class="inner_old_data w-full">
                    <prime_card class="w-full">
                      <!-- ================================================= -->
                      <!-- Header / Images -->
                      <!-- ================================================= -->

                      <template #header>
                        <!-- Owner -->
                        <div v-if="isOwner" class="w-full">
                          <!-- Cover -->
                          <div class="image_cover">
                            <img
                              v-if="ownerCover"
                              :src="ownerCover"
                              alt="Profile cover"
                              class="w-full h-64 object-cover"
                            />

                            <img
                              v-else
                              :src="fallbackImage"
                              alt="Default cover"
                              class="w-full h-64 object-cover"
                            />
                          </div>

                          <!-- Avatar -->
                          <div
                            class="image_avatar border rounded-full"
                            style="
                              width: 75px;
                              height: 75px;
                              display: flex;
                              justify-content: center;
                              align-items: center;
                              margin-top: -37px;
                              margin-left: 10px;
                              position: relative;
                              background: white;
                            "
                          >
                            <img
                              :src="ownerAvatar"
                              alt="Profile avatar"
                              class="w-full h-full shadow-lg rounded-full object-cover"
                            />

                            <prime_badge
                              size="small"
                              :severity="currentUser?.is_online ? 'success' : 'danger'"
                              style="position: absolute; bottom: -8px; opacity: 0.8"
                            ></prime_badge>
                          </div>
                        </div>

                        <!-- Visitor -->
                        <div v-else class="w-full">
                          <!-- Cover -->
                          <div class="image_cover">
                            <img
                              v-if="profileCover"
                              :src="profileCover"
                              alt="Profile cover"
                              class="w-full h-64 object-cover"
                            />

                            <img
                              v-else
                              :src="fallbackImage"
                              alt="Default cover"
                              class="w-full h-64 object-cover"
                            />
                          </div>

                          <!-- Avatar -->
                          <div
                            class="image_avatar border rounded-full"
                            style="
                              width: 75px;
                              height: 75px;
                              display: flex;
                              justify-content: center;
                              align-items: center;
                              margin-top: -37px;
                              margin-left: 10px;
                              position: relative;
                              background: white;
                            "
                          >
                            <img
                              :src="profileAvatar"
                              alt="Profile avatar"
                              class="w-full h-full shadow-lg rounded-full object-cover"
                            />

                            <prime_badge
                              size="small"
                              :severity="user?.is_online ? 'success' : 'danger'"
                              style="position: absolute; bottom: -8px; opacity: 0.8"
                            ></prime_badge>
                          </div>
                        </div>
                      </template>

                      <!-- ================================================= -->
                      <!-- Content -->
                      <!-- ================================================= -->

                      <template #content>
                        <div
                          class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
                        >
                          <!-- Left -->
                          <div
                            class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_6 desktop_item_6 desktop_lg_item_6 mr-1"
                          >
                            <!-- Name -->
                            <div>
                              <h3 class="text-2xl font-bold">
                                {{ isOwner ? formInfo.name : user?.name || '' }}
                              </h3>
                            </div>

                            <!-- Surname -->
                            <div>
                              <h3 class="text-1xl font-bold">
                                {{ isOwner ? formInfo.surname : user?.surname || '' }}
                              </h3>
                            </div>

                            <!-- Email -->
                            <div>
                              <small class="text-1xl font-bold">
                                {{ isOwner ? formInfo.email : user?.email || '' }}
                              </small>
                            </div>

                            <!-- DOB + Gender -->
                            <div class="flex justify-between items-center">
                              <div class="mr-4">
                                <h3 class="text-1xl font-bold">
                                  {{ isOwner ? formInfo.date_of_birth : user?.date_of_birth || '' }}
                                </h3>
                              </div>

                              <div class="mr-4">
                                <h3 class="text-1xl font-bold">
                                  {{ isOwner ? formInfo.gender : user?.gender || '' }}
                                </h3>
                              </div>
                            </div>
                          </div>

                          <!-- Right -->
                          <div
                            class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_6 desktop_item_6 desktop_lg_item_6 ml-1"
                          >
                            <div class="flex justify-between items-center my-2">
                              <!-- Skills -->
                              <div>
                                <!-- Owner -->
                                <div v-if="isOwner">
                                  <prime_tag
                                    severity="success"
                                    v-for="skill in formInfo.skills"
                                    :key="skill"
                                    :value="skill"
                                    class="mb-1 ml-1"
                                  />
                                </div>

                                <!-- Visitor -->
                                <div v-else>
                                  <prime_tag
                                    severity="success"
                                    v-for="skill in profileSkills"
                                    :key="skill"
                                    :value="skill"
                                    class="mb-1 ml-1"
                                  />
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </template>

                      <!-- ================================================= -->
                      <!-- Footer -->
                      <!-- ================================================= -->

                      <template #footer>
                        <div class="flex justify-between items-center py-1">
                          <!-- Friends -->
                          <div>
                            <prime_button
                              type="button"
                              label="Friends"
                              :badge="friendsCount"
                              badgeSeverity="contrast"
                              outlined
                            />
                          </div>

                          <!-- Tasks -->
                          <div>
                            <prime_button
                              type="button"
                              label="Tasks"
                              :badge="taskCount"
                              badgeSeverity="contrast"
                              outlined
                            />
                          </div>

                          <!-- Last Login -->
                          <div class="flex justify-between items-center py-1">
                            <small>
                              Last Login:
                              {{ lastLogin || 'Unknown' }}
                              <span v-if="lastLogin"> Ago </span>
                            </small>
                          </div>
                        </div>

                        <!-- Visitor Actions -->
                        <div v-if="!isOwner" class="mt-2">
                          <div class="flex justify-between py-2">
                            <!-- Add Friend -->
                            <prime_button
                              @click="sendFriendshipRequest"
                              class="border py-2 px-4 btn-primary Add_friend"
                              v-if="can_send_friendship_request"
                            >
                              <span class="icon">
                                <fa :icon="['fas', 'plus']" />
                              </span>

                              <span class="text"> Add Friend </span>
                            </prime_button>

                            <!-- Existing Friendship -->
                            <div v-else class="flex flex-wrap gap-2">
                              <!-- Unfriend -->
                              <prime_button
                                class="mr-1 un_friend"
                                v-if="!isOwner && isFriendsAccepted"
                                @click="handleRequest('unfriend', user?.id)"
                              >
                                <span class="icon">
                                  <fa :icon="['fas', 'user']" />
                                </span>

                                <span class="text"> Un Friend </span>
                              </prime_button>

                              <!-- Friend -->
                              <prime_button class="friend" v-if="!isOwner && isFriendsAccepted">
                                <span class="icon">
                                  <fa :icon="['fas', 'user']" />
                                </span>

                                <span class="text"> Friend </span>
                              </prime_button>

                              <!-- Accepted -->
                              <prime_button
                                class="btn btn-primary Add_friend"
                                v-if="!isOwner && isFriendsSend"
                                @click="handleRequest('accepted', user?.id)"
                              >
                                <span class="icon">
                                  <fa :icon="['fas', 'user-check']" />
                                </span>

                                <span class="text"> accepted </span>
                              </prime_button>

                              <!-- Rejected -->
                              <prime_button
                                class="btn btn-primary Add_friend"
                                v-if="!isOwner && isFriendsSend"
                                @click="handleRequest('rejected', user?.id)"
                              >
                                <span class="icon">
                                  <fa :icon="['fas', 'user-check']" />
                                </span>

                                <span class="text"> rejected </span>
                              </prime_button>

                              <!-- Cancel -->
                              <prime_button
                                class="btn btn-primary Add_friend"
                                v-if="!isOwner && isFriendsWaiting"
                                @click="handleRequest('cancel', user?.id)"
                              >
                                <span class="icon">
                                  <fa :icon="['fas', 'user-check']" />
                                </span>

                                <span class="text"> Cancel Request </span>
                              </prime_button>
                            </div>

                            <!-- Message -->
                            <prime_button
                              class="message_friend"
                              @click="sendDirectMessage"
                              v-if="!isOwner"
                            >
                              <span class="icon">
                                <fa :icon="['fab', 'facebook-messenger']" />
                              </span>

                              <span class="text"> Message </span>
                            </prime_button>
                          </div>
                        </div>
                      </template>
                    </prime_card>
                  </div>
                </div>
              </div>

              <!-- ================================================= -->
              <!-- Owner Edit -->
              <!-- ================================================= -->

              <div
                class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_6 desktop_item_6 desktop_lg_item_6"
              >
                <div class="wrapper_new_data" v-if="isOwner">
                  <form class="space-y-4" @submit.prevent="formEditProfileInfo">
                    <!-- Images -->
                    <div
                      class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12 gap_10"
                    >
                      <!-- Avatar -->
                      <div
                        class="new_data mobile_item_12 tablet_item_12 laptop_item_12 laptop_lg_item_12 desktop_item_6 desktop_lg_item_6"
                      >
                        <label class="font-semibold block my-2"> Avatar </label>

                        <prime_file_upload
                          type="file"
                          ref="fileAvatar"
                          :multiple="false"
                          name="avatar"
                          @select="handleAvatarFileUpload"
                          accept="image/*"
                          :maxFileSize="1000000"
                        >
                          <template #empty>
                            <span> Drag and drop files here to upload. </span>
                          </template>
                        </prime_file_upload>
                      </div>

                      <!-- Cover -->
                      <div
                        class="new_data mobile_item_12 tablet_item_12 laptop_item_12 laptop_lg_item_12 desktop_item_6 desktop_lg_item_6"
                      >
                        <label class="font-semibold block my-2"> Cover </label>

                        <prime_file_upload
                          type="file"
                          ref="fileCover"
                          :multiple="false"
                          name="cover"
                          @select="handleCoverFileUpload"
                          accept="image/*"
                          :maxFileSize="1000000"
                        >
                          <template #empty>
                            <span> Drag and drop files here to upload. </span>
                          </template>
                        </prime_file_upload>
                      </div>
                    </div>

                    <!-- Name + Surname -->
                    <div class="flex justify-between items-center gap-4">
                      <div class="new_data w-full">
                        <label>Name</label>

                        <input
                          type="text"
                          v-model="formInfo.name"
                          placeholder="Your full name"
                          class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                        />
                      </div>

                      <div class="new_data w-full">
                        <label> Surname </label>

                        <input
                          type="text"
                          v-model="formInfo.surname"
                          placeholder="Your full surname"
                          class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                        />
                      </div>
                    </div>

                    <!-- Email -->
                    <div class="new_data">
                      <label>E-mail</label>

                      <input
                        type="email"
                        v-model="formInfo.email"
                        placeholder="Your e-mail address"
                        class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                      />
                    </div>

                    <!-- Skills -->
                    <div class="new_data">
                      <label> Skills [press Enter or comma to add]: </label>

                      <input
                        type="text"
                        v-model="tempSkill"
                        @keydown.enter.prevent="addSkill"
                        @keydown="addSkill"
                        placeholder="Your Skills"
                        class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                      />

                      <div class="grid_12 mt-4">
                        <div>
                          <span
                            v-for="skill in formInfo.skills"
                            :key="skill"
                            @click="deleteSkill(skill)"
                            class="cursor-pointer inline-block mr-1 mb-1"
                          >
                            <prime_tag severity="success" :value="skill" />
                          </span>
                        </div>
                      </div>
                    </div>

                    <!-- Date -->
                    <div class="col-span-full">Date of birth</div>

                    <div class="col-span-full">
                      <div class="flex flex-col md:flex-row gap-2">
                        <prime_input_group>
                          <prime_date_picker v-model="day" view="day" dateFormat="dd" />
                        </prime_input_group>

                        <prime_input_group>
                          <prime_date_picker v-model="month" view="month" dateFormat="mm" />
                        </prime_input_group>

                        <prime_input_group>
                          <prime_date_picker v-model="year" view="year" dateFormat="yy" />
                        </prime_input_group>
                      </div>
                    </div>

                    <!-- Gender -->
                    <div class="col-span-full">Gender</div>

                    <div class="flex flex-col md:flex-row gap-2">
                      <prime_input_group>
                        <prime_radio_button
                          v-model="formInfo.gender"
                          inputId="ingredient1"
                          name="gender"
                          value="female"
                        />

                        <label for="ingredient1" class="ml-2"> Female </label>
                      </prime_input_group>

                      <prime_input_group>
                        <prime_radio_button
                          v-model="formInfo.gender"
                          inputId="ingredient2"
                          name="gender"
                          value="male"
                        />

                        <label for="ingredient2" class="ml-2"> Male </label>
                      </prime_input_group>

                      <prime_input_group>
                        <prime_radio_button
                          v-model="formInfo.gender"
                          inputId="ingredient3"
                          name="gender"
                          value="custom"
                        />

                        <label for="ingredient3" class="ml-2"> Custom </label>
                      </prime_input_group>
                    </div>

                    <!-- Online -->
                    <div class="new_data">
                      <label> Is Online </label>

                      <br />

                      <input type="checkbox" v-model="formInfo.is_online" />

                      <label class="ml-2">
                        {{ formInfo.is_online }}
                      </label>
                    </div>

                    <!-- Save -->
                    <div>
                      <button
                        type="submit"
                        class="py-4 px-6 bg-blue-400 text-white rounded-lg"
                        :disabled="savingProfile"
                      >
                        {{ savingProfile ? 'Saving...' : 'Save changes' }}
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>

            <!-- ================================================= -->
            <!-- TAB 2 - PASSWORD -->
            <!-- ================================================= -->

            <div
              class="wrapper_password_data flex justify-between items-center w-full"
              v-if="activeTab === '2' && isOwner"
            >
              <!-- User Card -->
              <div class="wrapper_old_data">
                <div class="inner_old_data flex justify-between items-end">
                  <prime_card class="w-96">
                    <template #header>
                      <img :src="ownerAvatar" alt="User avatar" class="w-full" />
                    </template>

                    <template #content>
                      <h3 class="text-2xl font-bold">
                        {{ currentUser?.name || '' }}
                      </h3>

                      <h3 class="text-1xl font-bold">
                        {{ currentUser?.surname || '' }}
                      </h3>
                    </template>

                    <template #body>
                      <div>
                        {{ currentUser?.email || '' }}
                      </div>
                    </template>

                    <template #footer>
                      {{ currentUser?.email || '' }}
                    </template>
                  </prime_card>
                </div>
              </div>

              <!-- Password Form -->
              <div class="wrapper_new_data ml-8">
                <form class="space-y-6" @submit.prevent="submitForm">
                  <div class="new_data">
                    <label> Old password </label>

                    <input
                      type="password"
                      v-model="formPassword.old_password"
                      placeholder="Your old password"
                      class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                    />
                  </div>

                  <div class="new_data">
                    <label> New password </label>

                    <input
                      type="password"
                      v-model="formPassword.new_password1"
                      placeholder="Your new password"
                      class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                    />
                  </div>

                  <div class="new_data">
                    <label> Repeat password </label>

                    <input
                      type="password"
                      v-model="formPassword.new_password2"
                      placeholder="Repeat password"
                      class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                    />
                  </div>

                  <div>
                    <button type="submit" class="py-4 px-6 bg-blue-400 text-white rounded-lg">
                      Save changes
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <!-- ================================================= -->
            <!-- TAB 3 - FRIENDS -->
            <!-- ================================================= -->

            <div class="w-full" v-if="activeTab === '3'">
              <div class="main-center col-span-2 space-y-4">
                <div class="flex justify-between items-center mb-6">
                  <h3 class="text-3xl">Your Friends</h3>

                  <prime_button
                    type="button"
                    label="All Friends"
                    icon="pi pi-user-plus"
                    :badge="allFriends.length"
                    badgeSeverity="contrast"
                    outlined
                  />
                </div>

                <!-- Friends -->
                <div
                  v-if="allFriends.length"
                  class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
                >
                  <prime_card
                    v-for="friend in allFriends"
                    :key="friend.id"
                    style="overflow: hidden; position: relative"
                    class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_2 desktop_item_3 desktop_lg_item_3 m-2"
                  >
                    <template #header>
                      <img
                        :src="friend.cover_url || fallbackImage"
                        alt="user header"
                        class="h-32 md:h-20 lg:h-32 w-full m-auto object-cover"
                      />

                      <div style="position: relative">
                        <img
                          :src="friend.avatar_url || fallbackImage"
                          alt="avatar"
                          class="mb-1 rounded-full h-14 md:h-10 w-14 md:w-10 m-auto object-cover"
                          style="margin-top: -7px; position: absolute; top: -15px; left: 10px"
                        />
                      </div>
                    </template>

                    <template #title>
                      <p class="mt-1 md:mt-1">
                        <strong>
                          <RouterLink
                            :to="{
                              name: 'profile',
                              params: {
                                id: friend.id,
                              },
                            }"
                          >
                            {{ friend.name || 'User' }}
                          </RouterLink>
                        </strong>
                      </p>
                    </template>

                    <template #subtitle>
                      {{ friend.email || '' }}
                    </template>

                    <template #content> </template>

                    <template #footer>
                      <div class="flex gap-2">
                        <prime_button
                          :label="'Friends ' + (friend.friends_count || 0)"
                          severity="secondary"
                          outlined
                          class="w-full"
                        />
                      </div>
                    </template>
                  </prime_card>
                </div>

                <!-- Empty -->
                <div v-else class="w-full p-8 text-center">
                  <h3 class="text-xl">No friends found</h3>
                </div>
              </div>
            </div>

            <!-- ================================================= -->
            <!-- TAB 4 - SUGGESTIONS -->
            <!-- ================================================= -->

            <div class="w-full" v-if="activeTab === '4'">
              <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl">People You May Know [ Suggest ]</h3>

                <prime_button
                  type="button"
                  label="Friendship Not Send"
                  icon="pi pi-user-plus"
                  :badge="friendsNotSend.length"
                  badgeSeverity="contrast"
                  outlined
                />
              </div>

              <div
                class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
              >
                <prime_card
                  v-for="suggestedUser in friendsNotSend"
                  :key="suggestedUser.id"
                  style="overflow: hidden; position: relative"
                  class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_3 desktop_item_3 desktop_lg_item_2 mx-2 mb-4"
                >
                  <template #header>
                    <img
                      :src="suggestedUser.cover_url || fallbackImage"
                      alt="user header"
                      class="h-32 md:h-20 lg:h-32 w-full m-auto object-cover"
                    />

                    <div style="position: relative">
                      <img
                        :src="suggestedUser.avatar_url || fallbackImage"
                        alt="avatar"
                        class="mb-1 rounded-full h-14 md:h-10 w-14 md:w-10 m-auto object-cover"
                        style="margin-top: -7px; position: absolute; top: -15px; left: 10px"
                      />
                    </div>
                  </template>

                  <template #title>
                    <p class="mt-4 md:mt-4">
                      <strong>
                        <RouterLink
                          :to="{
                            name: 'profile',
                            params: {
                              id: suggestedUser.id,
                            },
                          }"
                        >
                          {{ suggestedUser.name || 'User Name' }}
                        </RouterLink>
                      </strong>
                    </p>
                  </template>

                  <template #subtitle>
                    {{ suggestedUser.email || '' }}
                  </template>

                  <template #content>
                    <prime_button
                      @click="sendFriendshipRequestById(suggestedUser.id)"
                      class="border py-2 px-4 btn-primary Add_friend"
                      v-if="can_send_friendship_request"
                    >
                      <span class="icon">
                        <fa :icon="['fas', 'plus']" />
                      </span>

                      <span class="text"> Add Friend </span>
                    </prime_button>
                  </template>

                  <template #footer>
                    <prime_button
                      :label="'Friends ' + (suggestedUser.friends_count || 0)"
                      severity="secondary"
                      outlined
                      class="w-full"
                    />
                  </template>
                </prime_card>
              </div>
            </div>

            <!-- ================================================= -->
            <!-- TAB 5 - REQUESTS -->
            <!-- ================================================= -->

            <div class="w-full" v-if="activeTab === '5' && isOwner">
              <div v-if="friendsWaiting.length" class="w-full">
                <div class="flex justify-between items-center mb-6">
                  <h3 class="text-xl">Friendship Requests Waiting</h3>

                  <prime_button
                    type="button"
                    label="Friendship Requests Waiting"
                    icon="pi pi-user-plus"
                    :badge="friendsWaiting.length"
                    badgeSeverity="contrast"
                    outlined
                  />
                </div>

                <div class="rounded-lg grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
                  <div
                    class="text-center border shadow-xl rounded-lg p-4"
                    v-for="friendWaiting in friendsWaiting"
                    :key="friendWaiting.id"
                  >
                    <img
                      :src="friendWaiting.get_avatar || friendWaiting.avatar_url || fallbackImage"
                      alt="avatar"
                      class="mb-6 rounded-full h-32 w-32 m-auto object-cover"
                    />

                    <p>
                      <strong>
                        <RouterLink
                          :to="{
                            name: 'profile',
                            params: {
                              id: friendWaiting.id,
                            },
                          }"
                        >
                          {{ friendWaiting.name || 'User' }}
                        </RouterLink>
                      </strong>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                      <p class="text-xs text-gray-500">
                        {{ friendWaiting.friends_count || 0 }}
                        Friends
                      </p>

                      <p class="text-xs text-gray-500">
                        {{ friendWaiting.posts_count || friendWaiting.task_count || 0 }}
                        Tasks
                      </p>
                    </div>

                    <div class="mt-4 flex justify-between">
                      <button
                        type="button"
                        class="inline-block py-2 px-4 bg-blue-400 text-white rounded-lg"
                        @click="handleRequest('accepted', friendWaiting.id)"
                      >
                        Accept
                      </button>

                      <button
                        type="button"
                        class="inline-block py-2 px-4 bg-red-600 text-white rounded-lg"
                        @click="handleRequest('rejected', friendWaiting.id)"
                      >
                        Reject
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="w-full">
                <div class="flex justify-between items-center mb-6">
                  <h3 class="text-xl">No Friendship Requests</h3>

                  <prime_button
                    type="button"
                    label="Friendship requests"
                    icon="pi pi-user-plus"
                    :badge="friendsWaiting.length"
                    badgeSeverity="contrast"
                    outlined
                  />
                </div>
              </div>
            </div>

            <!-- ================================================= -->
            <!-- TAB 6 - SENT -->
            <!-- ================================================= -->

            <div class="w-full" v-if="activeTab === '6' && isOwner">
              <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl uppercase">User Is [Send]</h3>

                <prime_button
                  type="button"
                  label="User Is [Send]"
                  icon="pi pi-user-plus"
                  :badge="friendsSend.length"
                  badgeSeverity="contrast"
                  outlined
                />
              </div>

              <div
                class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
              >
                <prime_card
                  v-for="sentUser in friendsSend"
                  :key="sentUser.id"
                  style="overflow: hidden; position: relative"
                  class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_2 desktop_item_3 desktop_lg_item_3 mx-2 mb-4"
                >
                  <template #header>
                    <img
                      :src="sentUser.cover_url || fallbackImage"
                      alt="user header"
                      class="h-32 md:h-20 lg:h-32 w-full m-auto object-cover"
                    />

                    <div style="position: relative">
                      <img
                        :src="sentUser.avatar_url || fallbackImage"
                        alt="avatar"
                        class="mb-1 rounded-full h-14 md:h-10 w-14 md:w-10 m-auto object-cover"
                        style="margin-top: -7px; position: absolute; top: -15px; left: 10px"
                      />
                    </div>
                  </template>

                  <template #title>
                    <p class="mt-4 md:mt-4">
                      <strong>
                        <RouterLink
                          :to="{
                            name: 'profile',
                            params: {
                              id: sentUser.id,
                            },
                          }"
                        >
                          {{ sentUser.name || 'User' }}
                        </RouterLink>
                      </strong>
                    </p>
                  </template>

                  <template #subtitle>
                    {{ sentUser.email || '' }}
                  </template>

                  <template #content> </template>

                  <template #footer>
                    <prime_button
                      :label="'Friends ' + (sentUser.friends_count || 0)"
                      severity="secondary"
                      outlined
                      class="w-full"
                    />
                  </template>
                </prime_card>
              </div>
            </div>

            <!-- ================================================= -->
            <!-- TAB 7 - TASKS -->
            <!-- ================================================= -->

            <div class="w-full" v-if="activeTab === '7'">
              <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl uppercase">Your Tasks</h3>

                <prime_button
                  type="button"
                  label="All Tasks"
                  icon="pi pi-user-plus"
                  :badge="friendsSuggest.length"
                  badgeSeverity="contrast"
                  outlined
                />
              </div>

              <div class="w-full p-6 text-center">
                <p>Tasks API is not connected yet.</p>
              </div>
            </div>

            <!-- ================================================= -->
            <!-- Errors -->
            <!-- ================================================= -->

            <template v-if="errorsFormInfo.length > 0">
              <div class="bg-red-300 text-white rounded-lg p-6 mt-4 w-full">
                <p v-for="(error, index) in errorsFormInfo" :key="index">
                  {{ error }}
                </p>
              </div>
            </template>

            <template v-if="errorsFormPassword.length > 0">
              <div class="bg-red-300 text-white rounded-lg p-6 mt-4 w-full">
                <p v-for="(error, index) in errorsFormPassword" :key="index">
                  {{ error }}
                </p>
              </div>
            </template>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
