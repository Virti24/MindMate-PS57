import streamlit as st
from datetime import datetime, date
from ai_helper import generate_supportive_reply
from journal import load_entries, save_entry, mood_from_text, delete_entry

st.set_page_config(page_title="MindMate | Journal Companion", page_icon="🌿", layout="wide")

st.markdown("""
<style>
.main {background: linear-gradient(135deg, #f5faf7 0%, #f7f7fc 100%);}
.block-container {padding-top: 2rem; max-width: 1100px;}
.hero {padding: 1.5rem 1.8rem; border-radius: 18px; background: linear-gradient(110deg,#dff3e8,#e9eaff); margin-bottom: 1rem;}
.small-note {color:#52616b; font-size:0.9rem;}
</style>
<div class="hero">
<h1>🌿 MindMate</h1>
<p>Your private space to pause, reflect, and feel heard.</p>
</div>
""", unsafe_allow_html=True)

entries = load_entries()
with st.sidebar:
    st.header("Your space")
    st.write("A gentle place to reflect on your day.")
    st.info("Your journal entries are saved locally on this device in journal_entries.json.")
    st.caption("MindMate is a supportive journaling tool, not a medical or crisis service.")

write_tab, history_tab, about_tab = st.tabs(["✍️ Write a journal", "📖 Journal history", "ℹ️ About MindMate"])

with write_tab:
    st.subheader("How are you feeling today?")
    entry_date = st.date_input("Date", value=date.today())
    entry_text = st.text_area("Write freely — what happened today, what is on your mind, or how you feel.", height=190,
                              placeholder="Today I felt…")
    if st.button("Reflect with MindMate", type="primary", use_container_width=True):
        if not entry_text.strip():
            st.warning("Please write a few lines before submitting.")
        else:
            mood, distress = mood_from_text(entry_text)
            with st.spinner("Preparing a thoughtful response…"):
                reply, used_fallback = generate_supportive_reply(entry_text, mood, distress)
            record = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "date": entry_date.isoformat(),
                "created_at": datetime.now().isoformat(timespec="minutes"),
                "entry": entry_text.strip(),
                "mood": mood,
                "reply": reply,
                "distress": distress,
            }
            save_entry(record)
            st.session_state["last_record"] = record
            st.session_state["fallback"] = used_fallback

    if "last_record" in st.session_state:
        r = st.session_state["last_record"]
        st.divider()
        st.markdown(f"### Your reflection: **{r['mood']}**")
        st.write(r["reply"])
        if st.session_state.get("fallback"):
            st.caption("Gemini was unavailable, so a safe local supportive response was shown.")
        if r["distress"]:
            st.error("You deserve support. If you are in India, Tele-MANAS offers free 24×7 mental health support: **14416** or **1-800-891-4416**. If you may be in immediate danger, contact local emergency services (112 in India) or go to the nearest emergency department. Please reach out to someone you trust and avoid being alone right now.")

with history_tab:
    st.subheader("Your saved reflections")
    entries = load_entries()
    if not entries:
        st.info("Your journal history will appear here after your first entry.")
    else:
        moods = [e.get("mood", "Unclassified") for e in entries]
        c1, c2 = st.columns(2)
        c1.metric("Journal entries", len(entries))
        c2.metric("Most recent mood", moods[0] if moods else "—")
        for e in entries:
            with st.expander(f"{e.get('date','')} · {e.get('mood','Reflection')}"):
                st.write("**Your entry**")
                st.write(e.get("entry", ""))
                st.write("**MindMate's response**")
                st.write(e.get("reply", ""))
                if e.get("distress"):
                    st.warning("Support information was displayed for this entry. Tele-MANAS (India): 14416.")
                if st.button("Delete this entry", key=f"del_{e.get('id')}"):
                    delete_entry(e.get("id"))
                    st.rerun()

with about_tab:
    st.subheader("A little about this project")
    st.write("MindMate is an LLM-powered journaling companion designed to encourage reflection and provide supportive, non-judgmental responses.")
    st.markdown("**What it does**\n- Generates supportive reflections from journal entries.\n- Estimates a simple mood label using transparent keyword rules.\n- Flags selected distress-related language and displays support resources.\n- Saves entries locally for later review.")
    st.caption("Mood labels are approximate and can be wrong. This app does not diagnose, treat, or replace a qualified professional.")

st.divider()
st.markdown("<p class='small-note'>Made as GenAI Mini Project · Problem Statement 57 · Mental Wellness Journal Companion</p>", unsafe_allow_html=True)
