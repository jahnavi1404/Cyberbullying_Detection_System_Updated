from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from detector import classify

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cyberbullying Detection</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #eceffa;
    --card: #ffffff;
    --ink: #1c1f3a;
    --muted: #6b7094;
    --line: #e3e6f4;
    --brand: #4c5bff;
    --brand-dark: #3644e0;
    --bad: #e5484d;
    --bad-soft: #fff0f0;
    --good: #12a37f;
    --good-soft: #e9f9f4;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: "Plus Jakarta Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--ink);
    min-height: 100vh;
  }

  /* top bar, like a social app header */
  .topbar {
    background: var(--card);
    border-bottom: 1px solid var(--line);
    position: sticky;
    top: 0;
    z-index: 5;
  }
  .topbar-inner {
    max-width: 640px;
    margin: 0 auto;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .logo {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    background: linear-gradient(135deg, #4c5bff, #9b5cff 55%, #ff6fa5);
    display: grid;
    place-items: center;
  }
  .logo svg { width: 22px; height: 22px; }
  .brand-name { font-weight: 800; font-size: 18px; letter-spacing: -0.01em; }
  .brand-sub { font-size: 12px; color: var(--muted); margin-top: 1px; }

  .feed {
    max-width: 640px;
    margin: 0 auto;
    padding: 24px 20px 60px;
    display: flex;
    flex-direction: column;
    gap: 18px;
  }

  .intro h1 {
    margin: 0 0 6px;
    font-size: 28px;
    line-height: 1.2;
    letter-spacing: -0.02em;
    font-weight: 800;
  }
  .intro p { margin: 0; color: var(--muted); font-size: 15px; line-height: 1.55; }

  .card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px;
  }

  /* avatar with story-style gradient ring */
  .avatar {
    flex: none;
    width: 46px;
    height: 46px;
    border-radius: 50%;
    padding: 2.5px;
    background: linear-gradient(135deg, #ffb347, #ff5f8f 50%, #7b5cff);
  }
  .avatar span {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: #fff;
    display: grid;
    place-items: center;
    font-weight: 800;
    color: var(--brand);
    font-size: 16px;
  }

  /* composer */
  .composer-row { display: flex; gap: 14px; }
  .composer-body { flex: 1; min-width: 0; }
  textarea {
    width: 100%;
    border: none;
    outline: none;
    resize: none;
    font: inherit;
    font-size: 17px;
    line-height: 1.5;
    color: var(--ink);
    padding: 10px 0;
    min-height: 92px;
    background: transparent;
  }
  textarea::placeholder { color: #a3a8c6; }

  .chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 4px 0 14px; }
  .chip {
    border: 1px solid var(--line);
    background: #f6f7fd;
    color: var(--muted);
    font: inherit;
    font-size: 13px;
    padding: 6px 12px;
    border-radius: 999px;
    cursor: pointer;
  }
  .chip:hover { border-color: var(--brand); color: var(--brand); }
  .chips-label { font-size: 13px; color: var(--muted); align-self: center; }

  .composer-foot {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 1px solid var(--line);
    padding-top: 14px;
  }
  .count { font-size: 13px; color: var(--muted); }
  .btn {
    border: none;
    background: var(--brand);
    color: #fff;
    font: inherit;
    font-weight: 700;
    font-size: 15px;
    padding: 11px 24px;
    border-radius: 999px;
    cursor: pointer;
  }
  .btn:hover { background: var(--brand-dark); }
  .btn:disabled { opacity: 0.6; cursor: wait; }
  .btn:focus-visible, .chip:focus-visible { outline: 3px solid #b7bdff; outline-offset: 2px; }

  /* result, shown as a post with a moderation banner */
  .post-head { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
  .post-name { font-weight: 700; font-size: 15px; }
  .post-meta { font-size: 12px; color: var(--muted); }
  .post-text {
    font-size: 17px;
    line-height: 1.55;
    margin: 0 0 16px;
    overflow-wrap: anywhere;
    white-space: pre-wrap;
  }
  .verdict {
    border-radius: 14px;
    padding: 14px 16px;
    display: flex;
    gap: 12px;
    align-items: flex-start;
  }
  .verdict.bad { background: var(--bad-soft); border: 1px solid #ffd3d4; }
  .verdict.good { background: var(--good-soft); border: 1px solid #bfeede; }
  .verdict-icon {
    flex: none;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: #fff;
    font-weight: 800;
  }
  .bad .verdict-icon { background: var(--bad); }
  .good .verdict-icon { background: var(--good); }
  .verdict-title { font-weight: 800; font-size: 16px; }
  .bad .verdict-title { color: #b42328; }
  .good .verdict-title { color: #0b7a5e; }
  .verdict-note { font-size: 14px; color: var(--muted); margin-top: 3px; line-height: 1.5; }
  .meter { margin-top: 10px; height: 8px; border-radius: 99px; background: rgba(0,0,0,0.07); overflow: hidden; }
  .meter > div { height: 100%; border-radius: 99px; }
  .bad .meter > div { background: var(--bad); }
  .good .meter > div { background: var(--good); }
  .meter-label { font-size: 12px; color: var(--muted); margin-top: 6px; }

  .result-in { animation: pop 0.35s ease-out; }
  @keyframes pop {
    from { opacity: 0; transform: translateY(10px) scale(0.98); }
    to { opacity: 1; transform: none; }
  }
  @media (prefers-reduced-motion: reduce) { .result-in { animation: none; } }

  .footer-note { text-align: center; font-size: 12px; color: var(--muted); }

  @media (max-width: 480px) {
    .intro h1 { font-size: 23px; }
    .card { padding: 14px; border-radius: 16px; }
  }
</style>
</head>
<body>

<header class="topbar">
  <div class="topbar-inner">
    <div class="logo" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6l7-3z"/>
        <path d="M9 12l2 2 4-4"/>
      </svg>
    </div>
    <div>
      <div class="brand-name">Cyberbullying Detection System</div>
      <div class="brand-sub">Check a comment before it gets posted</div>
    </div>
  </div>
</header>

<main class="feed">

  <section class="intro">
    <h1>Think before you post.</h1>
    <p>Write a comment, caption or message below and the model will tell you whether it reads as cyberbullying.</p>
  </section>

  <form class="card" method="post" action="/predict_form" id="check-form">
    <div class="composer-row">
      <div class="avatar"><span>Y</span></div>
      <div class="composer-body">
        <textarea id="message" name="message" maxlength="280" required
                  placeholder="What do you want to say?">{{ message or '' }}</textarea>
        <div class="chips">
          <span class="chips-label">Try:</span>
          <button type="button" class="chip" data-text="You are so stupid">You are so stupid</button>
          <button type="button" class="chip" data-text="Nice work, keep smiling!">Nice work, keep smiling!</button>
          <button type="button" class="chip" data-text="Have a great day">Have a great day</button>
        </div>
      </div>
    </div>
    <div class="composer-foot">
      <span class="count" id="count">0 / 280</span>
      <button class="btn" type="submit" id="submit-btn">Check message</button>
    </div>
  </form>

  {% if prediction %}
  <article class="card result-in" aria-live="polite">
    <div class="post-head">
      <div class="avatar"><span>Y</span></div>
      <div>
        <div class="post-name">Your message</div>
        <div class="post-meta">Just now</div>
      </div>
    </div>
    <p class="post-text">{{ message }}</p>

    {% if is_bullying %}
    <div class="verdict bad">
      <div class="verdict-icon">!</div>
      <div style="flex:1">
        <div class="verdict-title">Result: {{ prediction }}</div>
        <div class="verdict-note">This message looks harmful ({{ reason }}). Consider rewording it before sharing.</div>
        <div class="meter"><div style="width: {{ confidence }}%"></div></div>
        <div class="meter-label">{{ confidence }}% confidence</div>
      </div>
    </div>
    {% else %}
    <div class="verdict good">
      <div class="verdict-icon">&#10003;</div>
      <div style="flex:1">
        <div class="verdict-title">Result: {{ prediction }}</div>
        <div class="verdict-note">No bullying detected. This message is fine to post.</div>
        <div class="meter"><div style="width: {{ confidence }}%"></div></div>
        <div class="meter-label">{{ confidence }}% confidence</div>
      </div>
    </div>
    {% endif %}
  </article>
  {% endif %}

  <p class="footer-note">Built with Flask, TF-IDF and Logistic Regression</p>
</main>

<script>
  var box = document.getElementById("message");
  var count = document.getElementById("count");
  var form = document.getElementById("check-form");
  var btn = document.getElementById("submit-btn");

  function updateCount() { count.textContent = box.value.length + " / 280"; }
  box.addEventListener("input", updateCount);
  updateCount();

  document.querySelectorAll(".chip").forEach(function (chip) {
    chip.addEventListener("click", function () {
      box.value = chip.getAttribute("data-text");
      updateCount();
      box.focus();
    });
  });

  form.addEventListener("submit", function () {
    btn.disabled = true;
    btn.textContent = "Checking...";
  });
</script>
</body>
</html>
"""


# Home route
@app.route('/')
def home():
    return render_template_string(HTML_PAGE)


# API route (for client.py / Postman)
@app.route('/predict', methods=['POST'])
def predict():
    text = (request.get_json(silent=True) or {}).get('message', '')
    r = classify(text)
    return jsonify({
        'prediction': '1' if r['is_bullying'] else '0',
        'label': r['label'],
        'confidence': r['confidence'],
        'reason': r['reason'],
    })


# Form route (for browser UI)
@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    # Reloading /predict_form in the browser sends a GET, so go back home
    if request.method == 'GET':
        return redirect(url_for('home'))

    text = request.form.get('message', '').strip()
    if not text:
        return redirect(url_for('home'))

    r = classify(text)

    return render_template_string(
        HTML_PAGE,
        prediction=r['label'],
        is_bullying=r['is_bullying'],
        confidence=r['confidence'],
        reason=r['reason'],
        message=text,
    )


if __name__ == '__main__':
    app.run(debug=True)
