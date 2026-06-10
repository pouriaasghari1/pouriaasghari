/* =============================================
   main.js — پوریا اصغری
============================================= */
'use strict';

const LS    = localStorage;
const $     = id  => document.getElementById(id);
const toFa  = n   => String(n).replace(/\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]);
const nowFa = ()  => new Date().toLocaleString('fa-IR');

/* ===== ثبت بازدید ===== */
(function trackVisit() {
  const today   = new Date().toDateString();
  const stored  = JSON.parse(LS.getItem('pa_traffic') || '{"total":0,"today":0,"todayDate":"","unique":0}');
  stored.total  = (stored.total  || 0) + 1;
  if (stored.todayDate !== today) { stored.today = 0; stored.todayDate = today; }
  stored.today  = (stored.today  || 0) + 1;
  if (!LS.getItem('pa_visited_once')) { stored.unique = (stored.unique || 0) + 1; LS.setItem('pa_visited_once', '1'); }
  LS.setItem('pa_traffic', JSON.stringify(stored));
})();

/* ===== لودر ===== */
window.addEventListener('load', () => {
  const loader = $('page-loader');
  if (loader) setTimeout(() => loader.classList.add('hide'), 400);
});

/* ===== پس‌زمینه Canvas ===== */
const canvas = $('bg-canvas');
if (canvas) {
  const ctx = canvas.getContext('2d');
  let W, H, pts = [];
  const resize = () => {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
    pts = Array.from({ length: 55 }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35,
      r: Math.random() * 1.5 + .5
    }));
  };
  resize();
  window.addEventListener('resize', resize, { passive: true });
  (function draw() {
    ctx.clearRect(0, 0, W, H);
    pts.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(108,99,255,.55)';
      ctx.fill();
    });
    pts.forEach((a, i) => pts.slice(i + 1).forEach(b => {
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      if (d < 120) {
        ctx.beginPath();
        ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = `rgba(108,99,255,${(1 - d / 120) * .18})`;
        ctx.lineWidth = .6; ctx.stroke();
      }
    }));
    requestAnimationFrame(draw);
  })();
}

/* ===== نوار پیشرفت اسکرول ===== */
const scrollProg = $('scroll-progress');
const navbar     = $('navbar');
const btt        = $('btt');

let ticking = false;
window.addEventListener('scroll', () => {
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => {
    const sy  = window.scrollY;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (scrollProg) scrollProg.style.transform = `scaleX(${max > 0 ? sy / max : 0})`;
    if (navbar) navbar.classList.toggle('scrolled', sy > 50);
    if (btt) {
      const show = sy > 400;
      btt.hidden = !show;
      btt.classList.toggle('show', show);
    }

    /* لینک فعال ناوبار */
    let cur = '';
    document.querySelectorAll('section[id]').forEach(s => {
      if (sy >= s.offsetTop - 200) cur = s.id;
    });
    document.querySelectorAll('.nl').forEach(l => {
      l.classList.toggle('active', l.getAttribute('href') === '#' + cur);
    });

    ticking = false;
  });
}, { passive: true });

/* ===== دکمه بالا ===== */
if (btt) btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

/* ===== منوی موبایل ===== */
const hbg     = $('hbg');
const mobMenu = $('mob-menu');
if (hbg && mobMenu) {
  hbg.addEventListener('click', () => {
    const open = hbg.classList.toggle('open');
    mobMenu.classList.toggle('open', open);
    hbg.setAttribute('aria-expanded', String(open));
    mobMenu.setAttribute('aria-hidden', String(!open));
    document.body.style.overflow = open ? 'hidden' : '';
  });
  document.querySelectorAll('.ml').forEach(l => l.addEventListener('click', () => {
    hbg.classList.remove('open');
    mobMenu.classList.remove('open');
    hbg.setAttribute('aria-expanded', 'false');
    mobMenu.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }));
  document.addEventListener('click', e => {
    if (!hbg.contains(e.target) && !mobMenu.contains(e.target)) {
      hbg.classList.remove('open');
      mobMenu.classList.remove('open');
      document.body.style.overflow = '';
    }
  });
}

/* ===== اسکرول روان روی لینک‌های anchor ===== */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    const offset = target.getBoundingClientRect().top + window.scrollY - 75;
    window.scrollTo({ top: offset, behavior: 'smooth' });
    /* بستن منوی موبایل */
    if (hbg && mobMenu) {
      hbg.classList.remove('open');
      mobMenu.classList.remove('open');
      document.body.style.overflow = '';
    }
  });
});

/* ===== کرسر سفارشی ===== */
const dot  = document.querySelector('.c-dot');
const ring = document.querySelector('.c-ring');
if (dot && ring && window.matchMedia('(pointer: fine)').matches) {
  let mx = 0, my = 0, rx = 0, ry = 0;
  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    dot.style.transform = `translate(${mx}px,${my}px) translate(-50%,-50%)`;
  }, { passive: true });
  (function animRing() {
    rx += (mx - rx) * 0.12;
    ry += (my - ry) * 0.12;
    ring.style.transform = `translate(${rx}px,${ry}px) translate(-50%,-50%)`;
    requestAnimationFrame(animRing);
  })();
  document.querySelectorAll('a, button, [role=button]').forEach(el => {
    el.addEventListener('mouseenter', () => ring.classList.add('big'));
    el.addEventListener('mouseleave', () => ring.classList.remove('big'));
  });
}

/* ===== انیمیشن IntersectionObserver ===== */
if ('IntersectionObserver' in window) {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('v'); obs.unobserve(e.target); }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.r').forEach(el => obs.observe(el));
} else {
  document.querySelectorAll('.r').forEach(el => el.classList.add('v'));
}

/* ===== تایپ‌رایتر ===== */
const typedEl = $('typed');
if (typedEl) {
  const words = ['طراح وب حرفه‌ای', 'توسعه‌دهنده بک‌اند', 'متخصص سئو', 'سازنده فروشگاه آنلاین'];
  let wi = 0, ci = 0, del = false;
  function typeStep() {
    const w = words[wi];
    typedEl.textContent = del ? w.slice(0, --ci) : w.slice(0, ++ci);
    if (!del && ci === w.length)      { del = true;  setTimeout(typeStep, 1400); return; }
    else if (del && ci === 0)          { del = false; wi = (wi + 1) % words.length; }
    setTimeout(typeStep, del ? 55 : 100);
  }
  typeStep();
}

/* ===== سال فوتر ===== */
document.querySelectorAll('#yr').forEach(el => {
  el.textContent = new Date().toLocaleDateString('fa-IR', { year: 'numeric' }).replace(/[^۰-۹]/g, '');
});
