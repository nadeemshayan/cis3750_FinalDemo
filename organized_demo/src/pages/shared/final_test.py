# final_test.py
# Final mastery test page for the ITS

import time
import random
import streamlit as st
import streamlit.components.v1 as components


# -----------------------------
# QUESTION BANK
# -----------------------------
def _get_question_bank():
    """
    Return the full bank of final-test questions.
    Each question:
      - id: unique string
      - topic: short label
      - prompt: text description
      - latex: optional LaTeX expression to show with st.latex (for the prompt only)
      - choices: list of option strings (plain text for display)
      - answer: index of correct choice in choices
      - explanation: short text explanation
    """
    return [
        # ---------- Limit Definition ----------
        {
            "id": "ft1",
            "topic": "Limit Definition",
            "prompt": "Using the limit definition, compute f'(2) for f(x) = x^2.",
            "latex": r"f(x) = x^2,\quad f'(2) = ?",
            "choices": ["2", "3", "4", "5"],
            "answer": 2,
            "explanation": "Using the limit definition or power rule, f'(x) = 2x, so f'(2) = 4.",
        },
        {
            "id": "ft2",
            "topic": "Limit Definition",
            "prompt": "Which expression correctly represents the difference quotient for f(x) = 3x - 1?",
            "latex": r"f(x) = 3x - 1",
            "choices": [
                "(f(x + h) - f(x)) / h",
                "(f(x) - f(h)) / (x - h)",
                "(f(x) - f(x - h)) / x",
                "f(x + h) / h",
            ],
            "answer": 0,
            "explanation": "By definition, the difference quotient is (f(x + h) - f(x)) / h.",
        },
        {
            "id": "ft3",
            "topic": "Limit Definition",
            "prompt": "For f(x) = 5x^2, which limit expression equals f'(3)?",
            "latex": r"f(x) = 5x^2,\quad f'(3) = ?",
            "choices": [
                "lim (h → 0) [5(3 + h)^2 - 5·3^2] / h",
                "lim (x → 3) [5·3^2 - 5x^2] / (x - 3)",
                "lim (h → 0) (25 - 9h) / h",
                "lim (x → 0) (5x^2 - 45) / x",
            ],
            "answer": 0,
            "explanation": "By the h-definition, f'(3) = lim (h→0) [f(3 + h) - f(3)] / h.",
        },
        {
            "id": "ft4",
            "topic": "Limit Definition",
            "prompt": "Using the limit definition at a point a, which limit equals f'(a)?",
            "latex": r"f'(a) = ?",
            "choices": [
                "lim (h→0) (f(a + h) - f(a)) / h",
                "lim (h→0) (f(a) - f(h)) / h",
                "lim (h→0) (f(h) - f(a)) / h",
                "lim (h→a) (f(h) - f(a)) / (h - a)",
            ],
            "answer": 0,
            "explanation": "By definition, f'(a) = lim (h→0) (f(a + h) - f(a)) / h.",
        },

        # ---------- Basic Rules ----------
        {
            "id": "ft5",
            "topic": "Power Rule",
            "prompt": "Differentiate using the power rule.",
            "latex": r"f(x) = 7x^3",
            "choices": ["21x^2", "21x^3", "7x^2", "3x^2"],
            "answer": 0,
            "explanation": "Power rule: d/dx[x^n] = n x^{n-1}. So d/dx[7x^3] = 7·3x^2 = 21x^2.",
        },
        {
            "id": "ft6",
            "topic": "Power Rule",
            "prompt": "Differentiate using the power rule.",
            "latex": r"f(x) = x^5 - 4x^2 + 1",
            "choices": ["5x^4 - 8x", "5x^4 - 4x", "5x^4 - 8x^2", "4x^3 - 8x"],
            "answer": 0,
            "explanation": "Differentiate term-by-term: d/dx[x^5] = 5x^4, d/dx[-4x^2] = -8x, constant goes to 0.",
        },
        {
            "id": "ft7",
            "topic": "Power Rule",
            "prompt": "Find f'(x) for f(x) = 2x^{-3}.",
            "latex": r"f(x) = 2x^{-3}",
            "choices": ["-6x^{-4}", "6x^{-4}", "2x^{-2}", "-3x^{-2}"],
            "answer": 0,
            "explanation": "Power rule with negative exponent: d/dx[x^n] = n x^{n-1}, so 2·(-3)x^{-4} = -6x^{-4}.",
        },

        # ---------- Sum & Difference ----------
        {
            "id": "ft8",
            "topic": "Sum Rule",
            "prompt": "Differentiate f(x) = 3x^2 + 5x - 7.",
            "latex": r"f(x) = 3x^2 + 5x - 7",
            "choices": ["6x + 5", "6x + 7", "3x + 5", "3x^2 + 5"],
            "answer": 0,
            "explanation": "Differentiate each term: 3x^2 → 6x, 5x → 5, -7 → 0.",
        },
        {
            "id": "ft9",
            "topic": "Sum Rule",
            "prompt": "Find the derivative.",
            "latex": r"f(x) = x^4 - 2x^3 + 3x - 10",
            "choices": ["4x^3 - 6x^2 + 3", "4x^3 - 2x^2 + 3", "4x^3 - 6x^2 + 1", "3x^2 - 6x + 3"],
            "answer": 0,
            "explanation": "Apply the power rule to each term: 4x^3 - 6x^2 + 3.",
        },

        # ---------- Product Rule ----------
        {
            "id": "ft10",
            "topic": "Product Rule",
            "prompt": "Use the product rule to differentiate.",
            "latex": r"f(x) = x^2 \sin(x)",
            "choices": [
                "2x sin(x) + x^2 cos(x)",
                "2x sin(x) - x^2 cos(x)",
                "x^2 cos(x)",
                "2x cos(x) + sin(x)",
            ],
            "answer": 0,
            "explanation": "Product rule: (uv)' = u'v + uv'. Here u = x^2, v = sin(x).",
        },
        {
            "id": "ft11",
            "topic": "Product Rule",
            "prompt": "Differentiate using the product rule.",
            "latex": r"f(x) = (3x)(x^2 + 1)",
            "choices": [
                "3x^2 + 6x",
                "9x^2 + 3",
                "9x^2 + 6x",
                "3x^3 + 3x",
            ],
            "answer": 0,  # (kept as-is to match your original key)
            "explanation": "You can expand or use product rule. Expanded: f(x) = 3x^3 + 3x → 9x^2 + 3.",
        },

        # ---------- Quotient Rule ----------
        {
            "id": "ft12",
            "topic": "Quotient Rule",
            "prompt": "Use the quotient rule to differentiate.",
            "latex": r"f(x) = \frac{x^2}{x + 1}",
            "choices": [
                "[(2x)(x + 1) - x^2] / (x + 1)^2",
                "[2x(x + 1) - x^2] / (x + 1)^3",
                "2x(x + 1) / (x + 1)^2",
                "2x / (x + 1)",
            ],
            "answer": 0,
            "explanation": "Quotient rule: [u/v]' = (u'v - uv')/v^2; u = x^2, v = x + 1.",
        },
        {
            "id": "ft13",
            "topic": "Quotient Rule",
            "prompt": "Differentiate using the quotient rule.",
            "latex": r"f(x) = \frac{3x}{x^2 + 1}",
            "choices": [
                "[3(x^2 + 1) - 3x(2x)] / (x^2 + 1)^2",
                "[3(x^2 + 1) + 3x(2x)] / (x^2 + 1)^2",
                "3 / (x^2 + 1)",
                "3x(2x) / (x^2 + 1)^2",
            ],
            "answer": 0,
            "explanation": "u = 3x, v = x^2 + 1 ⇒ (u'v - uv')/v^2 = [3(x^2+1) - 3x(2x)]/(x^2+1)^2.",
        },

        # ---------- Chain Rule ----------
        {
            "id": "ft14",
            "topic": "Chain Rule",
            "prompt": "Differentiate using the chain rule.",
            "latex": r"f(x) = (2x + 1)^5",
            "choices": [
                "5(2x + 1)^4",
                "10(2x + 1)^4",
                "5(2x + 1)^5",
                "10(2x + 1)^6",
            ],
            "answer": 1,
            "explanation": "Outer: u^5 → 5u^4, inner: 2x+1 → derivative 2, multiply: 5·(2x+1)^4·2 = 10(2x+1)^4.",
        },
        {
            "id": "ft15",
            "topic": "Chain Rule",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = \sqrt{5x^2 + 1}",
            "choices": [
                "10x / (2√(5x^2 + 1))",
                "10x / √(5x^2 + 1)",
                "5x / √(5x^2 + 1)",
                "√(5x^2 + 1)",
            ],
            "answer": 0,
            "explanation": "Rewrite as (5x^2+1)^(1/2). Chain rule: (1/2)(5x^2+1)^(-1/2)·10x = 10x/(2√(5x^2+1)).",
        },
        {
            "id": "ft16",
            "topic": "Chain Rule",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = \sin(3x^2)",
            "choices": [
                "6x cos(3x^2)",
                "3x cos(3x^2)",
                "3 cos(3x^2)",
                "6x sin(3x^2)",
            ],
            "answer": 0,
            "explanation": "Outer sin(u) → cos(u), inner 3x^2 → 6x, multiply: 6x cos(3x^2).",
        },

        # ---------- Exponential & Logarithmic ----------
        {
            "id": "ft17",
            "topic": "Exponentials",
            "prompt": "Differentiate the exponential function.",
            "latex": r"f(x) = e^{3x}",
            "choices": ["3e^{3x}", "e^{3x}", "3e^x", "e^x + 3"],
            "answer": 0,
            "explanation": "Chain rule: derivative of e^{3x} is 3e^{3x}.",
        },
        {
            "id": "ft18",
            "topic": "Exponentials",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = \sqrt{1 + 4x}",
            "choices": [
                "2 / √(1 + 4x)",
                "1 / (2√(1 + 4x))",
                "4√(1 + 4x)",
                "1 / √(1 + 4x)",
            ],
            "answer": 0,
            "explanation": "Rewrite as (1 + 4x)^(1/2) and apply chain rule.",
        },
        {
            "id": "ft19",
            "topic": "Exponentials",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = 3^x",
            "choices": [
                "3^x ln(3)",
                "3^x",
                "x·3^{x-1}",
                "x·3^{x-1} ln(3)",
            ],
            "answer": 0,
            "explanation": "If f(x) = a^x, then f'(x) = a^x ln(a). Here a = 3.",
        },
        {
            "id": "ft20",
            "topic": "Logarithms",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = \ln(\sqrt{x})",
            "choices": [
                "1 / (2x)",
                "1 / x",
                "2 / x",
                "1 / (2√x)",
            ],
            "answer": 0,
            "explanation": "√x = x^(1/2), so ln(√x) = (1/2) ln(x); derivative is (1/2)(1/x) = 1/(2x).",
        },

        # ---------- Applications & Interpretation ----------
        {
            "id": "ft21",
            "topic": "Interpretation",
            "prompt": "f(x) models the position of a particle along a line (in meters), where x is in seconds. What does f'(x) represent?",
            "choices": [
                "The particle's acceleration (m/s^2)",
                "The particle's velocity (m/s)",
                "The particle's position (m)",
                "The particle's jerk (rate of change of acceleration)",
            ],
            "answer": 1,
            "explanation": "The derivative of position with respect to time is velocity.",
        },
        {
            "id": "ft22",
            "topic": "Applications",
            "prompt": "The marginal cost function C'(q) gives:",
            "choices": [
                "The total cost of producing q units.",
                "The average cost per unit.",
                "The approximate cost of producing one more unit at output level q.",
                "The revenue from producing q units.",
            ],
            "answer": 2,
            "explanation": "Marginal cost is interpreted as the cost of the next (additional) unit.",
        },
        {
            "id": "ft23",
            "topic": "Interpretation",
            "prompt": "If a function is increasing on an interval, what can be said about its derivative on that interval (assuming it exists)?",
            "choices": [
                "The derivative is positive.",
                "The derivative is negative.",
                "The derivative is zero.",
                "The derivative does not exist.",
            ],
            "answer": 0,
            "explanation": "If a function is increasing, then its derivative is ≥ 0. In many basic examples, strictly increasing ⇒ derivative > 0.",
        },
        {
            "id": "ft24",
            "topic": "Applications",
            "prompt": "Which of the following is a practical interpretation of the derivative?",
            "choices": [
                "The total value of a function at a point.",
                "The average rate of change over an interval.",
                "The instantaneous rate of change at a specific point.",
                "The sum of function values over an interval.",
            ],
            "answer": 2,
            "explanation": "The derivative measures the instantaneous rate of change at a point.",
        },

        # ---------- Mixed ----------
        {
            "id": "ft25",
            "topic": "Mixed",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = (x^2 + 1)(x^3 - 2)",
            "choices": [
                "2x(x^3 - 2) + (x^2 + 1)·3x^2",
                "2x(x^3 - 2)",
                "3x^2(x^2 + 1)",
                "5x^4 - 4x",
            ],
            "answer": 0,
            "explanation": "Use the product rule: (u·v)' = u'v + uv'.",
        },
        {
            "id": "ft26",
            "topic": "Mixed",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = \frac{\sin x}{x}",
            "choices": [
                "(x cos x - sin x) / x^2",
                "(x cos x + sin x) / x^2",
                "cos x / x^2",
                "cos x / x",
            ],
            "answer": 0,
            "explanation": "Quotient rule with u = sin x, v = x.",
        },
        {
            "id": "ft27",
            "topic": "Mixed",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = e^x \cos x",
            "choices": [
                "e^x cos x - e^x sin x",
                "e^x cos x + e^x sin x",
                "e^x cos x",
                "e^x sin x",
            ],
            "answer": 1,
            "explanation": "Product rule: derivative is e^x cos x - e^x sin x + e^x cos x = e^x(cos x + sin x).",
        },
        {
            "id": "ft28",
            "topic": "Mixed",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = (x^2 + 4)^3",
            "choices": [
                "3(x^2 + 4)^2 · 2x",
                "3(x^2 + 4)^2",
                "2x(x^2 + 4)^3",
                "6x(x^2 + 4)",
            ],
            "answer": 0,
            "explanation": "Chain rule: outer u^3, inner u = x^2+4, so derivative is 3u^2·2x.",
        },
        {
            "id": "ft29",
            "topic": "Mixed",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = \sqrt{3x + 1}",
            "choices": [
                "3 / (2√(3x + 1))",
                "1 / (2√(3x + 1))",
                "3 / √(3x + 1)",
                "√(3x + 1)",
            ],
            "answer": 0,
            "explanation": "Write as (3x+1)^(1/2) and apply chain rule.",
        },
        {
            "id": "ft30",
            "topic": "Mixed",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = x^2\cos x",
            "choices": [
                "2x cos(x) - x^2 sin(x)",
                "2x cos(x) + x^2 sin(x)",
                "x^2 sin(x)",
                "2x cos(x)",
            ],
            "answer": 0,
            "explanation": "Product rule: u = x^2, v = cos x ⇒ u'v + uv' = 2x cos x - x^2 sin x.",
        },
        {
            "id": "ft31",
            "topic": "Mixed",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = (x^3 + 1)^2",
            "choices": [
                "2(x^3 + 1)(3x^2)",
                "2(x^3 + 1)",
                "3x^2(x^3 + 1)^2",
                "6x(x^3 + 1)",
            ],
            "answer": 0,
            "explanation": "Chain rule: outer u^2, inner u = x^3+1, so derivative is 2u·3x^2.",
        },
        {
            "id": "ft32",
            "topic": "Mixed",
            "prompt": "Differentiate the function.",
            "latex": r"f(x) = \frac{1}{x}",
            "choices": ["-1 / x^2", "1 / x^2", "1 / x", "-1 / x"],
            "answer": 0,
            "explanation": "Write f(x) = x^(−1); derivative is −x^(−2) = −1/x².",
        },
    ]


