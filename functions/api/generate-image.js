const MODEL = "fal-ai/flux/schnell";

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }
  });
}

export async function onRequestPost({ request, env }) {
  if (!env.APP_ACCESS_CODE || !env.FAL_KEY) {
    return json({ error: "سرویس هنوز پیکربندی نشده است. متغیرهای FAL_KEY و APP_ACCESS_CODE را در تنظیمات Cloudflare تعریف کن." }, 503);
  }
  if (request.headers.get("x-app-code") !== env.APP_ACCESS_CODE) {
    return json({ error: "کد دسترسی معتبر نیست. کد را در قسمت تنظیمات سرویس وارد کن." }, 401);
  }

  let body;
  try { body = await request.json(); } catch { return json({ error: "درخواست JSON معتبر نیست." }, 400); }
  const prompt = typeof body.prompt === "string" ? body.prompt.trim() : "";
  const allowedSizes = ["landscape_16_9", "square", "portrait_16_9"];
  if (prompt.length < 4 || prompt.length > 1200) {
    return json({ error: "توضیح تصویر باید بین ۴ تا ۱۲۰۰ نویسه باشد." }, 400);
  }
  const imageSize = allowedSizes.includes(body.image_size) ? body.image_size : "landscape_16_9";

  try {
    const upstream = await fetch("https://fal.run/" + MODEL, {
      method: "POST",
      headers: { "Authorization": "Key " + env.FAL_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, image_size: imageSize, num_images: 1, enable_safety_checker: true, output_format: "jpeg" })
    });
    const data = await upstream.json().catch(() => ({}));
    if (!upstream.ok) {
      console.error("fal image API error", upstream.status);
      return json({ error: data.detail || data.message || "سرویس تصویرساز خطا داد. اعتبار حساب و تنظیمات API را بررسی کن." }, upstream.status >= 400 && upstream.status < 500 ? 502 : 503);
    }
    const imageUrl = data.images?.[0]?.url;
    if (!imageUrl) return json({ error: "سرویس تصویرساز خروجی قابل‌استفاده برنگرداند." }, 502);
    return json({ imageUrl, model: MODEL });
  } catch {
    return json({ error: "ارتباط با سرویس تصویرساز برقرار نشد." }, 502);
  }
}

export async function onRequest(context) {
  if (context.request.method !== "POST") return json({ error: "فقط درخواست POST مجاز است." }, 405);
  return onRequestPost(context);
}
