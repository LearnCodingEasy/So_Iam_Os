# social workflows

## Routed screens and source evidence

- Route /social (social) is declared at router/index.js:L198; metadata: requiresAuth.

### views/social/SocialView.vue
import { onMounted, ref } from 'vue'
import { getRecommendations, getSocialProfile, updateSocialProfile, sendFriendRequest } from '@/services/Social/social'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
