import os
import pandas as pd
import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import ast

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

# --- Define prompt for code generation ---
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

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}")
])

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Chat input ---
question = st.chat_input("Ask your question:")

def safe_execute(code, local_vars):
    try:
        tree = ast.parse(code, mode='exec')
        safe_globals = {"__builtins__": {}}
        safe_locals = local_vars.copy()

        exec(compile(tree, filename="<ast>", mode="exec"), safe_globals, safe_locals)
        if hasattr(tree.body[-1], 'value'):
            result = eval(compile(ast.Expression(tree.body[-1].value), filename="<ast>", mode="eval"), safe_globals, safe_locals)
        else:
            result = None
        return result
    except Exception as e:
        return f"❌ Execution error: {str(e)}"

if question:
    st.session_state["messages"].append({"role": "user", "content": question})

    with st.spinner("Generating answer..."):
        try:
            # Step 1: Generate python code string
            code_response_obj = llm.invoke(prompt_template.format_prompt(question=question).to_messages())
            code_response = code_response_obj.content.strip()

            # Step 2: Execute generated code safely on df
            result = safe_execute(code_response, {"df": df})

            # Step 3: Generate explanation focused on question and result only
            explanation_prompt = f"""
You are a helpful data analyst assistant.

Provide a concise explanation related to the user's question and the result obtained.

Do NOT mention pandas, code, or technical details.

Question: {question}
Result: {result}
"""

            explanation_response = llm.invoke(explanation_prompt).content.strip()

            # Format result nicely for display
            if isinstance(result, (int, float)):
                total_sales_str = f"{result:,.2f}"
            elif isinstance(result, pd.DataFrame) or isinstance(result, pd.Series):
                total_sales_str = result.to_markdown()
            else:
                total_sales_str = str(result)

            # Combine explanation and formatted result in the response
            response = explanation_response + "\n\nSummary:\n" + total_sales_str

        except Exception as e:
            response = f"❌ Error: {str(e)}"

    st.session_state["messages"].append({"role": "assistant", "content": response})

# --- Display chat history with simple labels ---
for msg in st.session_state["messages"]:
    role = msg["role"]
    content = msg["content"]

    if role == "user":
        name = "You"
    else:
        name = "Bot"

    with st.chat_message(role):
        st.markdown(f"**{name}:**\n\n{content}")
