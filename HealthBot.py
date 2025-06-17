# %%
!pip install --quiet -U langchain==0.2.16
!pip install --quiet -U langchain_openai==0.1.23
!pip install --quiet -U langgraph==0.2.19
!pip install --quiet -U langchainhub==0.1.21
!pip install --quiet -U tavily-python==0.4.0
!pip install --quiet -U langchain-community==0.2.16
!pip install --quiet -U python-dotenv==1.0.1

# %%
import os
from dotenv import load_dotenv #type: ignore
from typing_extensions import TypedDict #type: ignore
from tavily import TavilyClient #type: ignore
from langchain_community.chat_models import ChatOpenAI  # type: ignore
from langgraph.graph import StateGraph, START, END  #type: ignore
from langchain.schema import HumanMessage


# %%

# API Keys
load_dotenv(".env")
assert os.getenv("OPENAI_API_KEY")
assert os.getenv("TAVILY_API_KEY")

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm    = ChatOpenAI(temperature=0.7, model_name="gpt-4")


# %%

# State
class HealthBotState(TypedDict):
    topic: str
    search_results: str
    summary: str
    ready_for_quiz: bool
    quiz_question: str
    user_answer: str
    grade: str
    feedback: str
    restart: bool



# %%

def ask_topic(state: HealthBotState) -> HealthBotState:
    state["topic"] = input("What health topic would you like to learn about? ")
    return state

def tavily_search(state: HealthBotState) -> HealthBotState:

    resp = tavily.search(
        query=state["topic"],
        max_results=5
    )
    
    texts = []
    for item in resp.get("results", []):
    
        texts.append(item.get("content") or item.get("raw_content", ""))
    
    state["search_results"] = "\n\n".join(texts)
    return state
def summarize_info(state: HealthBotState) -> HealthBotState:
    prompt = (
        "You are a medical educator. Summarize the following into a 3–4 paragraph,"
        " patient-friendly explanation, using only this text:\n\n"
        + state["search_results"]
    )
    messages = [HumanMessage(content=prompt)]
    response = llm(messages)     
    state["summary"] = response.content
    
    return state

def display_summary(state: HealthBotState) -> HealthBotState:
    print("\n--- Summary ---\n", state["summary"])
    return state

def wait_for_ready(state: HealthBotState) -> HealthBotState:
    input("Press Enter when you’re ready for a short quiz… ")
    state["ready_for_quiz"] = True
    return state

def generate_quiz_question(state: HealthBotState) -> HealthBotState:
    prompt = (
        "Based only on this summary, generate ONE clear quiz question:\n\n"
        + state["summary"]
    )
    state["quiz_question"] = llm(prompt)
    return state

def ask_quiz_question(state: HealthBotState) -> HealthBotState:
    print("\n--- Quiz Question ---\n", state["quiz_question"])
    state["user_answer"] = input("Your answer: ")
    return state

def grade_answer(state: HealthBotState) -> HealthBotState:
    prompt = (
        "Grade the answer A–F based only on the summary, and justify using citations:\n\n"
        f"Summary:\n{state['summary']}\n\n"
        f"Question:\n{state['quiz_question']}\n\n"
        f"Answer:\n{state['user_answer']}"
    )
    graded = llm(prompt).splitlines()
    state["grade"]    = graded[0].replace("Grade:", "").strip()
    state["feedback"] = "\n".join(graded[1:]).replace("Feedback:", "").strip()
    return state

def display_grade(state: HealthBotState) -> HealthBotState:
    print(f"\nYour Grade: {state['grade']}\nFeedback:\n{state['feedback']}")
    return state

def ask_restart(state: HealthBotState) -> HealthBotState:
    state["restart"] = input("Learn another topic? (yes/no) ").lower().startswith("y")
    return state


# %%

builder = StateGraph(state_schema=HealthBotState)

builder.add_node("ask_topic",           ask_topic)
builder.add_node("tavily_search",       tavily_search)
builder.add_node("summarize_info",      summarize_info)
builder.add_node("display_summary",     display_summary)
builder.add_node("wait_for_ready",      wait_for_ready)
builder.add_node("generate_quiz_question", generate_quiz_question)
builder.add_node("ask_quiz_question",   ask_quiz_question)
builder.add_node("grade_answer",        grade_answer)
builder.add_node("display_grade",       display_grade)
builder.add_node("ask_restart",         ask_restart)

builder.add_edge(START,            "ask_topic")
builder.add_edge("ask_topic",      "tavily_search")
builder.add_edge("tavily_search",  "summarize_info")
builder.add_edge("summarize_info", "display_summary")
builder.add_edge("display_summary","wait_for_ready")
builder.add_edge("wait_for_ready", "generate_quiz_question")
builder.add_edge("generate_quiz_question","ask_quiz_question")
builder.add_edge("ask_quiz_question","grade_answer")
builder.add_edge("grade_answer",   "display_grade")
builder.add_edge("display_grade",  "ask_restart")
builder.add_edge("ask_restart",    END)

app = builder.compile()



# %%

while True:

    state: HealthBotState = {
        "topic": "",
        "search_results": "",
        "summary": "",
        "ready_for_quiz": False,
        "quiz_question": "",
        "user_answer": "",
        "grade": "",
        "feedback": "",
        "restart": False,
    }
    final_state = app.invoke(state)
    if not final_state["restart"]:
        print("\nGood Job, Happy Learning!")
        break
    print("\n Starting over with a fresh topic…\n")


# %%


# %%



