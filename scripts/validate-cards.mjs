import { readFile, readdir } from 'node:fs/promises'
import { languages, sets } from '../src/cards.js'

const assetDir = new URL('../src/assets/', import.meta.url)
const assetFiles = new Set((await readdir(assetDir)).filter(file => file.endsWith('.svg')))
const languageCodes = languages.map(({ code }) => code)
const usedAssets = new Set()
let cards = 0

for (const set of sets) {
  for (const code of languageCodes) {
    if (!set.name[code]) throw new Error(`${set.id} has no ${code} name`)
  }
  for (const card of set.cards) {
    cards += 1
    for (const code of languageCodes) {
      if (!card.word[code]) throw new Error(`${set.id} has a card with no ${code} word`)
    }
    const asset = typeof card.art === 'string' ? card.art : 'n' in card.art ? `number-${card.art.n}` : `color-${card.art.c}`
    if (typeof card.art === 'object' && 'n' in card.art && (!Number.isInteger(card.art.n) || card.art.n < 1 || card.art.n > 10)) {
      throw new Error(`${set.id} has an invalid number card`)
    }
    if (typeof card.art === 'object' && !('n' in card.art) && !('c' in card.art)) {
      throw new Error(`${set.id} has an unknown card art type`)
    }
    if (!assetFiles.has(`${asset}.svg`)) throw new Error(`${set.id} references missing SVG: ${asset}.svg`)
    usedAssets.add(`${asset}.svg`)
  }
}

for (const file of assetFiles) {
  const svg = await readFile(new URL(file, assetDir), 'utf8')
  if (!svg.startsWith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"')) {
    throw new Error(`${file} is not a standalone 200 × 200 SVG`)
  }
  if (/\bv-(?:if|else|for|bind)\b|\{\{/.test(svg)) throw new Error(`${file} contains Vue template syntax`)
}

if (usedAssets.size !== assetFiles.size) throw new Error('Every SVG asset must be used by a card')
console.log(`Validated ${assetFiles.size} standalone SVGs for ${sets.length} categories and ${cards} cards.`)
