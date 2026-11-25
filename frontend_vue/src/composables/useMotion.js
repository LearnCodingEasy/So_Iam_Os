// Motion helpers built on GSAP (already a dependency).
// Rules: respect prefers-reduced-motion, never animate form inputs, always clean up.
import { onBeforeUnmount, onMounted, unref } from 'vue'
import { gsap } from 'gsap'

export function prefersReducedMotion() {
  try {
    return window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false
  } catch {
    return false
  }
}

const INTERACTIVE = 'input, textarea, select, .p-inputtext, .p-select, .p-datepicker, .p-editor'

/**
 * Staggered entrance for the direct children (or `selector` matches) of a root element.
 * Returns a gsap.Context so callers can revert() it. Safe under reduced motion (no-op).
 */
export function revealChildren(
  root,
  { selector = ':scope > *', y = 14, stagger = 0.06, duration = 0.5, delay = 0 } = {},
) {
  if (!root || prefersReducedMotion()) return null
  const ctx = gsap.context(() => {
    const targets = Array.from(root.querySelectorAll(selector)).filter(
      (el) => !el.matches(INTERACTIVE),
    )
    if (!targets.length) return
    gsap.from(targets, {
      opacity: 0,
      y,
      duration,
      delay,
      stagger,
      ease: 'power2.out',
      clearProps: 'opacity,transform', // leave no inline styles behind (keeps PrimeVue / Vue in control)
    })
  }, root)
  return ctx
}

/** Composable: reveal children of a template ref on mount; reverts on unmount. */
export function useReveal(targetRef, options = {}) {
  let ctx = null
  onMounted(() => {
    const el = unref(targetRef)
    el && (ctx = revealChildren(el instanceof Element ? el : el.$el, options))
  })
  onBeforeUnmount(() => ctx?.revert())
}

/** Tween a number; returns a kill function. Under reduced motion it jumps to the end value. */
export function tweenNumber(from, to, onUpdate, { duration = 0.9, decimals = 0 } = {}) {
  if (prefersReducedMotion() || from === to) {
    onUpdate(to)
    return () => {}
  }
  const state = { v: from }
  const tween = gsap.to(state, {
    v: to,
    duration,
    ease: 'power2.out',
    onUpdate: () => onUpdate(Number(state.v.toFixed(decimals))),
    onComplete: () => onUpdate(to),
  })
  return () => tween.kill()
}

export { gsap }
