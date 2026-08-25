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
    if (e.key === 'ArrowLeft') swipe(1) // left = next, mirrors swipe
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

/* ── tinder-style swipe ── */
const pose = ref('idle') // idle | drag | flyL | flyR | enterL | enterR
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
  if (!moved.value) { pose.value = 'idle'; speak(); return } // tap → read the word
  const vx = (e.clientX - lx) / Math.max(1, performance.now() - lt) * 1000
  if (Math.abs(dx.value) >= 90 || Math.abs(vx) >= 700) swipe(-(Math.sign(dx.value) || Math.sign(vx))) // left swipe = next
  else { dx.value = 0; dy.value = 0; pose.value = 'idle' } // spring back
}
function swipe(dir) {
  if (busy.value || !dir) return
  busy.value = true
  pose.value = dir > 0 ? 'flyL' : 'flyR' // dir = nav delta; card travels toward -dir
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

    <div
      class="stage"
      @pointerdown="down" @pointermove="move" @pointerup="up" @pointercancel="up"
    >
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
/* gentle palette — light-dark() keeps everything readable in both modes */
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
  --c-apple: light-dark(#f5a09a, #d97e76);
  --c-banana: light-dark(#f7d774, #e2b64e);
  --c-orange: light-dark(#f8b46e, #e09a52);
  --c-straw: light-dark(#f28f92, #d56a6e);
  --c-grape: light-dark(#b9a3db, #937bc0);
  --c-leaf: light-dark(#9ec98f, #79a76c);
  --c-stem: light-dark(#b98a6a, #a37a5d);
  --c-line: light-dark(#96745a, #8c6f5b);
  --c-tip: light-dark(#8f6a4e, #7c5c45);
  --c-seed: light-dark(#fdf3ec, #f0dcc6);
  --c-hi: light-dark(rgba(255, 255, 255, .65), rgba(255, 255, 255, .16));
  --c-shadow: light-dark(rgba(122, 82, 50, .10), rgba(0, 0, 0, .38));
  --c-eyes: light-dark(#5f4b3b, #2b2536);
  --c-pink: light-dark(#e8a0a0, #c98181);
  --c-cat: light-dark(#e6ded2, #948a80);
  --c-dog: light-dark(#eed9b8, #b39468);
  --c-dog-ear: light-dark(#d9bd96, #96764f);
  --c-dog-patch: light-dark(#fbf0df, #c9b393);
  --c-bunny: light-dark(#ecd5d8, #b9a5a3);
  --c-bird: light-dark(#a3c8ec, #6f95c4);
  --c-bird-wing: light-dark(#8fb4dc, #5c82b0);
  --c-fish: light-dark(#f7c37c, #db994f);
  --c-fish-fin: light-dark(#e8a95f, #c98a47);
  --c-elephant: light-dark(#bfb2e0, #8778b5);
  --c-red: light-dark(#ef8e83, #d4695d);
  --c-blue: light-dark(#a3c8ec, #6f95c4);
  --c-yellow: light-dark(#f6d76c, #dfb14c);
  --c-green: light-dark(#9ec98f, #79a76c);
  --c-purple: light-dark(#b9a3db, #937bc0);
  --n1: light-dark(#fbe9b4, #6d5c2e);
  --n2: light-dark(#cdeeda, #38614a);
  --n3: light-dark(#fde0bd, #6e4c2c);
  --n4: light-dark(#e6dcf7, #4d4170);
  --n5: light-dark(#d2ecf9, #365f7b);
  --n6: light-dark(#f6d3e0, #6b3c50);
  --n7: light-dark(#cfe8e3, #37605a);
  --n8: light-dark(#f3ead0, #685e34);
  --n9: light-dark(#d6d9f4, #3f4374);
  --n10: light-dark(#fbd9c7, #6b4636);
  --num-ink: light-dark(#7a6248, #f6efe2);
}

* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  background: var(--bg);
  color: var(--ink);
  font-family: ui-rounded, "SF Pro Rounded", "Nunito", "Segoe UI", system-ui, sans-serif;
}
main {
  max-width: 560px;
  margin: 0 auto;
  padding: 20px 16px 36px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}
h1 { margin: 0; font-size: 1.35rem; font-weight: 700; letter-spacing: .02em; }
.heart { color: var(--c-straw); }
header { width: 100%; display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap; }
nav { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
button { font: inherit; cursor: pointer; border: none; }
.langs button, .sets button { padding: 8px 16px; border-radius: 999px; background: var(--chip); color: var(--ink); font-weight: 600; }
.langs button.on, .sets button.on { background: var(--chip-on); color: var(--chip-on-text); }

/* ── tinder-style stage ── */
.stage {
  position: relative;
  width: min(420px, 92vw, 46vh); /* aspect 3/4 → height = 62vh */
  aspect-ratio: 3 / 4;
  touch-action: none;
}
.card {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  background: var(--card);
  border: 1.5px solid var(--outline);
  border-radius: 40px;
  box-shadow: 0 16px 40px rgb(0 0 0 / .14);
  padding: 6%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3%;
  touch-action: none;
  will-change: transform;
  transition: transform .38s cubic-bezier(.22, 1.35, .36, 1); /* spring back */
}
.card.drag { transition: none; }
.card.flyL, .card.flyR { transition: transform .4s cubic-bezier(.3, .7, .25, 1); }
.card.enterL, .card.enterR { transition: none; }
.card.enterR { transform: translate(65%, 0) rotate(10deg); }
.card.enterL { transform: translate(-65%, 0) rotate(-10deg); }
.art { width: 92%; }
.word { font-size: clamp(2.6rem, 9vw, 3.5rem); font-weight: 800; letter-spacing: .02em; }
.speaker { position: absolute; top: 18px; right: 18px; width: 24px; height: 24px; color: var(--ink-soft); }
.count { margin: 0; color: var(--ink-soft); font-weight: 600; }

/* ── SVG art fills ── */
.shadow { fill: var(--c-shadow); }
.c-apple  { fill: var(--c-apple);  stroke: var(--c-line); stroke-width: 2.5; stroke-linejoin: round; }
.c-banana { fill: var(--c-banana); stroke: var(--c-line); stroke-width: 2.5; stroke-linejoin: round; }
.c-orange { fill: var(--c-orange); stroke: var(--c-line); stroke-width: 2.5; }
.c-straw  { fill: var(--c-straw);  stroke: var(--c-line); stroke-width: 2.5; stroke-linejoin: round; }
.c-grape  { fill: var(--c-grape);  stroke: var(--c-line); stroke-width: 2.5; }
.c-leaf   { fill: var(--c-leaf);   stroke: var(--c-line); stroke-width: 2; }
.c-stem   { stroke: var(--c-stem); }
.c-tip    { fill: var(--c-tip); }
.c-ridge  { fill: none; stroke: var(--c-line); stroke-width: 2; opacity: .45; stroke-linecap: round; }
.c-dimple { fill: var(--c-line); opacity: .35; }
.c-seed   { fill: var(--c-seed); }
.hi       { fill: var(--c-hi); }
.c-eyes   { fill: var(--c-eyes); }
.c-eyeline { fill: none; stroke: var(--c-eyes); stroke-width: 4.5; stroke-linecap: round; }
.c-whisker { fill: none; stroke: var(--c-eyes); stroke-width: 2.5; stroke-linecap: round; opacity: .75; }
.c-pink   { fill: var(--c-pink); }
.c-cat    { fill: var(--c-cat); stroke: var(--c-line); stroke-width: 2.5; stroke-linejoin: round; }
.c-dog    { fill: var(--c-dog); stroke: var(--c-line); stroke-width: 2.5; }
.c-dog-ear { fill: var(--c-dog-ear); stroke: var(--c-line); stroke-width: 2.5; }
.c-dog-patch { fill: var(--c-dog-patch); }
.c-bunny  { fill: var(--c-bunny); stroke: var(--c-line); stroke-width: 2.5; }
.c-bird   { fill: var(--c-bird); stroke: var(--c-line); stroke-width: 2.5; }
.c-bird-wing { fill: var(--c-bird-wing); stroke: var(--c-line); stroke-width: 2.5; }
.c-beak   { fill: var(--c-orange); stroke: var(--c-line); stroke-width: 2; stroke-linejoin: round; }
.c-feather { fill: none; stroke: var(--c-bird); stroke-width: 7; stroke-linecap: round; }
.c-fish   { fill: var(--c-fish); stroke: var(--c-line); stroke-width: 2.5; stroke-linejoin: round; }
.c-fish-fin { fill: var(--c-fish-fin); stroke: var(--c-line); stroke-width: 2.5; }
.c-bubble { fill: none; stroke: var(--c-line); stroke-width: 2; opacity: .45; }
.c-elephant { fill: var(--c-elephant); stroke: var(--c-line); stroke-width: 2.5; }
.c-trunk-line { fill: none; stroke: var(--c-line); stroke-width: 25; stroke-linecap: round; }
.c-trunk { fill: none; stroke: var(--c-elephant); stroke-width: 19; stroke-linecap: round; }
.blob { stroke: var(--c-line); stroke-width: 2.5; stroke-linejoin: round; }
.c-red { fill: var(--c-red); }
.c-blue { fill: var(--c-blue); }
.c-yellow { fill: var(--c-yellow); }
.c-green { fill: var(--c-green); }
.c-purple { fill: var(--c-purple); }
.num-bg { stroke: var(--c-line); stroke-width: 2.5; }
.num-bg.n1 { fill: var(--n1); }
.num-bg.n2 { fill: var(--n2); }
.num-bg.n3 { fill: var(--n3); }
.num-bg.n4 { fill: var(--n4); }
.num-bg.n5 { fill: var(--n5); }
.num-bg.n6 { fill: var(--n6); }
.num-bg.n7 { fill: var(--n7); }
.num-bg.n8 { fill: var(--n8); }
.num-bg.n9 { fill: var(--n9); }
.num-bg.n10 { fill: var(--n10); }
.num-digit { fill: var(--num-ink); font-size: 84px; font-weight: 800; }
.num-dot { fill: var(--num-ink); }
</style>