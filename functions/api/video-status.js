const MODEL = "lightricks/ltx-2.5/text-to-video/fast";

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }
  });
}

export async function onRequestGet({ request, env }) {
  if (!env.APP_ACCESS_CODE || !env.FAL_KEY) return json({ error: "تنظیمات سرور کامل نیست." }, 503);
  if (request.headers.get("x-app-code") !== env.APP_ACCESS_CODE) return json({ error: "کد دسترسی معتبر نیست." }, 401);

  const url = new URL(request.url);
  const id = url.searchParams.get("request_id") || "";
  if (!/^[a-zA-Z0-9_-]{8,100}$/.test(id)) return json({ error: "شناسه درخواست معتبر نیست." }, 400);

  const base = "https://queue.fal.run/" + MODEL + "/requests/" + encodeURIComponent(id);
  try {
    const statusResponse = await fetch(base + "/status", {
      headers: { "Authorization": "Key " + env.FAL_KEY }
    });
    const statusData = await statusResponse.json().catch(() => ({}));
    if (!statusResponse.ok) return json({ error: "دریافت وضعیت ویدئو ناموفق بود." }, 502);
    if (statusData.status === "FAILED" || statusData.status === "CANCELLED") {
      return json({ status: statusData.status, error: statusData.error || "پردازش ویدئو ناموفق بود." });
    }
    if (statusData.status !== "COMPLETED") return json({ status: statusData.status || "IN_QUEUE" });

    const resultResponse = await fetch(base, { headers: { "Authorization": "Key " + env.FAL_KEY } });
    const result = await resultResponse.json().catch(() => ({}));
    if (!resultResponse.ok) return json({ error: "دریافت فایل ویدئو ناموفق بود." }, 502);
    const videoUrl = result.video?.url || result.output?.video?.url;
    if (!videoUrl) return json({ error: "پردازش کامل شد، اما لینک ویدئو در پاسخ وجود نداشت." }, 502);
    return json({ status: "COMPLETED", videoUrl });
  } catch {
    return json({ error: "ارتباط برای بررسی وضعیت ویدئو ناموفق بود." }, 502);
  }
}

export async function onRequest(context) {
  if (context.request.method !== "GET") return json({ error: "فقط درخواست GET مجاز است." }, 405);
  return onRequestGet(context);
}
