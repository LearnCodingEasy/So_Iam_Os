<script setup>
// Original inline-SVG illustrations (no external images). Colors come from design-system CSS variables.
import { useId } from 'vue'

defineProps({ kind: { type: String, default: 'dashboard' } })
// Unique gradient id per instance so a hidden (display:none) copy cannot break the others.
const gid = `ds-g-${useId()}`
const grad = `url(#${gid})`
</script>

<template>
  <svg
    class="ds-illus"
    viewBox="0 0 240 180"
    role="img"
    aria-hidden="true"
    xmlns="http://www.w3.org/2000/svg"
  >
    <defs>
      <linearGradient :id="gid" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="var(--ds-accent-1)" />
        <stop offset="1" stop-color="var(--ds-accent-2)" />
      </linearGradient>
    </defs>
    <ellipse cx="120" cy="160" rx="82" ry="9" class="ds-illus__shadow" />

    <!-- goals: target + arrow -->
    <g v-if="kind === 'goals'">
      <circle cx="120" cy="82" r="62" class="ds-illus__soft" />
      <circle cx="120" cy="82" r="46" fill="none" :stroke="grad" stroke-width="10" />
      <circle
        cx="120"
        cy="82"
        r="28"
        fill="none"
        stroke="var(--ds-accent-2)"
        stroke-width="8"
        opacity=".55"
      />
      <circle cx="120" cy="82" r="10" :fill="grad" />
      <path d="M120 82 L186 24" stroke="var(--ds-ink)" stroke-width="5" stroke-linecap="round" />
      <path d="M176 22 L190 20 L188 34 Z" fill="var(--ds-ink)" />
      <g class="ds-illus__float">
        <rect x="24" y="104" width="46" height="14" rx="7" class="ds-illus__chip" />
        <rect x="170" y="112" width="44" height="14" rx="7" class="ds-illus__chip" />
      </g>
    </g>

    <!-- finance: coins + bars -->
    <g v-else-if="kind === 'finance'">
      <rect x="40" y="96" width="26" height="52" rx="6" fill="var(--ds-accent-2)" opacity=".55" />
      <rect x="78" y="72" width="26" height="76" rx="6" fill="var(--ds-accent-1)" opacity=".75" />
      <rect x="116" y="48" width="26" height="100" rx="6" :fill="grad" />
      <path
        d="M40 70 L90 50 L130 30 L196 18"
        fill="none"
        stroke="var(--ds-ink)"
        stroke-width="4"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <g class="ds-illus__float">
        <circle cx="178" cy="104" r="26" :fill="grad" />
        <circle
          cx="178"
          cy="104"
          r="18"
          fill="none"
          stroke="#fff"
          stroke-opacity=".7"
          stroke-width="4"
        />
        <path
          d="M178 94v20M172 99h9a4 4 0 010 8h-9"
          stroke="#fff"
          stroke-width="3.5"
          fill="none"
          stroke-linecap="round"
        />
      </g>
    </g>

    <!-- learning: book + path -->
    <g v-else-if="kind === 'learning'">
      <path d="M40 64 Q80 50 120 66 V142 Q80 126 40 140 Z" fill="var(--ds-accent-2)" opacity=".5" />
      <path d="M200 64 Q160 50 120 66 V142 Q160 126 200 140 Z" :fill="grad" />
      <path d="M120 66 V142" stroke="var(--ds-ink)" stroke-width="3" />
      <g class="ds-illus__float">
        <path d="M120 18 L150 32 L120 46 L90 32 Z" fill="var(--ds-ink)" />
        <path
          d="M104 40 V52 Q120 60 136 52 V40"
          fill="none"
          stroke="var(--ds-ink)"
          stroke-width="4"
        />
      </g>
    </g>

    <!-- ai: network -->
    <g v-else-if="kind === 'ai'">
      <g stroke="var(--ds-accent-2)" stroke-width="3" opacity=".6">
        <line x1="120" y1="84" x2="52" y2="42" />
        <line x1="120" y1="84" x2="190" y2="40" />
        <line x1="120" y1="84" x2="60" y2="130" />
        <line x1="120" y1="84" x2="188" y2="128" />
      </g>
      <circle cx="120" cy="84" r="30" :fill="grad" />
      <path d="M120 66 l5 12 12 5 -12 5 -5 12 -5 -12 -12 -5 12 -5 z" fill="#fff" />
      <g class="ds-illus__float">
        <circle cx="52" cy="42" r="12" class="ds-illus__chip" />
        <circle cx="190" cy="40" r="14" class="ds-illus__chip" />
        <circle cx="60" cy="130" r="14" class="ds-illus__chip" />
        <circle cx="188" cy="128" r="12" class="ds-illus__chip" />
      </g>
    </g>

    <!-- tasks: checklist -->
    <g v-else-if="kind === 'tasks'">
      <rect x="64" y="22" width="112" height="132" rx="14" class="ds-illus__card" />
      <g v-for="(y, i) in [50, 82, 114]" :key="y">
        <rect
          x="80"
          :y="y - 10"
          width="20"
          height="20"
          rx="6"
          :fill="i < 2 ? grad : 'none'"
          :stroke="i < 2 ? 'none' : 'var(--ds-accent-2)'"
          stroke-width="3"
        />
        <path
          v-if="i < 2"
          :d="`M85 ${y} l5 5 8 -9`"
          stroke="#fff"
          stroke-width="3.5"
          fill="none"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <rect
          x="110"
          :y="y - 5"
          :width="i === 1 ? 44 : 52"
          height="10"
          rx="5"
          class="ds-illus__chip"
        />
      </g>
    </g>

    <!-- jobs / projects: briefcase -->
    <g v-else-if="kind === 'jobs' || kind === 'projects'">
      <rect x="52" y="62" width="136" height="86" rx="14" :fill="grad" />
      <path
        d="M96 62 V50 a8 8 0 018-8 h32 a8 8 0 018 8 V62"
        fill="none"
        stroke="var(--ds-ink)"
        stroke-width="6"
      />
      <rect x="52" y="96" width="136" height="8" fill="#fff" opacity=".35" />
      <rect x="108" y="90" width="24" height="20" rx="5" fill="var(--ds-ink)" />
      <g class="ds-illus__float"><circle cx="196" cy="40" r="12" class="ds-illus__chip" /></g>
    </g>

    <!-- knowledge: layered cards -->
    <g v-else-if="kind === 'knowledge'">
      <rect
        x="62"
        y="30"
        width="116"
        height="84"
        rx="12"
        fill="var(--ds-accent-2)"
        opacity=".35"
        transform="rotate(-6 120 72)"
      />
      <rect
        x="62"
        y="44"
        width="116"
        height="84"
        rx="12"
        fill="var(--ds-accent-1)"
        opacity=".55"
        transform="rotate(3 120 86)"
      />
      <rect x="62" y="56" width="116" height="84" rx="12" class="ds-illus__card" />
      <rect x="80" y="76" width="80" height="9" rx="4.5" :fill="grad" />
      <rect x="80" y="96" width="60" height="8" rx="4" class="ds-illus__chip" />
      <rect x="80" y="114" width="70" height="8" rx="4" class="ds-illus__chip" />
    </g>

    <!-- empty -->
    <g v-else-if="kind === 'empty'">
      <path
        d="M52 78 L120 52 L188 78 V132 L120 158 L52 132 Z"
        fill="var(--ds-accent-2)"
        opacity=".28"
      />
      <path
        d="M52 78 L120 104 L188 78 M120 104 V158"
        fill="none"
        stroke="var(--ds-accent-1)"
        stroke-width="5"
        stroke-linejoin="round"
      />
      <g class="ds-illus__float">
        <circle cx="120" cy="36" r="9" :fill="grad" />
        <circle cx="166" cy="46" r="5" class="ds-illus__chip" />
        <circle cx="78" cy="42" r="5" class="ds-illus__chip" />
      </g>
    </g>

    <!-- error -->
    <g v-else-if="kind === 'error'">
      <path
        d="M120 24 L202 148 H38 Z"
        fill="var(--ds-danger)"
        opacity=".16"
        stroke="var(--ds-danger)"
        stroke-width="6"
        stroke-linejoin="round"
      />
      <rect x="114" y="68" width="12" height="46" rx="6" fill="var(--ds-danger)" />
      <circle cx="120" cy="130" r="7.5" fill="var(--ds-danger)" />
    </g>

    <!-- default: dashboard -->
    <g v-else>
      <rect x="34" y="28" width="172" height="118" rx="16" class="ds-illus__card" />
      <rect x="34" y="28" width="172" height="26" rx="16" :fill="grad" />
      <rect x="50" y="72" width="38" height="58" rx="7" fill="var(--ds-accent-2)" opacity=".55" />
      <rect x="98" y="88" width="38" height="42" rx="7" fill="var(--ds-accent-1)" opacity=".75" />
      <rect x="146" y="64" width="38" height="66" rx="7" :fill="grad" />
      <g class="ds-illus__float"><circle cx="206" cy="30" r="10" class="ds-illus__chip" /></g>
    </g>
  </svg>
</template>
