<script setup>
import { computed } from 'vue'

const props = defineProps({ art: { type: [String, Object], required: true } })
const assets = import.meta.glob('./assets/*.svg', { eager: true, import: 'default', query: '?url' })

const name = computed(() => typeof props.art === 'string'
  ? props.art
  : 'n' in props.art ? `number-${props.art.n}` : `color-${props.art.c}`)
const src = computed(() => assets[`./assets/${name.value}.svg`])
</script>

<template>
  <img :src="src" alt="" />
</template>
