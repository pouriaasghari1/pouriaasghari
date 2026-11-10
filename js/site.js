/* ==========================================================================
   Gridline Systems — site behaviour
   Vanilla JS, no dependencies. Progressive enhancement only.
   ========================================================================== */
(function () {
  'use strict';

  var doc = document;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- sticky nav ---------- */
  var nav = doc.querySelector('.nav');
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('is-stuck', window.scrollY > 12);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- mobile drawer ---------- */
  var burger = doc.querySelector('.burger');
  var drawer = doc.querySelector('.drawer');
  if (burger && drawer) {
    var setDrawer = function (open) {
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      drawer.classList.toggle('is-open', open);
      drawer.inert = !open;
      doc.body.style.overflow = open ? 'hidden' : '';
    };
    setDrawer(false);
    burger.addEventListener('click', function () {
      setDrawer(burger.getAttribute('aria-expanded') !== 'true');
    });
    drawer.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setDrawer(false); });
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
        setDrawer(false);
        burger.focus();
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 1060 && drawer.classList.contains('is-open')) setDrawer(false);
    });
  }

  /* ---------- products dropdown (keyboard/touch friendly) ---------- */
  doc.querySelectorAll('.has-menu > .nav__link').forEach(function (trigger) {
    var wrap = trigger.parentElement;
    trigger.setAttribute('aria-haspopup', 'true');
    trigger.setAttribute('aria-expanded', 'false');
    var setOpen = function (open) {
      wrap.classList.toggle('is-open', open);
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    trigger.addEventListener('click', function (e) {
      if (window.innerWidth < 1060) return;
      var isOpen = wrap.classList.contains('is-open');
      if (isOpen) { setOpen(false); return; }
      e.preventDefault();
      doc.querySelectorAll('.has-menu.is-open').forEach(function (w) {
        w.classList.remove('is-open');
        var t = w.querySelector('.nav__link');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
      setOpen(true);
    });
    doc.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) setOpen(false);
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  });

  /* ---------- active nav link ---------- */
  (function () {
    var path = location.pathname.replace(/\/index\.html$/, '/').replace(/\/$/, '/index.html');
    doc.querySelectorAll('.nav__link, .drawer a[data-nav]').forEach(function (link) {
      var href = link.getAttribute('href');
      if (!href || href.charAt(0) === '#' || /^https?:/.test(href)) return;
      var target = new URL(href, location.href).pathname.replace(/\/index\.html$/, '/').replace(/\/$/, '/index.html');
      if (target === path) {
        link.classList.add('is-active');
        if (link.closest('.nav__links')) link.setAttribute('aria-current', 'page');
      }
    });
  })();

  /* ---------- reveal on scroll ---------- */
  var revealEls = doc.querySelectorAll('.reveal');
  if (revealEls.length) {
    if (reduceMotion || !('IntersectionObserver' in window)) {
      revealEls.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
      revealEls.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---------- generic tab groups ---------- */
  doc.querySelectorAll('[data-tabs]').forEach(function (group) {
    var buttons = Array.prototype.slice.call(group.querySelectorAll('[role="tab"]'));
    if (!buttons.length) return;
    var activate = function (btn) {
      buttons.forEach(function (b) {
        var selected = b === btn;
        b.setAttribute('aria-selected', selected ? 'true' : 'false');
        b.tabIndex = selected ? 0 : -1;
        var panel = doc.getElementById(b.getAttribute('aria-controls'));
        if (panel) panel.hidden = !selected;
      });
    };
    buttons.forEach(function (btn, i) {
      btn.addEventListener('click', function () { activate(btn); });
      btn.addEventListener('keydown', function (e) {
        var dir = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!dir) return;
        e.preventDefault();
        var next = buttons[(i + dir + buttons.length) % buttons.length];
        next.focus();
        activate(next);
      });
    });
    var initial = buttons.filter(function (b) { return b.getAttribute('aria-selected') === 'true'; })[0] || buttons[0];
    activate(initial);
  });

  /* ---------- product catalogue filter ---------- */
  var filterBar = doc.querySelector('[data-filter-bar]');
  if (filterBar) {
    var cards = doc.querySelectorAll('[data-category]');
    var empty = doc.querySelector('[data-filter-empty]');
    filterBar.querySelectorAll('button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = btn.dataset.filter;
        filterBar.querySelectorAll('button').forEach(function (b) {
          b.setAttribute('aria-selected', b === btn ? 'true' : 'false');
        });
        var shown = 0;
        cards.forEach(function (card) {
          var cats = (card.dataset.category || '').split(/\s+/);
          var show = f === 'all' || cats.indexOf(f) > -1;
          card.style.display = show ? '' : 'none';
          if (show) shown++;
        });
        if (empty) empty.hidden = shown !== 0;
      });
    });
  }

  /* ---------- toast helper ---------- */
  window.gridToast = function (msg) {
    var t = doc.querySelector('.toast');
    if (!t) {
      t = doc.createElement('div');
      t.className = 'toast';
      t.setAttribute('role', 'status');
      t.setAttribute('aria-live', 'polite');
      doc.body.appendChild(t);
    }
    t.textContent = msg;
    requestAnimationFrame(function () { t.classList.add('is-shown'); });
    clearTimeout(t._timer);
    t._timer = setTimeout(function () { t.classList.remove('is-shown'); }, 3200);
  };

  /* ---------- demo builder links (products) ---------- */
  doc.querySelectorAll('[data-demo-link]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      var id = el.dataset.demoLink;
      try { sessionStorage.setItem('gridline:demo', id); } catch (err) {}
      window.location.href = (el.dataset.demoRoot || '') + 'demo.html#' + id;
    });
  });

  /* ---------- contact / briefing forms ----------
     Static GitHub Pages site: the form composes a pre-filled email
     in the visitor's own mail client. Nothing is uploaded anywhere.   */
  doc.querySelectorAll('form[data-mailto]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var to = form.dataset.mailto;
      var data = new FormData(form);
      var lines = [];
      var subject = form.dataset.subject || 'Project enquiry — Gridline Systems';
      data.forEach(function (value, key) {
        if (!value) return;
        var label = key.replace(/[-_]/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
        lines.push(label + ': ' + value);
      });
      var body = (form.dataset.intro || 'Hello Pouria,\n\nI would like to discuss an Excel automation project.\n\n') +
        lines.join('\n') + '\n\n— Sent from the Gridline Systems website';
      var href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var status = form.querySelector('.form__status');
      if (status) {
        status.className = 'form__status is-shown form__status--ok';
        status.textContent = 'Your email app should now open with the details filled in. If nothing happens, write to ' + to + ' directly.';
      }
      window.location.href = href;
      if (window.gridToast) window.gridToast('Opening your email app…');
    });
  });

  /* ---------- price / package quick pick ---------- */
  doc.querySelectorAll('[data-select-plan]').forEach(function (link) {
    link.addEventListener('click', function () {
      var plan = link.dataset.selectPlan;
      try { sessionStorage.setItem('gridline:plan', plan); } catch (err) {}
      var select = doc.querySelector('#project-type');
      if (select) {
        var opt = Array.prototype.slice.call(select.options).filter(function (o) {
          return o.value.toLowerCase().indexOf(plan.toLowerCase()) > -1;
        })[0];
        if (opt) select.value = opt.value;
      }
    });
  });

  /* ---------- prefill contact form from stored plan ---------- */
  (function () {
    var select = doc.querySelector('#project-type');
    if (select) {
      var plan;
      try { plan = sessionStorage.getItem('gridline:plan'); } catch (err) {}
      if (plan) {
        var opt = Array.prototype.slice.call(select.options).filter(function (o) {
          return o.value.toLowerCase().indexOf(plan.toLowerCase()) > -1;
        })[0];
        if (opt) select.value = opt.value;
      }
    }
  })();

  /* ---------- current year ---------- */
  doc.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- copy email ---------- */
  doc.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.dataset.copy;
      var done = function () {
        if (window.gridToast) window.gridToast('Copied: ' + text);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, done);
      } else {
        var ta = doc.createElement('textarea');
        ta.value = text;
        doc.body.appendChild(ta);
        ta.select();
        try { doc.execCommand('copy'); } catch (err) {}
        doc.body.removeChild(ta);
        done();
      }
    });
  });

  /* ---------- share / demo reset buttons ---------- */
  doc.querySelectorAll('[data-action="print"]').forEach(function (b) {
    b.addEventListener('click', function () { window.print(); });
  });
})();
