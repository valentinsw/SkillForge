(function() {
  // Theme toggle (persisted); default to DARK when none saved
  const btn = document.getElementById('themeToggle');
  const key = 'sf-theme';
  const root = document.documentElement;
  const saved = localStorage.getItem(key);

  // Default: dark
  const initial = saved ? saved : 'dark';
  root.setAttribute('data-bs-theme', initial);

  if (btn) {
    btn.addEventListener('click', function() {
      const cur = root.getAttribute('data-bs-theme') || initial;
      const next = cur === 'light' ? 'dark' : 'light';
      root.setAttribute('data-bs-theme', next);
      localStorage.setItem(key, next);
    });
  }
})();



// Simple counter animation for stats
document.addEventListener('DOMContentLoaded', function () {
  const counters = document.querySelectorAll('.counter');
  if (!counters.length) return;

  const ease = t => 1 - Math.pow(1 - t, 3);
  counters.forEach(el => {
    const target = parseInt(el.getAttribute('data-target') || '0', 10);
    const duration = 1200 + Math.random() * 600;
    const start = performance.now();

    function tick(now) {
      const p = Math.min(1, (now - start) / duration);
      const value = Math.floor(ease(p) * target);
      el.textContent = value.toLocaleString();
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
});
