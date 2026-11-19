# Guía de Estilo e Identidad Visual — Suite WINE³ai · TRIsat · ST3LLA

## 1. Arquitectura de Marca y Sistema Geométrico

La suite comparte una estructura geométrica común basada en la **triqueta** (nudo celta de tres hojas entrelazadas), que simboliza la interconexión entre observación espacial, navegación segura e inteligencia aplicada:

| Marca | Rol en el Ecosistema | Símbolos Distintivos |
| :--- | :--- | :--- |
| **WINE³ai** | Aplicación Sectorial (Viticultura de Precisión & IA) | Copa de vino central, racimo minimalista de 3 uvas en la hoja derecha y surco de tierra ondulado en la base. |
| **TRIsat** | Sistema Base (Navegación GNSS Segura y Autenticación OSNMA) | Candado de autenticación en la hoja izquierda, barras horizontales de robustez frente a *jamming*/*spoofing*, arco protector superior y satélite orbital. |
| **ST3LLA** | Observación (Constelación, Telemetría y Seguimiento Orbital) | Estrella central de 5 puntas en la hoja superior, satélite orbital y órbita discontinua envolvente. |

---

## 2. Paletas Cromáticas Oficiales (Códigos Hexadecimales)

### 2.1 WINE³ai
| Muestra / Rol | Nombre del Color | HEX | RGB | Aplicación |
| :--- | :--- | :--- | :--- | :--- |
| Primario | **Burdeos Vino** (*Wine Burgundy*) | `#5E1C37` | `rgb(94, 28, 55)` | Hoja superior, copa central y sufijo tipográfico `ai`. |
| Secundario | **Oro Cálido** (*Warm Gold*) | `#B08D4B` | `rgb(176, 141, 75)` | Hoja derecha, racimo de 3 uvas y prefijo tipográfico `WINE³`. |
| Acento | **Verde Salvia** (*Sage Green*) | `#819B7F` | `rgb(129, 155, 127)` | Hoja izquierda y línea ondulada de tierra. |

### 2.2 TRIsat
| Muestra / Rol | Nombre del Color | HEX | RGB | Aplicación |
| :--- | :--- | :--- | :--- | :--- |
| Primario | **Azul Petróleo** (*Deep Marine Teal*) | `#17576B` | `rgb(23, 87, 107)` | Hoja izquierda, satélite orbital y sufijo tipográfico `sat`. |
| Secundario | **Oro Apagado** (*Muted Gold*) | `#BA9857` | `rgb(186, 152, 87)` | Hoja superior, arco protector exterior y prefijo tipográfico `TRI`. |
| Acento | **Verde Salvia** (*Sage Green*) | `#819B7E` | `rgb(129, 155, 126)` | Hoja derecha, candado de autenticación y barras de señal. |

### 2.3 ST3LLA
| Muestra / Rol | Nombre del Color | HEX | RGB | Aplicación |
| :--- | :--- | :--- | :--- | :--- |
| Primario | **Azul Pizarra Pastel** (*Pastel Slate Blue*) | `#738AAD` | `rgb(115, 138, 173)` | Hoja izquierda, satélite orbital, trazo discontinuo izquierdo y sufijo `LLA`. |
| Secundario | **Oro Suave** (*Soft Pastel Gold*) | `#B9995D` | `rgb(185, 153, 93)` | Hoja superior, estrella central, órbita derecha/inferior y prefijo `ST3`. |
| Acento | **Verde Salvia** (*Sage Green*) | `#809A7F` | `rgb(128, 154, 127)` | Hoja derecha. |

### 2.4 Variantes Monocromáticas y Fondos de Contraste
| Variante | Color | HEX | RGB | Uso Recomendado |
| :--- | :--- | :--- | :--- | :--- |
| Monocromo Claro | **Blanco Puro** | `#FFFFFF` | `rgb(255, 255, 255)` | Sobre fondos oscuros (`#262E36`), fotografía o vídeo. |
| Monocromo Oscuro | **Negro Puro** | `#000000` | `rgb(0, 0, 0)` | Sobre fondos claros (`#F6F8FA`), impresión, sellos o grabado. |
| Fondo Oscuro UI | **Pizarra Oscuro** (*Dark Slate*) | `#262E36` | `rgb(38, 46, 54)` | Modo oscuro de aplicaciones y presentaciones. |
| Fondo Claro UI | **Blanco Neutro** (*Soft Surface*) | `#F6F8FA` | `rgb(246, 248, 250)` | Modo claro de aplicaciones y documentación. |

---

## 3. Tipografía y Reglas de Uso

* **Familia Tipográfica:** **Noto Sans Display** (*Bold* para bloques principales en mayúsculas y superíndice; *SemiBold* para los sufijos en minúsculas `ai` y `sat`). Todos los SVG entregan las letras convertidas a trazados vectoriales (`<path>`) para garantizar fidelidad absoluta sin depender de fuentes instaladas.
* **Área de Protección (Clear Space):** Mantener un margen libre mínimo alrededor del logotipo equivalente al **15 % de la altura total** del isotipo.
* **Tamaño Mínimo:**
  * Isotipo solo: `24 × 24 px` en pantalla / `10 mm` en impreso.
  * Lockup horizontal: `120 px` de ancho en pantalla / `35 mm` en impreso.
* **Usos Incorrectos:** No aplicar degradados brillantes, sombras paralelas externas, deformaciones de proporción ni alterar la asignación cromática de cada hoja.

---

## 4. Tokens de Color para Desarrollo (CSS / SwiftUI / Kotlin)

```css
/* CSS Custom Properties */
:root {
  /* WINE3ai */
  --wine3ai-burgundy: #5E1C37;
  --wine3ai-gold:     #B08D4B;
  --wine3ai-sage:     #819B7F;

  /* TRIsat */
  --trisat-teal:      #17576B;
  --trisat-gold:      #BA9857;
  --trisat-sage:      #819B7E;

  /* ST3LLA */
  --st3lla-blue:      #738AAD;
  --st3lla-gold:      #B9995D;
  --st3lla-sage:      #809A7F;
}
```