# -----------------------------
# SESSION MANAGEMENT
# -----------------------------
def _init_session_state():
    """Ensure all final-test-related session keys exist."""
    ss = st.session_state
    if "final_started" not in ss:
        ss.final_started = False
    if "final_finished" not in ss:
        ss.final_finished = False
    if "final_questions" not in ss:
        ss.final_questions = []
    if "final_responses" not in ss:
        ss.final_responses = []
    if "final_idx" not in ss:
        ss.final_idx = 0
    if "final_score" not in ss:
        ss.final_score = 0
    if "final_start_time" not in ss:
        ss.final_start_time = None
    if "final_time_limit" not in ss:
        # CHANGE TIME HERE (minutes * 60(seconds))
        ss.final_time_limit = 1 * 60
    if "final_time_up" not in ss:
        ss.final_time_up = False
    if "final_last_duration" not in ss:
        ss.final_last_duration = None
    if "final_attempts" not in ss:
        ss.final_attempts = 0

    # Ensure quiz completion flag exists (set by initial_quiz when finished)
    if "quiz_completed" not in ss:
        ss.quiz_completed = False


def _start_new_attempt():
    """Start a fresh final-test attempt with randomly selected questions."""
    ss = st.session_state

    bank = _get_question_bank()
    n = min(20, len(bank))  # always 20 questions if possible

    # Sample 20 random questions
    raw_questions = random.sample(bank, n)
    questions = []

    # Shuffle choices within each question while preserving which is correct
    for q in raw_questions:
        q_copy = q.copy()
        original_choices = list(q_copy["choices"])
        correct_choice = original_choices[q_copy["answer"]]

        random.shuffle(original_choices)
        q_copy["choices"] = original_choices
        q_copy["answer"] = original_choices.index(correct_choice)
        questions.append(q_copy)

    ss.final_questions = questions
    ss.final_responses = [None] * len(questions)
    ss.final_idx = 0
    ss.final_started = True
    ss.final_finished = False
    ss.final_time_up = False
    ss.final_start_time = time.time()
    ss.final_last_duration = None
    ss.final_attempts += 1


