# Warehouse Data Q&A ChatBot

📦 An interactive chatbot web app that answers questions about warehouse and retail sales data using natural language queries on a CSV dataset. Powered by LangChain LLM (LLaMA 3 - 8B) with Groq API backend and Streamlit for UI.

---

## Features

- Ask natural language questions about warehouse & retail sales data.
- Bot dynamically generates and executes Python pandas code on the dataset.
- Safe execution environment ensures secure code evaluation.
- Provides concise explanations and data summaries.
- Easy to extend for other datasets or domains.

---

## Demo Screenshot
![Screenshot 2025-05-28 133742](https://github.com/user-attachments/assets/a306a580-dd29-4621-8497-7a1bd29cb9d4)
![Screenshot 2025-05-28 133821](https://github.com/user-attachments/assets/95e87261-cc9c-4761-bda7-e9e8928800ee)
![Screenshot 2025-05-28 133854](https://github.com/user-attachments/assets/d7aad07f-cc28-4bcd-8e84-8bfff4c23c76) 
![Screenshot 2025-05-28 133931](https://github.com/user-attachments/assets/399dd956-1d6b-4925-b0e3-0a386b96002b)
![Screenshot 2025-05-28 134008](https://github.com/user-attachments/assets/e3cb19c2-d8bc-45fd-a7fa-a53d399e948f)
![Screenshot 2025-05-28 134019](https://github.com/user-attachments/assets/4968dd4e-d70d-4b5c-aa16-43bc28a858aa)


---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Pip (Python package manager)
- Access to Groq LLM API key (`GROQ_API_KEY`)
- CSV dataset file named `cleaned_dataset.csv`

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/warehouse-chatbot.git
   cd warehouse-chatbot

2. Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows

3. Install required packages:
    pip install -r requirements.txt
   
5. Create a .env file in the root folder and add your Groq API key:
   GROQ_API_KEY=your_groq_api_key_here

### Example Queries and Expected Answers
Q: What’s the total sales (retail + warehouse) by item type?
A: 
![image](https://github.com/user-attachments/assets/bae9ba1f-050d-4796-ab77-2f2058cbecc4)

Q:What is the total warehouse sales in January 2020?
A: 
![image](https://github.com/user-attachments/assets/162a7c8d-52eb-4f90-8641-4e4a0b595e1c)

### Assumptions & Known Limitations
- The dataset must be a CSV file named cleaned_dataset.csv and located in the app root directory.
- The DataFrame structure is assumed to be static; major changes in columns or data format may require prompt updates.
- The chatbot only generates and executes Python code using pandas; other languages or libraries are unsupported.
- Safe code execution is limited to prevent malicious commands but may not cover all edge cases.
- Responses depend heavily on the quality and scope of the LLM model (LLaMA 3 via Groq).
- The app assumes environment variable GROQ_API_KEY is set correctly.
- Streamlit session state stores conversation history but is reset when the app restarts.
- Performance and response time depend on your internet connection and Groq API service availability.
- The bot currently handles only warehouse and retail sales datasets; adapting it for other datasets requires prompt and code adjustments.

### Code Overview
#### app.py (or your main Streamlit file):

- Loads environment variables using python-dotenv.
- Loads the warehouse CSV into a pandas DataFrame.
- Initializes the LLM chat model (llama3-8b-8192) via Groq API.
- Defines a system prompt that guides the LLM to generate Python pandas code to answer queries.
- Executes generated code safely on the DataFrame and captures results.
- Displays the conversation in a chat interface.
  
#### Safe code execution uses Python ast to parse and run only non-malicious code snippets.

### Dependencies
- streamlit
- pandas
- langchain
- langchain_core
- python-dotenv
- groq

Make sure to check requirements.txt for exact versions.





