# Email-AI-Agent
Email AI Agent that summarizes emails, extracts meetings, and detects action items using a lightweight Qwen model, routing logic, and regex-based rules.
# Email AI Agent 📨🤖

An email assistant that can:

- Summarize emails in one clean sentence  
- Extract meeting details (day, time, location)  
- Detect and list action items / tasks  

The project uses a lightweight Qwen transformer for smart summarization, and a routing-style, multi-agent design (inspired by LangGraph) combined with regex rules to keep behaviour reliable and fast.

---

## ✨ Features

- ✂️ **One-line email summary**  
  Generates a short, focused summary of the email without extra explanation or fluff.

- 🗓 **Calendar extraction**  
  Detects calendar-related information such as:
  - Day (e.g. `Friday`)
  - Time (e.g. `8 PM`, `3:30 PM`)
  - Location (e.g. `Room 204`, `cafe near Podar`, `office`)

- ✅ **Task / action item extraction**  
  Finds action phrases like:
  - `Please prepare the slide deck`
  - `Please send the latest report`
  - `Please review the API documentation`

  and converts them into a clean task list.

- 🧠 **Multi-agent, routing-style design**  
  The app conceptually has three agents:
  1. **Summarizer agent** – generates a short, human-like summary.  
  2. **Calendar agent** – extracts structured meeting info using regex.  
  3. **Task agent** – extracts to-dos from patterns like `please ...` / `can you ...`.

  A simple routing pattern (inspired by LangGraph) determines the primary intent of each email (summary / calendar / tasks), while still running all three agents so you always see a complete view.

- ⚙️ **Hybrid rules + LLM**  
  - Qwen transformer is used for generative summarization.  
  - Regex and keyword rules handle structured patterns like dates, times, rooms, and “please do X” tasks.
  - This mix keeps the system both **smart** and **predictable**.

- 🖥 **Streamlit UI**  
  A minimal web interface where you:
  - Paste an email  
  - Click “Process Email”  
  - Instantly see **Summary**, **Calendar Events**, and **Tasks**.

---

## 🏗 Architecture Overview

At a high level:

1. **Input**: Raw email text from the Streamlit UI.
2. **Routing logic**:
   - Checks for time/day/“meeting” keywords → calendar intent.
   - Looks for `please / can you / could you / kindly` → task intent.
   - Otherwise → summary intent.
3. **Agents**:
   - **Summarizer**: Generates a one-sentence summary and trims it.
   - **Calendar extractor**: Uses regex to find day/time/location.
   - **Task extractor**: Uses regex to capture “please ...” instructions and split them into individual tasks.
4. **Output**:
   - Summary (string)  
   - Calendar events (list of dicts)  
   - Tasks (list of strings)  

All results are shown together in the Streamlit app.

---

## 🧰 Tech Stack

- **Python 3**
- **Qwen/Qwen2.5-0.5B-Instruct** (Hugging Face Transformers) – for summarization  
- **Regex** – for detecting dates, times, locations, and tasks  
- **Streamlit** – for the UI

*(In some variants, a pure-regex summarizer is used instead of Qwen for ultra-fast, no-LLM mode.)*

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/ShivamSutar11/Email-AI-Agent
cd Email_Workflow
2. Create and activate a virtual environment (optional but recommended)
bash
Copy code
python -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate    # Windows
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
A minimal requirements.txt might look like:

text
Copy code
streamlit
transformers
torch
(If you use the pure-regex version without Qwen, you can drop transformers and torch.)

▶️ Running the App
From the project root:

bash
Copy code
streamlit run email_app.py
Then open the URL shown in the terminal (usually http://localhost:8501).

🧪 Example Usage
Try pasting this email into the app:

text
Copy code
Hey Suyash,

The internal review for our project is complete and nothing urgent is pending on your side.

Let’s meet on Friday at 8 PM in the cafe near Podar to discuss the next steps.

Please bring the updated project report, prepare the new slide deck, and send me the latest metrics before the meeting.

Thanks,
Manager
You should see:

Summary
A short sentence capturing review status + meeting context.

Calendar Events (example)

json
Copy code
[
  {
    "day": "Friday",
    "time": "8 PM",
    "location": "cafe"
  }
]
Tasks (example)

Please bring the updated project report

Please prepare the new slide deck

Please send me the latest metrics before the meeting

🔮 Possible Extensions
Connect with Gmail API to process real inbox emails.

Automatically create calendar events from extracted meeting info.

Assign priorities to emails (e.g., urgent / action required / FYI).

Experiment with different LLMs or fine-tuned models for summarization.

Add evaluation using a small Hugging Face dataset of labeled emails for routing / extraction quality.

📌 Summary
This project is a small but complete example of:

Using a lightweight transformer model (Qwen) for local summarization,

Combining it with regex-based rules for reliable extraction,

Applying a simple multi-agent / routing-style pattern (inspired by LangGraph),

And wrapping everything in a Streamlit app to make the agent easy to test and demo.
