import streamlit as st

# -------------------------
# LESSONS - Modern Design
# -------------------------

st.set_page_config(page_title="Lessons - Derivatives", layout="wide", page_icon="📚", initial_sidebar_state="collapsed")

# -------------------------
# STYLE SECTION
# -------------------------
st.markdown("""
<style>
    /* Main background */
    [data-testid="stAppViewContainer"] {
        background-color: #F5FBF8;
    }

    /* Hide default sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Header styling */
    .main-header {
        font-size: 48px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 10px;
        line-height: 1.2;
    }

    .sub-header {
        font-size: 20px;
        color: #666;
        margin-bottom: 30px;
    }

    /* Lesson card */
    .lesson-card {
        background-color: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .lesson-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    .lesson-topic {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .lesson-title {
        font-size: 28px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 15px;
    }

    .lesson-goal {
        font-size: 16px;
        color: #666;
        font-style: italic;
        margin-bottom: 20px;
    }

    /* Info box */
    .info-box {
        background-color: #E5F4FF;
        border-left: 4px solid #2196F3;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
    }

    .warning-box {
        background-color: #FFF4E5;
        border-left: 4px solid #FF9800;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
    }

    .success-box {
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
    }

    /* Example box */
    .example-box {
        background-color: #F8F9FA;
        border: 2px solid #E0E0E0;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }

    .example-title {
        font-size: 18px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 10px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: white;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 12px 20px;
        font-weight: 600;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }

    /* Button styling */
    .stButton > button {
        border-radius: 15px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Don't hide header - it contains the sidebar collapse button */
</style>
""", unsafe_allow_html=True)

