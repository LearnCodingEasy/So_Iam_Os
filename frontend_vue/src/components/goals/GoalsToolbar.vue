<template>
  <section class="goals-toolbar">
    <span class="p-input-icon-left search-control">
      <i class="pi pi-search" />
      <prime_input_text
        :modelValue="search"
        @update:modelValue="$emit('update:search', $event)"
        placeholder="ابحث بالعنوان أو الوصف"
      />
    </span>
    <prime_select
      :modelValue="statusFilter"
      @update:modelValue="$emit('update:statusFilter', $event)"
      :options="statusOptions"
      option-label="label"
      option-value="value"
      placeholder="كل الحالات"
      show-clear
    />
    <prime_select
      :modelValue="categoryFilter"
      @update:modelValue="$emit('update:categoryFilter', $event)"
      :options="categoryOptions"
      option-label="label"
      option-value="value"
      placeholder="كل التصنيفات"
      show-clear
    />
    <prime_select
      :modelValue="sortBy"
      @update:modelValue="$emit('update:sortBy', $event)"
      :options="sortOptions"
      option-label="label"
      option-value="value"
    />
  </section>
</template>

<script setup>
defineProps({
  search: String,
  statusFilter: [String, null],
  categoryFilter: [String, null],
  sortBy: String,
  statusOptions: Array,
  categoryOptions: Array,
  sortOptions: Array,
})

defineEmits(['update:search', 'update:statusFilter', 'update:categoryFilter', 'update:sortBy'])
</script>
