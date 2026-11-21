# accounts source-file catalog

Files associated with this domain's view/service/store/component directories are listed. Imports and declaration names are static excerpts; global callers are not exhaustive.


## views/accounts/auth-callback.vue
- Type: .vue
- Declarations: L14: const response = await api.get('/users/me/')
- Imports (first five): import api from '@/services/Shared/api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/accounts/AuthCallback.vue
- Type: .vue
- Declarations: L13: const route = useRoute(); L14: const router = useRouter(); L15: const userStore = useUserStore(); L18: const access = route.query.access; L19: const refresh = route.query.refresh; L25: const userData = {
- Imports (first five): import { onMounted } from 'vue'; import { useRoute, useRouter } from 'vue-router'; import { useUserStore } from '@/stores/accounts/user'; import axios from 'axios'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/accounts/LoginView.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import LoginForm from '@/components/accounts/LoginForm.vue'; import SignupForm from '@/components/accounts/SignupForm.vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/accounts/ProfileView.vue
- Type: .vue
- Declarations: L10: const route = useRoute(); L11: const userStore = useUserStore(); L17: const user = ref(null); L18: const storeReady = ref(false); L19: const loadingProfile = ref(false); L20: const savingProfile = ref(false); L26: const sidebar_open = ref(false); L27: const activeTab = ref('1'); L33: const can_send_friendship_request = ref(false); L39: const formInfo = ref({; L54: const selectedImageAvatarFile = ref(null); L55: const selectedImageCoverFile = ref(null); L56: const cropTarget = ref(null); L57: const cropTargetType = ref('avatar'); L63: const tempSkill = ref(''); L69: const day = ref(null); L70: const month = ref(null); L71: const year = ref(null); L77: const formPassword = ref({; L83: const errorsFormInfo = ref([]); L84: const errorsFormPassword = ref([]); L90: const friendsAccepted = ref([]); L91: const friendsWaiting = ref([]); L92: const friendsNotSend = ref([]); L93: const friendsSend = ref([]); L94: const friendsSuggest = ref([]); L95: const allFriends = ref([]); L97: const isFriendsAccepted = ref(false); L98: const isFriendsWaiting = ref(false); L99: const isFriendsSend = ref(false)
- Imports (first five): import { ref, computed, watch, onMounted } from 'vue'; import { useRoute } from 'vue-router'; import { useUserStore } from '@/stores/accounts/user'; import { usersAccountsAPI } from '@/services/Accounts/usersAccounts'; import ImageCropperDialog from '@/components/accounts/ImageCropperDialog.vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Accounts/usersAccounts.js
- Type: .js
- Declarations: L4: const API_URL = 'http://127.0.0.1:8000/api'; L6: export const usersAccountsAPI = {
- Imports (first five): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/accounts/user.js
- Type: .js
- Declarations: L9: const ACCESS_TOKEN_KEY = 'user.access'; L10: const REFRESH_TOKEN_KEY = 'user.refresh'; L11: const USER_KEY = 'user.info'; L16: const defaultUser = () => ({; L48: export const useUserStore = defineStore('user', {; L127: const accessToken = event.detail?.access; L128: const refreshToken = event.detail?.refresh; L140: const access = localStorage.getItem(ACCESS_TOKEN_KEY); L142: const refresh = localStorage.getItem(REFRESH_TOKEN_KEY); L144: const storedUser = localStorage.getItem(USER_KEY); L172: const parsedUser = JSON.parse(storedUser); L199: const response = await api.get('/users/me/'); L210: const hasStoredSession = Boolean(; L309: const refresh = this.user.refresh || localStorage.getItem(REFRESH_TOKEN_KEY); L316: const response = await api.post('/users/refresh/', {; L320: const newAccess = response.data?.access; L321: const newRefresh = response.data?.refresh || refresh
- Imports (first five): import { defineStore } from 'pinia'; import api from '@/services/Shared/api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/accounts/ImageCropperDialog.vue
- Type: .vue
- Declarations: L15: const props = defineProps({ file: { type: [File, Object], default: null }, aspectRatio: { type: Number, default: 1 } }); L16: const emit = defineEmits(['cropped', 'cancel']); L17: const visible = ref(false), previewUrl = ref(''), imageRef = ref(null), cropper = ref(null); L20: function crop() { const canvas = cropper.value?.getCroppedCanvas({ maxWidth: 1200, maxHeight: 1200 }); if (!canvas) return; canvas.toBlob((blob) => { if (!blob) return; emit('cropped', new File([blob], props.file?.name || 'cropped-image.jpg', { type: blob.type || 'image/jpeg' })); visible.value = false }, 'image/jpeg', 0.9) }; L21: function cleanup(emitCancel = true) { cropper.value?.destroy(); cropper.value = null; if (objectUrl) URL.revokeObjectURL(objectUrl); objectUrl = ''; previewUrl.value = ''; if (emitCancel && visible.value) emit('cancel') }
- Imports (first five): import { nextTick, onBeforeUnmount, ref, watch } from 'vue'; import Dialog from 'primevue/dialog'; import Button from 'primevue/button'; import Cropper from 'cropperjs'; import 'cropperjs/dist/cropper.css'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/accounts/LoginForm.vue
- Type: .vue
- Declarations: L63: const router = useRouter(); L64: const userStore = useUserStore(); L70: const loading = ref(false); L71: const error = ref(null); L73: const formLogin = ref({; L82: const submitFormLogin = async () => {; L88: const response = await usersAccountsAPI.login({; L97: const userResponse = await usersAccountsAPI.me(); L118: const loginWithGoogle = () => {; L126: const loginWithFacebook = () => {
- Imports (first five): import { ref } from 'vue'; import { useRouter } from 'vue-router'; import { usersAccountsAPI } from '@/services/Accounts/usersAccounts'; import { useUserStore } from '@/stores/accounts/user'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/accounts/SignupForm.vue
- Type: .vue
- Declarations: L102: const formSignup = ref({; L116: const day = ref(''); L117: const month = ref(''); L118: const year = ref(''); L124: const errorsSignup = ref([]); L125: const loading = ref(false); L131: const submitFormSignup = async () => {; L177: const response = await usersAccountsAPI.signup({; L219: const data = err.response.data
- Imports (first five): import { ref } from 'vue'; import { usersAccountsAPI } from '@/services/Accounts/usersAccounts'
- Consumers: direct route/import references are listed where identified; no full call graph.