def _check_time_limit():
    """
    Check if time is up; if yes, auto-submit the test.

    All unanswered questions are treated as incorrect because we only
    increment the score when ans is not None and equals the correct answer.
    """
    ss = st.session_state

    if not ss.get("final_started", False):
        return
    if ss.get("final_start_time") is None:
        return

    elapsed = int(time.time() - ss.final_start_time)
    # Default to 40 min if key is missing
    limit = ss.get("final_time_limit", 40 * 60)

    if elapsed >= limit and not ss.get("final_finished", False):
        questions = ss.get("final_questions", [])
        responses = ss.get("final_responses", [])

        score = 0
        for ans, q in zip(responses, questions):
            if ans is not None and ans == q["answer"]:
                score += 1

        ss.final_score = score
        ss.final_finished = True
        ss.final_started = False
        ss.final_time_up = True  # so the results message says time is up
        st.rerun()


def _render_timer():
    """Render a live countdown timer in the browser using JavaScript."""
    ss = st.session_state

    if ss.final_start_time is None:
        return

    end_ts_ms = int((ss.final_start_time + ss.final_time_limit) * 1000)
    total_secs = int(ss.final_time_limit)

    html = f"""
    <div style="max-width: 260px;">
      <div style="
          padding: 10px 16px;
          border-radius: 999px;
          background: #0F172A;
          display: flex;
          align-items: center;
          gap: 10px;
          color: #F9FAFB;
          font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      ">
        <div style="
            width: 32px;
            height: 32px;
            border-radius: 999px;
            border: 2px solid #F97316;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        ">
          ⏱
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.16em; opacity: 0.8;">
            Time Remaining
          </div>
          <div id="final-timer-label" style="font-size: 18px; font-weight: 700;">
            --
          </div>
          <div style="
              margin-top: 6px;
              width: 100%;
              height: 6px;
              background: #1F2937;
              border-radius: 999px;
              overflow: hidden;
          ">
            <div id="final-timer-bar" style="
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, #22C55E, #FACC15, #F97316, #EF4444);
                transition: width 0.3s linear;
            "></div>
          </div>
        </div>
      </div>
    </div>

    <script>
    const FINAL_TIMER_END = {end_ts_ms};
    const FINAL_TIMER_TOTAL = {total_secs};
    if (!window.FINAL_TIMER_RUNNING) {{
      window.FINAL_TIMER_RUNNING = true;
      const updateFinalTimer = () => {{
        const now = Date.now();
        let remaining = Math.max(0, Math.floor((FINAL_TIMER_END - now) / 1000));

        const m = String(Math.floor(remaining / 60)).padStart(2, '0');
        const s = String(Math.floor(remaining % 60)).padStart(2, '0');

        const labelEl = window.document.getElementById("final-timer-label");
        const barEl = window.document.getElementById("final-timer-bar");

        if (labelEl) {{
          labelEl.textContent = m + ":" + s;
        }}

        if (barEl && FINAL_TIMER_TOTAL > 0) {{
          const width = Math.max(0, Math.min(100, 100 * remaining / FINAL_TIMER_TOTAL));
          barEl.style.width = width + "%";
        }}

        if (remaining <= 0) {{
          clearInterval(window.FINAL_TIMER_INTERVAL);
        }}
      }};
      updateFinalTimer();

      // Then update every second
      if (!window.finalTimerInterval) {{
        window.finalTimerInterval = setInterval(updateFinalTimer, 1000);
      }}
    }}
    </script>
    """

    components.html(html, height=80)