# -------------------------
# NAVIGATION ICONS
# -------------------------
st.markdown("""
<div style="position: fixed; left: 20px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 20px; z-index: 1000;">
    <div style="width: 50px; height: 50px; background-color: white; border: 2px solid #e0e0e0; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">🏠</div>
    <div style="width: 50px; height: 50px; background-color: #1a1a1a; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">📚</div>
    <div style="width: 50px; height: 50px; background-color: white; border: 2px solid #e0e0e0; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">🎯</div>
    <div style="width: 50px; height: 50px; background-color: white; border: 2px solid #e0e0e0; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">💳</div>
    <div style="width: 50px; height: 50px; background-color: white; border: 2px solid #e0e0e0; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">📊</div>
    <div style="width: 50px; height: 50px; background-color: white; border: 2px solid #e0e0e0; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">⚙️</div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# MAIN CONTENT
# -------------------------

st.markdown('<h1 class="main-header">Master the Fundamentals</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive lessons on <b>Introduction to Derivatives</b></p>',
            unsafe_allow_html=True)

# Lesson tabs
lesson_tabs = st.tabs([
    "📐 Limit Definition",
    "⚡ Basic Rules",
    "✖️ Product Rule",
    "🔗 Chain Rule",
    "∂ Implicit Diff.",
    "🎯 Applications"
])

# -------------------------
# LESSON 1: Limit Definition
# -------------------------
with lesson_tabs[0]:
    st.markdown("""
    <div class="lesson-card" style="background: linear-gradient(135deg, #FFD4D4 0%, #FFE5E5 100%);">
        <div class="lesson-topic" style="background-color: white; color: #DC143C;">Lesson 1</div>
        <div class="lesson-title">Limit Definition of Derivatives</div>
        <div class="lesson-goal">🎯 Understand why the derivative is the instantaneous rate of change</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📖 Definition")
    st.latex(r"f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}")
    st.write("This is the **slope of the tangent line** to y=f(x) at x=a, provided this limit exists.")

    st.markdown("### 🤔 Why the Difference Quotient?")
    st.write("Take two nearby points on the curve: (a, f(a)) and (a+h, f(a+h)). The **secant slope** is:")
    st.latex(r"m_{sec} = \frac{f(a+h) - f(a)}{h}")
    st.write("As h→0, the secant slope approaches the tangent slope.")

    st.markdown("### ✍️ Worked Examples")

    with st.expander("📌 Example 1: Polynomial f(x) = x²"):
        st.markdown("""
        <div class="example-box">
            <div class="example-title">Compute f'(a) from the limit definition:</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\frac{f(a+h) - f(a)}{h} = \frac{(a+h)^2 - a^2}{h} = \frac{2ah + h^2}{h} = 2a + h")
        st.write("Taking h→0 gives **f'(a) = 2a**")

    with st.expander("📌 Example 2: Square root f(x) = √x"):
        st.markdown("""
        <div class="example-box">
            <div class="example-title">Use rationalization:</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(
            r"\frac{\sqrt{a+h} - \sqrt{a}}{h} \cdot \frac{\sqrt{a+h} + \sqrt{a}}{\sqrt{a+h} + \sqrt{a}} = \frac{1}{\sqrt{a+h} + \sqrt{a}}")
        st.write("Limit as h→0 is 1/(2√a), so **f'(a) = 1/(2√a)**")

    with st.expander("📌 Example 3: Absolute value (non-differentiable)"):
        st.markdown("""
        <div class="example-box">
            <div class="example-title">f(x) = |x| at a=0:</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("• For h>0: |h|/h = 1")
        st.write("• For h<0: |h|/h = -1")
        st.write("Limits disagree, so **derivative does not exist at 0**")

    st.markdown("""
    <div class="info-box">
        <b>💡 Key Takeaway:</b> If f is differentiable at a, then f is continuous at a. The converse is not true!
    </div>
    """, unsafe_allow_html=True)
    # -------------------------
    # 🧪 Practice (Lesson 1)
    # -------------------------
    st.markdown("### 🧪 Practice")
    st.write("Using the limit definition, compute **f′(5)** for **f(x) = x²**.")

    # Keep hint visibility across reruns
    if "l1_show_hint" not in st.session_state:
        st.session_state.l1_show_hint = False

    # Input + hint side-by-side
    col_a, col_b = st.columns([3, 1])
    with col_a:
        user_ans = st.text_input("Your answer:", key="l1_answer", placeholder="e.g., 10")
    with col_b:
        if st.button("Hint", key="l1_hint_btn"):
            st.session_state.l1_show_hint = True

    if st.session_state.l1_show_hint:
        st.info("Start from the difference quotient, simplify, then take the limit. "
                "For f(x)=x², **f′(a) = 2a**. Now plug in **a = 5**.")

    if st.button("Check answer", key="l1_check_btn"):
        normalized = (user_ans or "").strip().lower().replace(" ", "")
        correct_set = {"10", "10.0"}
        if normalized in correct_set:
            st.success("Correct! Since f′(a)=2a, f′(5)=2·5=**10**.")
        else:
            st.error("Not quite. Remember f′(a)=2a for x². Try again!")

    # -------------------------
    # 🧪 Practice (Lesson 1) - Q2
    # -------------------------
    st.markdown("### 🧪 Practice 2")
    st.write("Using the limit definition, compute **f′(2)** for **f(x) = 3x**.")

    if "l1_q2_show_hint" not in st.session_state:
        st.session_state.l1_q2_show_hint = False

    col_a2, col_b2 = st.columns([3, 1])
    with col_a2:
        l1_q2_ans = st.text_input("Your answer:", key="l1_q2_answer", placeholder="e.g., 3")
    with col_b2:
        if st.button("Hint", key="l1_q2_hint_btn"):
            st.session_state.l1_q2_show_hint = True

    if st.session_state.l1_q2_show_hint:
        st.info("Write the difference quotient for f(x)=3x, simplify, and then take h → 0. "
                "You should get a constant derivative.")

    if st.button("Check answer", key="l1_q2_check_btn"):
        normalized = (l1_q2_ans or "").strip().lower().replace(" ", "")
        correct_set = {"3", "3.0"}
        if normalized in correct_set:
            st.success("Correct! f′(x) = 3 for all x, so f′(2) = 3.")
        else:
            st.error("Not quite. For a linear function 3x, the slope is constant.")

    # -------------------------
    # 🧪 Practice (Lesson 1) - Q3
    # -------------------------
    st.markdown("### 🧪 Practice 3")
    st.write("Using the limit definition, compute **f′(1)** for **f(x) = 1/x**.")

    if "l1_q3_show_hint" not in st.session_state:
        st.session_state.l1_q3_show_hint = False

    col_a3, col_b3 = st.columns([3, 1])
    with col_a3:
        l1_q3_ans = st.text_input("Your answer:", key="l1_q3_answer", placeholder="e.g., -1")
    with col_b3:
        if st.button("Hint", key="l1_q3_hint_btn"):
            st.session_state.l1_q3_show_hint = True

    if st.session_state.l1_q3_show_hint:
        st.info("Start from f(x) = x^{-1}. You can use the limit definition or recall the power rule "
                "once it's justified: f′(x) = -x^{-2}. Evaluate at x = 1.")

    if st.button("Check answer", key="l1_q3_check_btn"):
        normalized = (l1_q3_ans or "").strip().lower().replace(" ", "")
        correct_set = {"-1", "-1.0"}
        if normalized in correct_set:
            st.success("Correct! f′(x) = -1/x², so f′(1) = -1.")
        else:
            st.error("Not quite. f′(x) = -1/x²; plug in x = 1.")


# -------------------------
# LESSON 2: Basic Rules
# -------------------------
with lesson_tabs[1]:
    st.markdown("""
    <div class="lesson-card" style="background: linear-gradient(135deg, #FFE5D0 0%, #FFF0E0 100%);">
        <div class="lesson-topic" style="background-color: white; color: #FF8C00;">Lesson 2</div>
        <div class="lesson-title">Basic Differentiation Rules</div>
        <div class="lesson-goal">🎯 Master power rule, constant multiple, and sum/difference rules</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📚 The Rules")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**1. Power Rule:**")
        st.latex(r"\frac{d}{dx}[x^n] = nx^{n-1}")

        st.markdown("**2. Constant Multiple:**")
        st.latex(r"\frac{d}{dx}[c \cdot f(x)] = c \cdot f'(x)")

    with col2:
        st.markdown("**3. Sum/Difference:**")
        st.latex(r"\frac{d}{dx}[f \pm g] = f' \pm g'")

        st.markdown("**4. Constant:**")
        st.latex(r"\frac{d}{dx}[c] = 0")

    st.markdown("### ✍️ Worked Examples")

    with st.expander("📌 Example 1: Simple polynomial"):
        st.markdown("**Differentiate: f(x) = 5x³ − 4x + 7**")
        st.latex(r"f'(x) = 5 \cdot 3x^2 - 4 \cdot 1 + 0 = 15x^2 - 4")

    with st.expander("📌 Example 2: Fractional powers"):
        st.markdown("**Differentiate: f(x) = 2√x + 1/x²**")
        st.write("Rewrite as: f(x) = 2x^(1/2) + x^(-2)")
        st.latex(r"f'(x) = 2 \cdot \frac{1}{2}x^{-1/2} + (-2)x^{-3} = \frac{1}{\sqrt{x}} - \frac{2}{x^3}")

    with st.expander("📌 Example 3: At a point"):
        st.markdown("**Find f'(2) if f(x) = x⁴ − 3x²**")
        st.latex(r"f'(x) = 4x^3 - 6x")
        st.write("Evaluate at x=2:")
        st.latex(r"f'(2) = 4(2)^3 - 6(2) = 32 - 12 = 20")

    st.markdown("""
    <div class="success-box">
        <b>✅ Pro Tip:</b> Always simplify your expression before differentiating! Converting radicals and fractions to power notation makes the power rule easier to apply.
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # 🧪 Practice (Lesson 2)
    # -------------------------
    st.markdown("### 🧪 Practice")
    st.write("Differentiate **f(x) = 4x³ − 5x + 2** and enter **f′(x)** below.")

    # Keep hint visibility across reruns
    if "l2_show_hint" not in st.session_state:
        st.session_state.l2_show_hint = False

    # Input + hint side-by-side
    col_a, col_b = st.columns([3, 1])
    with col_a:
        l2_ans = st.text_input(
            "Your answer for f′(x):",
            key="l2_answer",
            placeholder="e.g., 12x^2 - 5"
        )
    with col_b:
        if st.button("Hint", key="l2_hint_btn"):
            st.session_state.l2_show_hint = True

    if st.session_state.l2_show_hint:
        st.info("Use the power rule term-by-term: derivative of 4x³, derivative of -5x, "
                "and derivative of the constant 2.")

    if st.button("Check answer", key="l2_check_btn"):
        normalized = (l2_ans or "").strip().lower().replace(" ", "")
        correct_set = {"12x^2-5", "12x^2-5.0"}
        if normalized in correct_set:
            st.success("Correct! f′(x) = 12x² − 5.")
        else:
            st.error("Not quite. Check each term: 4x³ → 12x², −5x → −5, constant → 0.")
        # -------------------------
        # 🧪 Practice (Lesson 2) - Q2
        # -------------------------
    st.markdown("### 🧪 Practice 2")
    st.write("Differentiate **f(x) = 7x⁴ + 2** and enter **f′(x)** below.")

    if "l2_q2_show_hint" not in st.session_state:
        st.session_state.l2_q2_show_hint = False

    col_a2, col_b2 = st.columns([3, 1])
    with col_a2:
        l2_q2_ans = st.text_input(
            "Your answer for f′(x):",
            key="l2_q2_answer",
            placeholder="e.g., 28x^3"
        )
    with col_b2:
        if st.button("Hint", key="l2_q2_hint_btn"):
            st.session_state.l2_q2_show_hint = True

    if st.session_state.l2_q2_show_hint:
        st.info("Differentiate each term separately. The derivative of a constant is 0.")

    if st.button("Check answer", key="l2_q2_check_btn"):
        normalized = (l2_q2_ans or "").strip().lower().replace(" ", "")
        correct_set = {"28x^3", "28x^3.0"}
        if normalized in correct_set:
            st.success("Correct! f′(x) = 28x³.")
        else:
            st.error("Not quite. Apply the power rule to 7x⁴ and drop the constant.")

    # -------------------------
    # 🧪 Practice (Lesson 2) - Q3
    # -------------------------
    st.markdown("### 🧪 Practice 3")
    st.write("Differentiate **f(x) = 5/x** and enter **f′(x)** below.")

    if "l2_q3_show_hint" not in st.session_state:
        st.session_state.l2_q3_show_hint = False

    col_a3, col_b3 = st.columns([3, 1])
    with col_a3:
        l2_q3_ans = st.text_input(
            "Your answer for f′(x):",
            key="l2_q3_answer",
            placeholder="e.g., -5/x^2"
        )
    with col_b3:
        if st.button("Hint", key="l2_q3_hint_btn"):
            st.session_state.l2_q3_show_hint = True

    if st.session_state.l2_q3_show_hint:
        st.info("Rewrite f(x) = 5x⁻¹, then use the power rule n x^{n-1}.")

    if st.button("Check answer", key="l2_q3_check_btn"):
        normalized = (l2_q3_ans or "").strip().lower().replace(" ", "")
        correct_set = {"-5/x^2", "-5x^-2"}
        if normalized in correct_set:
            st.success("Correct! f′(x) = -5/x².")
        else:
            st.error("Not quite. Remember x^{-1} → -x^{-2}.")

# -------------------------
# LESSON 3: Product Rule
# -------------------------
with lesson_tabs[2]:
    st.markdown("""
    <div class="lesson-card" style="background: linear-gradient(135deg, #E5D4FF 0%, #F0E8FF 100%);">
        <div class="lesson-topic" style="background-color: white; color: #6B46C1;">Lesson 3</div>
        <div class="lesson-title">Product Rule</div>
        <div class="lesson-goal">🎯 Learn to differentiate products of functions</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📖 The Rule")
    st.latex(r"\frac{d}{dx}[u \cdot v] = u' \cdot v + u \cdot v'")
    st.write("In words: **(first)' × (second) + (first) × (second)'**")

    st.markdown("### ✍️ Worked Examples")

    with st.expander("📌 Example 1: f(x) = x² · sin x"):
        st.markdown("**Let u = x², v = sin x**")
        st.write("• u' = 2x")
        st.write("• v' = cos x")
        st.latex(r"f'(x) = 2x \cdot \sin x + x^2 \cdot \cos x")

    with st.expander("📌 Example 2: f(x) = (x³)(eˣ)"):
        st.markdown("**Let u = x³, v = eˣ**")
        st.write("• u' = 3x²")
        st.write("• v' = eˣ")
        st.latex(r"f'(x) = 3x^2 \cdot e^x + x^3 \cdot e^x = e^x(3x^2 + x^3)")

    with st.expander("📌 Example 3: Three functions"):
        st.markdown("**Differentiate: f(x) = x · sin x · eˣ**")
        st.write("Apply product rule twice:")
        st.write("Let u = x · sin x, v = eˣ")
        st.write("First find u' = sin x + x cos x (using product rule)")
        st.latex(r"f'(x) = (sin x + x \cos x) \cdot e^x + (x \sin x) \cdot e^x")

    st.markdown("""
    <div class="warning-box">
        <b>⚠️ Common Mistake:</b> Don't just multiply the derivatives! (uv)' ≠ u'v'. You must use the full product rule formula.
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # 🧪 Practice (Lesson 3)
    # -------------------------
    st.markdown("### 🧪 Practice")
    st.write("Differentiate **f(x) = x² eˣ** and enter **f′(x)** below.")

    if "l3_show_hint" not in st.session_state:
        st.session_state.l3_show_hint = False

    col_a, col_b = st.columns([3, 1])
    with col_a:
        l3_ans = st.text_input(
            "Your answer for f′(x):",
            key="l3_answer",
            placeholder="e.g., 2x e^x + x^2 e^x"
        )
    with col_b:
        if st.button("Hint", key="l3_hint_btn"):
            st.session_state.l3_show_hint = True

    if st.session_state.l3_show_hint:
        st.info("Let u = x² and v = eˣ. Use (uv)′ = u′v + uv′, then plug in u′ and v′.")

    if st.button("Check answer", key="l3_check_btn"):
        normalized = (l3_ans or "").strip().lower().replace(" ", "")
        # Allow a few common equivalent forms
        correct_set = {
            "2xe^x+x^2e^x",
            "e^x(2x+x^2)",
            "e^x(x^2+2x)"
        }
        if normalized in correct_set:
            st.success("Nice! f′(x) = 2x eˣ + x² eˣ = eˣ(2x + x²).")
        else:
            st.error("Not quite. Remember: (uv)′ = u′v + uv′, not u′v′.")
        # -------------------------
        # 🧪 Practice (Lesson 3) - Q2
        # -------------------------
    st.markdown("### 🧪 Practice 2")
    st.write("Differentiate **f(x) = x · cos x** and enter **f′(x)** below.")

    if "l3_q2_show_hint" not in st.session_state:
        st.session_state.l3_q2_show_hint = False

    col_a2, col_b2 = st.columns([3, 1])
    with col_a2:
        l3_q2_ans = st.text_input(
            "Your answer for f′(x):",
            key="l3_q2_answer",
            placeholder="e.g., cos x - x sin x"
        )
    with col_b2:
        if st.button("Hint", key="l3_q2_hint_btn"):
            st.session_state.l3_q2_show_hint = True

    if st.session_state.l3_q2_show_hint:
        st.info("Let u = x and v = cos x. Then u′ = 1 and v′ = -sin x. Use (uv)′ = u′v + uv′.")

    if st.button("Check answer", key="l3_q2_check_btn"):
        normalized = (l3_q2_ans or "").strip().lower().replace(" ", "")
        correct_set = {"cosx-xsinx"}
        if normalized in correct_set:
            st.success("Correct! f′(x) = cos x − x sin x.")
        else:
            st.error("Not quite. Check the sign on the derivative of cos x.")

    # -------------------------
    # 🧪 Practice (Lesson 3) - Q3
    # -------------------------
    st.markdown("### 🧪 Practice 3")
    st.write("Differentiate **f(x) = (x² + 1)x³** and enter **f′(x)** below (simplified).")

    if "l3_q3_show_hint" not in st.session_state:
        st.session_state.l3_q3_show_hint = False

    col_a3, col_b3 = st.columns([3, 1])
    with col_a3:
        l3_q3_ans = st.text_input(
            "Your answer for f′(x):",
            key="l3_q3_answer",
            placeholder="e.g., 5x^4 + 3x^2"
        )
    with col_b3:
        if st.button("Hint", key="l3_q3_hint_btn"):
            st.session_state.l3_q3_show_hint = True

    if st.session_state.l3_q3_show_hint:
        st.info("Let u = x² + 1 and v = x³. Compute u′ and v′, then expand and combine like terms.")

    if st.button("Check answer", key="l3_q3_check_btn"):
        normalized = (l3_q3_ans or "").strip().lower().replace(" ", "")
        correct_set = {"5x^4+3x^2"}
        if normalized in correct_set:
            st.success("Correct! f′(x) = 5x⁴ + 3x².")
        else:
            st.error("Not quite. Carefully expand (2x)x³ + (x²+1)3x² and simplify.")
# -------------------------
# LESSON 4: Chain Rule
# -------------------------
with lesson_tabs[3]:
    st.markdown("""
    <div class="lesson-card" style="background: linear-gradient(135deg, #D4FFE5 0%, #E5FFF0 100%);">
        <div class="lesson-topic" style="background-color: white; color: #10B981;">Lesson 4</div>
        <div class="lesson-title">Chain Rule</div>
        <div class="lesson-goal">🎯 Master composition of functions differentiation</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📖 The Rule")
    st.latex(r"\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)")
    st.write("In words: **derivative of outer × derivative of inner**")

    st.markdown("### 🔍 How to Identify")
    st.write("Look for a function inside another function:")
    st.write("• (3x² + 1)⁴ → outer: ()⁴, inner: 3x² + 1")
    st.write("• sin(5x²) → outer: sin(), inner: 5x²")

    st.markdown("### ✍️ Worked Examples")

    with st.expander("📌 Example 1: f(x) = (3x² + 1)⁴"):
        st.markdown("**Step by step:**")
        st.write("1. Outer function: u⁴ where u = 3x² + 1")
        st.write("2. Derivative of outer: 4u³")
        st.write("3. Derivative of inner: 6x")
        st.latex(r"f'(x) = 4(3x^2 + 1)^3 \cdot 6x = 24x(3x^2 + 1)^3")

    with st.expander("📌 Example 2: f(x) = sin(5x²)"):
        st.markdown("**Identify parts:**")
        st.write("• Outer: sin(u), derivative = cos(u)")
        st.write("• Inner: u = 5x², derivative = 10x")
        st.latex(r"f'(x) = \cos(5x^2) \cdot 10x")

    with st.expander("📌 Example 3: Nested composition"):
        st.markdown("**f(x) = sin(cos(x²))**")
        st.write("Work from outside in:")
        st.write("1. Outermost: sin() → cos()")
        st.write("2. Middle: cos() → -sin()")
        st.write("3. Innermost: x² → 2x")
        st.latex(r"f'(x) = \cos(\cos(x^2)) \cdot (-\sin(x^2)) \cdot 2x")

    st.markdown("""
    <div class="info-box">
        <b>💡 Memory Aid:</b> "Outside-In" - differentiate the outer function first, then multiply by the derivative of what's inside.
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # 🧪 Practice (Lesson 4)
    # -------------------------
    st.markdown("### 🧪 Practice")
    st.write("Differentiate **f(x) = (5x² − 1)³** and enter **f′(x)** below.")

    if "l4_show_hint" not in st.session_state:
        st.session_state.l4_show_hint = False

    col_a, col_b = st.columns([3, 1])
    with col_a:
        l4_ans = st.text_input(
            "Your answer for f′(x):",
            key="l4_answer",
            placeholder="e.g., 30x(5x^2 - 1)^2"
        )
    with col_b:
        if st.button("Hint", key="l4_hint_btn"):
            st.session_state.l4_show_hint = True

    if st.session_state.l4_show_hint:
        st.info("Let u = 5x² − 1, so f(x) = u³. Then f′(x) = 3u² · u′. "
                "Compute u′ and substitute back.")

    if st.button("Check answer", key="l4_check_btn"):
        normalized = (l4_ans or "").strip().lower().replace(" ", "").replace("*", "")
        correct_set = {
            "30x(5x^2-1)^2",
            "3(5x^2-1)^2(10x)"
        }
        if normalized in correct_set:
            st.success("Correct! f′(x) = 30x(5x² − 1)².")
        else:
            st.error("Not quite. Be sure to multiply the outer derivative 3u² by u′ = 10x.")

        # -------------------------
        # 🧪 Practice (Lesson 4) - Q2
        # -------------------------
    st.markdown("### 🧪 Practice 2")
    st.write("Differentiate **f(x) = (2x + 3)⁵** and enter **f′(x)** below.")

    if "l4_q2_show_hint" not in st.session_state:
        st.session_state.l4_q2_show_hint = False

    col_a2, col_b2 = st.columns([3, 1])
    with col_a2:
        l4_q2_ans = st.text_input(
            "Your answer for f′(x):",
            key="l4_q2_answer",
            placeholder="e.g., 10(2x + 3)^4"
        )
    with col_b2:
        if st.button("Hint", key="l4_q2_hint_btn"):
            st.session_state.l4_q2_show_hint = True

    if st.session_state.l4_q2_show_hint:
        st.info("Think of f(x) = u⁵ with u = 2x + 3. Use f′(x) = 5u⁴ · u′ and plug in u′ = 2.")

    if st.button("Check answer", key="l4_q2_check_btn"):
        normalized = (l4_q2_ans or "").strip().lower().replace(" ", "").replace("*", "")
        correct_set = {"10(2x+3)^4"}
        if normalized in correct_set:
            st.success("Correct! f′(x) = 10(2x + 3)⁴.")
        else:
            st.error("Not quite. Remember to multiply the outer derivative by u′ = 2.")

        # -------------------------
        # 🧪 Practice (Lesson 4) - Q3
        # -------------------------
    st.markdown("### 🧪 Practice 3")
    st.write("Differentiate **f(x) = cos(4x)** and enter **f′(x)** below.")

    if "l4_q3_show_hint" not in st.session_state:
        st.session_state.l4_q3_show_hint = False

    col_a3, col_b3 = st.columns([3, 1])
    with col_a3:
        l4_q3_ans = st.text_input(
            "Your answer for f′(x):",
            key="l4_q3_answer",
            placeholder="e.g., -4 sin(4x)"
        )
    with col_b3:
        if st.button("Hint", key="l4_q3_hint_btn"):
            st.session_state.l4_q3_show_hint = True

    if st.session_state.l4_q3_show_hint:
        st.info("Outer: cos(u) → -sin(u). Inner: u = 4x → u′ = 4. Multiply them: -sin(u)·u′.")

    if st.button("Check answer", key="l4_q3_check_btn"):
        normalized = (l4_q3_ans or "").strip().lower().replace(" ", "")
        correct_set = {"-4sin(4x)"}
        if normalized in correct_set:
            st.success("Correct! f′(x) = -4 sin(4x).")
        else:
            st.error("Not quite. Don't forget the negative sign from cos → -sin.")

# -------------------------
# LESSON 5: Implicit Differentiation
# -------------------------
with lesson_tabs[4]:
    st.markdown("""
    <div class="lesson-card" style="background: linear-gradient(135deg, #D4E8FF 0%, #E5F2FF 100%);">
        <div class="lesson-topic" style="background-color: white; color: #2196F3;">Lesson 5</div>
        <div class="lesson-title">Implicit Differentiation</div>
        <div class="lesson-goal">🎯 Differentiate equations not solved for y</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📖 The Concept")
    st.write("When y is not isolated, differentiate both sides with respect to x.")
    st.write("**Key:** Treat y as a function of x. Every time you differentiate y, multiply by dy/dx.")

    st.markdown("### 📚 The Process")
    st.write("1. Differentiate both sides with respect to x")
    st.write("2. Apply chain rule to y-terms (multiply by dy/dx)")
    st.write("3. Collect all dy/dx terms on one side")
    st.write("4. Factor out dy/dx and solve")

    st.markdown("### ✍️ Worked Examples")

    with st.expander("📌 Example 1: Circle x² + y² = 25"):
        st.markdown("**Find dy/dx:**")
        st.write("Step 1: Differentiate both sides")
        st.latex(r"\frac{d}{dx}[x^2 + y^2] = \frac{d}{dx}[25]")
        st.latex(r"2x + 2y\frac{dy}{dx} = 0")
        st.write("Step 2: Solve for dy/dx")
        st.latex(r"2y\frac{dy}{dx} = -2x \Rightarrow \frac{dy}{dx} = -\frac{x}{y}")

    with st.expander("📌 Example 2: Product with y: xy = 1"):
        st.markdown("**Differentiate using product rule:**")
        st.latex(r"\frac{d}{dx}[xy] = \frac{d}{dx}[1]")
        st.latex(r"1 \cdot y + x \cdot \frac{dy}{dx} = 0")
        st.latex(r"\frac{dy}{dx} = -\frac{y}{x}")

    with st.expander("📌 Example 3: More complex: x² + xy + y² = 7"):
        st.markdown("**Step by step:**")
        st.latex(r"2x + (y + x\frac{dy}{dx}) + 2y\frac{dy}{dx} = 0")
        st.write("Collect dy/dx terms:")
        st.latex(r"x\frac{dy}{dx} + 2y\frac{dy}{dx} = -2x - y")
        st.latex(r"\frac{dy}{dx}(x + 2y) = -2x - y")
        st.latex(r"\frac{dy}{dx} = -\frac{2x + y}{x + 2y}")

    st.markdown("""
    <div class="warning-box">
        <b>⚠️ Don't Forget:</b> Every y-term gets a dy/dx when you differentiate! This is the most common mistake.
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # 🧪 Practice (Lesson 5)
    # -------------------------
    st.markdown("### 🧪 Practice")
    st.write("For the curve **x² + y² = 9**, find **dy/dx** and enter it below.")

    if "l5_show_hint" not in st.session_state:
        st.session_state.l5_show_hint = False

    col_a, col_b = st.columns([3, 1])
    with col_a:
        l5_ans = st.text_input(
            "Your answer for dy/dx:",
            key="l5_answer",
            placeholder="e.g., -x / y"
        )
    with col_b:
        if st.button("Hint", key="l5_hint_btn"):
            st.session_state.l5_show_hint = True

    if st.session_state.l5_show_hint:
        st.info("Differentiate both sides: d/dx[x² + y²] = d/dx[9]. "
                "Remember y is a function of x, so d/dx[y²] = 2y·(dy/dx). "
                "Then solve for dy/dx.")

    if st.button("Check answer", key="l5_check_btn"):
        normalized = (l5_ans or "").strip().lower().replace(" ", "")
        correct_set = {
            "-x/y",
            "(-x)/y",
            "-1*x/y"
        }
        if normalized in correct_set:
            st.success("Correct! dy/dx = -x / y.")
        else:
            st.error("Not quite. You should get dy/dx = -x / y after solving.")

        # -------------------------
        # 🧪 Practice (Lesson 5) - Q2
        # -------------------------
        st.markdown("### 🧪 Practice 2")
        st.write("For the curve **x² + 3y² = 7**, find **dy/dx** and enter it below.")

        if "l5_q2_show_hint" not in st.session_state:
            st.session_state.l5_q2_show_hint = False

        col_a2, col_b2 = st.columns([3, 1])
        with col_a2:
            l5_q2_ans = st.text_input(
                "Your answer for dy/dx:",
                key="l5_q2_answer",
                placeholder="e.g., -x / (3y)"
            )
        with col_b2:
            if st.button("Hint", key="l5_q2_hint_btn"):
                st.session_state.l5_q2_show_hint = True

        if st.session_state.l5_q2_show_hint:
            st.info("Differentiate: 2x + 6y·(dy/dx) = 0, then solve for dy/dx.")

        if st.button("Check answer", key="l5_q2_check_btn"):
            normalized = (l5_q2_ans or "").strip().lower().replace(" ", "")
            correct_set = {"-x/(3y)", "(-x)/(3y)"}
            if normalized in correct_set:
                st.success("Correct! dy/dx = -x / (3y).")
            else:
                st.error("Not quite. Make sure the 3 in 3y² becomes 6y after differentiating.")

        # -------------------------
        # 🧪 Practice (Lesson 5) - Q3
        # -------------------------
        st.markdown("### 🧪 Practice 3")
        st.write("For the curve **x² − xy + y² = 4**, find **dy/dx** and enter it below (simplified).")

        if "l5_q3_show_hint" not in st.session_state:
            st.session_state.l5_q3_show_hint = False

        col_a3, col_b3 = st.columns([3, 1])
        with col_a3:
            l5_q3_ans = st.text_input(
                "Your answer for dy/dx:",
                key="l5_q3_answer",
                placeholder="e.g., (2x - y) / (x - 2y)"
            )
        with col_b3:
            if st.button("Hint", key="l5_q3_hint_btn"):
                st.session_state.l5_q3_show_hint = True

        if st.session_state.l5_q3_show_hint:
            st.info(
                "Differentiate each term: x² → 2x, -xy → -(y + x·dy/dx), y² → 2y·dy/dx, then collect dy/dx terms and solve.")

        if st.button("Check answer", key="l5_q3_check_btn"):
            normalized = (l5_q3_ans or "").strip().lower().replace(" ", "")
            # dy/dx = (2x - y) / (x - 2y)
            correct_set = {"(2x-y)/(x-2y)", "2x-y/x-2y"}
            if normalized in correct_set:
                st.success("Correct! dy/dx = (2x − y) / (x − 2y).")
            else:
                st.error("Not quite. Carefully handle the product term -xy when differentiating.")

# -------------------------
# LESSON 6: Applications
# -------------------------
with lesson_tabs[5]:
    st.markdown("""
    <div class="lesson-card" style="background: linear-gradient(135deg, #FFF4D4 0%, #FFFAE5 100%);">
        <div class="lesson-topic" style="background-color: white; color: #F59E0B;">Lesson 6</div>
        <div class="lesson-title">Applications of Derivatives</div>
        <div class="lesson-goal">🎯 Apply derivatives to real-world problems</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📐 Tangent Lines")
    st.write("**Equation of tangent line at (x₀, y₀):**")
    st.latex(r"y - y_0 = m(x - x_0) \text{ where } m = f'(x_0)")

    st.markdown("### 📈 Rate of Change")
    st.write("The derivative represents:")
    st.write("• **Velocity:** v(t) = s'(t) if s(t) is position")
    st.write("• **Acceleration:** a(t) = v'(t) = s''(t)")
    st.write("• **Marginal cost/revenue** in economics")

    st.markdown("### ✍️ Worked Examples")

    with st.expander("📌 Example 1: Tangent line to f(x) = x²"):
        st.markdown("**Find tangent line at x = 2:**")
        st.write("Step 1: Find the point")
        st.write("• f(2) = 4, so point is (2, 4)")
        st.write("Step 2: Find the slope")
        st.write("• f'(x) = 2x, so f'(2) = 4")
        st.write("Step 3: Write equation")
        st.latex(r"y - 4 = 4(x - 2) \Rightarrow y = 4x - 4")

    with st.expander("📌 Example 2: Velocity and acceleration"):
        st.markdown("**Position: s(t) = t³ - 6t² + 9t**")
        st.write("Velocity: v(t) = s'(t) = 3t² - 12t + 9")
        st.write("Acceleration: a(t) = v'(t) = 6t - 12")
        st.write("At t = 1:")
        st.write("• v(1) = 3 - 12 + 9 = 0 (momentarily stopped)")
        st.write("• a(1) = 6 - 12 = -6 (slowing down)")

    with st.expander("📌 Example 3: Maximum height"):
        st.markdown("**Ball thrown: h(t) = -16t² + 64t + 5**")
        st.write("Maximum occurs when v(t) = 0:")
        st.write("v(t) = h'(t) = -32t + 64 = 0")
        st.write("Solve: t = 2 seconds")
        st.write("Max height: h(2) = -16(4) + 64(2) + 5 = 69 feet")

    st.markdown("""
    <div class="success-box">
        <b>✅ Real World:</b> Derivatives help us find optimal solutions - maximum profit, minimum cost, fastest route, and much more!
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # 🧪 Practice (Lesson 6)
    # -------------------------
    st.markdown("### 🧪 Practice")
    st.write("Find the equation of the tangent line to **f(x) = x² + 1** at **x = 1**.")

    if "l6_show_hint" not in st.session_state:
        st.session_state.l6_show_hint = False

    col_a, col_b = st.columns([3, 1])
    with col_a:
        l6_ans = st.text_input(
            "Your tangent line (in terms of y and x):",
            key="l6_answer",
            placeholder="e.g., y = 2x - 1"
        )
    with col_b:
        if st.button("Hint", key="l6_hint_btn"):
            st.session_state.l6_show_hint = True

    if st.session_state.l6_show_hint:
        st.info("1️⃣ Find the point: (1, f(1)). 2️⃣ Find the slope m = f′(1). "
                "3️⃣ Use point-slope form: y − y₀ = m(x − x₀).")

    if st.button("Check answer", key="l6_check_btn"):
        normalized = (l6_ans or "").strip().lower().replace(" ", "")
        # Accept 'y=2x-1' and '2x-1'
        correct_set = {
            "y=2x-1",
            "2x-1"
        }
        if normalized in correct_set:
            st.success("Correct! The tangent line is y = 2x − 1.")
        else:
            st.error("Not quite. You should get slope m = 2 and point (1, 2).")

        # -------------------------
        # 🧪 Practice (Lesson 6) - Q2
        # -------------------------
    st.markdown("### 🧪 Practice 2")
    st.write("Find the equation of the tangent line to **f(x) = 3x² − 2x** at **x = 1**.")

    if "l6_q2_show_hint" not in st.session_state:
        st.session_state.l6_q2_show_hint = False

    col_a2, col_b2 = st.columns([3, 1])
    with col_a2:
        l6_q2_ans = st.text_input(
            "Your tangent line (in terms of y and x):",
            key="l6_q2_answer",
            placeholder="e.g., y = 4x - 3"
        )
    with col_b2:
        if st.button("Hint", key="l6_q2_hint_btn"):
            st.session_state.l6_q2_show_hint = True

    if st.session_state.l6_q2_show_hint:
        st.info("Compute f(1) and f′(1). Then plug into y − y₀ = m(x − x₀).")

    if st.button("Check answer", key="l6_q2_check_btn"):
        normalized = (l6_q2_ans or "").strip().lower().replace(" ", "")
        correct_set = {"y=4x-3", "4x-3"}
        if normalized in correct_set:
            st.success("Correct! The tangent line is y = 4x − 3.")
        else:
            st.error("Not quite. f(1) = 1 and f′(1) = 4, so use point (1,1) and slope 4.")

    # -------------------------
    # 🧪 Practice (Lesson 6) - Q3
    # -------------------------
    st.markdown("### 🧪 Practice 3")
    st.write("Given position **s(t) = 2t³ − 5t**, find the **velocity v(t)** and enter it below.")

    if "l6_q3_show_hint" not in st.session_state:
        st.session_state.l6_q3_show_hint = False

    col_a3, col_b3 = st.columns([3, 1])
    with col_a3:
        l6_q3_ans = st.text_input(
            "Your answer for v(t):",
            key="l6_q3_answer",
            placeholder="e.g., 6t^2 - 5"
        )
    with col_b3:
        if st.button("Hint", key="l6_q3_hint_btn"):
            st.session_state.l6_q3_show_hint = True

    if st.session_state.l6_q3_show_hint:
        st.info("Velocity is the derivative of position: v(t) = s′(t). Differentiate term-by-term.")

    if st.button("Check answer", key="l6_q3_check_btn"):
        normalized = (l6_q3_ans or "").strip().lower().replace(" ", "")
        correct_set = {"6t^2-5", "6t^2-5.0"}
        if normalized in correct_set:
            st.success("Correct! v(t) = 6t² − 5.")
        else:
            st.error("Not quite. Differentiate 2t³ and −5t separately.")

# -------------------------
# FOOTER NAVIGATION
# -------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Back to Home", use_container_width=True):
        if "current_page" in st.session_state:
            st.session_state.current_page = "home"
            st.rerun()
with col2:
    if st.button("🎯 Take Quiz", type="primary", use_container_width=True):
        if "current_page" in st.session_state:
            st.session_state.current_page = "quiz"
            st.rerun()
with col3:
    quiz_completed = st.session_state.get("quiz_completed", False)
    if quiz_completed:
        if st.button("📊 View Feedback", use_container_width=True):
            if "current_page" in st.session_state:
                st.session_state.current_page = "feedback"
                st.rerun()
    else:
        st.button("📊 View Feedback 🔒", use_container_width=True, disabled=True)
        st.caption("Complete the quiz first")