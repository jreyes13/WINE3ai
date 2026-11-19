# Paquete Completo de Identidad Visual — WINE³ai · TRIsat · ST3LLA

Este documento reúne la especificación completa del paquete de marca unificado, los tokens de color en formato hexadecimal listos para desarrollo (CSS, JSON, SwiftUI y Android) y el código fuente vectorial **SVG puro** (con fondo transparente y geometría Bézier limpia) de los iconos y nombres de la suite.

---

## 1. Estructura del Paquete Completo de Activos

```text
Suite_Identidad_Visual_Completa/
├── Guia_Estilo_Suite_Visual.pdf
├── color/
│   ├── logos/
│   │   ├── WINE3ai_logo.svg          # 1024x1024 px (fondo transparente)
│   │   ├── TRIsat_logo.svg           # 1024x1024 px (fondo transparente)
│   │   └── ST3LLA_logo.svg           # 1024x1024 px (fondo transparente)
│   ├── nombres/
│   │   ├── WINE3ai_nombre.svg        # 1200x300 px (fondo transparente)
│   │   ├── TRIsat_nombre.svg         # 1200x300 px (fondo transparente)
│   │   └── ST3LLA_nombre.svg         # 1200x300 px (fondo transparente)
│   └── lockups/
│       ├── horizontal/               # 1600x500 px (WINE3ai, TRIsat, ST3LLA)
│       └── vertical/                 # 1000x1150 px (WINE3ai, TRIsat, ST3LLA)
├── blanco/                           # Variante monocromática #FFFFFF
│   ├── logos/
│   ├── nombres/
│   └── lockups/
└── negro/                            # Variante monocromática #000000
    ├── logos/
    ├── nombres/
    └── lockups/
```

---

## 2. Tabla Maestra de Colores Hexadecimales

### 2.1 Paletas por Proyecto

| Proyecto | Elemento / Rol | Nombre del Color | HEX | RGB |
| :--- | :--- | :--- | :--- | :--- |
| **WINE³ai** | Hoja superior, copa central, texto `ai` | Burdeos Vino | `#5E1C37` | `rgb(94, 28, 55)` |
| **WINE³ai** | Hoja derecha, 3 puntos (uvas), texto `WINE³` | Oro Cálido | `#B08D4B` | `rgb(176, 141, 75)` |
| **WINE³ai** | Hoja izquierda, línea ondulada de tierra | Verde Salvia | `#819B7F` | `rgb(129, 155, 127)` |
| **TRIsat** | Hoja izquierda, satélite, texto `sat` | Azul Petróleo Profundo | `#17576B` | `rgb(23, 87, 107)` |
| **TRIsat** | Hoja superior, arco protector, texto `TRI` | Oro Apagado | `#BA9857` | `rgb(186, 152, 87)` |
| **TRIsat** | Hoja derecha, candado, barras de señal | Verde Salvia | `#819B7E` | `rgb(129, 155, 126)` |
| **ST3LLA** | Hoja izquierda, satélite, órbita izq., texto `LLA` | Azul Pizarra Pastel | `#738AAD` | `rgb(115, 138, 173)` |
| **ST3LLA** | Hoja superior, estrella, órbita der./inf., texto `ST3` | Oro Pastel Suave | `#B9995D` | `rgb(185, 153, 93)` |
| **ST3LLA** | Hoja inferior derecha | Verde Salvia | `#809A7F` | `rgb(128, 154, 127)` |

### 2.2 Variantes Monocromáticas y Fondos de Referencia

| Uso | Nombre | HEX | RGB |
| :--- | :--- | :--- | :--- |
| Monocromo Negativo (sobre oscuro) | Blanco Puro | `#FFFFFF` | `rgb(255, 255, 255)` |
| Monocromo Positivo (sobre claro) | Negro Puro | `#000000` | `rgb(0, 0, 0)` |
| Fondo Oscuro Recomendado | Pizarra Oscuro | `#232B35` | `rgb(35, 43, 53)` |
| Fondo Claro Recomendado | Blanco Neutro | `#F8FAFC` | `rgb(248, 250, 252)` |

