(() => {
  const $ = (selector) => document.querySelector(selector);
  const form = $("#generateForm");
  const prompt = $("#prompt");
  const imageMode = $("#imageMode");
  const videoMode = $("#videoMode");
  const ratio = $("#ratio");
  const duration = $("#duration");
  const durationSetting = $("#durationSetting");
  const button = $("#generateBtn");
  const buttonLabel = $("#buttonLabel");
  const canvas = $("#canvas");
  const emptyCopy = $("#emptyCopy");
  const loader = $("#loader");
  const loaderTitle = $("#loaderTitle");
  const loaderText = $("#loaderText");
  const mediaOutput = $("#mediaOutput");
  const resultBadge = $("#resultBadge");
  const outputStatus = $("#outputStatus");
  const downloadLink = $("#downloadLink");
  const errorDialog = $("#errorDialog");
  const errorText = $("#errorText");
  let mode = "image";
  let activeObjectUrl = null;

  const digits = (value) => String(value).replace(/\d/g, d => "۰۱۲۳۴۵۶۷۸۹"[Number(d)]);
  prompt.addEventListener("input", () => { $("#charCount").textContent = digits(prompt.value.length) + " / ۱۲۰۰"; });

  function setMode(next) {
    mode = next;
    imageMode.classList.toggle("active", mode === "image");
    videoMode.classList.toggle("active", mode === "video");
    imageMode.setAttribute("aria-selected", String(mode === "image"));
    videoMode.setAttribute("aria-selected", String(mode === "video"));
    durationSetting.hidden = mode !== "video";
    ratio.innerHTML = mode === "image"
      ? '<option value="landscape_16_9">افقی 16:9</option><option value="square">مربع 1:1</option><option value="portrait_16_9">عمودی 9:16</option>'
      : '<option value="16:9">افقی 16:9</option><option value="9:16">عمودی 9:16</option>';
    buttonLabel.textContent = mode === "image" ? "تولید تصویر" : "تولید ویدئو";
    $("#promptHint").textContent = mode === "image" ? "توضیحات دقیق‌تر معمولاً نتیجه بهتری می‌دهند." : "حرکت دوربین، سوژه و تغییرات صحنه را هم توضیح بده.";
    prompt.placeholder = mode === "image"
      ? "مثلاً: یک شهر آینده‌نگر در دل کویر، معماری شیشه‌ای، نور طلایی غروب، سینمایی و بسیار پرجزئیات..."
      : "مثلاً: دوربین آرام به سمت یک شهر آینده‌نگر حرکت می‌کند، نورهای نئونی روشن می‌شوند و مه میان ساختمان‌ها جریان دارد...";
    $("#resultBadge").textContent = mode === "image" ? "تصویر / FLUX" : "ویدئو / LTX";
  }
  imageMode.addEventListener("click", () => setMode("image"));
  videoMode.addEventListener("click", () => setMode("video"));
  $("#closeError").addEventListener("click", () => errorDialog.close());

  function showError(message) {
    errorText.textContent = message || "خطای نامشخصی رخ داد.";
    if (typeof errorDialog.showModal === "function") errorDialog.showModal();
    else window.alert(errorText.textContent);
  }
  function busy(value, title = "در حال ساخت...", detail = "مدل هوش مصنوعی درخواست را پردازش می‌کند.") {
    button.disabled = value;
    buttonLabel.textContent = value ? "در حال تولید..." : (mode === "image" ? "تولید تصویر" : "تولید ویدئو");
    emptyCopy.hidden = value || Boolean(mediaOutput.firstChild);
    loader.hidden = !value;
    if (value) {
      loaderTitle.textContent = title;
      loaderText.textContent = detail;
      resultBadge.textContent = "در حال پردازش";
      outputStatus.textContent = "مدل در حال تولید خروجی است";
      downloadLink.hidden = true;
      mediaOutput.hidden = true;
    }
  }
  function showMedia(url, type) {
    if (activeObjectUrl) { URL.revokeObjectURL(activeObjectUrl); activeObjectUrl = null; }
    mediaOutput.replaceChildren();
    let element;
    if (type === "video") {
      element = document.createElement("video");
      element.controls = true;
      element.playsInline = true;
      element.preload = "metadata";
    } else {
      element = document.createElement("img");
      element.alt = "تصویر تولیدشده با هوش مصنوعی";
    }
    element.src = url;
    mediaOutput.appendChild(element);
    mediaOutput.hidden = false;
    emptyCopy.hidden = true;
    loader.hidden = true;
    resultBadge.textContent = "تولید کامل شد";
    outputStatus.textContent = type === "video" ? "ویدئو آماده مشاهده است" : "تصویر آماده مشاهده است";
    $(".output-dot").classList.add("ready");
    downloadLink.href = url;
    downloadLink.download = type === "video" ? "neuraframe-video.mp4" : "neuraframe-image.jpg";
    downloadLink.hidden = false;
    button.disabled = false;
    buttonLabel.textContent = mode === "image" ? "تولید تصویر دیگر" : "تولید ویدئوی دیگر";
  }
  async function parseResponse(response) {
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.error || "درخواست ناموفق بود. تنظیمات سرور را بررسی کن.");
    return data;
  }
  async function generateImage(text) {
    const data = await parseResponse(await fetch("/api/generate-image", {
      method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({prompt:text, image_size:ratio.value})
    }));
    if (!data.imageUrl) throw new Error("سرویس پاسخی داد اما لینک تصویر در خروجی نبود.");
    showMedia(data.imageUrl, "image");
  }
  async function generateVideo(text) {
    const started = await parseResponse(await fetch("/api/generate-video", {
      method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({prompt:text, aspect_ratio:ratio.value, duration:duration.value})
    }));
    if (!started.request_id) {
      if (started.videoUrl) return showMedia(started.videoUrl, "video");
      throw new Error("سرویس شناسه پردازش ویدئو برنگرداند.");
    }
    const id = started.request_id;
    const maxAttempts = 150;
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      await new Promise(resolve => setTimeout(resolve, 4000));
      loaderText.textContent = "درخواست در صف سرویس است؛ این مرحله ممکن است چند دقیقه طول بکشد.";
      const status = await parseResponse(await fetch("/api/video-status?request_id=" + encodeURIComponent(id)));
      if (status.status === "COMPLETED" && status.videoUrl) return showMedia(status.videoUrl, "video");
      if (status.status === "FAILED" || status.status === "CANCELLED") throw new Error(status.error || "مدل نتوانست ویدئو را تولید کند. دوباره امتحان کن.");
    }
    throw new Error("ساخت ویدئو بیشتر از زمان انتظار طول کشید. ممکن است درخواست هنوز در صف باشد؛ هزینه را در داشبورد سرویس بررسی کن.");
  }
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const text = prompt.value.trim();
    if (text.length < 4) return showError("لطفاً یک توضیح کمی دقیق‌تر بنویس.");
    mediaOutput.replaceChildren();
    mediaOutput.hidden = true;
    $(".output-dot").classList.remove("ready");
    busy(true, mode === "image" ? "در حال ساخت تصویر..." : "در حال ساخت ویدئو...", mode === "image" ? "درخواست به مدل تصویرساز ارسال شده است." : "درخواست به صف تولید ویدئو ارسال شده است.");
    try {
      if (mode === "image") await generateImage(text);
      else await generateVideo(text);
    } catch (error) {
      busy(false);
      resultBadge.textContent = "تولید ناموفق";
      outputStatus.textContent = "خروجی تولید نشد";
      showError(error.message);
    }
  });
})();