# ============================================================
#      EMAIL AI AGENT (PURE PYTHON • SUPER FAST • 3 AGENTS)
# ============================================================

import re
import streamlit as st
from typing import TypedDict, Optional, List, Dict


# ------------------------------------------------------------
# Agent State (for clarity)
# ------------------------------------------------------------
class AgentState(TypedDict):
    email_text: str
    summary: Optional[str]
    calendar_events: Optional[List[Dict]]
    tasks: Optional[List[str]]
    route: Optional[str]


# ------------------------------------------------------------
# Small helpers
# ------------------------------------------------------------

GREETING_REGEX = re.compile(
    r"^\s*(hi|hello|hey|dear)\b.*$", re.IGNORECASE
)
SIGNOFF_REGEX = re.compile(
    r"^\s*(thanks|regards|best|cheers|sincerely)\b.*$", re.IGNORECASE
)


def clean_email_lines(email: str) -> List[str]:
    """Split into lines, drop greetings + sign-offs + empty lines."""
    lines = []
    for line in email.splitlines():
        line = line.strip()
        if not line:
            continue
        if GREETING_REGEX.match(line):
            continue
        if SIGNOFF_REGEX.match(line):
            continue
        lines.append(line)
    return lines


def split_sentences(text: str) -> List[str]:
    """Very simple sentence splitter."""
    # Replace newlines with spaces
    text = re.sub(r"\s+", " ", text).strip()
    # Split by . ? !
    raw = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in raw if s.strip()]
    return sentences


# ------------------------------------------------------------
# 1) SUMMARY AGENT  (no LLM, 1 short sentence)
# ------------------------------------------------------------

def summarize_email(state: AgentState) -> None:
    email = state["email_text"]

    # Remove greetings / sign-offs
    lines = clean_email_lines(email)
    if not lines:
        state["summary"] = ""
        return

    core_text = " ".join(lines)
    sentences = split_sentences(core_text)

    if not sentences:
        state["summary"] = ""
        return

    # Try to pick a "meaningful" sentence, else first one
    important_keywords = [
        "meeting", "deadline", "review", "update", "completed",
        "finished", "urgent", "call", "exam", "project"
    ]

    chosen = sentences[0]
    for s in sentences:
        if any(word in s.lower() for word in important_keywords):
            chosen = s
            break

    # Make it one clean sentence, capitalized
    chosen = chosen.strip()
    if not chosen.endswith("."):
        chosen += "."

    # Hard length cap to keep it short
    MAX_LEN = 140
    if len(chosen) > MAX_LEN:
        chosen = chosen[:MAX_LEN].rsplit(" ", 1)[0] + "..."

    state["summary"] = chosen


# ------------------------------------------------------------
# 2) CALENDAR AGENT  (regex only)
# ------------------------------------------------------------

DAY_PATTERN = r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
TIME_PATTERN = r"\b\d{1,2}(:\d{2})?\s?(am|pm)\b"
LOCATION_PATTERN = r"\b(room\s*\d+|cafe|office|podar|classroom|lab)\b"


def extract_calendar(state: AgentState) -> None:
    email = state["email_text"].lower()

    day_match = re.search(DAY_PATTERN, email, re.IGNORECASE)
    time_match = re.search(TIME_PATTERN, email, re.IGNORECASE)
    loc_match = re.search(LOCATION_PATTERN, email, re.IGNORECASE)

    events: List[Dict] = []

    if day_match or time_match or loc_match:
        events.append(
            {
                "day": day_match.group(0).capitalize() if day_match else "",
                "time": time_match.group(0) if time_match else "",
                "location": loc_match.group(0) if loc_match else "",
            }
        )

    state["calendar_events"] = events or None


# ------------------------------------------------------------
# 3) TASK AGENT  (regex only)
# ------------------------------------------------------------

def extract_tasks(state: AgentState) -> None:
    email = state["email_text"]

    # Pattern: sentences starting with "please ..." or containing "please ...".
    task_pattern = re.compile(
        r"(please\s+[a-z].*?)(?:[.!?]|$)", re.IGNORECASE | re.DOTALL
    )

    tasks: List[str] = []

    for match in task_pattern.findall(email):
        task = match.strip()
        # Clean trailing punctuation / spaces
        task = re.sub(r"[\s.]+$", "", task)
        tasks.append(task[0].upper() + task[1:])

    state["tasks"] = tasks or None


# ------------------------------------------------------------
# 4) ROUTER  (decide dominant route)
# ------------------------------------------------------------

def decide_route(state: AgentState) -> None:
    """Route priority: calendar > tasks > summary."""
    email = state["email_text"].lower()

    has_calendar = bool(
        re.search(DAY_PATTERN, email, re.IGNORECASE)
        or re.search(TIME_PATTERN, email, re.IGNORECASE)
        or re.search(r"\bmeeting\b", email)
    )

    has_task = bool(
        re.search(r"\bplease\b", email)
        or re.search(r"\bcan you\b", email)
        or re.search(r"\bcould you\b", email)
        or re.search(r"\bkindly\b", email)
    )

    if has_calendar:
        state["route"] = "calendar"
    elif has_task:
        state["route"] = "tasks"
    else:
        state["route"] = "summary"


# ------------------------------------------------------------
# 5) STREAMLIT UI
# ------------------------------------------------------------

st.set_page_config(page_title="Email AI Agent ", layout="wide")
st.title("Email AI Agent ")

email_text = st.text_area("Email:", height=220)

if st.button("Process Email"):
    state: AgentState = {
        "email_text": email_text,
        "summary": None,
        "calendar_events": None,
        "tasks": None,
        "route": None,
    }

    # Run all three agents
    summarize_email(state)
    extract_calendar(state)
    extract_tasks(state)
    decide_route(state)

    # ---------------- Route ----------------
    #st.subheader("Route")
    #st.write(state["route"])

    # ---------------- Summary ----------------
    st.subheader("Summary")
    if state["summary"]:
        st.write(state["summary"])
    else:
        st.write("No summary generated.")

    # ---------------- Calendar ----------------
    st.subheader("Calendar Events")
    if state["calendar_events"]:
        st.json(state["calendar_events"])
    else:
        st.write("No calendar events found.")

    # ---------------- Tasks ----------------
    st.subheader("Tasks")
    if state["tasks"]:
        for t in state["tasks"]:
            st.write("• " + t)
    else:
        st.write("No tasks found.")
