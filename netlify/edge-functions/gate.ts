import type { Config, Context } from "https://edge.netlify.com";

const COOKIE_NAME = "triage4us-gate";
const COOKIE_MAX_AGE = 60 * 60 * 24; // 24h
const BRAND = "Triage4US";

export default async function gate(request: Request, ctx: Context) {
  const password = Deno.env.get("GATE_PASSWORD") ?? "";

  // Gate disabled if env var unset/empty.
  if (!password) {
    return ctx.next();
  }

  const url = new URL(request.url);

  // Handle login form submission.
  if (request.method === "POST" && url.pathname === "/__gate") {
    const form = await request.formData();
    const submitted = String(form.get("password") ?? "").trim();

    if (submitted.toLowerCase() === password.toLowerCase()) {
      const headers = new Headers({ Location: "/" });
      headers.append(
        "Set-Cookie",
        `${COOKIE_NAME}=1; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${COOKIE_MAX_AGE}`,
      );
      return new Response(null, { status: 302, headers });
    }

    return renderLogin({ error: "Incorrect password. Try again.", status: 401 });
  }

  // Already authenticated → let the request through.
  const cookie = request.headers.get("cookie") ?? "";
  if (cookie.split(";").some((c) => c.trim() === `${COOKIE_NAME}=1`)) {
    return ctx.next();
  }

  // Otherwise show login screen.
  return renderLogin({});
}

function renderLogin({ error, status = 200 }: { error?: string; status?: number }) {
  const errorMarkup = error
    ? `<p class="gate_error" role="alert">${escapeHtml(error)}</p>`
    : "";

  const html = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="robots" content="noindex, nofollow" />
  <title>${BRAND} — Secure Preview</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" />
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    html, body { height: 100%; }
    body {
      margin: 0;
      font-family: "Poppins", system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background-color: #0a0a0a;
      color: #f5f5f5;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      -webkit-font-smoothing: antialiased;
    }
    .gate_card {
      width: 100%;
      max-width: 360px;
      display: flex;
      flex-direction: column;
      gap: 24px;
      text-align: center;
    }
    .gate_wordmark {
      font-size: 24px;
      font-weight: 700;
      letter-spacing: -0.01em;
      color: #ffffff;
    }
    .gate_eyebrow {
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: rgba(255, 255, 255, 0.55);
      margin: 0;
    }
    .gate_hint {
      font-size: 14px;
      line-height: 1.5;
      color: rgba(255, 255, 255, 0.7);
      margin: 0;
    }
    .gate_form {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 4px;
    }
    .gate_input {
      width: 100%;
      padding: 12px 14px;
      font-family: inherit;
      font-size: 15px;
      text-align: center;
      letter-spacing: 0.04em;
      color: #ffffff;
      background-color: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 10px;
      outline: none;
      transition: border-color 120ms ease, background-color 120ms ease;
    }
    .gate_input::placeholder { color: rgba(255, 255, 255, 0.35); }
    .gate_input:focus {
      border-color: rgba(255, 255, 255, 0.55);
      background-color: rgba(255, 255, 255, 0.08);
    }
    .gate_button {
      width: 100%;
      padding: 12px 14px;
      font-family: inherit;
      font-size: 15px;
      font-weight: 600;
      color: #0a0a0a;
      background-color: #ffffff;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      transition: transform 120ms ease, background-color 120ms ease;
    }
    .gate_button:hover { background-color: #e9e9e9; }
    .gate_button:active { transform: translateY(1px); }
    .gate_error {
      margin: 0;
      font-size: 13px;
      color: #ff6b6b;
    }
  </style>
</head>
<body>
  <main class="gate_card">
    <p class="gate_eyebrow">Secure Preview</p>
    <h1 class="gate_wordmark">${BRAND}</h1>
    <p class="gate_hint">This preview is private. Enter the access password to continue.</p>
    <form class="gate_form" method="POST" action="/__gate" autocomplete="off">
      <input
        class="gate_input"
        type="password"
        name="password"
        placeholder="Password"
        autofocus
        required
      />
      <button class="gate_button" type="submit">Enter</button>
      ${errorMarkup}
    </form>
  </main>
</body>
</html>`;

  return new Response(html, {
    status,
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}

function escapeHtml(s: string) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

export const config: Config = {
  path: "/*",
  excludedPath: [
    "/assets/*",
    "/robots.txt",
    "/sitemap.xml",
    "/favicon.ico",
    "*.css",
    "*.js",
    "*.mjs",
    "*.map",
    "*.svg",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.webp",
    "*.avif",
    "*.ico",
    "*.woff",
    "*.woff2",
    "*.ttf",
    "*.otf",
  ],
};
