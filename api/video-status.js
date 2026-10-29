const MODEL = "lightricks/ltx-2.5/text-to-video/fast";

module.exports = async (req, res) => {
  if (req.method !== "GET") return res.status(405).json({ error: "فقط درخواست GET مجاز است." });
  const access = process.env.APP_ACCESS_CODE;
  const supplied = req.headers["x-app-code"];
  if (!access || !process.env.FAL_KEY) return res.status(503).json({ error: "تنظیمات سرور کامل نیست." });
  if (typeof supplied !== "string" || supplied !== access) return res.status(401).json({ error: "کد دسترسی معتبر نیست." });
  const id = typeof req.query?.request_id === "string" ? req.query.request_id : "";
  if (!/^[a-zA-Z0-9_-]{8,100}$/.test(id)) return res.status(400).json({ error: "شناسه درخواست معتبر نیست." });
  const base = "https://queue.fal.run/" + MODEL + "/requests/" + encodeURIComponent(id);
  try {
    const statusResponse = await fetch(base + "/status", { headers: { "Authorization": "Key " + process.env.FAL_KEY } });
    const statusData = await statusResponse.json().catch(() => ({}));
    if (!statusResponse.ok) return res.status(502).json({ error: "دریافت وضعیت ویدئو ناموفق بود." });
    if (statusData.status === "FAILED" || statusData.status === "CANCELLED") {
      return res.status(200).json({ status: statusData.status, error: statusData.error || "پردازش ویدئو ناموفق بود." });
    }
    if (statusData.status !== "COMPLETED") return res.status(200).json({ status: statusData.status || "IN_QUEUE" });
    const resultResponse = await fetch(base, { headers: { "Authorization": "Key " + process.env.FAL_KEY } });
    const result = await resultResponse.json().catch(() => ({}));
    if (!resultResponse.ok) return res.status(502).json({ error: "دریافت فایل ویدئو ناموفق بود." });
    const videoUrl = result.video?.url || result.output?.video?.url;
    if (!videoUrl) return res.status(502).json({ error: "پردازش کامل شد، اما لینک ویدئو در پاسخ وجود نداشت." });
    return res.status(200).json({ status: "COMPLETED", videoUrl });
  } catch (error) {
    console.error("video status error", error);
    return res.status(502).json({ error: "ارتباط برای بررسی وضعیت ویدئو ناموفق بود." });
  }
};