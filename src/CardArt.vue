<script setup>
// art: { n: 1..10 } numbers · { c: color-key } colors · a fruit/animal key string.
defineProps({ art: { type: [String, Object], required: true } })
</script>

<template>
  <svg viewBox="0 0 200 200" class="art" aria-hidden="true">
    <!-- ── numbers: pastel tile + digit + matching dots (two rows for 6+) ── -->
    <template v-if="typeof art === 'object' && art.n">
      <rect x="14" y="14" width="172" height="172" rx="40" :class="'num-bg n' + art.n" />
      <text x="100" :y="art.n <= 5 ? 126 : 112" text-anchor="middle" class="num-digit">{{ art.n }}</text>
      <template v-if="art.n <= 5">
        <circle v-for="i in art.n" :key="i" class="num-dot" :cx="100 + (i - 1 - (art.n - 1) / 2) * 34" cy="163" r="9" />
      </template>
      <template v-else>
        <circle v-for="i in art.n" :key="i" class="num-dot" :cx="100 + ((i - 1) % 5 - 2) * 34" :cy="i <= 5 ? 148 : 178" r="8" />
      </template>
    </template>

    <!-- ── apple ── -->
    <g v-else-if="art === 'apple'">
      <ellipse cx="100" cy="170" rx="34" ry="7" class="shadow" />
      <path d="M100 154 C145 154 158 130 158 100 C158 80 148 66 134 62 C131 58 127 56 123 56 C113 56 107 60 100 60 C93 60 87 56 77 56 C73 56 69 58 66 62 C52 66 42 80 42 100 C42 130 55 154 100 154 Z" class="c-apple" />
      <line x1="100" y1="60" x2="100" y2="44" class="c-stem" stroke-width="5" stroke-linecap="round" />
      <ellipse cx="112" cy="41" rx="14" ry="8" transform="rotate(-28 112 41)" class="c-leaf" />
      <ellipse cx="79" cy="81" rx="9" ry="13" transform="rotate(-24 79 81)" class="hi" />
    </g>

    <!-- ── banana ── -->
    <g v-else-if="art === 'banana'">
      <ellipse cx="95" cy="164" rx="44" ry="6" class="shadow" />
      <path d="M146 38 C172 94 150 138 52 152 C86 143 129 124 134 60 C135 47 140 41 146 38 Z" class="c-banana" />
      <circle cx="146" cy="40" r="5" class="c-tip" />
      <circle cx="52" cy="150" r="5" class="c-tip" />
      <path d="M120 76 C110 92 104 100 96 114" class="c-ridge" />
      <ellipse cx="118" cy="58" rx="7" ry="4" transform="rotate(-40 118 58)" class="hi" />
    </g>

    <!-- ── orange ── -->
    <g v-else-if="art === 'orange'">
      <ellipse cx="100" cy="162" rx="30" ry="6" class="shadow" />
      <circle cx="100" cy="104" r="47" class="c-orange" />
      <line x1="100" y1="57" x2="100" y2="44" class="c-stem" stroke-width="5" stroke-linecap="round" />
      <ellipse cx="112" cy="42" rx="13" ry="7" transform="rotate(-24 112 42)" class="c-leaf" />
      <circle cx="86" cy="90" r="2" class="c-dimple" />
      <circle cx="118" cy="92" r="2" class="c-dimple" />
      <circle cx="99" cy="120" r="2" class="c-dimple" />
      <circle cx="74" cy="112" r="2" class="c-dimple" />
      <circle cx="122" cy="104" r="2" class="c-dimple" />
      <ellipse cx="78" cy="84" rx="8" ry="11" transform="rotate(-25 78 84)" class="hi" />
    </g>

    <!-- ── strawberry ── -->
    <g v-else-if="art === 'strawberry'">
      <ellipse cx="100" cy="174" rx="30" ry="6" class="shadow" />
      <path d="M100 172 C62 144 40 118 44 90 C47 66 66 51 80 55 C87 51 96 55 100 63 C104 55 113 51 120 55 C134 52 153 66 156 90 C160 118 138 144 100 172 Z" class="c-straw" />
      <ellipse cx="84" cy="48" rx="13" ry="6" transform="rotate(-34 84 48)" class="c-leaf" />
      <ellipse cx="100" cy="42" rx="14" ry="6" class="c-leaf" />
      <ellipse cx="116" cy="48" rx="13" ry="6" transform="rotate(34 116 48)" class="c-leaf" />
      <ellipse cx="78" cy="94" rx="2.4" ry="4.4" transform="rotate(-12 78 94)" class="c-seed" />
      <ellipse cx="112" cy="88" rx="2.4" ry="4.4" transform="rotate(10 112 88)" class="c-seed" />
      <ellipse cx="90" cy="112" rx="2.4" ry="4.4" class="c-seed" />
      <ellipse cx="120" cy="106" rx="2.4" ry="4.4" class="c-seed" />
      <ellipse cx="100" cy="128" rx="2.4" ry="4.4" class="c-seed" />
      <ellipse cx="72" cy="122" rx="2.4" ry="4.4" class="c-seed" />
      <ellipse cx="128" cy="126" rx="2.4" ry="4.4" class="c-seed" />
      <ellipse cx="74" cy="98" rx="7" ry="10" transform="rotate(-18 74 98)" class="hi" />
    </g>

    <!-- ── grape ── -->
    <g v-else-if="art === 'grape'">
      <ellipse cx="100" cy="170" rx="38" ry="7" class="shadow" />
      <line x1="114" y1="38" x2="114" y2="58" class="c-stem" stroke-width="5" stroke-linecap="round" />
      <ellipse cx="126" cy="48" rx="12" ry="6" transform="rotate(-20 126 48)" class="c-leaf" />
      <g class="c-grape">
        <circle cx="80" cy="74" r="15" />
        <circle cx="103" cy="67" r="15" />
        <circle cx="126" cy="74" r="15" />
        <circle cx="68" cy="96" r="15" />
        <circle cx="91" cy="94" r="15" />
        <circle cx="114" cy="92" r="15" />
        <circle cx="136" cy="96" r="15" />
        <circle cx="80" cy="117" r="15" />
        <circle cx="103" cy="115" r="15" />
        <circle cx="126" cy="113" r="15" />
        <circle cx="93" cy="137" r="15" />
        <circle cx="113" cy="135" r="15" />
      </g>
      <ellipse cx="86" cy="86" rx="6" ry="9" transform="rotate(-22 86 86)" class="hi" />
    </g>

    <!-- ── cat ── -->
    <g v-else-if="art === 'cat'">
      <ellipse cx="100" cy="176" rx="40" ry="7" class="shadow" />
      <path d="M62 76 L48 38 L86 60 Z" class="c-cat" />
      <path d="M138 76 L152 38 L114 60 Z" class="c-cat" />
      <path d="M64 66 L56 46 L78 60 Z" class="c-pink" />
      <path d="M136 66 L144 46 L122 60 Z" class="c-pink" />
      <path d="M100 54 C 134 54 160 78 160 110 C 160 142 132 162 100 162 C 68 162 40 142 40 110 C 40 78 66 54 100 54 Z" class="c-cat" />
      <path d="M74 100 Q82 88 90 100" class="c-eyeline" />
      <path d="M110 100 Q118 88 126 100" class="c-eyeline" />
      <path d="M96 116 L104 116 L100 123 Z" class="c-pink" />
      <path d="M100 123 Q100 132 90 132 M100 123 Q100 132 110 132" class="c-eyeline" />
      <path d="M62 104 L34 98 M62 112 L32 112 M62 120 L34 126" class="c-whisker" />
      <path d="M138 104 L166 98 M138 112 L168 112 M138 120 L166 126" class="c-whisker" />
    </g>

    <!-- ── dog ── -->
    <g v-else-if="art === 'dog'">
      <ellipse cx="100" cy="174" rx="42" ry="7" class="shadow" />
      <ellipse cx="46" cy="118" rx="17" ry="36" transform="rotate(14 46 118)" class="c-dog-ear" />
      <ellipse cx="154" cy="118" rx="17" ry="36" transform="rotate(-14 154 118)" class="c-dog-ear" />
      <circle cx="100" cy="102" r="56" class="c-dog" />
      <circle cx="76" cy="86" r="18" class="c-dog-patch" />
      <circle cx="76" cy="86" r="5" class="c-eyes" />
      <circle cx="124" cy="86" r="5" class="c-eyes" />
      <ellipse cx="100" cy="120" rx="13" ry="10" class="c-tip" />
      <path d="M100 130 L100 136" class="c-eyeline" />
      <path d="M92 136 Q100 150 108 136 Z" class="c-pink" />
    </g>

    <!-- ── bunny ── -->
    <g v-else-if="art === 'bunny'">
      <ellipse cx="100" cy="176" rx="38" ry="7" class="shadow" />
      <ellipse cx="63" cy="58" rx="16" ry="40" transform="rotate(-10 63 58)" class="c-bunny" />
      <ellipse cx="137" cy="58" rx="16" ry="40" transform="rotate(10 137 58)" class="c-bunny" />
      <ellipse cx="63" cy="60" rx="8" ry="30" transform="rotate(-10 63 60)" class="c-pink" />
      <ellipse cx="137" cy="60" rx="8" ry="30" transform="rotate(10 137 60)" class="c-pink" />
      <circle cx="100" cy="112" r="50" class="c-bunny" />
      <circle cx="82" cy="102" r="4.5" class="c-eyes" />
      <circle cx="118" cy="102" r="4.5" class="c-eyes" />
      <path d="M96 116 L104 116 L100 122 Z" class="c-pink" />
      <path d="M100 122 Q100 130 92 132 M100 122 Q100 130 108 132" class="c-eyeline" />
    </g>

    <!-- ── bird ── -->
    <g v-else-if="art === 'bird'">
      <ellipse cx="95" cy="162" rx="38" ry="6" class="shadow" />
      <path d="M56 100 L26 84 M56 108 L22 108 M56 116 L26 132" class="c-feather" />
      <circle cx="95" cy="105" r="52" class="c-bird" />
      <ellipse cx="78" cy="116" rx="17" ry="23" transform="rotate(18 78 116)" class="c-bird-wing" />
      <path d="M142 96 L164 88 L160 108 Z" class="c-beak" />
      <circle cx="126" cy="86" r="5" class="c-eyes" />
      <path d="M104 128 Q112 132 118 126" class="c-eyeline" />
    </g>

    <!-- ── fish ── -->
    <g v-else-if="art === 'fish'">
      <ellipse cx="95" cy="160" rx="44" ry="6" class="shadow" />
      <path d="M134 105 L168 82 L168 128 Z" class="c-fish" />
      <path d="M76 78 C 82 54 102 50 112 72 Z" class="c-fish" />
      <ellipse cx="90" cy="105" rx="52" ry="34" class="c-fish" />
      <ellipse cx="52" cy="112" rx="14" ry="20" transform="rotate(20 52 112)" class="c-fish-fin" />
      <circle cx="122" cy="93" r="4.5" class="c-eyes" />
      <path d="M110 120 Q116 125 122 120" class="c-eyeline" />
      <circle cx="158" cy="56" r="4" class="c-bubble" />
      <circle cx="170" cy="42" r="3" class="c-bubble" />
      <circle cx="152" cy="40" r="2.5" class="c-bubble" />
    </g>

    <!-- ── elephant ── -->
    <g v-else-if="art === 'elephant'">
      <ellipse cx="100" cy="172" rx="42" ry="7" class="shadow" />
      <circle cx="104" cy="106" r="48" class="c-elephant" />
      <ellipse cx="66" cy="112" rx="26" ry="32" transform="rotate(12 66 112)" class="c-elephant" />
      <path d="M106 142 C 108 164 118 178 132 180 C 144 182 150 172 144 164 C 138 156 130 158 126 150" class="c-trunk-line" />
      <path d="M106 142 C 108 164 118 178 132 180 C 144 182 150 172 144 164 C 138 156 130 158 126 150" class="c-trunk" />
      <circle cx="126" cy="94" r="5" class="c-eyes" />
    </g>

    <!-- ── colors: paint blob + droplet ── -->
    <template v-else-if="typeof art === 'object'">
      <ellipse cx="100" cy="164" rx="38" ry="7" class="shadow" />
      <path :class="'c-' + art.c" class="blob" d="M100 74 C 126 62 156 72 160 98 C 164 124 140 148 113 149 C 88 150 63 138 58 112 C 54 88 76 84 100 74 Z" />
      <path :class="'c-' + art.c" class="blob" d="M166 50 C 160 58 160 66 166 70 C 172 66 172 58 166 50 Z" />
      <ellipse cx="84" cy="98" rx="9" ry="13" transform="rotate(-24 84 98)" class="hi" />
    </template>
  </svg>
</template>