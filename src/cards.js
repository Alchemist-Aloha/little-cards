// Add languages here: { code, name (button label), tts (SpeechSynthesis lang) }
export const languages = [
  { code: 'en', name: 'EN', tts: 'en-US' },
  { code: 'zh', name: '中文', tts: 'zh-CN' },
  { code: 'es', name: 'ES', tts: 'es-ES' },
]

// Add sets here: { id, name (per language), cards }
// card.word = word per language
// card.art = a named motif implemented in CardArt.vue,
//         or { n: 1..10 } for numbers, or { c: 'red'|'blue'|'yellow'|'green'|'purple' } for colors
export const sets = [
  {
    id: 'numbers',
    name: { en: 'Numbers', zh: '数字', es: 'Números' },
    cards: [
      { word: { en: 'one', zh: '一', es: 'uno' }, art: { n: 1 } },
      { word: { en: 'two', zh: '二', es: 'dos' }, art: { n: 2 } },
      { word: { en: 'three', zh: '三', es: 'tres' }, art: { n: 3 } },
      { word: { en: 'four', zh: '四', es: 'cuatro' }, art: { n: 4 } },
      { word: { en: 'five', zh: '五', es: 'cinco' }, art: { n: 5 } },
      { word: { en: 'six', zh: '六', es: 'seis' }, art: { n: 6 } },
      { word: { en: 'seven', zh: '七', es: 'siete' }, art: { n: 7 } },
      { word: { en: 'eight', zh: '八', es: 'ocho' }, art: { n: 8 } },
      { word: { en: 'nine', zh: '九', es: 'nueve' }, art: { n: 9 } },
      { word: { en: 'ten', zh: '十', es: 'diez' }, art: { n: 10 } },
    ],
  },
  {
    id: 'fruits',
    name: { en: 'Fruits', zh: '水果', es: 'Frutas' },
    cards: [
      { word: { en: 'apple', zh: '苹果', es: 'manzana' }, art: 'apple' },
      { word: { en: 'banana', zh: '香蕉', es: 'plátano' }, art: 'banana' },
      { word: { en: 'orange', zh: '橙子', es: 'naranja' }, art: 'orange' },
      { word: { en: 'strawberry', zh: '草莓', es: 'fresa' }, art: 'strawberry' },
      { word: { en: 'grape', zh: '葡萄', es: 'uva' }, art: 'grape' },
      { word: { en: 'pear', zh: '梨', es: 'pera' }, art: 'pear' },
      { word: { en: 'watermelon', zh: '西瓜', es: 'sandía' }, art: 'watermelon' },
    ],
  },
  {
    id: 'animals',
    name: { en: 'Animals', zh: '动物', es: 'Animales' },
    cards: [
      { word: { en: 'cat', zh: '猫', es: 'gato' }, art: 'cat' },
      { word: { en: 'dog', zh: '狗', es: 'perro' }, art: 'dog' },
      { word: { en: 'bunny', zh: '兔子', es: 'conejo' }, art: 'bunny' },
      { word: { en: 'bird', zh: '鸟', es: 'pájaro' }, art: 'bird' },
      { word: { en: 'fish', zh: '鱼', es: 'pez' }, art: 'fish' },
      { word: { en: 'elephant', zh: '大象', es: 'elefante' }, art: 'elephant' },
      { word: { en: 'turtle', zh: '乌龟', es: 'tortuga' }, art: 'turtle' },
      { word: { en: 'penguin', zh: '企鹅', es: 'pingüino' }, art: 'penguin' },
    ],
  },
  {
    id: 'colors',
    name: { en: 'Colors', zh: '颜色', es: 'Colores' },
    cards: [
      { word: { en: 'red', zh: '红色', es: 'rojo' }, art: { c: 'red' } },
      { word: { en: 'blue', zh: '蓝色', es: 'azul' }, art: { c: 'blue' } },
      { word: { en: 'yellow', zh: '黄色', es: 'amarillo' }, art: { c: 'yellow' } },
      { word: { en: 'green', zh: '绿色', es: 'verde' }, art: { c: 'green' } },
      { word: { en: 'purple', zh: '紫色', es: 'morado' }, art: { c: 'purple' } },
    ],
  },
  {
    id: 'food',
    name: { en: 'Food', zh: '食物', es: 'Comida' },
    cards: [
      { word: { en: 'bread', zh: '面包', es: 'pan' }, art: 'bread' },
      { word: { en: 'egg', zh: '鸡蛋', es: 'huevo' }, art: 'egg' },
      { word: { en: 'milk', zh: '牛奶', es: 'leche' }, art: 'milk' },
      { word: { en: 'cheese', zh: '奶酪', es: 'queso' }, art: 'cheese' },
    ],
  },
  {
    id: 'vehicles',
    name: { en: 'Vehicles', zh: '交通工具', es: 'Vehículos' },
    cards: [
      { word: { en: 'car', zh: '汽车', es: 'coche' }, art: 'car' },
      { word: { en: 'bus', zh: '公共汽车', es: 'autobús' }, art: 'bus' },
      { word: { en: 'train', zh: '火车', es: 'tren' }, art: 'train' },
      { word: { en: 'bicycle', zh: '自行车', es: 'bicicleta' }, art: 'bicycle' },
    ],
  },
  {
    id: 'nature',
    name: { en: 'Nature', zh: '自然', es: 'Naturaleza' },
    cards: [
      { word: { en: 'tree', zh: '树', es: 'árbol' }, art: 'tree' },
      { word: { en: 'flower', zh: '花', es: 'flor' }, art: 'flower' },
      { word: { en: 'sun', zh: '太阳', es: 'sol' }, art: 'sun' },
      { word: { en: 'moon', zh: '月亮', es: 'luna' }, art: 'moon' },
    ],
  },
]
