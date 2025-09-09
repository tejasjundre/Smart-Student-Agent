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
# 🧠 Base function with fallback
# -------------------------------
async def run_model(prompt: str) -> str:
    try:
        # ⚡ First try Mistral (fast + good quality)
        response = await client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("⚠️ Mistral failed, switching to LLaMA 3:", e)
        try:
            # 🔁 Fallback to LLaMA 3 (better reasoning, slightly slower)
            response = await client.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct:free",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except OpenAIError as e2:
            return f"⚠️ Model error: {str(e2)}"
        except Exception as e2:
            return f"⚠️ Unexpected error: {str(e2)}"

# -------------------------------
# 📚 Academic Q&A
# -------------------------------
async def ask_academic_question(query: str) -> str:
    prompt = f"Answer the academic question clearly and simply:\n{query}"
    return await run_model(prompt)

# -------------------------------
# 📖 Study Tips
# -------------------------------
async def provide_study_tips(topic: str) -> str:
    prompt = f"Give me 5 practical study tips for the topic: {topic}"
    return await run_model(prompt)

# -------------------------------
# ✂️ Summarizer
# -------------------------------
async def summarize_text(text: str) -> str:
    prompt = f"Summarize this passage in 3 clear lines:\n{text}"
    return await run_model(prompt)

# -------------------------------
# ✅ Local test mode
# -------------------------------
if __name__ == "__main__":
    async def main():
        print(await ask_academic_question("Explain photosynthesis."))
        print(await provide_study_tips("Time Management"))
        print(await summarize_text("Python is a popular programming language used in AI."))

    asyncio.run(main())
