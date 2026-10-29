# فعال‌سازی ثبت‌نام و ورود با ایمیل

این سایت از Supabase Email OTP / Magic Link استفاده می‌کند؛ کاربر ایمیلش را وارد می‌کند و لینک تأیید واقعی دریافت می‌کند. پسورد در سایت ذخیره نمی‌شود.

## راه‌اندازی

1. در https://supabase.com یک پروژه بساز.
2. از **Project Settings → API**، مقدار **Project URL** و **publishable key** (یا anon public key قدیمی) را بردار.
3. دو مقدار را در ابتدای `auth.js` جایگزین `YOUR_SUPABASE_PROJECT_URL` و `YOUR_SUPABASE_PUBLISHABLE_OR_ANON_KEY` کن.
4. در **Authentication → URL Configuration**، آدرس زیر را در Redirect URLs ثبت کن:
   `https://pouriaasghari1.github.io/pouriaasghari/auth.html`
   آدرس سایت را هم در Site URL تنظیم کن.
5. در **Authentication → Providers → Email** ورود با ایمیل را فعال کن. برای ارسال مطمئن ایمیل به کاربران واقعی، SMTP اختصاصی را پیکربندی کن.
6. فایل‌ها را commit کن و پس از انتشار GitHub Pages، مسیر `/auth.html` را آزمایش کن.

## امنیت

- فقط Project URL و publishable/anon key در مرورگر مجازند.
- **هرگز** کلید `service_role`، رمز دیتابیس یا رمز SMTP را در فایل‌های سایت قرار نده.
- ارسال موفق درخواست لزوماً تضمین نمی‌کند که ایمیل به Inbox برسد؛ تنظیمات SMTP، محدودیت ارسال و پوشه Spam را بررسی کن.
- تا وقتی مقادیر Supabase تنظیم نشده‌اند، فرم عمداً غیرفعال می‌ماند و پیام موفقیت ساختگی نشان نمی‌دهد.

## وضعیت

رابط و منطق فرانت‌اند آماده است، اما احراز هویت واقعی تا اتصال پروژه Supabase و تنظیم URLهای مجاز فعال نمی‌شود.
