<script setup>
import { computed } from 'vue'

const props = defineProps({
  review: {
    type: Object,
    default: null,
  },
})

const score = computed(() => {
  return Number(props.review?.score || 0)
})

const scoreClass = computed(() => {
  if (score.value >= 90) {
    return 'excellent'
  }

  if (score.value >= 70) {
    return 'good'
  }

  if (score.value >= 50) {
    return 'developing'
  }

  return 'needs-work'
})

const list = (value) => {
  return Array.isArray(value) ? value : []
}
</script>

<template>
  <section v-if="review" class="ai-review">
    <header class="review-header">
      <div>
        <span class="section-kicker"> AI EVALUATION </span>

        <h2>Application Review</h2>
      </div>

      <div class="review-score" :class="scoreClass">
        <strong>
          {{ score }}
        </strong>

        <span> / 100 </span>
      </div>
    </header>

    <div class="mastery-row">
      <span> Mastery </span>

      <strong>
        {{ review.mastery_level }}
      </strong>
    </div>

    <div class="review-grid">
      <!-- Understood -->
      <article class="review-section">
        <h3>What you understood</h3>

        <ul>
          <li v-for="(item, index) in list(review.understood)" :key="index">
            {{ typeof item === 'object' ? item.description : item }}
          </li>

          <li v-if="!list(review.understood).length">No data.</li>
        </ul>
      </article>

      <!-- Applied -->
      <article class="review-section">
        <h3>What you applied</h3>

        <ul>
          <li v-for="(item, index) in list(review.applied)" :key="index">
            {{ typeof item === 'object' ? item.description : item }}
          </li>

          <li v-if="!list(review.applied).length">No data.</li>
        </ul>
      </article>

      <!-- Strengths -->
      <article class="review-section">
        <h3>Strengths</h3>

        <ul>
          <li v-for="(item, index) in list(review.strengths)" :key="index">
            {{ typeof item === 'object' ? item.description : item }}
          </li>
        </ul>
      </article>

      <!-- Weaknesses -->
      <article class="review-section warning">
        <h3>Weaknesses</h3>

        <ul>
          <li v-for="(item, index) in list(review.weaknesses)" :key="index">
            {{ typeof item === 'object' ? item.description : item }}
          </li>
        </ul>
      </article>

      <!-- Errors -->
      <article v-if="list(review.errors).length" class="review-section error">
        <h3>Errors</h3>

        <ul>
          <li v-for="(item, index) in list(review.errors)" :key="index">
            {{
              typeof item === 'object'
                ? `${item.description}${item.severity ? ` (${item.severity})` : ''}`
                : item
            }}
          </li>
        </ul>
      </article>

      <!-- Review -->
      <article v-if="list(review.needs_review).length" class="review-section review-needed">
        <h3>Needs Review</h3>

        <ul>
          <li v-for="(item, index) in list(review.needs_review)" :key="index">
            {{ typeof item === 'object' ? item.description : item }}
          </li>
        </ul>
      </article>
    </div>

    <div v-if="review.feedback" class="review-feedback">
      <span> AI Feedback </span>

      <p>
        {{ review.feedback }}
      </p>
    </div>
  </section>
</template>

<style scoped>
.ai-review {
  margin-top: 28px;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 18px;
  padding: 24px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.review-header h2 {
  margin: 5px 0;
}

.review-score {
  display: flex;
  align-items: baseline;
  gap: 3px;
}

.review-score strong {
  font-size: 42px;
  line-height: 1;
}

.review-score span {
  opacity: 0.5;
}

.review-score.excellent,
.review-score.good {
  font-weight: 800;
}

.review-score.developing {
  opacity: 0.75;
}

.review-score.needs-work {
  opacity: 0.6;
}

.mastery-row {
  display: flex;
  gap: 10px;
  margin: 22px 0;
  padding: 12px 14px;
  border-radius: 10px;
  background: rgba(127, 127, 127, 0.07);
}

.mastery-row span {
  opacity: 0.55;
}

.mastery-row strong {
  text-transform: capitalize;
}

.review-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.review-section {
  padding: 18px;
  border-radius: 12px;
  background: rgba(127, 127, 127, 0.05);
}

.review-section h3 {
  margin: 0 0 12px;
  font-size: 14px;
}

.review-section ul {
  margin: 0;
  padding-left: 18px;
}

.review-section li {
  margin-bottom: 7px;
  opacity: 0.75;
  line-height: 1.5;
}

.review-section.warning {
  background: rgba(200, 150, 50, 0.08);
}

.review-section.error {
  background: rgba(200, 50, 50, 0.08);
}

.review-section.review-needed {
  background: rgba(80, 130, 220, 0.08);
}

.review-feedback {
  margin-top: 16px;
  padding: 18px;
  border-left: 3px solid currentColor;
  background: rgba(127, 127, 127, 0.05);
}

.review-feedback span {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.12em;
  opacity: 0.5;
}

.review-feedback p {
  margin: 8px 0 0;
  line-height: 1.7;
}

@media (max-width: 700px) {
  .review-grid {
    grid-template-columns: 1fr;
  }
}
</style>
