<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { languages, sets } from './cards.js'
import CardArt from './CardArt.vue'

const lang = ref(navigator.language.startsWith('zh') ? 'zh' : navigator.language.startsWith('es') ? 'es' : 'en')
const setIdx = ref(0)
const cardIdx = ref(0)

const set = computed(() => sets[setIdx.value])
const card = computed(() => set.value.cards[cardIdx.value])
const langMeta = computed(() => languages.find(l => l.code === lang.value))

const voices = ref([])
function refreshVoices() { voices.value = speechSynthesis.getVoices() }
onMounted(() => {
  refreshVoices()
  speechSynthesis.onvoiceschanged = refreshVoices
  window.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') swipe(1)
    if (e.key === 'ArrowRight') swipe(-1)
  })
})

function speak() {
  const u = new SpeechSynthesisUtterance(card.value.word[lang.value])
  u.lang = langMeta.value.tts
  const v = voices.value.find(v => v.lang.toLowerCase().startsWith(u.lang.toLowerCase()))
  if (v) u.voice = v
  speechSynthesis.cancel()
  speechSynthesis.speak(u)
}
watch(() => card.value.word[lang.value], speak, { immediate: true })

const pose = ref('idle')
const dx = ref(0)
const dy = ref(0)
const busy = ref(false)
const moved = ref(false)
let sx = 0, sy = 0, lx = 0, lt = 0

function down(e) {
  if (busy.value || pose.value !== 'idle') return
  e.currentTarget.setPointerCapture(e.pointerId)
  sx = lx = e.clientX; sy = e.clientY; lt = performance.now()
  dx.value = 0; dy.value = 0; moved.value = false
  pose.value = 'drag'
}
function move(e) {
  if (pose.value !== 'drag') return
  dx.value = e.clientX - sx
  dy.value = e.clientY - sy
  if (Math.abs(dx.value) > 6 || Math.abs(dy.value) > 6) moved.value = true
  lx = e.clientX; lt = performance.now()
}
function up(e) {
  if (pose.value !== 'drag') return
  if (!moved.value) { pose.value = 'idle'; speak(); return }
  const vx = (e.clientX - lx) / Math.max(1, performance.now() - lt) * 1000
  if (Math.abs(dx.value) >= 90 || Math.abs(vx) >= 700) swipe(-(Math.sign(dx.value) || Math.sign(vx)))
  else { dx.value = 0; dy.value = 0; pose.value = 'idle' }
}
function swipe(dir) {
  if (busy.value || !dir) return
  busy.value = true
  pose.value = dir > 0 ? 'flyL' : 'flyR'
  setTimeout(() => {
    cardIdx.value = (cardIdx.value + dir + set.value.cards.length) % set.value.cards.length
    dx.value = 0; dy.value = 0
    pose.value = dir > 0 ? 'enterL' : 'enterR'
    requestAnimationFrame(() => requestAnimationFrame(() => { pose.value = 'idle'; busy.value = false }))
  }, 400)
}
function pickSet(i) {
  if (busy.value) return
  setIdx.value = i
  cardIdx.value = 0
}

const cardStyle = computed(() => {
  const p = pose.value
  if (p === 'drag') return { transform: `translate(${dx.value}px, ${dy.value * 0.4}px) rotate(${dx.value * 0.08}deg)` }
  if (p === 'flyR') return { transform: `translate(130%, ${dy.value * 0.5}px) rotate(28deg)` }
  if (p === 'flyL') return { transform: `translate(-130%, ${dy.value * 0.5}px) rotate(-28deg)` }
  return {}
})
</script>

<template>
  <main>
    <header>
      <h1>Little Cards <span class="heart">♥</span></h1>
      <nav class="langs" aria-label="Language">
        <button v-for="l in languages" :key="l.code" :class="{ on: lang === l.code }" @click="lang = l.code">{{ l.name }}</button>
      </nav>
    </header>

    <nav class="sets" aria-label="Card set">
      <button v-for="(s, i) in sets" :key="s.id" :class="{ on: i === setIdx }" @click="pickSet(i)">{{ s.name[lang] }}</button>
    </nav>

    <div class="stage" @pointerdown="down" @pointermove="move" @pointerup="up" @pointercancel="up">
      <button class="card" :class="pose" :style="cardStyle" aria-label="Hear the word spoken" @click="e => e.detail === 0 && speak()">
        <CardArt :art="card.art" class="art" />
        <div class="word">{{ card.word[lang] }}</div>
        <svg class="speaker" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor" />
          <path d="M16 8a5 5 0 0 1 0 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
      </button>
    </div>

    <p class="count">{{ cardIdx + 1 }} / {{ set.cards.length }}</p>
  </main>
</template>

<style>
:root {
  color-scheme: light dark;
  --bg: light-dark(#fbf3e8, #171526);
  --card: light-dark(#fffdf7, #241f38);
  --ink: light-dark(#6b543f, #f0e9db);
  --ink-soft: light-dark(#a08a72, #8f8176);
  --chip: light-dark(#efe3d0, #37304f);
  --chip-on: light-dark(#e8a87c, #b97f57);
  --chip-on-text: #fff;
  --outline: light-dark(#e5d5bf, #3a3455);
  --heart: light-dark(#f28f92, #d56a6e);
}

* { box-sizing: border-box; }
body { margin: 0; min-height: 100vh; background: var(--bg); color: var(--ink); font-family: ui-rounded, "SF Pro Rounded", "Nunito", "Segoe UI", system-ui, sans-serif; }
main { max-width: 560px; margin: 0 auto; padding: 20px 16px 36px; display: flex; flex-direction: column; align-items: center; gap: 14px; user-select: none; -webkit-tap-highlight-color: transparent; }
h1 { margin: 0; font-size: 1.35rem; font-weight: 700; letter-spacing: .02em; }
.heart { color: var(--heart); }
header { width: 100%; display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap; }
nav { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
button { font: inherit; cursor: pointer; border: none; }
.langs button, .sets button { padding: 8px 16px; border-radius: 999px; background: var(--chip); color: var(--ink); font-weight: 600; }
.langs button.on, .sets button.on { background: var(--chip-on); color: var(--chip-on-text); }

.stage { position: relative; width: min(420px, 92vw, 46vh); aspect-ratio: 3 / 4; touch-action: none; }
.card { position: absolute; inset: 0; width: 100%; height: 100%; background: var(--card); border: 1.5px solid var(--outline); border-radius: 40px; box-shadow: 0 16px 40px rgb(0 0 0 / .14); padding: 6%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3%; touch-action: none; will-change: transform; transition: transform .38s cubic-bezier(.22, 1.35, .36, 1); }
.card.drag { transition: none; }
.card.flyL, .card.flyR { transition: transform .4s cubic-bezier(.3, .7, .25, 1); }
.card.enterL, .card.enterR { transition: none; }
.card.enterR { transform: translate(65%, 0) rotate(10deg); }
.card.enterL { transform: translate(-65%, 0) rotate(-10deg); }
.art { width: 92%; display: block; }
.word { font-size: clamp(2.6rem, 9vw, 3.5rem); font-weight: 800; letter-spacing: .02em; }
.speaker { position: absolute; top: 18px; right: 18px; width: 24px; height: 24px; color: var(--ink-soft); }
.count { margin: 0; color: var(--ink-soft); font-weight: 600; }
</style>
