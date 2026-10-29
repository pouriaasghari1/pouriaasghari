const MODEL = "lightricks/ltx-2.5/text-to-video/fast";

module.exports = async (req, res) => {
  if (req.method !== "POST") return res.status(405).json({ error: "فقط درخواست POST مجاز است." });
  const access = process.env.APP_ACCESS_CODE;
  const supplied = req.headers["x-app-code"];
  if (!access || !process.env.FAL_KEY) {
    return res.status(503).json({ error: "سرویس هنوز پیکربندی نشده است. متغیرهای FAL_KEY و APP_ACCESS_CODE را در تنظیمات سرور تعریف کن." });
  }
  if (typeof supplied !== "string" || supplied !== access) {
    return res.status(401).json({ error: "کد دسترسی معتبر نیست. کد را در قسمت تنظیمات سرویس وارد کن." });
  }
  const prompt = typeof req.body?.prompt === "string" ? req.body.prompt.trim() : "";
  const aspect = req.body?.aspect_ratio === "9:16" ? "9:16" : "16:9";
  const requestedDuration = String(req.body?.duration || "6");
  const duration = ["6", "8", "10"].includes(requestedDuration) ? requestedDuration : "6";
  if (prompt.length < 4 || prompt.length > 1200) return res.status(400).json({ error: "توضیح ویدئو باید بین ۴ تا ۱۲۰۰ نویسه باشد." });
  try {
    const upstream = await fetch("https://queue.fal.run/" + MODEL, {
      method: "POST",
      headers: { "Authorization": "Key " + process.env.FAL_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, aspect_ratio: aspect, duration, resolution: "1080p", fps: "25", generate_audio: false, enable_safety_checker: true })
    });
    const data = await upstream.json().catch(() => ({}));
    if (!upstream.ok || !data.request_id) {
      console.error("fal video submit error", upstream.status, data);
      return res.status(upstream.status >= 400 && upstream.status < 500 ? 502 : 503).json({ error: data.detail || data.message || "سرویس ویدئوساز درخواست را نپذیرفت. تنظیمات یا اعتبار حساب را بررسی کن." });
    }
    return res.status(202).json({ request_id: data.request_id, model: MODEL });
  } catch (error) {
    console.error("video generation submit failed", error);
    return res.status(502).json({ error: "ارتباط با صف تولید ویدئو برقرار نشد." });
  }
};