---

## 3. Tokens de Color para Desarrollo

### 3.1 CSS Variables (`brand-colors.css`)

```css
:root {
  /* WINE3ai */
  --wine3ai-burgundy: #5E1C37;
  --wine3ai-gold: #B08D4B;
  --wine3ai-sage: #819B7F;

  /* TRIsat */
  --trisat-teal: #17576B;
  --trisat-gold: #BA9857;
  --trisat-sage: #819B7E;

  /* ST3LLA */
  --st3lla-slate-blue: #738AAD;
  --st3lla-gold: #B9995D;
  --st3lla-sage: #809A7F;

  /* Monocromo y Superficies */
  --brand-white: #FFFFFF;
  --brand-black: #000000;
  --surface-dark: #232B35;
  --surface-light: #F8FAFC;
}
```

### 3.2 JSON Design Tokens (`brand-tokens.json`)

```json
{
  "WINE3ai": {
    "burgundy": "#5E1C37",
    "gold": "#B08D4B",
    "sage": "#819B7F"
  },
  "TRIsat": {
    "teal": "#17576B",
    "gold": "#BA9857",
    "sage": "#819B7E"
  },
  "ST3LLA": {
    "slateBlue": "#738AAD",
    "gold": "#B9995D",
    "sage": "#809A7F"
  },
  "monochrome": {
    "white": "#FFFFFF",
    "black": "#000000"
  },
  "surfaces": {
    "dark": "#232B35",
    "light": "#F8FAFC"
  }
}
```

---

## 4. Código Vectorial SVG Puro — Iconos Individuales (`1024 × 1024`)

Cada archivo `.svg` puede guardarse directamente con su nombre correspondiente. Para generar las variantes monocromáticas en blanco o negro puro, basta con sustituir los atributos `fill` y `stroke` de color por `#FFFFFF` o `#000000`.

