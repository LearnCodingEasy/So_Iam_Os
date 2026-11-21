# learning workflows

## Routed screens and source evidence

- Route /learning (learning) is declared at router/index.js:L127; metadata: requiresAuth.
- Route /learning/topics/:topicId (learning-topic) is declared at router/index.js:L135; metadata: requiresAuth.

### views/learning/LearningTopic.vue
import { computed, onMounted, ref } from 'vue'
import api from '@/services/Shared/api'
import { endpoints } from '@/services/Shared/endpoints'
import { RouterLink, useRoute } from 'vue-router'
import {
import ApplicationComposer from '@/components/learning/ApplicationComposer.vue'
import AIReviewPanel from '@/components/learning/AIReviewPanel.vue'

### views/learning/LearningView.vue
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { getLearningDashboard, updateLearningProgress, pauseLearningGoal, resumeLearningGoal } from '@/services/Learning/learning'
import LearningPathEditor from '@/components/learning/LearningPathEditor.vue'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
