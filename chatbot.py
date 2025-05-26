import os
import pandas as pd
import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_experimental.tools import PythonAstREPLTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found in .env file.")
    st.stop()

os.environ["GROQ_API_KEY"] = groq_api_key

# === Streamlit page setup ===
st.set_page_config(page_title="Warehouse QA Bot", layout="centered")
st.title("📦 Warehouse Data Q&A ChatBot")

# Load dataset
df = pd.read_csv("cleaned_dataset.csv", low_memory=False)

# Initialize LLM
llm = init_chat_model("llama3-8b-8192", model_provider="groq")

# Setup Pandas agent tool
tool = PythonAstREPLTool(locals={"df": df})
llm_with_tools = llm.bind_tools([tool], tool_choice=tool.name)
parser = JsonOutputKeyToolsParser(key_name=tool.name, first_tool_only=True)

# --- Define prompt with additional context ---

additional_context = """
You are a helpful data analyst assistant with access to a pandas DataFrame called `df`.
The DataFrame contains warehouse and retail sales data.

Your task:
- Use only Python built-in libraries and pandas to analyze and answer the user's questions.
- Return ONLY the valid Python code (no explanations) that performs the required operation on `df`.
- Make sure the code returns the final result explicitly (e.g., a DataFrame, a value, or a print statement).
- If the user asks for data summaries, aggregations, or filters, write the appropriate pandas code.
- Do not include import statements; pandas is already imported.
- Here is a preview of the DataFrame to help you understand its structure:
"""

df_preview = df.head().to_markdown()

system_prompt = f"{additional_context}\n{df_preview}\n\nAnswer user queries by generating python code to execute on `df`."

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}")
])

pandas_chain = prompt | llm_with_tools | parser | tool

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Chat input ---
question = st.chat_input("Ask your question:")

if question:
    # Append user message to session_state immediately
    st.session_state["messages"].append({"role": "user", "content": question})

    # Generate assistant response
    with st.spinner("Processing..."):
        try:
            response = pandas_chain.invoke({"question": question})
        except Exception as e:
            response = f"❌ Error: {str(e)}"

    # Append assistant response to session_state
    st.session_state["messages"].append({"role": "assistant", "content": response})

# --- Display chat history with avatars and names ---
for msg in st.session_state["messages"]:
    role = msg["role"]
    content = msg["content"]

    if role == "user":
        name = "You"
        avatar = "👤"
    else:
        name = "Bot"
        avatar = "🤖"

    st.markdown(f"**{avatar} {name}:**")
    with st.chat_message(role):
        st.markdown(content)