### 4.1 `logos/WINE3ai_logo.svg`

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <mask id="wine-weave-mask">
      <rect width="1024" height="1024" fill="white"/>
      <!-- Cruces limpios del nudo triqueta -->
      <path d="M 300 475 Q 405 425 512 425" stroke="black" stroke-width="82" fill="none" stroke-linecap="round"/>
      <path d="M 655 595 Q 590 660 512 695" stroke="black" stroke-width="82" fill="none" stroke-linecap="round"/>
      <path d="M 412 585 Q 445 645 488 682" stroke="black" stroke-width="82" fill="none" stroke-linecap="round"/>
    </mask>
  </defs>

  <!-- Hoja inferior izquierda (Verde Salvia #819B7F) -->
  <path d="M 455 685 C 335 765 205 765 118 725 C 145 615 215 515 315 462"
        fill="none" stroke="#819B7F" stroke-width="52" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Hoja inferior derecha (Oro Cálido #B08D4B) -->
  <path d="M 709 462 C 809 515 879 615 906 725 C 819 765 689 765 569 685"
        fill="none" stroke="#B08D4B" stroke-width="52" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Hoja superior (Burdeos Vino #5E1C37) -->
  <path d="M 456 626 C 350 510 342 290 512 118 C 682 290 674 510 568 626"
        fill="none" stroke="#5E1C37" stroke-width="52" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Copa de vino central (Burdeos Vino #5E1C37) -->
  <path d="M 442 282 L 582 282 C 602 332 608 386 588 430 C 572 464 532 480 526 520 L 526 608 C 526 635 544 654 562 664 C 530 680 494 680 462 664 C 480 654 498 635 498 608 L 498 520 C 492 480 452 464 436 430 C 416 386 422 332 442 282 Z"
        fill="#5E1C37"/>
  <path d="M 462 306 L 562 306 C 576 346 580 388 564 420 C 550 448 526 458 512 458 C 498 458 474 448 460 420 C 444 388 448 346 462 306 Z"
        fill="#FFFFFF" opacity="0"/>
  <!-- Vaciado interior de la copa con evenodd -->
  <path fill-rule="evenodd" fill="#5E1C37"
        d="M 442 282 L 582 282 C 602 332 608 386 588 430 C 572 464 532 480 526 520 L 526 608 C 526 635 544 654 562 664 C 530 680 494 680 462 664 C 480 654 498 635 498 608 L 498 520 C 492 480 452 464 436 430 C 416 386 422 332 442 282 Z
           M 463 308 L 561 308 C 575 346 579 386 563 418 C 550 444 526 455 512 455 C 498 455 474 444 461 418 C 445 386 449 346 463 308 Z"/>

  <!-- Tres puntos circulares definidos representando las uvas (Oro Cálido #B08D4B) -->
  <circle cx="732" cy="596" r="22" fill="#B08D4B"/>
  <circle cx="702" cy="648" r="22" fill="#B08D4B"/>
  <circle cx="762" cy="648" r="22" fill="#B08D4B"/>

  <!-- Línea ondulada de tierra en la base (Verde Salvia #819B7F) -->
  <path d="M 96 892 C 165 862 225 845 290 865 C 345 882 375 902 422 882 C 462 864 484 836 512 836 C 540 836 562 864 602 882 C 649 902 679 882 734 865 C 799 845 859 862 928 892"
        fill="none" stroke="#819B7F" stroke-width="26" stroke-linecap="round"/>
</svg>
```

### 4.2 `logos/TRIsat_logo.svg`

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <!-- Máscaras transparentes para los cruces de la triqueta -->
    <mask id="trisat-top-mask">
      <rect width="1024" height="1024" fill="white"/>
      <path d="M 135 815 C 185 575 385 455 618 498" stroke="black" stroke-width="84" fill="none" stroke-linecap="round"/>
    </mask>
    <mask id="trisat-left-mask">
      <rect width="1024" height="1024" fill="white"/>
      <path d="M 385 552 C 455 765 665 865 889 815" stroke="black" stroke-width="84" fill="none" stroke-linecap="round"/>
    </mask>
    <mask id="trisat-right-mask">
      <rect width="1024" height="1024" fill="white"/>
      <path d="M 552 708 C 685 555 685 315 512 152" stroke="black" stroke-width="84" fill="none" stroke-linecap="round"/>
    </mask>
  </defs>

  <!-- Hoja superior (Oro Apagado #BA9857) -->
  <path d="M 366 472 C 362 340 412 232 512 152 C 685 315 685 555 552 708"
        fill="none" stroke="#BA9857" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"
        mask="url(#trisat-top-mask)"/>

  <!-- Arco exterior protector anti-jamming/spoofing (Oro Apagado #BA9857) -->
  <path d="M 304 475 C 296 315 368 188 512 96 C 552 122 586 150 612 180"
        fill="none" stroke="#BA9857" stroke-width="24" stroke-linecap="round"/>

  <!-- Hoja inferior izquierda (Azul Petróleo Profundo #17576B) -->
  <path d="M 618 498 C 385 455 185 575 135 815 C 258 855 375 842 478 782"
        fill="none" stroke="#17576B" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"
        mask="url(#trisat-left-mask)"/>

  <!-- Hoja inferior derecha (Verde Salvia #819B7E) -->
  <path d="M 385 552 C 455 765 665 865 889 815 C 858 672 785 568 688 518"
        fill="none" stroke="#819B7E" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"
        mask="url(#trisat-right-mask)"/>

  <!-- Candado de autenticación en hoja izquierda (Verde Salvia #819B7E) -->
  <g transform="translate(306, 718)">
    <!-- Arco superior del candado -->
    <path d="M -24 -16 L -24 -32 A 24 24 0 0 1 24 -32 L 24 -16"
          fill="none" stroke="#819B7E" stroke-width="12" stroke-linecap="round"/>
    <!-- Cuerpo del candado con cerradura -->
    <path fill-rule="evenodd" fill="#819B7E"
          d="M -42 -16 L 42 -16 C 46 -16 48 -12 48 -6 L 44 26 C 40 48 22 64 0 72 C -22 64 -40 48 -44 26 L -48 -6 C -48 -12 -46 -16 -42 -16 Z
             M 0 6 A 9 9 0 0 0 -5 23 L -8 38 L 8 38 L 5 23 A 9 9 0 0 0 0 6 Z"/>
  </g>

  <!-- Barras de robustez de señal en flanco izquierdo (Verde Salvia #819B7E) -->
  <g stroke="#819B7E" stroke-width="18" stroke-linecap="round">
    <line x1="142" y1="330" x2="152" y2="330"/>
    <line x1="186" y1="330" x2="232" y2="330"/>
    <line x1="266" y1="330" x2="296" y2="330"/>

    <line x1="74" y1="382" x2="86" y2="382"/>
    <line x1="120" y1="382" x2="196" y2="382"/>
    <line x1="230" y1="382" x2="262" y2="382"/>

    <line x1="154" y1="434" x2="164" y2="434"/>
    <line x1="198" y1="434" x2="226" y2="434"/>
    <line x1="260" y1="434" x2="286" y2="434"/>
  </g>

  <!-- Satélite minimalista en esquina superior derecha (Azul Petróleo #17576B) -->
  <g transform="translate(796, 244) rotate(45)">
    <!-- Cuerpo central -->
    <rect x="-24" y="-32" width="48" height="64" rx="12" fill="#17576B"/>
    <!-- Conectores de paneles -->
    <rect x="-42" y="-7" width="18" height="14" fill="#17576B"/>
    <rect x="24" y="-7" width="18" height="14" fill="#17576B"/>
    <!-- Paneles solares -->
    <rect x="-124" y="-22" width="84" height="44" rx="8" fill="#17576B"/>
    <rect x="40" y="-22" width="84" height="44" rx="8" fill="#17576B"/>
    <!-- Antena parabólica curva -->
    <path d="M -26 42 Q 0 62 26 42" fill="none" stroke="#17576B" stroke-width="11" stroke-linecap="round"/>
  </g>
</svg>
```

### 4.3 `logos/ST3LLA_logo.svg`

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <!-- Máscaras transparentes para el entrelazado de la triqueta -->
    <mask id="st3lla-top-mask">
      <rect width="1024" height="1024" fill="white"/>
      <path d="M 118 748 C 175 495 385 385 605 425" stroke="black" stroke-width="84" fill="none" stroke-linecap="round"/>
    </mask>
    <mask id="st3lla-left-mask">
      <rect width="1024" height="1024" fill="white"/>
      <path d="M 366 492 C 445 715 665 815 896 748" stroke="black" stroke-width="84" fill="none" stroke-linecap="round"/>
    </mask>
    <mask id="st3lla-right-mask">
      <rect width="1024" height="1024" fill="white"/>
      <path d="M 542 652 C 675 495 675 255 504 92" stroke="black" stroke-width="84" fill="none" stroke-linecap="round"/>
    </mask>
  </defs>

  <!-- Hoja superior (Oro Pastel Suave #B9995D) -->
  <path d="M 352 402 C 352 275 404 172 504 92 C 675 255 675 495 542 652"
        fill="none" stroke="#B9995D" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"
        mask="url(#st3lla-top-mask)"/>

  <!-- Estrella simétrica de cinco puntas (Oro Pastel Suave #B9995D) -->
  <polygon points="504,218 521,264 570,266 532,296 545,344 504,316 463,344 476,296 438,266 487,264"
           fill="#B9995D"/>

  <!-- Hoja inferior izquierda (Azul Pizarra Pastel #738AAD) -->
  <path d="M 605 425 C 385 385 175 495 118 748 C 245 788 362 775 462 715"
        fill="none" stroke="#738AAD" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"
        mask="url(#st3lla-left-mask)"/>

  <!-- Hoja inferior derecha (Verde Salvia #809A7F) -->
  <path d="M 366 492 C 445 715 665 815 896 748 C 864 605 788 502 688 455"
        fill="none" stroke="#809A7F" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"
        mask="url(#st3lla-right-mask)"/>

  <!-- Órbita discontinua izquierda (Azul Pizarra Pastel #738AAD) -->
  <path d="M 118 565 A 405 405 0 0 1 395 148"
        fill="none" stroke="#738AAD" stroke-width="22" stroke-linecap="round" stroke-dasharray="52 42"/>

  <!-- Órbita discontinua derecha y arco inferior (Oro Pastel Suave #B9995D, igual que la estrella) -->
  <path d="M 835 308 A 405 405 0 0 1 886 472"
        fill="none" stroke="#B9995D" stroke-width="22" stroke-linecap="round" stroke-dasharray="52 40"/>
  <path d="M 792 638 L 758 696"
        fill="none" stroke="#B9995D" stroke-width="22" stroke-linecap="round"/>
  <path d="M 615 878 A 405 405 0 0 1 285 824"
        fill="none" stroke="#B9995D" stroke-width="22" stroke-linecap="round"/>

  <!-- Satélite unificado minimalista en esquina superior derecha (Azul Pizarra Pastel #738AAD) -->
  <g transform="translate(822, 174) rotate(45)">
    <rect x="-24" y="-32" width="48" height="64" rx="12" fill="#738AAD"/>
    <rect x="-42" y="-7" width="18" height="14" fill="#738AAD"/>
    <rect x="24" y="-7" width="18" height="14" fill="#738AAD"/>
    <rect x="-124" y="-22" width="84" height="44" rx="8" fill="#738AAD"/>
    <rect x="40" y="-22" width="84" height="44" rx="8" fill="#738AAD"/>
    <path d="M -26 42 Q 0 62 26 42" fill="none" stroke="#738AAD" stroke-width="11" stroke-linecap="round"/>
  </g>
</svg>
```

---

## 5. Código Vectorial SVG — Nombres Independientes (`1200 × 300`)

### 5.1 `nombres/WINE3ai_nombre.svg`

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300">
  <text x="600" y="196" text-anchor="middle"
        font-family="'Helvetica Neue', 'Segoe UI', Arial, sans-serif"
        font-weight="800" font-size="136" letter-spacing="4">
    <tspan fill="#B08D4B">WINE</tspan><tspan fill="#B08D4B" font-size="82" dy="-46">3</tspan><tspan fill="#5E1C37" dy="46">ai</tspan>
  </text>
</svg>
```

### 5.2 `nombres/TRIsat_nombre.svg`

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300">
  <text x="600" y="196" text-anchor="middle"
        font-family="'Helvetica Neue', 'Segoe UI', Arial, sans-serif"
        font-weight="800" font-size="136" letter-spacing="4">
    <tspan fill="#BA9857">TRI</tspan><tspan fill="#17576B">sat</tspan>
  </text>
</svg>
```

### 5.3 `nombres/ST3LLA_nombre.svg`

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300">
  <text x="600" y="196" text-anchor="middle"
        font-family="'Helvetica Neue', 'Segoe UI', Arial, sans-serif"
        font-weight="800" font-size="136" letter-spacing="6">
    <tspan fill="#B9995D">ST3</tspan><tspan fill="#738AAD">LLA</tspan>
  </text>
</svg>
```

---

## 6. Especificaciones de Composiciones Combinadas (Lockups)

* **Lockup Horizontal (`1600 × 500` px):** Icono escalado a `380 × 380` px centrado verticalmente en `x = 120..500`, separación de respeto de `70` px, y logotipo nominal centrado verticalmente a partir de `x = 570`.
* **Lockup Vertical (`1000 × 1150` px):** Icono escalado a `720 × 720` px centrado horizontalmente en `y = 80..800`, separación vertical de `50` px, y logotipo nominal centrado horizontalmente en `y = 850..1070`.