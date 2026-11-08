// WINE³ai — Motor de Inteligencia Sommelier & Algoritmo de Maridaje en 3 Presupuestos
// Basado en los estándares de cata y armonía de UDIMA, CMS y WSET

(function(root) {
  'use strict';

  var PAIRING_DATA = (typeof window !== 'undefined' && window.PAIRING_RULES) 
    ? window.PAIRING_RULES 
    : (typeof require !== 'undefined' ? require('../data/pairing_rules.js') : null);

  var SommelierEngine = {
    /**
     * Analiza el texto de un plato o busca en la base de datos de platos
     */
    analyzeDish: function(input) {
      if (!input || typeof input !== 'string') return null;
      var query = input.toLowerCase().trim();

      // 1. Buscar coincidencia exacta o por ID en la base de datos
      if (PAIRING_DATA && PAIRING_DATA.dishesDatabase) {
        for (var i = 0; i < PAIRING_DATA.dishesDatabase.length; i++) {
          var d = PAIRING_DATA.dishesDatabase[i];
          if (d.id === query || d.name_es.toLowerCase().includes(query) || query.includes(d.name_es.toLowerCase())) {
            return d;
          }
          // Comprobar por tags
          for (var t = 0; t < d.tags.length; t++) {
            if (query.includes(d.tags[t])) {
              return d;
            }
          }
        }
      }

      // 2. Detección heurística de ingredientes difíciles (Cinarina, Ácido acético, Picante, etc.)
      var difficultFlags = [];
      if (query.match(/alcachofa|esparrago|espárrago/i)) {
        difficultFlags.push(PAIRING_DATA.difficultFoods.artichoke_asparagus);
      }
      if (query.match(/vinagre|escabeche|encurtido|marinad/i)) {
        difficultFlags.push(PAIRING_DATA.difficultFoods.vinegar_pickles);
      }
      if (query.match(/huevo|tortilla|yema|poché|revuelto/i)) {
        difficultFlags.push(PAIRING_DATA.difficultFoods.egg);
      }
      if (query.match(/picante|chile|guindilla|jalapeño|curry|wasabi|kimchi/i)) {
        difficultFlags.push(PAIRING_DATA.difficultFoods.spicy_capsaicin);
      }
      if (query.match(/queso azul|cabrales|roquefort|gorgonzola|stilton/i)) {
        difficultFlags.push(PAIRING_DATA.difficultFoods.blue_cheese);
      }
      if (query.match(/sardina|caballa|atun|atún|salmon|salmón|arenque/i)) {
        difficultFlags.push(PAIRING_DATA.difficultFoods.oily_fish);
      }

      // Detección de perfil estructural
      var isMeat = !!query.match(/carne|ternera|buey|chuleton|cordero|presa|cochinillo|solomillo/i);
      var isFish = !!query.match(/pescado|lubina|rodaballo|merluza|bacalao|dorada/i);
      var isSeafood = !!query.match(/marisco|gamba|langostino|ostra|almeja|bogavante|percebe/i);
      var isRice = !!query.match(/arroz|paella|risotto/i);

      return {
        id: "custom_" + Date.now(),
        name_es: input,
        tags: [isMeat ? 'carne' : (isFish ? 'pescado' : (isSeafood ? 'marisco' : 'general'))],
        weight: isMeat ? "alto" : (isRice ? "medio" : "ligero-medio"),
        fat: isMeat ? "alto" : "medio-bajo",
        acidity: "medio",
        spiciness: difficultFlags.some(f => f.id === 'spicy_capsaicin') ? "alto" : "nulo",
        difficultFlags: difficultFlags,
        sommelier_note_es: difficultFlags.length > 0 
          ? "Atención: Contiene ingredientes críticos (" + difficultFlags.map(f => f.name_es).join(', ') + ") que interactúan químicamente con el vino (" + difficultFlags[0].compound + ")."
          : (isMeat ? "Plato de alta carga proteica y grasa que agradece tintos con tanino estructurado y buena frescura." : "Plato delicado que exige frescura, acidez y respeto absoluto por los matices marinos/vegetales.")
      };
    },

    /**
     * Parsea texto sin procesar de una carta de vinos escaneada (OCR)
     */
    parseWineMenu: function(rawText) {
      if (!rawText) return [];
      var lines = rawText.split('\n');
      var results = [];

      var priceRegex = /(\d+[\.,]?\d*)\s*(?:€|eur|euros|\$)/i;
      var yearRegex = /\b(19\d{2}|20\d{2})\b/;

      for (var i = 0; i < lines.length; i++) {
        var line = lines[i].trim();
        if (line.length < 5) continue;

        var priceMatch = line.match(priceRegex);
        var yearMatch = line.match(yearRegex);

        var price = null;
        if (priceMatch) {
          price = parseFloat(priceMatch[1].replace(',', '.'));
        }

        var year = yearMatch ? parseInt(yearMatch[1], 10) : null;

        // Limpiar el nombre quitando el precio
        var cleanName = line.replace(priceRegex, '').replace(/[-–—._]{2,}/g, ' ').trim();

        if (cleanName.length > 3) {
          var type = "tinto";
          if (cleanName.match(/blanco|verdejo|albarino|albariño|chardonnay|sauvignon|godello|riesling/i)) {
            type = "blanco";
          } else if (cleanName.match(/cava|champagne|corpinnat|prosecco|espumoso|sparkling/i)) {
            type = "espumoso";
          } else if (cleanName.match(/rosado|rose|rosé/i)) {
            type = "rosado";
          } else if (cleanName.match(/fino|manzanilla|amontillado|oloroso|jerez|sherry|oporto|porto/i)) {
            type = "generoso";
          }

          results.push({
            id: "wine_" + i,
            raw: line,
            name: cleanName,
            year: year,
            type: type,
            price: price || 25.0
          });
        }
      }

      return results;
    },

    /**
     * Evalúa y devuelve las 3 recomendaciones de presupuesto para un plato
     */
    recommend: function(dishInput, optionalMenuWines) {
      var dish = this.analyzeDish(dishInput);
      if (!dish) return null;

      // Si el plato viene con maridajes pre-calculados y no se proporciona carta personalizada
      if ((!optionalMenuWines || optionalMenuWines.length === 0) && dish.pairings) {
        return {
          dish: dish,
          tiers: {
            budget: {
              ...PAIRING_DATA.budgetTiers.budget,
              recommendation: dish.pairings.budget
            },
            balanced: {
              ...PAIRING_DATA.budgetTiers.balanced,
              recommendation: dish.pairings.balanced
            },
            prestige: {
              ...PAIRING_DATA.budgetTiers.prestige,
              recommendation: dish.pairings.prestige
            }
          }
        };
      }

      // Si se proporciona una carta de vinos escaneada, filtramos y ordenamos por precio y afinidad
      var wines = optionalMenuWines || [];
      wines.sort(function(a, b) { return a.price - b.price; });

      var budgetWine = wines.find(function(w) { return w.price <= 26; }) || wines[0];
      var balancedWine = wines.find(function(w) { return w.price > 26 && w.price <= 55; }) || wines[Math.floor(wines.length / 2)] || wines[0];
      var prestigeWine = wines.slice().reverse().find(function(w) { return w.price > 55; }) || wines[wines.length - 1];

      return {
        dish: dish,
        tiers: {
          budget: {
            ...PAIRING_DATA.budgetTiers.budget,
            recommendation: {
              wine: budgetWine ? budgetWine.name : "Vino Joven de Selección",
              price_est: budgetWine ? budgetWine.price + "€" : "18€",
              why: "Opción accesible con acidez refrescante y fruta primaria limpia que acompaña el plato sin enmascarar sus sabores."
            }
          },
          balanced: {
            ...PAIRING_DATA.budgetTiers.balanced,
            recommendation: {
              wine: balancedWine ? balancedWine.name : "Crianza Clásica de Terruño",
              price_est: balancedWine ? balancedWine.price + "€" : "36€",
              why: "El equilibrio canónico: armonía entre el peso del plato y la estructura del vino, con crianza justa y tipicidad regional."
            }
          },
          prestige: {
            ...PAIRING_DATA.budgetTiers.prestige,
            recommendation: {
              wine: prestigeWine ? prestigeWine.name : "Gran Reserva / Parcela Singular",
              price_est: prestigeWine ? prestigeWine.price + "€" : "75€",
              why: "Alta expresión gastronómica: complejidad terciaria, sedosidad y concentración mineral para elevar el bocado a una vivencia sublime."
            }
          }
        }
      };
    }
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = SommelierEngine;
  } else {
    root.SommelierEngine = SommelierEngine;
  }
})(typeof window !== 'undefined' ? window : globalThis);
