<template>
  <div
    class="flex min-h-[360px] flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center dark:border-slate-700 dark:bg-slate-900"
  >
    <div
      class="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-indigo-50 text-2xl text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400"
    >
      🧠
    </div>

    <h3 class="mb-2 text-lg font-semibold text-slate-900 dark:text-white">
      Your knowledge base is empty
    </h3>

    <p class="max-w-md text-sm leading-6 text-slate-500 dark:text-slate-400">
      Start capturing notes, ideas, documentation, learning resources, project information, and
      anything you want So_Iam_OS to understand.
    </p>

    <button
      type="button"
      class="mt-6 rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-700"
      @click="$emit('create')"
    >
      Add your first knowledge
    </button>
  </div>
</template>
