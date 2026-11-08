// WINE³ai — Controlador de Interfaz: Sommelier Pocket & Fichas de Estudio
// Vincula SommelierEngine, PAIRING_RULES y STUDY_CARDS con el DOM

document.addEventListener('DOMContentLoaded', function() {
  'use strict';

  // ==========================================
  // 1. SOMMELIER POCKET: SCAN & PAIR
  // ==========================================
  var dishInput = document.getElementById('dish-input');
  var btnPair = document.getElementById('btn-pair');
  var dishChips = document.querySelectorAll('.dish-chip');
  var toggleMenuBtn = document.getElementById('toggle-menu-btn');
  var menuInputContainer = document.getElementById('menu-input-container');
  var menuTextInput = document.getElementById('menu-text-input');
  var analysisBanner = document.getElementById('dish-analysis-banner');
  var analysisTitle = document.getElementById('analysis-title');
  var analysisText = document.getElementById('analysis-text');
  var resultsGrid = document.getElementById('results-grid');

  if (toggleMenuBtn && menuInputContainer) {
    toggleMenuBtn.addEventListener('click', function() {
      var isHidden = menuInputContainer.classList.contains('hidden');
      if (isHidden) {
        menuInputContainer.classList.remove('hidden');
        document.getElementById('toggle-menu-label').textContent = 'Ocultar editor de carta de vinos ▲';
      } else {
        menuInputContainer.classList.add('hidden');
        document.getElementById('toggle-menu-label').textContent = '¿Tienes la carta de vinos del restaurante? Pégala o simúlala aquí ▼';
      }
    });
  }

  function runSommelier() {
    if (!dishInput || !window.SommelierEngine) return;
    var dishText = dishInput.value.trim();
    if (!dishText) return;

    var customMenuText = menuTextInput ? menuTextInput.value.trim() : '';
    var parsedWines = null;
    if (customMenuText) {
      parsedWines = window.SommelierEngine.parseWineMenu(customMenuText);
    }

    var result = window.SommelierEngine.recommend(dishText, parsedWines);
    if (!result) return;

    // Actualizar Banner de Diagnóstico
    if (analysisBanner && analysisText) {
      var dish = result.dish;
      if (dish.difficultFlags && dish.difficultFlags.length > 0) {
        var flag = dish.difficultFlags[0];
        analysisBanner.className = "max-w-4xl mx-auto mb-8 p-4 rounded-2xl bg-rose-950/40 border border-rose-700/50 flex items-start gap-3.5 text-xs text-rose-200 font-mono shadow-lg";
        analysisTitle.textContent = "⚠️ Alimento Crítico para la Sumillería: " + flag.name_es + " (" + flag.compound + ")";
        analysisText.innerHTML = "<strong>Problema químico:</strong> " + flag.problem + "<br><strong class='text-amber-300'>Solución de Sumiller:</strong> " + flag.solution_es;
      } else {
        analysisBanner.className = "max-w-4xl mx-auto mb-8 p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-start gap-3.5 text-xs text-amber-200 font-mono";
        analysisTitle.textContent = "Diagnóstico Sensorial & Estructural:";
        analysisText.textContent = dish.sommelier_note_es || "Equilibrio estructural de peso, acidez y persistencia.";
      }
    }

    // Renderizar las 3 Cards de Presupuesto
    if (resultsGrid) {
      resultsGrid.innerHTML = '';
      var tiers = [
        { key: 'budget', border: 'border-emerald-600/30', bgGlow: 'bg-emerald-600/10', badgeBg: 'bg-emerald-950 text-emerald-300 border-emerald-800/50', icon: '🟢', tierNum: '1' },
        { key: 'balanced', border: 'border-amber-600/30', bgGlow: 'bg-amber-600/10', badgeBg: 'bg-amber-950 text-amber-300 border-amber-800/50', icon: '🟡', tierNum: '2' },
        { key: 'prestige', border: 'border-rose-600/30', bgGlow: 'bg-rose-600/10', badgeBg: 'bg-rose-950 text-rose-300 border-rose-800/50', icon: '🟣', tierNum: '3' }
      ];

      tiers.forEach(function(t) {
        var tierData = result.tiers[t.key];
        var rec = tierData.recommendation;

        var card = document.createElement('div');
        card.className = "bg-[#12141c] border " + t.border + " rounded-2xl p-6 relative flex flex-col justify-between overflow-hidden group hover:border-opacity-80 transition-all";

        var grapesHtml = '';
        if (rec.grapes && rec.grapes.length) {
          grapesHtml = rec.grapes.map(function(g) {
            return "<span class='px-2 py-0.5 rounded bg-white/5 border border-white/10 text-[10px] text-slate-300'>" + g + "</span>";
          }).join(' ');
        }

        card.innerHTML = 
          "<div class='absolute -top-10 -right-10 w-28 h-28 " + t.bgGlow + " rounded-full blur-2xl group-hover:scale-125 transition-transform'></div>" +
          "<div>" +
            "<div class='flex items-center justify-between mb-3 relative z-10'>" +
              "<span class='text-[10px] font-mono px-2.5 py-1 rounded " + t.badgeBg + " border uppercase font-bold'>" +
                t.icon + " " + tierData.name_es +
              </span>" +
              "<span class='text-xs font-mono font-bold text-amber-400'>" + (rec.price_est || tierData.priceRange) + "</span>" +
            "</div>" +
            "<h4 class='text-xl font-bold font-serif-wine text-white mb-1.5 leading-snug'>" + rec.wine + "</h4>" +
            "<div class='text-xs text-rose-400 font-mono mb-3'>" + (rec.region || 'Selección del Sumiller') + "</div>" +
            (grapesHtml ? "<div class='flex flex-wrap gap-1 mb-4'>" + grapesHtml + "</div>" : "") +
            "<p class='text-slate-300 text-xs leading-relaxed mb-4 font-sans bg-black/40 p-3.5 rounded-xl border border-white/5'>" +
              "<strong class='text-amber-300 block font-mono text-[11px] mb-1'>Por qué funciona (Química & Maridaje):</strong>" +
              rec.why +
            "</p>" +
          "</div>" +
          "<div class='pt-3 border-t border-white/10 text-[11px] font-mono text-slate-400 italic'>" +
            tierData.philosophy_es +
          "</div>";

        resultsGrid.appendChild(card);
      });
    }
  }

  if (btnPair) {
    btnPair.addEventListener('click', runSommelier);
  }

  if (dishChips) {
    dishChips.forEach(function(chip) {
      chip.addEventListener('click', function() {
        var dish = chip.getAttribute('data-dish');
        if (dishInput && dish) {
          dishInput.value = dish;
          runSommelier();
        }
      });
    });
  }

  // Ejecución inicial automática
  runSommelier();

  // ==========================================
  // 2. FICHAS DE ESTUDIO INTERACTIVAS (WSET3 / CMS / UDIMA)
  // ==========================================
  var deckFilterBtns = document.querySelectorAll('.deck-filter');
  var cardBadge = document.getElementById('card-standard-badge');
  var cardCategory = document.getElementById('card-category');
  var cardQuestion = document.getElementById('card-question');
  var cardAnswerBox = document.getElementById('card-answer-box');
  var cardAnswer = document.getElementById('card-answer');
  var cardSolution = document.getElementById('card-solution');
  var cardCounter = document.getElementById('card-counter');
  var btnReveal = document.getElementById('btn-reveal-answer');
  var btnPrevCard = document.getElementById('btn-prev-card');
  var btnNextCard = document.getElementById('btn-next-card');

  var allCards = window.STUDY_CARDS || [];
  var filteredCards = allCards.slice();
  var currentIndex = 0;

  function renderCard() {
    if (!filteredCards.length || !cardQuestion) return;
    var c = filteredCards[currentIndex];

    if (cardBadge) {
      cardBadge.textContent = c.standard;
      if (c.standard.includes('UDIMA')) {
        cardBadge.className = "px-2.5 py-1 rounded text-[11px] font-mono font-bold bg-amber-950 text-amber-300 border border-amber-800/40";
      } else if (c.standard.includes('CMS')) {
        cardBadge.className = "px-2.5 py-1 rounded text-[11px] font-mono font-bold bg-rose-950 text-rose-300 border border-rose-800/40";
      } else {
        cardBadge.className = "px-2.5 py-1 rounded text-[11px] font-mono font-bold bg-purple-950 text-purple-300 border border-purple-800/40";
      }
    }

    if (cardCategory) cardCategory.textContent = c.category;
    if (cardQuestion) cardQuestion.textContent = c.question_es;
    if (cardAnswer) cardAnswer.textContent = c.answer_es;
    if (cardSolution) cardSolution.textContent = c.solution_es;
    if (cardCounter) cardCounter.textContent = "Ficha " + (currentIndex + 1) + " de " + filteredCards.length;

    // Ocultar respuesta al cambiar de ficha
    if (cardAnswerBox) cardAnswerBox.classList.add('hidden');
    if (btnReveal) {
      btnReveal.innerHTML = "<span>👁️</span> <span>Mostrar Solución</span>";
    }
  }

  if (btnReveal && cardAnswerBox) {
    btnReveal.addEventListener('click', function() {
      var isHidden = cardAnswerBox.classList.contains('hidden');
      if (isHidden) {
        cardAnswerBox.classList.remove('hidden');
        btnReveal.innerHTML = "<span>🙈</span> <span>Ocultar Solución</span>";
      } else {
        cardAnswerBox.classList.add('hidden');
        btnReveal.innerHTML = "<span>👁️</span> <span>Mostrar Solución</span>";
      }
    });
  }

  if (btnNextCard) {
    btnNextCard.addEventListener('click', function() {
      if (currentIndex < filteredCards.length - 1) {
        currentIndex++;
      } else {
        currentIndex = 0; // loop
      }
      renderCard();
    });
  }

  if (btnPrevCard) {
    btnPrevCard.addEventListener('click', function() {
      if (currentIndex > 0) {
        currentIndex--;
      } else {
        currentIndex = filteredCards.length - 1; // loop
      }
      renderCard();
    });
  }

  if (deckFilterBtns) {
    deckFilterBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        var filter = btn.getAttribute('data-filter');
        deckFilterBtns.forEach(function(b) {
          b.className = "deck-filter px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300";
        });
        btn.className = "deck-filter px-3 py-1.5 rounded-lg bg-rose-950 text-rose-300 border border-rose-800/50";

        if (filter === 'all') {
          filteredCards = allCards.slice();
        } else {
          filteredCards = allCards.filter(function(card) {
            return card.standard.includes(filter);
          });
        }
        currentIndex = 0;
        renderCard();
      });
    });
  }

  renderCard();
});