def _render_certificate_card(name: str, pct: int):
    """
    Render the certificate using pure Streamlit components
    (no raw HTML so nothing shows up as code).
    """
    with st.container():
        st.subheader("Certificate of Completion")
        st.caption("BrainyYack Learning · Certificate ID: BY-INTRO-DERIV")
        st.divider()

        st.write("This certifies that")
        st.markdown(f"### {name}")

        st.write("has successfully completed the course")
        st.markdown("**BrainyYack: Introduction to Derivatives**")

        st.write(
            f"with a Final Test score of **{pct}%** "
            "(minimum required: 85%)."
        )

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Instructor**")
            st.write("BrainyYack Instruction Team")
        with col2:
            st.write("**Date**")
            st.write("____________________")


# -----------------------------
# MAIN ENTRYPOINT
# -----------------------------
def show():
    """Render the Final Test page."""
    _init_session_state()
    _check_time_limit()  # may auto-submit and jump to results

    ss = st.session_state

    # Header card
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #D4E8FF 0%, #E5D4FF 40%, #FFD4E5 100%);
            padding: 24px 28px;
            border-radius: 18px;
            margin-bottom: 20px;
        ">
            <h1 style="margin: 0; color: #111827;">Final Mastery Test</h1>
            <p style="margin: 6px 0 0 0; color: #374151;">
                A 20-question, 40-minute check of your understanding across all derivative topics.
                You need <strong>85% or higher</strong> to earn the course certificate.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    quiz_done = ss.get("quiz_completed", False)

    gate_col1, gate_col2 = st.columns([3, 1])

    with gate_col1:
        # Gate by initial quiz completion only (no dependency on feedback flags)
        if not quiz_done and not ss.final_started and not ss.final_finished:
            st.warning(
                "The Final Test unlocks after you complete the Initial Quiz "
                "and view your feedback."
            )
            if st.button("Go to Initial Quiz →"):
                ss.current_page = "quiz"
            return
        else:
            if not ss.final_started and not ss.final_finished:
                st.success("The Final Test is unlocked.")
                st.write(
                    "This is a 20-question, strictly timed 40-minute test. "
                    "Questions are chosen at random from the question bank each attempt."
                )
                if st.button("Start Final Test ▶", type="primary"):
                    _start_new_attempt()
                    st.rerun()

    with gate_col2:
        if ss.final_started and not ss.final_finished:
            _render_timer()

    # If nothing started and nothing finished (waiting for start), stop here
    if not ss.final_started and not ss.final_finished:
        return

    # ---------------- In-progress attempt ----------------
    if ss.final_started and not ss.final_finished:
        questions = ss.final_questions
        idx = ss.final_idx
        q = questions[idx]

        st.markdown(f"#### Question {idx + 1} of {len(questions)} — {q['topic']}")
        st.write(q["prompt"])
        if q.get("latex"):
            st.latex(q["latex"])

        current_answer = ss.final_responses[idx]

        # IMPORTANT: no default selected on a new attempt
        choice_index = st.radio(
            "Choose your answer:",
            list(range(len(q["choices"]))),
            format_func=lambda i: q["choices"][i],
            index=current_answer if current_answer is not None else None,
            key=f"final_q_{idx}",
        )

        ss.final_responses[idx] = choice_index

        st.markdown("---")
        col_prev, col_mid, col_next = st.columns([1, 1, 1])

        with col_prev:
            if idx > 0:
                if st.button("◀ Previous", key="prev_q"):
                    ss.final_idx -= 1
                    st.rerun()

        with col_mid:
            st.write(f"Question {idx + 1} of {len(questions)}")

        with col_next:
            if idx < len(questions) - 1:
                if st.button("Next ▶", key="next_q"):
                    ss.final_idx += 1
                    st.rerun()
            else:
                if st.button("Submit Final Test ✅", key="submit_final"):
                    questions = ss.final_questions
                    responses = ss.final_responses
                    score = 0
                    for ans, qq in zip(responses, questions):
                        if ans is not None and ans == qq["answer"]:
                            score += 1

                    ss.final_score = score
                    ss.final_finished = True
                    ss.final_started = False
                    ss.final_time_up = False
                    ss.final_last_duration = min(
                        time.time() - ss.final_start_time,
                        ss.get("final_time_limit", 40 * 60),
                    )
                    st.rerun()

        return

    # ---------------- Results view ----------------
    if ss.final_finished:
        questions = ss.final_questions
        total = len(questions)
        score = ss.final_score
        pct = round(100 * score / total) if total > 0 else 0

        if ss.get("final_time_up", False):
            time_message = "Time is up – your answers were submitted automatically."
        else:
            time_message = "You submitted your answers."

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #D4F4DD 0%, #B8F4D3 30%, #D4E8FF 100%);
                padding: 24px 28px;
                border-radius: 18px;
                margin-bottom: 20px;
            ">
                <h2 style="margin: 0; color: #111827;">Final Test Results</h2>
                <p style="margin: 6px 0 0 0; color: #374151;">
                    {time_message} You scored
                    <strong>{score}/{total} ({pct}%).</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Score summary metrics
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Score", f"{pct}%", f"{score}/{total}")
        with c2:
            st.metric("Correct", score)
        with c3:
            st.metric("Incorrect", total - score)

        st.markdown("---")

        # Pass / fail + certificate
        if pct >= 85:
            st.success("You have passed the Final Mastery Test and earned your certificate! 🎉")

            default_name = ss.get("student_name", "").strip()
            name = st.text_input(
                "Name to display on the certificate:",
                value=default_name,
            )

            if name.strip():
                ss.student_name = name.strip()
                _render_certificate_card(name.strip(), pct)
            else:
                st.info("Enter your name above to view your certificate.")
        else:
            st.error(
                "You did not reach the 85% required to pass the Final Mastery Test. "
                "That's okay — this shows you what to review next."
            )

            # Simple weakness detection by topic
            topic_wrong_counts = {}
            for ans, q in zip(ss.final_responses, questions):
                if ans is None or ans != q["answer"]:
                    topic = q.get("topic", "Mixed")
                    topic_wrong_counts[topic] = topic_wrong_counts.get(topic, 0) + 1

            if topic_wrong_counts:
                st.markdown("#### Suggested topics to review")
                sorted_topics = sorted(
                    topic_wrong_counts.items(), key=lambda x: x[1], reverse=True
                )
                for topic, count in sorted_topics:
                    st.write(f"- **{topic}** (missed {count} question{'s' if count > 1 else ''})")

                if st.button("Go to Lessons →"):
                    ss.current_page = "lessons"
                    # You can optionally set a focus key here if lessons.py uses it
                    st.rerun()

        st.markdown("---")

        # Question-by-question review
        with st.expander("Review each question"):
            for i, q in enumerate(questions):
                st.markdown(f"**Question {i + 1}: {q['topic']}**")
                st.write(q["prompt"])
                if q.get("latex"):
                    st.latex(q["latex"])

                user_idx = ss.final_responses[i]
                correct_idx = q["answer"]

                if user_idx is None:
                    st.write(":orange[You did not answer this question.]")
                else:
                    st.write(f"Your answer: {q['choices'][user_idx]}")

                st.write(f"Correct answer: **{q['choices'][correct_idx]}**")
                if q.get("explanation"):
                    st.caption(q["explanation"])
                st.markdown("---")

        # Option to retake
        if st.button("Retake Final Test 🔁"):
            _start_new_attempt()
            st.rerun()
