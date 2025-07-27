import streamlit as st
import random
import datetime
import json
import os
import io
import matplotlib.pyplot as plt

def apply_theme(mood):
    mood_colors_light = {
        "happy": "#FFFACD",
        "sad": "#D8EAFB",
        "angry": "#FDDCDC",
        "anxious": "#E8E8E8",
        "loved": "#FFE4F0",
        "stressed": "#F0EAD6",
    }
    mood_colors_dark = {
        "happy": "#BDB76B",
        "sad": "#5F9EA0",
        "angry": "#CD5C5C",
        "anxious": "#A9A9A9",
        "loved": "#DB7093",
        "stressed": "#8B8378",
    }

    style = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        html, body, [class*="css"]  {{
            font-family: 'Press Start 2P', cursive;
            letter-spacing: 0.5px;
        }}

        @media (prefers-color-scheme: light) {{
            .stApp {{
                background-color: #F4C2C2;
                color: black;
            }}
        }}

        @media (prefers-color-scheme: dark) {{
            .stApp {{
                background-color: #2D033B;
                color: #D8B4F8;
            }}
        }}

        .glass-box {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
            padding: 20px;
            margin-bottom: 20px;
        }}

        .glow-text {{
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.6);
        }}

        .mood-bar {{
            height: 12px;
            border-radius: 8px;
            margin-top: 5px;
            animation: mood-glow 4s infinite ease-in-out;
        }}

        @keyframes mood-glow {{
            0% {{ filter: brightness(1); }}
            50% {{ filter: brightness(1.4); }}
            100% {{ filter: brightness(1); }}
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

mood_map = {
    "angry": 0,
    "sad": 1,
    "anxious": 2,
    "stressed": 2.5,
    "neutral": 3,
    "loved": 4,
    "happy": 5,
}


st.set_page_config(page_title="Mood Mirror 💖", layout="centered")

if "username" not in st.session_state:
    st.session_state.username = ""
if "mood" not in st.session_state:
    st.session_state.mood = None
if "journal_saved" not in st.session_state:
    st.session_state.journal_saved = False

apply_theme(st.session_state.mood or "neutral")


if st.session_state.username == "":
    st.title("🪞 Mood Mirror")
    st.markdown("Hey, 👤 **Enter your name or nickname:**")
    username_input = st.text_input("", key="name")
    if username_input:
        st.session_state.username = "".join(c for c in username_input.strip().lower() if c.isalnum())
        st.rerun()
else:
    username = st.session_state.username
    user_file = f"data/journals/{username}.json"
    if not os.path.exists("data/journals"):
        os.makedirs("data/journals")

    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            journal_data = json.load(f)
    else:
        journal_data = []

    
    if st.session_state.mood is None:
        st.markdown("## How are you feeling today?")
        moods = {
            "😊": "happy",
            "😔": "sad",
            "😠": "angry",
            "😰": "anxious",
            "🥰": "loved",
            "🧟": "stressed",
        }
        cols = st.columns(len(moods))
        for idx, (emoji, mood) in enumerate(moods.items()):
            if cols[idx].button(emoji):
                st.session_state.mood = mood
                st.rerun()

    
    elif not st.session_state.journal_saved:
        affirmations = {
            "happy": ["Keep shining ✨", "Your joy is contagious!"],
            "sad": ["It’s okay to feel this way ❤️", "You’ve made it through tough times before."],
            "angry": ["Take a breath. You're in control.", "Anger shows you care — now use it to make something better."],
            "anxious": ["You are safe in this moment.", "Breathe in... and out. You’ve got this."],
            "loved": ["You are deeply cared for 💖", "Love surrounds you — feel it."],
            "stressed": ["One step at a time 🧘", "You don’t have to do it all right now."],
        }
        affirmation = random.choice(affirmations[st.session_state.mood])
        st.markdown(f"<div class='glass-box glow-text'>💬 {affirmation}</div>", unsafe_allow_html=True)
        st.button("Next ➡️", on_click=lambda: st.session_state.update({"journal_saved": True}))

    
    else:
        st.markdown("### ✍️ Write about your day")
        journal_input = st.text_area("What's on your mind?", height=150, placeholder="You can write anything... or nothing at all.")
        if st.button("Save Entry"):
            if journal_input.strip() == "":
                st.warning("Write something before saving.")
            else:
                new_entry = {
                    "date": datetime.date.today().isoformat(),
                    "mood": st.session_state.mood,
                    "text": journal_input.strip()
                }
                journal_data.append(new_entry)
                with open(user_file, "w") as f:
                    json.dump(journal_data, f, indent=4)
                st.success("✅ Journal saved!")

        
        st.markdown("---")
        st.markdown("### 📖 My Entries")
        if journal_data:
            for entry in reversed(journal_data[-5:]):
                bar_color = {
                    "happy": "linear-gradient(to right, #fdf497, #fbc2eb)",
                    "sad": "linear-gradient(to right, #89f7fe, #66a6ff)",
                    "angry": "linear-gradient(to right, #ff758c, #ff7eb3)",
                    "anxious": "linear-gradient(to right, #c2e9fb, #a1c4fd)",
                    "loved": "linear-gradient(to right, #fbc2eb, #a6c1ee)",
                    "stressed": "linear-gradient(to right, #fddb92, #d1fdff)",
                }.get(entry['mood'], "linear-gradient(to right, #ccc, #eee)")
                
                st.markdown(f"""
                    <div class='glass-box'>
                        <strong>🗓️ {entry['date']} — Mood: {entry['mood'].capitalize()}</strong>
                        <div class='mood-bar' style='background: {bar_color};'></div>
                        <p>{entry['text']}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No entries yet.")

        
        st.markdown("### 📈 Mood Over Time")
        if journal_data:
            dates = [entry["date"] for entry in journal_data]
            moods = [entry["mood"] for entry in journal_data]
            scores = [mood_map.get(m, 3) for m in moods]
            fig, ax = plt.subplots()
            ax.plot(dates, scores, marker='o', color='purple')
            ax.set_ylim(0, 5.5)
            ax.set_ylabel("Mood Level")
            ax.set_xlabel("Date")
            ax.set_title("Your Mood Journey 🪞")
            ax.set_yticks([0, 1, 2, 3, 4, 5])
            ax.set_yticklabels(["Angry", "Sad", "Anxious", "Neutral", "Loved", "Happy"])
            st.pyplot(fig)
        else:
            st.info("Add entries to see your mood graph.")

        
        st.markdown("### 🛂 Export Your Journal")
        def generate_txt(entries):
            content = f"🪞 Mood Mirror Journal – {username}\n\n"
            for e in entries:
                content += f"Date: {e['date']}\nMood: {e['mood'].capitalize()}\nEntry: {e['text']}\n"
                content += "-" * 40 + "\n"
            return content

        if journal_data:
            txt = generate_txt(journal_data)
            st.download_button("📥 Download My Journal (.txt)", txt, file_name=f"{username}_journal.txt")
