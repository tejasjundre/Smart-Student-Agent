import streamlit as st
import asyncio
import time
from main import ask_academic_question, provide_study_tips, summarize_text

# -------------------------------
# App Config
# -------------------------------
st.set_page_config(page_title="📚 MySmartStudyAI", layout="centered")

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>
@keyframes fadeIn { from {opacity: 0; transform: translateY(10px);} to {opacity: 1; transform: translateY(0);} }
.title {text-align: center; color: #2E86C1; font-size: 42px; font-weight: bold; animation: fadeIn 1.2s ease-in-out;}
.subtitle {text-align: center; color: gray; font-size: 18px; margin-top: -10px; animation: fadeIn 2s ease-in-out;}
.response-box {background-color: #F4F9FF; border: 1px solid #D6EAF8; border-radius: 12px; padding: 15px; margin-top: 15px; font-size: 16px; animation: fadeIn 0.5s ease-in-out; color: #333;}
.user-box {background-color: #D6EAF8; border-radius: 12px; padding: 12px; margin-top: 15px; font-size: 16px; color: #2E4053;}
.progress-bar {height: 5px; background-color: #2E86C1; width: 0%; border-radius: 5px; transition: width 0.2s;}
.footer {text-align: center; color: gray; font-size: 14px; margin-top: 30px; animation: fadeIn 3s ease-in-out;}
div.stButton > button {background-color: #2E86C1; color: white; border-radius: 8px; transition: 0.3s;}
div.stButton > button:hover {background-color: #1B4F72; transform: scale(1.05);}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.markdown("<h1 class='title'>📚 MySmartStudyAI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Personal AI Study Buddy — Ask, Learn & Succeed 🚀</p>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=100)
    st.markdown("## ℹ️ About MySmartStudyAI")
    st.markdown("""
**MySmartStudyAI** helps students:
- 📘 Answer academic questions  
- 🧠 Get personalized study tips  
- 📝 Summarize long passages  

---
**Version:** 1.0.2
""")
    st.markdown("### 🔗 Connect")
    st.markdown("[🌐 GitHub](https://github.com/your-username)  \n[💼 LinkedIn](https://linkedin.com/in/your-link)  \n[📧 Email](mailto:your-email@example.com)")

# -------------------------------
# Navigation Menu
# -------------------------------
feature = st.radio(
    "✨ Choose a Feature",
    ["📘 Academic Q&A", "🧠 Study Tips", "📝 Text Summary"],
    horizontal=True
)

# -------------------------------
# Async Runner
# -------------------------------
def run_async(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(func(*args))

# -------------------------------
# Typing + Progress Effect
# -------------------------------
def stream_response_with_progress(response_text):
    placeholder = st.empty()
    progress = st.progress(0)
    text = ""
    for i, char in enumerate(response_text):
        text += char
        placeholder.markdown(f"<div class='response-box'>{text}</div>", unsafe_allow_html=True)
        progress.progress(min((i+1)/len(response_text), 1.0))
        time.sleep(0.02)  # controls typing speed
    progress.empty()

# -------------------------------
# Feature: Academic Questions
# -------------------------------
if feature == "📘 Academic Q&A":
    st.subheader("❓ Ask any academic question")
    question = st.text_area("Type your question here:")
    if st.button("Get Answer"):
        if question.strip():
            st.markdown(f"<div class='user-box'>{question}</div>", unsafe_allow_html=True)
            with st.spinner("💡 Thinking..."):
                answer = run_async(ask_academic_question, question)
            stream_response_with_progress(answer)
        else:
            st.warning("⚠️ Please enter a valid question.")

# -------------------------------
# Feature: Study Tips
# -------------------------------
elif feature == "🧠 Study Tips":
    st.subheader("📖 Get personalized study tips")
    topic = st.text_input("Enter a topic you want help with:")
    if st.button("Get Tips"):
        if topic.strip():
            st.markdown(f"<div class='user-box'>{topic}</div>", unsafe_allow_html=True)
            with st.spinner("✨ Generating tips..."):
                tips = run_async(provide_study_tips, topic)
            stream_response_with_progress(tips)
        else:
            st.warning("⚠️ Please enter a topic.")

# -------------------------------
# Feature: Text Summarization
# -------------------------------
elif feature == "📝 Text Summary":
    st.subheader("📝 Summarize long passages")
    passage = st.text_area("Paste your text passage here:")
    if st.button("Summarize"):
        if passage.strip():
            st.markdown(f"<div class='user-box'>{passage[:50]}...</div>", unsafe_allow_html=True)
            with st.spinner("📌 Summarizing..."):
                summary = run_async(summarize_text, passage)
            stream_response_with_progress(summary)
        else:
            st.warning("⚠️ Please paste a passage to summarize.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Made with ❤️ by Tejas | Powered by OpenAI</p>", unsafe_allow_html=True)
