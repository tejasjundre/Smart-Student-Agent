import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAIError

# 🔐 Load API key from .env (local only, ignored on Streamlit Cloud)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Please set it in .env (local) or Streamlit Secrets (cloud).")

# ✅ OpenRouter client
client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1/"
)

# -------------------------------
# 🧠 Base function to call model
# -------------------------------
async def run_model(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        return f"⚠️ Model error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

# -------------------------------
# 📚 Academic Q&A
# -------------------------------
async def ask_academic_question(query: str) -> str:
    prompt = (
        "You are a helpful study assistant.\n"
        "Answer the academic question below in a simple and clear tone:\n"
        f"{query}"
    )
    return await run_model(prompt)

# -------------------------------
# 📖 Study Tips
# -------------------------------
async def provide_study_tips(topic: str) -> str:
    prompt = f"Give me 5 simple study tips for the topic: {topic}"
    return await run_model(prompt)

# -------------------------------
# ✂️ Summarizer
# -------------------------------
async def summarize_text(text: str) -> str:
    prompt = f"Summarize this in 3 lines:\n{text}"
    return await run_model(prompt)

# -------------------------------
# ✅ Local test mode
# -------------------------------
if __name__ == "__main__":
    async def main():
        print(await ask_academic_question("Explain photosynthesis."))
        print(await provide_study_tips("Time Management"))
        print(await summarize_text("Python is a popular programming language."))

    asyncio.run(main())
