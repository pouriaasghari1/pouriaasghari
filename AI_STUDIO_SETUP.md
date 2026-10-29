# NEURAFRAME AI Studio

This is a real image/video generation frontend plus server-side API routes. It does not fake output. Until configured with a working fal.ai key, API requests return a clear configuration error.

## Features
- Text-to-image through `fal-ai/flux/schnell`
- Text-to-video through `lightricks/ltx-2.5/text-to-video/fast`
- Video queue polling and output links
- API credentials stay on the server; they are never embedded in browser JavaScript
- Persian RTL responsive interface

## Deploy on Vercel
GitHub Pages only serves static files and cannot execute the `api/*.js` server functions. Deploy this repository to Vercel to use the API routes.

1. Sign in to Vercel and import `pouriaasghari1/pouriaasghari`.
2. Keep the project root at the repository root. The site page is `/studio.html`.
3. In Project Settings → Environment Variables, add:
   - `FAL_KEY`: a private API key from fal.ai
   - `APP_ACCESS_CODE`: create a long, unique access code for your own use. Do not publish it.
4. Redeploy after adding environment variables.
5. Open `/studio.html` on the deployed Vercel domain.
6. The browser UI needs to send `x-app-code`; enter your access code when prompted by the browser. Do not send either secret to anyone.

## API and cost notes
- Image generation uses FLUX Schnell.
- Video generation uses LTX 2.5 Fast through fal's queue API.
- Provider usage is billable. Check the current model price in the provider dashboard before generating. The app does not promise free generation.
- The access code is a simple private-use gate, not a full user-account/payment system. Do not publish this as a public paid SaaS until proper authentication, per-user quotas, rate limiting, billing, and abuse controls are added.
- Do not paste API keys into HTML/JS or commit them to Git.
- Availability, pricing, account eligibility, and payment options are controlled by the API provider and can change.

## Notes
The static preview can load on GitHub Pages, but generation will not work there because GitHub Pages does not run serverless functions. For real generation, use the Vercel deployment and configure both environment variables.
