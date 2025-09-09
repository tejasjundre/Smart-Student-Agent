import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAIError
from huggingface_hub import InferenceClient
from graphviz import Digraph

# 🔐 Load API key from .env (local only)
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
# Hugging Face free image client
# -------------------------------
hf_client = InferenceClient("stabilityai/stable-diffusion-2")

# -------------------------------
# Helper: Detect diagram-related questions
# -------------------------------
def needs_diagram(prompt: str) -> bool:
    keywords = ["diagram", "flowchart", "graph", "illustration", "chart"]
    return any(word.lower() in prompt.lower() for word in keywords)

# -------------------------------
# Generate Graphviz fallback diagram
# -------------------------------
def generate_graphviz_diagram(question: str):
    if "binary search" in question.lower():
        dot = Digraph(comment='Binary Search Flowchart')
        dot.node('A', 'Start')
        dot.node('B', 'Check Mid')
        dot.node('C', 'Left/Right')
        dot.node('D', 'Found / End')
        dot.edges(['AB', 'BC', 'CD'])
        return dot
    # Add more topics as needed
    return "📄 Diagram not available for this topic."

# -------------------------------
# Generate free AI image
# -------------------------------
def generate_free_image(prompt: str):
    try:
        image = hf_client.text_to_image(prompt)
        return image  # returns image bytes for Streamlit
    except:
        return None

# -------------------------------
# Base async model with fallback
# -------------------------------
async def run_model(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("⚠️ Mistral failed, switching to LLaMA 3:", e)
        try:
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
# Academic Q&A (with image/diagram support)
# -------------------------------
async def ask_academic_question(query: str):
    if needs_diagram(query):
        image = generate_free_image(query)
        if image:
            return image  # Streamlit can display image bytes
        else:
            return generate_graphviz_diagram(query)  # fallback

    prompt = f"Answer the academic question clearly and simply:\n{query}"
    return await run_model(prompt)

# -------------------------------
# Study Tips
# -------------------------------
async def provide_study_tips(topic: str) -> str:
    prompt = f"Give me 5 practical study tips for the topic: {topic}"
    return await run_model(prompt)

# -------------------------------
# Summarizer
# -------------------------------
async def summarize_text(text: str) -> str:
    prompt = f"Summarize this passage in 3 clear lines:\n{text}"
    return await run_model(prompt)

# -------------------------------
# Local test mode
# -------------------------------
if __name__ == "__main__":
    async def main():
        result = await ask_academic_question("Draw a flowchart of binary search")
        print(result)
        print(await provide_study_tips("Time Management"))
        print(await summarize_text("Python is a popular programming language used in AI."))

    asyncio.run(main())
