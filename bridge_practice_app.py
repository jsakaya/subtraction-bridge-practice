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
      --dot-locked: #e5cfb7;
      --line: #6f7479;
      --accent: #2f6fcb;
      --ok: #1a7f46;
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
      width: min(980px, 100%);
      background: var(--card);
      border: 1px solid #d8d8d8;
      border-radius: 14px;
      padding: 14px 12px 18px;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
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

    .problem {
      margin: 4px 0 10px;
      text-align: center;
      font-size: clamp(36px, 7vw, 58px);
      font-weight: 900;
      letter-spacing: 0.02em;
    }

    .board {
      background: var(--panel);
      border: 3px solid var(--panel-border);
      border-radius: 8px;
      padding: 10px 10px;
      overflow-x: auto;
    }

    .row-wrap {
      display: grid;
      grid-template-columns: 62px 1fr;
      align-items: center;
      gap: 8px;
      margin: 5px 0;
    }

    .label {
      text-align: right;
      color: var(--muted);
      font-size: 20px;
      font-weight: 800;
    }

    .row {
      width: 590px;
      min-width: 590px;
      display: grid;
      grid-template-columns: repeat(10, 50px);
      gap: 10px;
      position: relative;
      align-items: center;
    }

    .slot {
      width: 50px;
      height: 50px;
    }

    .dot {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      border: 2px solid var(--dot-border);
      background: var(--dot);
      color: #1f2933;
      font-size: 13px;
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

    .dot.faded {
      background: var(--dot-faded);
      border-color: var(--dot-faded-border);
      color: #656d75;
      position: relative;
    }

    .dot.faded::after {
      content: "";
      position: absolute;
      left: -5px;
      right: -5px;
      top: calc(50% - 2px);
      height: 4px;
      border-radius: 999px;
      background: var(--line);
    }

    .dot.locked {
      background: var(--dot-locked);
      opacity: 0.7;
    }

    .dot:active {
      transform: scale(0.98);
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
      color: #8c2a2a;
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
      .row-wrap { grid-template-columns: 52px 1fr; gap: 6px; }
      .label { font-size: 18px; }
      .row {
        width: 460px;
        min-width: 460px;
        grid-template-columns: repeat(10, 40px);
        gap: 6px;
      }
      .slot, .dot {
        width: 40px;
        height: 40px;
        font-size: 11px;
      }
    }
  </style>
</head>
<body>
  <main class="app">
    <div class="topbar">
      <h1 class="title">Bridge Through 10</h1>
      <div id="meta" class="meta"></div>
    </div>

    <div id="problem" class="problem"></div>

    <section class="board">
      <div class="row-wrap">
        <div id="topLabel" class="label"></div>
        <div id="topRow" class="row"></div>
      </div>
      <div class="row-wrap">
        <div id="bottomLabel" class="label"></div>
        <div id="bottomRow" class="row"></div>
      </div>
    </section>

    <div id="status" class="status"></div>

    <div class="controls">
      <button id="resetBtn" class="ctrl alt" type="button">Reset Problem</button>
      <button id="sayBtn" class="ctrl alt" type="button">Say It Again</button>
      <button id="nextBtn" class="ctrl next" type="button">Next Problem</button>
    </div>

    <div class="legend">
      Top row is the smaller decade. Bottom row is the bigger decade.<br/>
      Tap bottom row first. When you hit the bridge ten, continue on the top row to y.
    </div>
  </main>

  <script>
    const DOTS_PER_ROW = 10;

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
        {
          name: "Level 1 • Around 10",
          bridges: [10],
          patterns: [[1,1],[2,1],[1,2],[2,2],[3,1],[3,2]],
        },
        {
          name: "Level 2 • Bridge 10 Bigger Jumps",
          bridges: [10],
          patterns: [[4,1],[5,1],[4,2],[5,2],[6,2],[7,2]],
        },
        {
          name: "Level 3 • 20s and 30s",
          bridges: [20, 30],
          patterns: [[1,1],[2,1],[2,2],[3,2],[4,2],[3,3],[5,2]],
        },
        {
          name: "Level 4 • 40s to 60s",
          bridges: [40, 50, 60],
          patterns: [[1,1],[2,1],[3,1],[2,2],[3,2],[4,2],[5,2],[3,3]],
        },
        {
          name: "Level 5 • 70s to 90s",
          bridges: [70, 80, 90],
          patterns: [[2,1],[3,1],[4,1],[3,2],[4,2],[5,2],[4,3],[5,3]],
        },
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

      // Ensure explicit examples.
      const examples = [
        makeProblem(10, 2, 2, "Level 1 • Around 10"),   // 12 - 8
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
      stage: "bottom",   // bottom -> top -> done
      bottomDone: 0,
      topDone: 0,
      lastShout: "",
    };

    const els = {
      meta: document.getElementById("meta"),
      problem: document.getElementById("problem"),
      topLabel: document.getElementById("topLabel"),
      bottomLabel: document.getElementById("bottomLabel"),
      topRow: document.getElementById("topRow"),
      bottomRow: document.getElementById("bottomRow"),
      status: document.getElementById("status"),
      resetBtn: document.getElementById("resetBtn"),
      sayBtn: document.getElementById("sayBtn"),
      nextBtn: document.getElementById("nextBtn"),
    };

    function currentProblem() {
      return state.problems[state.index];
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

    function expectedBottomValue(p) {
      // x, x-1, ...
      return p.minuend - state.bottomDone;
    }

    function expectedTopValue(p) {
      // bridge-1, bridge-2, ... down to y
      return p.bridge - 1 - state.topDone;
    }

    function onDotTap(row, index) {
      const p = currentProblem();

      if (state.stage === "done") {
        setStatus(`Finished: ${p.minuend} - ${p.subtrahend} = ${p.difference}`, "cheer");
        return;
      }

      if (state.stage === "bottom") {
        if (row !== "bottom") {
          setStatus(`Start on bottom row at ${expectedBottomValue(p)}.`, "error");
          return;
        }

        const expected = state.bottomDone; // left -> right
        if (index !== expected) {
          setStatus(`Tap ${expectedBottomValue(p)} next.`, "error");
          return;
        }

        state.bottomDone += 1;
        renderRows();

        if (state.bottomDone === p.jumpToTen) {
          state.stage = "top";
          shout(`Nice! You reached the bridge at ${p.bridge}.`);
          setTimeout(() => {
            if (state.stage === "top") {
              setStatus(`Now top row from right: start at ${expectedTopValue(p)}.`, "normal");
            }
          }, 900);
        } else {
          setStatus(`Good. Keep going: ${expectedBottomValue(p)} next.`, "normal");
        }
        return;
      }

      // stage: top
      if (row !== "top") {
        setStatus(`Now use the top row. Tap ${expectedTopValue(p)} next.`, "error");
        return;
      }

      const expectedTopIndex = DOTS_PER_ROW - 1 - state.topDone; // right -> left
      if (index !== expectedTopIndex) {
        setStatus(`Tap ${expectedTopValue(p)} next.`, "error");
        return;
      }

      state.topDone += 1;
      renderRows();

      if (state.topDone === p.jumpToSub) {
        state.stage = "done";
        shout(`Awesome! ${p.minuend} minus ${p.subtrahend} equals ${p.difference}.`);
      } else {
        setStatus(`Great. Keep going: ${expectedTopValue(p)} next.`, "normal");
      }
    }

    function makeDot(value, classes, onTap) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = classes;
      button.textContent = String(value);
      button.addEventListener("pointerdown", (event) => {
        event.preventDefault();
        onTap();
      });
      return button;
    }

    function makeSlot() {
      const slot = document.createElement("div");
      slot.className = "slot";
      return slot;
    }

    function renderRows() {
      const p = currentProblem();

      // Top row values: smaller decade ascending left->right (80..89).
      const topValues = Array.from(
        { length: DOTS_PER_ROW },
        (_, i) => (p.bridge - 10) + i
      );

      // Bottom row active values: bigger decade descending from x (95..91).
      const bottomValues = Array.from(
        { length: p.jumpToTen },
        (_, i) => p.minuend - i
      );

      const topCrossStart = DOTS_PER_ROW - state.topDone;

      els.topRow.textContent = "";
      for (let i = 0; i < DOTS_PER_ROW; i++) {
        const value = topValues[i];
        const isCrossed = i >= topCrossStart;
        const isLockedZone = i < (DOTS_PER_ROW - p.jumpToSub);
        const classes = [
          "dot",
          isCrossed ? "faded" : "",
          isLockedZone && !isCrossed ? "locked" : "",
        ]
          .filter(Boolean)
          .join(" ");
        els.topRow.appendChild(makeDot(value, classes, () => onDotTap("top", i)));
      }

      els.bottomRow.textContent = "";
      for (let i = 0; i < DOTS_PER_ROW; i++) {
        if (i >= bottomValues.length) {
          els.bottomRow.appendChild(makeSlot());
          continue;
        }
        const value = bottomValues[i];
        const isCrossed = i < state.bottomDone;
        const classes = ["dot", isCrossed ? "faded" : ""].filter(Boolean).join(" ");
        els.bottomRow.appendChild(makeDot(value, classes, () => onDotTap("bottom", i)));
      }
    }

    function renderMeta() {
      const p = currentProblem();
      els.problem.textContent = `${p.minuend} - ${p.subtrahend}`;
      els.meta.textContent = `${p.level} • ${state.index + 1} / ${state.problems.length}`;
      els.topLabel.textContent = `${p.bridge - 10}s`;
      els.bottomLabel.textContent = `${p.bridge}s`;
    }

    function resetCurrentProblem() {
      const p = currentProblem();
      state.stage = "bottom";
      state.bottomDone = 0;
      state.topDone = 0;
      renderMeta();
      renderRows();
      setStatus(`Tap bottom row from left. Start at ${p.minuend}.`, "normal");
    }

    function nextProblem() {
      state.index = (state.index + 1) % state.problems.length;
      resetCurrentProblem();
    }

    function sayAgain() {
      const p = currentProblem();
      const line =
        state.lastShout ||
        `Try this one: ${p.minuend} minus ${p.subtrahend}.`;
      speak(line);
    }

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
