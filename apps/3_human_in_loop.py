from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
from typing import Literal

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b")

class State(BaseModel):
    query: str = Field(description="User query",default="")
    draft: str = ""
    human_feedback: str = ""
    final_response: str = ""


# defining nodes

def draft_email(state: State) -> State:
    if state.human_feedback:
        draft = llm.invoke(f"""
            You have generate this mail: {state.draft}
            human feedback to apply: {state.human_feedback}

            rewrite this draft email for {state.query}
    """)
    else:
        draft = llm.invoke(state.query)
    state.draft = draft.content
    return state


def human_feedback(state: State) -> State:
    feedback = interrupt({
        "draft_email": state.draft,
        'question': 'Do you want to continue or re-write the mail'
    })

    fb = (feedback or "").strip().lower()
    if fb in ("approved", "ok", "yes"):
        state.human_feedback = ""
        return state
    else:
        state.human_feedback = feedback
        return state

def finalize(state: State) -> State:
    if state.human_feedback:
        state.final_response = state.human_feedback
        return state
    else:
        print('Email sent successfully')
        state.final_response = "Email sent"
        return state

def conditional_routing(state: State) -> Literal["draft", "final"]:
    if state.human_feedback:
        return "draft"
    else:
        return "final"

# Graph
builder = StateGraph(State)

builder.add_node("draft", draft_email)
builder.add_node("human_fb", human_feedback)
builder.add_node("final", finalize)

builder.add_edge(START, "draft")
builder.add_edge("draft", "human_fb")
builder.add_conditional_edges("human_fb", conditional_routing)
builder.add_edge("final", END)

graph = builder.compile(checkpointer=InMemorySaver())


config = {"configurable": {"thread_id": "varsha"}}

res = graph.invoke({"query": "I want to send a email for Medical Leave request. Please help me draft a mail for 3 days"}, config=config)
res = graph.invoke(Command(resume="I want to send this email"), config=config)
print(res)


