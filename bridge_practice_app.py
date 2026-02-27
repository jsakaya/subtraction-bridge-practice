from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import webbrowser


HTML_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Bridge Through 10 Practice</title>
  <style>
    :root {
      --bg: #f4f4f4;
      --card: #ededed;
      --ink: #1f2933;
      --muted: #55616d;
      --panel: #d7d7d7;
      --panel-border: #ababab;
      --dot: #eda35e;
      --dot-border: #d37b2f;
      --dot-faded: #d5ccb9;
      --dot-faded-border: #bea982;
      --line: #6f7479;
      --ok: #1a7f46;
      --bad: #8c2a2a;
      --accent: #2f6fcb;
      --bridge: #7d5a23;
      --btn: #34495e;
      --btn-alt: #5a6e80;
      --btn-next: #1f7a47;
    }

    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: "Avenir Next", "Trebuchet MS", "Verdana", sans-serif;
      display: flex;
      justify-content: center;
      padding: 16px 10px 28px;
    }

    .app {
      width: min(1000px, 100%);
      background: var(--card);
      border: 1px solid #d8d8d8;
      border-radius: 14px;
      padding: 14px 12px 18px;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }

    .title {
      margin: 0;
      font-size: clamp(22px, 3.8vw, 34px);
      font-weight: 900;
      letter-spacing: 0.01em;
    }

    .meta {
      color: var(--muted);
      font-weight: 700;
      font-size: clamp(15px, 2.2vw, 19px);
    }

    .tally {
      font-size: clamp(18px, 2.5vw, 24px);
      font-weight: 900;
      color: #2f4b66;
      padding: 4px 10px;
      border-radius: 8px;
      background: #d8e3ef;
    }

    .problem {
      margin: 4px 0 8px;
      text-align: center;
      font-size: clamp(36px, 7vw, 58px);
      font-weight: 900;
      letter-spacing: 0.02em;
    }

    .chips {
      margin-top: 4px;
      margin-bottom: 10px;
      display: flex;
      justify-content: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .chip {
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 16px;
      font-weight: 800;
      background: #dde4ea;
      color: #3f5162;
    }

    .chip.bridge {
      background: #f0e1c7;
      color: var(--bridge);
    }

    .line-shell {
      background: var(--panel);
      border: 3px solid var(--panel-border);
      border-radius: 8px;
      padding: 10px 8px 12px;
      overflow-x: auto;
      touch-action: none;
    }

    .line-track {
      position: relative;
      display: grid;
      grid-auto-flow: column;
      grid-auto-columns: 58px;
      gap: 8px;
      width: max-content;
      margin: 0 auto;
      padding: 12px 10px 18px;
    }

    .line-track::before {
      content: "";
      position: absolute;
      left: 26px;
      right: 26px;
      top: 40%;
      height: 4px;
      border-radius: 999px;
      background: #b1b8bf;
    }

    .tick-cell {
      position: relative;
      width: 58px;
      height: 78px;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      z-index: 1;
    }

    .tick {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      border: 2px solid var(--dot-border);
      background: var(--dot);
      color: #1f2933;
      font-size: 14px;
      font-weight: 900;
      display: inline-flex;
      justify-content: center;
      align-items: center;
      user-select: none;
      touch-action: manipulation;
      box-shadow: 0 1px 0 rgba(0, 0, 0, 0.08);
      cursor: pointer;
      padding: 0;
    }

    .tick.current {
      box-shadow: 0 0 0 4px var(--accent);
    }

    .tick.bridge {
      border-color: #ba8a3f;
    }

    .tick.visited {
      background: var(--dot-faded);
      border-color: var(--dot-faded-border);
      color: #656d75;
      position: relative;
    }

    .tick.visited::after {
      content: "";
      position: absolute;
      left: -5px;
      right: -5px;
      top: calc(50% - 2px);
      height: 4px;
      border-radius: 999px;
      background: var(--line);
    }

    .bridge-tag {
      position: absolute;
      bottom: 0;
      font-size: 11px;
      font-weight: 800;
      border-radius: 999px;
      padding: 2px 7px;
      background: #f0e1c7;
      color: #7c5b24;
      white-space: nowrap;
    }

    .status {
      margin-top: 10px;
      min-height: 56px;
      padding: 10px 12px;
      border-radius: 10px;
      background: #e6ebf1;
      color: #324658;
      font-size: clamp(18px, 2.8vw, 27px);
      font-weight: 900;
      text-align: center;
      line-height: 1.2;
      transition: transform 160ms ease;
    }

    .status.cheer {
      background: #e6f4eb;
      color: var(--ok);
      transform: scale(1.01);
    }

    .status.error {
      background: #f6e5e5;
      color: var(--bad);
    }

    .answer-panel {
      margin-top: 10px;
      padding: 10px 10px 12px;
      border-radius: 10px;
      background: #e8ecef;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .answer-input {
      width: 112px;
      border: 2px solid #a8b2bc;
      border-radius: 9px;
      padding: 6px 8px;
      background: #fff;
      color: var(--ink);
      text-align: center;
      font-size: 30px;
      font-weight: 900;
    }

    .controls {
      margin-top: 12px;
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 10px;
    }

    button.ctrl {
      border: 0;
      border-radius: 10px;
      padding: 10px 14px;
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      background: var(--btn);
      cursor: pointer;
      touch-action: manipulation;
    }

    button.ctrl.alt { background: var(--btn-alt); }
    button.ctrl.next { background: var(--btn-next); }

    .legend {
      margin-top: 12px;
      text-align: center;
      color: #5b6772;
      font-size: 16px;
      font-weight: 700;
      line-height: 1.3;
    }

    @media (max-width: 720px) {
      .app { padding: 12px 8px 16px; }
      .line-track {
        grid-auto-columns: 46px;
        gap: 6px;
        padding: 10px 8px 16px;
      }
      .tick-cell { width: 46px; height: 66px; }
      .tick { width: 40px; height: 40px; font-size: 12px; }
      .line-track::before { left: 20px; right: 20px; top: 36%; }
    }
  </style>
</head>
<body>
  <main class="app">
    <div class="topbar">
      <h1 class="title">Bridge Through 10</h1>
      <div id="meta" class="meta"></div>
      <div id="tally" class="tally">Right: 0</div>
    </div>

    <div id="problem" class="problem"></div>

    <div class="chips">
      <span id="chipStart" class="chip"></span>
      <span id="chipBridge" class="chip bridge"></span>
      <span id="chipTarget" class="chip"></span>
    </div>

    <section class="line-shell">
      <div id="lineTrack" class="line-track"></div>
    </section>

    <div id="status" class="status"></div>

    <div class="answer-panel">
      <label for="answerInput" class="meta">Answer:</label>
      <input id="answerInput" class="answer-input" inputmode="numeric" />
      <button id="checkBtn" class="ctrl" type="button">Check Answer</button>
    </div>

    <div class="controls">
      <button id="resetBtn" class="ctrl alt" type="button">Reset Problem</button>
      <button id="sayBtn" class="ctrl alt" type="button">Say It Again</button>
      <button id="nextBtn" class="ctrl next" type="button">Next Problem</button>
    </div>

    <div class="legend">
      Start at x (right side), drag left across the number line to y.<br/>
      We celebrate at the bridge ten, then at the final answer.
    </div>
  </main>

  <script>
    function makeProblem(bridge, jumpToTen, jumpToSub, level) {
      const minuend = bridge + jumpToTen;
      const subtrahend = bridge - jumpToSub;
      return {
        bridge,
        minuend,
        subtrahend,
        jumpToTen,
        jumpToSub,
        difference: minuend - subtrahend,
        level,
      };
    }

    function buildProblems() {
      const levels = [
        { name: "Level 1 • Around 10", bridges: [10], patterns: [[1,1],[2,1],[1,2],[2,2],[3,1],[3,2]] },
        { name: "Level 2 • Bridge 10 Bigger Jumps", bridges: [10], patterns: [[4,1],[5,1],[4,2],[5,2],[6,2],[7,2]] },
        { name: "Level 3 • 20s and 30s", bridges: [20, 30], patterns: [[1,1],[2,1],[2,2],[3,2],[4,2],[3,3],[5,2]] },
        { name: "Level 4 • 40s to 60s", bridges: [40, 50, 60], patterns: [[1,1],[2,1],[3,1],[2,2],[3,2],[4,2],[5,2],[3,3]] },
        { name: "Level 5 • 70s to 90s", bridges: [70, 80, 90], patterns: [[2,1],[3,1],[4,1],[3,2],[4,2],[5,2],[4,3],[5,3]] },
      ];

      const out = [];
      const seen = new Set();
      for (const level of levels) {
        for (const bridge of level.bridges) {
          for (const [jumpToTen, jumpToSub] of level.patterns) {
            const p = makeProblem(bridge, jumpToTen, jumpToSub, level.name);
            if (p.minuend > 99 || p.subtrahend < 0) continue;
            const key = `${p.minuend}-${p.subtrahend}`;
            if (seen.has(key)) continue;
            seen.add(key);
            out.push(p);
          }
        }
      }

      const examples = [
        makeProblem(10, 2, 2, "Level 1 • Around 10"),   // 12 - 8
        makeProblem(20, 2, 1, "Level 1 • Around 10"),   // 22 - 19
        makeProblem(70, 3, 5, "Level 5 • 70s to 90s"),  // 73 - 65
        makeProblem(90, 5, 3, "Level 5 • 70s to 90s"),  // 95 - 87
      ];
      for (const p of examples) {
        const key = `${p.minuend}-${p.subtrahend}`;
        if (!seen.has(key)) {
          seen.add(key);
          out.push(p);
        }
      }
      return out;
    }

    const state = {
      problems: buildProblems(),
      index: 0,
      currentIndex: 0,
      stepsTaken: 0,
      bridgeShouted: false,
      done: false,
      lastShout: "",
      dragActive: false,
      dragPointerId: null,
      dragLastIndex: -1,
      rightKeys: new Set(),
    };

    const els = {
      meta: document.getElementById("meta"),
      tally: document.getElementById("tally"),
      problem: document.getElementById("problem"),
      chipStart: document.getElementById("chipStart"),
      chipBridge: document.getElementById("chipBridge"),
      chipTarget: document.getElementById("chipTarget"),
      lineTrack: document.getElementById("lineTrack"),
      status: document.getElementById("status"),
      answerInput: document.getElementById("answerInput"),
      checkBtn: document.getElementById("checkBtn"),
      resetBtn: document.getElementById("resetBtn"),
      sayBtn: document.getElementById("sayBtn"),
      nextBtn: document.getElementById("nextBtn"),
    };

    function currentProblem() {
      return state.problems[state.index];
    }

    function valuesForProblem(p) {
      const count = p.minuend - p.subtrahend + 1;
      return Array.from({ length: count }, (_, i) => p.subtrahend + i);
    }

    function problemKey(p) {
      return `${p.minuend}-${p.subtrahend}`;
    }

    function setStatus(text, tone = "normal") {
      els.status.textContent = text;
      els.status.className = `status ${tone}`;
    }

    function speak(text) {
      if (!("speechSynthesis" in window)) return;
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.95;
      utterance.pitch = 1.05;
      window.speechSynthesis.speak(utterance);
    }

    function shout(text) {
      state.lastShout = text;
      setStatus(text, "cheer");
      if ("vibrate" in navigator) {
        try { navigator.vibrate(35); } catch (_) {}
      }
      speak(text);
    }

    function renderMeta() {
      const p = currentProblem();
      els.problem.textContent = `${p.minuend} - ${p.subtrahend}`;
      els.meta.textContent = `${p.level} • ${state.index + 1} / ${state.problems.length}`;
      els.tally.textContent = `Right: ${state.rightKeys.size}`;
      els.chipStart.textContent = `Start ${p.minuend}`;
      els.chipBridge.textContent = `Bridge ${p.bridge}`;
      els.chipTarget.textContent = `Target ${p.subtrahend}`;
    }

    function currentValue() {
      const values = valuesForProblem(currentProblem());
      return values[state.currentIndex];
    }

    function renderLine() {
      const p = currentProblem();
      const values = valuesForProblem(p);
      els.lineTrack.textContent = "";

      for (let i = 0; i < values.length; i++) {
        const value = values[i];
        const cell = document.createElement("div");
        cell.className = "tick-cell";

        const classes = ["tick"];
        if (i > state.currentIndex) classes.push("visited");
        if (i === state.currentIndex) classes.push("current");
        if (value === p.bridge) classes.push("bridge");

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = classes.join(" ");
        btn.textContent = String(value);
        btn.dataset.index = String(i);

        cell.appendChild(btn);

        if (value === p.bridge) {
          const tag = document.createElement("div");
          tag.className = "bridge-tag";
          tag.textContent = "bridge";
          cell.appendChild(tag);
        }

        els.lineTrack.appendChild(cell);
      }
    }

    function advanceToIndex(targetIndex, strict) {
      const p = currentProblem();
      if (targetIndex > state.currentIndex) {
        if (strict) {
          setStatus(`Move left from ${currentValue()}.`, "error");
        }
        return;
      }
      if (targetIndex === state.currentIndex || state.done) return;

      const values = valuesForProblem(p);
      while (state.currentIndex > targetIndex && !state.done) {
        state.currentIndex -= 1;
        state.stepsTaken += 1;
        const valueNow = values[state.currentIndex];

        if (valueNow === p.bridge && !state.bridgeShouted) {
          state.bridgeShouted = true;
          shout(`Nice! You reached the bridge at ${p.bridge}.`);
        }

        if (valueNow === p.subtrahend) {
          state.done = true;
          shout(`Awesome! ${p.minuend} minus ${p.subtrahend} equals ${p.difference}.`);
        }
      }

      renderLine();
      if (!state.done) {
        if (!state.bridgeShouted) {
          setStatus(`Great. Keep going left to bridge ${p.bridge}.`, "normal");
        } else {
          setStatus(`Great. Keep going left to ${p.subtrahend}.`, "normal");
        }
      } else {
        setStatus(`Line complete. Type the answer below.`, "cheer");
      }
    }

    function checkAnswer() {
      const p = currentProblem();
      const guessed = Number.parseInt(els.answerInput.value.trim(), 10);
      if (Number.isNaN(guessed)) {
        setStatus("Type a number answer first.", "error");
        return;
      }

      if (guessed === p.difference) {
        state.rightKeys.add(problemKey(p));
        renderMeta();
        setStatus(`Correct! ${p.minuend} - ${p.subtrahend} = ${p.difference}`, "cheer");
        speak(`Correct! ${p.minuend} minus ${p.subtrahend} is ${p.difference}.`);
      } else {
        setStatus("Not yet. Try again.", "error");
      }
    }

    function parseTickElement(element) {
      if (!element || !element.closest) return null;
      const tick = element.closest(".tick[data-index]");
      if (!tick) return null;
      const index = Number.parseInt(tick.dataset.index, 10);
      if (Number.isNaN(index)) return null;
      return { index };
    }

    function processPointerAt(clientX, clientY, strict) {
      const target = document.elementFromPoint(clientX, clientY);
      const hit = parseTickElement(target);
      if (!hit) return;
      if (!strict && state.dragLastIndex === hit.index) return;
      state.dragLastIndex = hit.index;
      advanceToIndex(hit.index, strict);
    }

    function resetCurrentProblem() {
      const p = currentProblem();
      const values = valuesForProblem(p);
      state.currentIndex = values.length - 1; // start at x on right side
      state.stepsTaken = 0;
      state.bridgeShouted = false;
      state.done = false;
      state.lastShout = "";
      state.dragActive = false;
      state.dragPointerId = null;
      state.dragLastIndex = -1;
      els.answerInput.value = "";
      renderMeta();
      renderLine();
      setStatus(`Start at ${p.minuend} on the right, then drag left.`, "normal");
    }

    function nextProblem() {
      state.index = (state.index + 1) % state.problems.length;
      resetCurrentProblem();
    }

    function sayAgain() {
      const p = currentProblem();
      const line = state.lastShout || `Try this one: ${p.minuend} minus ${p.subtrahend}.`;
      speak(line);
    }

    els.lineTrack.addEventListener("pointerdown", (event) => {
      if (event.button !== undefined && event.button !== 0) return;
      const hit = parseTickElement(event.target);
      if (!hit) return;

      state.dragActive = true;
      state.dragPointerId = event.pointerId;
      state.dragLastIndex = -1;
      processPointerAt(event.clientX, event.clientY, true);
      event.preventDefault();
    });

    window.addEventListener("pointermove", (event) => {
      if (!state.dragActive || event.pointerId !== state.dragPointerId) return;
      processPointerAt(event.clientX, event.clientY, false);
      event.preventDefault();
    });

    function stopDrag(event) {
      if (!state.dragActive || event.pointerId !== state.dragPointerId) return;
      state.dragActive = false;
      state.dragPointerId = null;
      state.dragLastIndex = -1;
    }

    window.addEventListener("pointerup", stopDrag);
    window.addEventListener("pointercancel", stopDrag);

    els.checkBtn.addEventListener("click", () => checkAnswer());
    els.answerInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") checkAnswer();
    });
    els.resetBtn.addEventListener("click", () => resetCurrentProblem());
    els.nextBtn.addEventListener("click", () => nextProblem());
    els.sayBtn.addEventListener("click", () => sayAgain());

    resetCurrentProblem();
  </script>
</body>
</html>
"""


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path not in ("/", "/index.html"):
            self.send_error(404, "Not Found")
            return
        payload = HTML_PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the bridge-through-10 subtraction practice app."
    )
    parser.add_argument("--port", type=int, default=8765, help="Port to serve on.")
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not auto-open a browser tab.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    host = "127.0.0.1"
    url = f"http://{host}:{args.port}/"
    server = ThreadingHTTPServer((host, args.port), AppHandler)

    if not args.no_browser:
        threading.Timer(0.25, lambda: webbrowser.open(url)).start()

    print(f"Bridge practice app running at {url}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Stopped.")


if __name__ == "__main__":
    main()
