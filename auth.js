import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';

/*
 * SETUP — one-time:
 * 1. Create a project at https://supabase.com/
 * 2. In Project Settings → API, copy the Project URL and publishable/anon key.
 * 3. Put those PUBLIC values in the two constants below (never use a service_role key).
 * 4. In Authentication → URL Configuration, add your GitHub Pages URL to Site URL
 *    and Redirect URLs, for example:
 *    https://pouriaasghari1.github.io/pouriaasghari/auth.html
 * 5. In Authentication → Providers → Email, enable email OTP/magic links and configure
 *    SMTP if you need reliable production delivery. Supabase's default mail service is limited.
 */
const SUPABASE_URL = 'YOUR_SUPABASE_PROJECT_URL';
const SUPABASE_PUBLISHABLE_KEY = 'YOUR_SUPABASE_PUBLISHABLE_OR_ANON_KEY';

const $ = (selector) => document.querySelector(selector);
const form = $('#email-form');
const emailInput = $('#email');
const sendButton = $('#send-link');
const buttonLabel = $('.btn-label');
const message = $('#auth-message');
const sessionPanel = $('#auth-session');
let supabase = null;

function setMessage(text, kind = '') {
  message.textContent = text;
  message.className = 'auth-message' + (kind ? ' ' + kind : '');
  message.hidden = false;
}
function setBusy(busy) {
  sendButton.disabled = busy;
  buttonLabel.textContent = busy ? 'در حال ارسال…' : 'ارسال لینک ورود';
}
function validEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) && value.length <= 254;
}
function configurationReady() {
  return SUPABASE_URL.startsWith('https://') &&
    !SUPABASE_URL.includes('YOUR_') &&
    SUPABASE_PUBLISHABLE_KEY.length > 20 &&
    !SUPABASE_PUBLISHABLE_KEY.includes('YOUR_');
}
function safeRedirectUrl() {
  const url = new URL('auth.html', window.location.href);
  url.hash = '';
  return url.href;
}
function renderSession(user) {
  if (!user) {
    sessionPanel.hidden = true;
    form.hidden = false;
    $('#auth-title').textContent = 'ورود یا ثبت‌نام';
    $('.auth-intro').textContent = 'ایمیل خودت را وارد کن؛ لینک ورود برایت ارسال می‌شود.';
    return;
  }
  form.hidden = true;
  sessionPanel.hidden = false;
  $('#session-email').textContent = user.email || 'ایمیل تأییدشده';
  $('#auth-title').textContent = 'حساب کاربری تو';
  $('.auth-intro').textContent = 'ورود با موفقیت انجام شده است.';
  message.hidden = true;
}
if (!configurationReady()) {
  setMessage('سیستم ورود هنوز به سرویس احراز هویت متصل نشده است. برای فعال‌سازی واقعی، پروژه Supabase بساز و URL و کلید عمومی پروژه را در ابتدای فایل auth.js قرار بده. این صفحه عمداً موفقیت ساختگی نشان نمی‌دهد.', 'error');
  sendButton.disabled = true;
} else {
  supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
  });
  supabase.auth.getSession().then(({ data, error }) => {
    if (error) setMessage('بررسی نشست انجام نشد. اتصال را بررسی و دوباره تلاش کن.', 'error');
    else renderSession(data.session?.user || null);
  });
  supabase.auth.onAuthStateChange((event, session) => {
    if (session?.user) renderSession(session.user);
    if (event === 'SIGNED_OUT') {
      renderSession(null);
      setMessage('از حساب خارج شدی.', 'success');
    }
  });
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const email = emailInput.value.trim().toLowerCase();
    if (!validEmail(email)) {
      setMessage('یک آدرس ایمیل معتبر وارد کن.', 'error');
      emailInput.focus();
      return;
    }
    setBusy(true);
    message.hidden = true;
    try {
      const { error } = await supabase.auth.signInWithOtp({
        email,
        options: { emailRedirectTo: safeRedirectUrl(), shouldCreateUser: true }
      });
      if (error) throw error;
      setMessage('اگر ارسال ایمیل برای این پروژه فعال باشد، لینک ورود به ' + email + ' فرستاده می‌شود. صندوق ورودی و پوشه Spam را بررسی کن؛ سپس لینک را روی همین سایت باز کن.', 'success');
    } catch (error) {
      setMessage('خطا در ارسال لینک: ' + (error?.message || 'کمی بعد دوباره تلاش کن.'), 'error');
    } finally {
      setBusy(false);
    }
  });
  $('#sign-out').addEventListener('click', async () => {
    const { error } = await supabase.auth.signOut();
    if (error) setMessage('خروج کامل نشد. دوباره تلاش کن.', 'error');
  });
}
