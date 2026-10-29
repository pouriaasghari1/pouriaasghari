const MODEL = "lightricks/ltx-2.5/text-to-video/fast";

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
  const aspect = body.aspect_ratio === "9:16" ? "9:16" : "16:9";
  const requestedDuration = String(body.duration || "6");
  const duration = ["6", "8", "10"].includes(requestedDuration) ? requestedDuration : "6";
  if (prompt.length < 4 || prompt.length > 1200) {
    return json({ error: "توضیح ویدئو باید بین ۴ تا ۱۲۰۰ نویسه باشد." }, 400);
  }

  try {
    const upstream = await fetch("https://queue.fal.run/" + MODEL, {
      method: "POST",
      headers: { "Authorization": "Key " + env.FAL_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, aspect_ratio: aspect, duration, resolution: "1080p", fps: "25", generate_audio: false, enable_safety_checker: true })
    });
    const data = await upstream.json().catch(() => ({}));
    if (!upstream.ok || !data.request_id) {
      console.error("fal video submit error", upstream.status);
      return json({ error: data.detail || data.message || "سرویس ویدئوساز درخواست را نپذیرفت. تنظیمات یا اعتبار حساب را بررسی کن." }, upstream.status >= 400 && upstream.status < 500 ? 502 : 503);
    }
    return json({ request_id: data.request_id, model: MODEL }, 202);
  } catch {
    return json({ error: "ارتباط با صف تولید ویدئو برقرار نشد." }, 502);
  }
}

export async function onRequest(context) {
  if (context.request.method !== "POST") return json({ error: "فقط درخواست POST مجاز است." }, 405);
  return onRequestPost(context);
}
