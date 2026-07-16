import streamlit as st
import sqlite3
from datetime import datetime

# ---------------------------------------------------------
# Setup
# ---------------------------------------------------------
st.set_page_config(page_title="Sorry Kutta", page_icon="🩷", layout="centered")

DB_PATH = "responses.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER,
            mood TEXT,
            note TEXT,
            submitted_at TEXT
        )
    """)
    return conn

conn = get_conn()

# ---------------------------------------------------------
# Simple styling
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #241226; color: #f7ede8; }
    h1, h2, h3 { font-family: Georgia, serif; }
    .stSlider label, .stTextArea label { color: #f2c4ce !important; }
    div.stButton > button {
        background-color: #c97b92;
        color: #241226;
        border-radius: 999px;
        border: none;
        font-weight: 600;
        padding: 0.6rem 1.4rem;
    }
    div.stButton > button:hover { background-color: #e8b86d; color: #241226; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# View routing: normal page vs dashboard (?view=dash)
# ---------------------------------------------------------
query_params = st.query_params
view = query_params.get("view", "main")

# ===========================================================
# DASHBOARD VIEW — only for Shlok
# ===========================================================
if view == "dash":
    st.title("🩷 Her response")

    ADMIN_PASSWORD = "chikubaccha"  # change this to whatever you like

    pw = st.text_input("Password", type="password")
    if pw != ADMIN_PASSWORD:
        st.info("Enter the password to see her response.")
        st.stop()

    rows = conn.execute(
        "SELECT score, mood, note, submitted_at FROM responses ORDER BY id DESC"
    ).fetchall()

    if not rows:
        st.warning("No response yet — waiting on her.")
    else:
        latest = rows[0]
        st.subheader("Latest response")
        st.metric("Forgiveness score", f"{latest[0]} / 100")
        st.write(f"**Mood:** {latest[1]}")
        if latest[2]:
            st.write(f"**Her note:** {latest[2]}")
        st.caption(f"Submitted: {latest[3]}")

        if len(rows) > 1:
            st.subheader("Earlier responses")
            for r in rows[1:]:
                st.write(f"- {r[3]} — score {r[0]}, mood: {r[1]}" + (f", note: {r[2]}" if r[2] else ""))

    if st.button("Refresh"):
        st.rerun()

    st.stop()

# ===========================================================
# MAIN VIEW — for Ritu
# ===========================================================
st.markdown("<p style='letter-spacing:3px;color:#c97b92;font-size:0.8rem;'>FOR BACCHA, FROM SOMEONE WHO MESSED UP</p>", unsafe_allow_html=True)
st.title("I'm Sorry.")
st.markdown("*You sent me your world, one reel at a time — and I gave you silence instead of my full presence.*")

st.divider()

st.subheader("What actually happened")
st.write(
    "Baccha, you kept sending me those reels because you wanted to share your day, "
    "your laughs, your little moments with me. That's not a small thing — that's you "
    "including me in your world."
)
st.write(
    "And instead of showing up for that, I brushed it off and said *'main aise react "
    "nahi karta'* — like your effort was something to be filtered through my mood, "
    "instead of something I should've just met with love."
)
st.write(
    "That excuse doesn't hold up. Being 'not a long-message person' was never a reason "
    "good enough to make you feel unheard, especially not this week, of all weeks."
)
st.write("I'm not going to explain it away. I was careless with something you were being soft and open about, and I'm genuinely sorry.")
st.markdown("*— Shlok*")

st.divider()

st.subheader("Official Kutta Reel Response Policy™")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**01.** Every reel gets a reaction. Minimum: one emoji. Ideal: unhinged enthusiasm.")
    st.markdown("**02.** 'Main aise nahi hoon' is retired. Apparently main aisa hi hoon ab.")
with col2:
    st.markdown("**03.** Dog reels get 🥹, dance reels get 🔥, your voice notes get a full essay.")
    st.markdown("**04.** Cramps era = extra soft mode. No exceptions.")

st.divider()

st.subheader("Baccha, will you forgive me?")
st.caption("drag it all the way, I promise I'll actually feel it")

score = st.slider("Forgiveness meter", 0, 100, 20)

if score < 20:
    mood = "okay this is fair, I did mess up"
elif score < 40:
    mood = "getting warmer..."
elif score < 60:
    mood = "halfway there 🥺"
elif score < 80:
    mood = "ooh I can feel it softening"
elif score < 100:
    mood = "almost fully forgiven"
else:
    mood = "fully forgiven. reel notifications are now sacred. 🩷"

st.write(f"*{mood}*")

note = st.text_area("Say something to him (optional)")

if st.button("Submit my response"):
    conn.execute(
        "INSERT INTO responses (score, mood, note, submitted_at) VALUES (?, ?, ?, ?)",
        (score, mood, note, datetime.now().strftime("%d %b %Y, %I:%M %p")),
    )
    conn.commit()
    st.success("Sent. He'll see it now 🩷")