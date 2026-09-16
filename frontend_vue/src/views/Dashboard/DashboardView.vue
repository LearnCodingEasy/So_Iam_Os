<template>
  <div class="dashboard">
    <section class="welcome-row">
      <div>
        <div class="eyebrow">FRIDAY · 21 AUGUST 2026</div>
        <h2>أهلاً يا حسام 👋</h2>
        <p>النظام لاقط فرص جديدة مناسبة لمهاراتك. خلينا نشوف أهم الفرص النهارده.</p>
      </div>

      <button class="primary-btn">+ تشغيل بحث جديد</button>
    </section>

    <section class="stats-grid">
      <StatCard label="إجمالي الفرص" value="1,284" change="+18.4%" icon="◈" />
      <StatCard label="فرص مناسبة" value="327" change="+12.8%" icon="◎" />
      <StatCard label="طلبات التقديم" value="42" change="+6.2%" icon="✓" />
      <StatCard label="متوسط Match Score" value="87%" change="+4.6%" icon="✦" />
    </section>

    <section class="content-grid">
      <div class="panel performance-panel">
        <div class="panel-header">
          <div>
            <h3>أداء الفرص</h3>
            <span>آخر 30 يوم</span>
          </div>
          <button class="ghost-btn">آخر 30 يوم⌄</button>
        </div>

        <div class="chart-legend">
          <span><i class="dot purple"></i> الفرص المكتشفة</span>
          <span><i class="dot green"></i> الفرص المناسبة</span>
        </div>

        <div class="chart">
          <div
            v-for="line in gridLines"
            :key="line"
            class="grid-line"
            :style="{ top: line + '%' }"
          ></div>
          <svg viewBox="0 0 700 260" preserveAspectRatio="none" class="chart-svg">
            <polyline
              :points="purplePoints"
              fill="none"
              stroke="currentColor"
              stroke-width="4"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <polyline
              :points="greenPoints"
              fill="none"
              stroke="currentColor"
              stroke-width="4"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <div class="chart-labels">
            <span>01 أغسطس</span>
            <span>08 أغسطس</span>
            <span>15 أغسطس</span>
            <span>22 أغسطس</span>
            <span>29 أغسطس</span>
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div>
            <h3>أفضل الفرص اليوم</h3>
            <span>مرتبة حسب الـ Match Score</span>
          </div>
          <button class="text-btn">عرض الكل</button>
        </div>

        <div class="opportunity-list">
          <OpportunityRow
            title="Senior Vue.js Developer"
            company="TechFlow"
            score="96%"
            salary="$2,500 – $4,000"
            icon="V"
          />
          <OpportunityRow
            title="Django Backend Engineer"
            company="CloudStack"
            score="92%"
            salary="$2,000 – $3,500"
            icon="D"
          />
          <OpportunityRow
            title="Full Stack Developer"
            company="Nova Labs"
            score="88%"
            salary="$1,800 – $3,000"
            icon="N"
          />
          <OpportunityRow
            title="AI Web Developer"
            company="FutureCode"
            score="84%"
            salary="$2,200 – $3,800"
            icon="AI"
          />
        </div>
      </div>
    </section>

    <section class="content-grid lower-grid">
      <div class="panel">
        <div class="panel-header">
          <div>
            <h3>الفرص المقترحة ليك</h3>
            <span>AI Matching Engine</span>
          </div>
          <button class="text-btn">عرض الكل</button>
        </div>

        <div class="recommendation-grid">
          <Recommendation
            title="تطوير تطبيق ويب"
            company="Digital Studio"
            score="95%"
            tags="Vue.js · Django · REST"
          />
          <Recommendation
            title="Full Stack Engineer"
            company="Remote Labs"
            score="91%"
            tags="Python · Vue.js · PostgreSQL"
          />
          <Recommendation
            title="AI Web Integration"
            company="AI Factory"
            score="87%"
            tags="LLM · APIs · JavaScript"
          />
        </div>
      </div>

      <div class="panel skills-panel">
        <div class="panel-header">
          <div>
            <h3>مهاراتك</h3>
            <span>مستوى الإتقان الحالي</span>
          </div>
          <button class="text-btn">تعديل</button>
        </div>

        <SkillBar name="HTML / CSS" value="95" />
        <SkillBar name="JavaScript" value="90" />
        <SkillBar name="Vue.js" value="88" />
        <SkillBar name="Django" value="84" />
        <SkillBar name="Python" value="80" />
      </div>
    </section>

    <section class="ai-banner">
      <div class="ai-orb">✦</div>
      <div class="ai-copy">
        <div class="ai-title">المساعد الذكي جاهز 🤖</div>
        <p>اسألني عن أفضل الفرص، المهارات الناقصة، أو إزاي تزود الـ Match Score بتاعك.</p>
      </div>
      <button class="secondary-btn">اسأل المساعد</button>
    </section>
  </div>
</template>

<script setup>
import StatCard from '@/components/AI/dashboard/StatCard.vue'
import OpportunityRow from '@/components/AI/dashboard/OpportunityRow.vue'
import Recommendation from '@/components/AI/dashboard/Recommendation.vue'
import SkillBar from '@/components/AI/dashboard/SkillBar.vue'

const gridLines = [10, 35, 60, 85]

const purplePoints =
  '0,190 60,160 120,175 180,110 240,145 300,125 360,155 420,85 480,115 540,75 600,110 660,65 700,85'

const greenPoints =
  '0,220 60,205 120,215 180,190 240,198 300,175 360,185 420,150 480,160 540,125 600,145 660,105 700,120'
</script>
