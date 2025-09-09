import streamlit as st
import asyncio
from main import ask_academic_question, provide_study_tips, summarize_text

# -------------------------------
# App Config
# -------------------------------
st.set_page_config(page_title="📚 MySmartStudyAI", layout="centered")

# -------------------------------
# Custom CSS for Animations & Styling
# -------------------------------
st.markdown(
    """
    <style>
        /* Fade-in animation */
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(10px);}
            to {opacity: 1; transform: translateY(0);}
        }

        /* Page title styling */
        .title {
            text-align: center;
            color: #2E86C1;
            font-size: 42px;
            font-weight: bold;
            animation: fadeIn 1.2s ease-in-out;
        }

        /* Subtitle */
        .subtitle {
            text-align: center;
            color: gray;
            font-size: 18px;
            margin-top: -10px;
            animation: fadeIn 2s ease-in-out;
        }

        /* Response box */
        .response-box {
            background-color: #F4F9FF;
            border: 1px solid #D6EAF8;
            border-radius: 12px;
            padding: 15px;
            margin-top: 15px;
            font-size: 16px;
            animation: fadeIn 1s ease-in-out;
            color: #333333; /* Added dark text color for readability */
        }

        /* Footer */
        .footer {
            text-align: center;
            color: gray;
            font-size: 14px;
            margin-top: 30px;
            animation: fadeIn 3s ease-in-out;
        }

        /* Streamlit button hover */
        div.stButton > button {
            background-color: #2E86C1;
            color: white;
            border-radius: 8px;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #1B4F72;
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Header
# -------------------------------
st.markdown("<h1 class='title'>📚 MySmartStudyAI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Personal AI Study Buddy — Ask, Learn & Succeed 🚀</p>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# Sidebar (About + Links + Contact)
# -------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=100)
    st.markdown("## ℹ️ About MySmartStudyAI")
    st.markdown(
        """
        **MySmartStudyAI** is an intelligent assistant designed 
        to help students:
        - 📘 Answer academic questions  
        - 🧠 Get personalized study tips  
        - 📝 Summarize long passages  

        ---
        **Version:** 1.0.0  
        """
    )
    st.markdown("### 🔗 Connect with Me")
    st.markdown("[🌐 GitHub](https://github.com/your-username)  \n"
                "[💼 LinkedIn](https://linkedin.com/in/your-link)  \n"
                "[📧 Email](mailto:your-email@example.com)")

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
# Feature 1: Academic Questions
# -------------------------------
if feature == "📘 Academic Q&A":
    st.subheader("❓ Ask any academic question")
    question = st.text_area("Type your question here:")
    if st.button("Get Answer"):
        if question.strip():
            with st.spinner("💡 Thinking..."):
                answer = run_async(ask_academic_question, question)
            st.markdown(f"<div class='response-box'>{answer}</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter a valid academic question.")

# -------------------------------
# Feature 2: Study Tips
# -------------------------------
elif feature == "🧠 Study Tips":
    st.subheader("📖 Get personalized study tips")
    topic = st.text_input("Enter a topic you want help with:")
    if st.button("Get Tips"):
        if topic.strip():
            with st.spinner("✨ Generating tips..."):
                tips = run_async(provide_study_tips, topic)
            st.markdown(f"<div class='response-box'>{tips}</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter a study topic.")

# -------------------------------
# Feature 3: Text Summarization
# -------------------------------
elif feature == "📝 Text Summary":
    st.subheader("📝 Summarize long passages")
    passage = st.text_area("Paste your text passage here:")
    if st.button("Summarize"):
        if passage.strip():
            with st.spinner("📌 Summarizing..."):
                summary = run_async(summarize_text, passage)
            st.markdown(f"<div class='response-box'>{summary}</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please paste a passage to summarize.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Made with ❤️ by Tejas | Powered by OpenAI</p>", unsafe_allow_html=True)