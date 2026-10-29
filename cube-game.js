'use strict';
(() => {
  const $ = (s, root = document) => root.querySelector(s);
  const cube = $('#cube-3d');
  const scene = $('#cube-scene');
  const faces = [...document.querySelectorAll('.cube-face')];
  const message = $('#cube-message');
  const attemptsLabel = $('#attempt-count');
  const faceCountLabel = $('#face-count');
  const inspected = new Set();
  const names = { front: 'جلو', back: 'پشت', right: 'راست', left: 'چپ', top: 'بالا', bottom: 'پایین' };
  let x = -22, y = -34, attempts = 0, target = 'front', finished = false;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const setMessage = (text, type = '') => { message.textContent = text; message.className = 'cube-message' + (type ? ' ' + type : ''); };
  function currentFace() {
    const normalizedY = ((Math.round(y / 90) * 90) % 360 + 360) % 360;
    const normalizedX = ((Math.round(x / 90) * 90) % 360 + 360) % 360;
    if (normalizedX === 90 || normalizedX === 270) return normalizedX === 90 ? 'top' : 'bottom';
    if (normalizedY === 0) return 'front';
    if (normalizedY === 90) return 'left';
    if (normalizedY === 180) return 'back';
    if (normalizedY === 270) return 'right';
    return 'front';
  }
  function render() {
    cube.style.transform = 'rotateX(' + x + 'deg) rotateY(' + y + 'deg)';
    const key = currentFace();
    faces.forEach(face => face.classList.toggle('current', face.dataset.face === key));
    faceCountLabel.textContent = inspected.size + ' / 6';
    attemptsLabel.textContent = String(attempts);
  }
  function rotate(direction) {
    if (finished) return;
    if (direction === 'left') y -= 90;
    if (direction === 'right') y += 90;
    if (direction === 'up') x += 90;
    if (direction === 'down') x -= 90;
    render();
    setMessage('وجه ' + names[currentFace()] + ' روبه‌روست. اگر آماده‌ای، آن را بررسی کن.');
  }
  function reset() {
    x = -22; y = -34; attempts = 0; inspected.clear(); finished = false;
    target = ['front','back','right','left','top','bottom'][Math.floor(Math.random() * 6)];
    faces.forEach(face => { face.classList.remove('inspected','found','missed'); $('.face-status', face).textContent = 'UNKNOWN'; });
    render();
    setMessage('مکعب را بچرخان و یکی از وجه‌ها را بررسی کن. هسته پنهان فقط روی یک وجه قرار دارد.');
    $('#inspect-face').disabled = false;
  }
  $('#inspect-face').addEventListener('click', () => {
    if (finished) return;
    const key = currentFace(), face = faces.find(item => item.dataset.face === key);
    if (inspected.has(key)) { setMessage('این وجه را قبلاً بررسی کرده‌ای. یک جهت دیگر را امتحان کن.', 'error'); return; }
    inspected.add(key); attempts++;
    face.classList.add('inspected');
    $('.face-status', face).textContent = 'SCANNED';
    if (key === target) {
      finished = true; face.classList.add('found'); $('.face-status', face).textContent = 'CORE FOUND';
      setMessage('هسته را پیدا کردی! در ' + attempts + ' تلاش موفق شدی. می‌توانی یک دور تازه شروع کنی.', 'success');
      $('#inspect-face').disabled = true;
    } else {
      face.classList.add('missed');
      setMessage('این وجه خالی بود. ' + (6 - inspected.size) + ' وجه بررسی‌نشده باقی مانده؛ انتخاب‌ها را به خاطر بسپار.');
      if (inspected.size === 6) {
        finished = true;
        faces.find(item => item.dataset.face === target).classList.add('found');
        $('.face-status', faces.find(item => item.dataset.face === target)).textContent = 'CORE LOCATION';
        setMessage('همه وجه‌ها بررسی شدند؛ هسته روی وجه ' + names[target] + ' بود. شروع دوباره را بزن.', 'error');
        $('#inspect-face').disabled = true;
      }
    }
    render();
  });
  document.querySelectorAll('[data-rotate]').forEach(button => button.addEventListener('click', () => rotate(button.dataset.rotate)));
  $('#new-cube').addEventListener('click', reset);
  scene.addEventListener('keydown', event => {
    const map = { ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'up', ArrowDown: 'down' };
    if (map[event.key]) { event.preventDefault(); rotate(map[event.key]); }
    if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); $('#inspect-face').click(); }
  });
  if (reduceMotion) cube.style.transition = 'none';
  reset();
})();
