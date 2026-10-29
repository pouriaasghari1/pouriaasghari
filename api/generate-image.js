const MODEL = "fal-ai/flux/schnell";

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
  const size = req.body?.image_size;
  const allowedSizes = ["landscape_16_9", "square", "portrait_16_9"];
  if (prompt.length < 4 || prompt.length > 1200) return res.status(400).json({ error: "توضیح تصویر باید بین ۴ تا ۱۲۰۰ نویسه باشد." });
  const imageSize = allowedSizes.includes(size) ? size : "landscape_16_9";
  try {
    const upstream = await fetch("https://fal.run/" + MODEL, {
      method: "POST",
      headers: { "Authorization": "Key " + process.env.FAL_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, image_size: imageSize, num_images: 1, enable_safety_checker: true, output_format: "jpeg" })
    });
    const data = await upstream.json().catch(() => ({}));
    if (!upstream.ok) {
      console.error("fal image API error", upstream.status, data);
      return res.status(upstream.status >= 400 && upstream.status < 500 ? 502 : 503).json({ error: data.detail || data.message || "سرویس تصویرساز خطا داد. اعتبار حساب و تنظیمات API را بررسی کن." });
    }
    const imageUrl = data.images?.[0]?.url;
    if (!imageUrl) return res.status(502).json({ error: "سرویس تصویرساز خروجی قابل‌استفاده برنگرداند." });
    return res.status(200).json({ imageUrl, model: MODEL });
  } catch (error) {
    console.error("image generation failed", error);
    return res.status(502).json({ error: "ارتباط با سرویس تصویرساز برقرار نشد." });
  }
};