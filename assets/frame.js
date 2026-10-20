// Cornice comune delle demo: barra in alto con ritorno alla landing, font e piè di pagina.
// Si include con <script src=".../assets/frame.js" defer></script>; i percorsi sono calcolati dalla posizione dello script.
(function () {
  var me = document.currentScript;
  if (!me) return;
  var assets = new URL('.', me.src).href;
  var root = new URL('..', assets).href;
  function link(href) {
    var l = document.createElement('link');
    l.rel = 'stylesheet'; l.href = href;
    document.head.appendChild(l);
  }
  link('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;600;700;800&display=swap');
  link(assets + 'frame.css');
  // foglio di adattamento opzionale per le pagine con una grafica propria: <script data-css="territorio">
  if (me.dataset.css) link(assets + me.dataset.css + '.css');

  // il vecchio pulsante tondo di ritorno è sostituito dalla barra
  Array.prototype.forEach.call(document.querySelectorAll('.pde-back'), function (e) { e.remove(); });

  var bar = document.createElement('div');
  bar.className = 'pde-bar';
  bar.innerHTML =
    '<div class="pde-bar-inner">' +
    '<a class="pde-brand" href="' + root + '" aria-label="PDE — Public Data Explorer, torna alla pagina iniziale">PDE<span>.</span></a>' +
    '<div class="pde-links" role="navigation" aria-label="Navigazione PDE">' +
    '<a href="' + root + '#demo">Dimostrazioni</a>' +
    '<a href="' + root + '#metodo">Metodo e limiti</a>' +
    '<a href="mailto:info@relatalab.it">Contatti</a>' +
    '</div></div>';
  document.body.insertBefore(bar, document.body.firstChild);

  var foot = document.createElement('footer');
  foot.className = 'pde-foot';
  foot.innerHTML =
    '<div class="pde-foot-inner">' +
    '<span>PDE — Public Data Explorer · RELATA Lab · <a href="mailto:info@relatalab.it">info@relatalab.it</a></span>' +
    '<span><a href="' + root + '#demo">Tutte le dimostrazioni</a></span>' +
    '<span>Grafica basata sul tema Nexora, © Harshad Mahadik (licenza MIT), distribuito da <a href="https://themewagon.com/" target="_blank" rel="noopener">ThemeWagon</a></span>' +
    '</div>';
  document.body.appendChild(foot);
})();
