from typing import Literal

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from state import BlogState
from agents import editor_agent, get_llm, writer_agent,research_agent



max_revisions = 3
builder = StateGraph(BlogState)

### nodes
def researcher_nodes(state: BlogState) -> BlogState:
    """
        Reasech Agent generates (or revise) the reseach outline
    """
    llm = get_llm()
    feedback = state.research_feedback

    agent = research_agent(llm, topic=state.topic, audience=state.audience, feedback=feedback)
    state.research = agent
    state.research_feedback = ""
    return state

def human_review_research_node(state: BlogState) -> BlogState:
    """
        Pause and Ask the human to approve the research or send the feedback
    """
    decision = interrupt({
        "stage": "researcher_review",
        "research": state.research,
        "instrcutions": {
            "Reply with 'approve' to continue to writing",
            "or describe what to change to send it back to the researcher"
        }
    })

    if isinstance(decision, dict):
        action = decision.get("action", "approve")
        feedback = decision.get("feedback", "")
    else:
        text = str(decision)
        action = "approve" if text.lower() in ["approve", "approved", "okay", "yes", ""] else "revise"
        feedback = "" if action == "approve" else text

    state.research_feedback = feedback
    return state


def writer_nodes(state: BlogState) -> BlogState:
    """
        Writer Agent produce the full draft blog (or revise it)
    """
    llm = get_llm()
    feedback = state.draft_feedback

    agent = writer_agent(llm, topic=state.topic, audience=state.audience,research=state.research, feedback=feedback)
    state.draft = agent
    state.draft_feedback = ""
    return state

def human_review_draft_node(state: BlogState) -> BlogState:
    """
        Pause and Ask the human to approve the draft or send the feedback
    """
    decision = interrupt({
        "stage": "draft_review",
        "research": state.draft,
        "instrcutions": {
            "Reply with 'approve' to continue to send it to editor",
            "or describe what to change to send it back to the writer"
        }
    })

    if isinstance(decision, dict):
        action = decision.get("action", "approve")
        feedback = decision.get("feedback", "")
    else:
        text = str(decision)
        action = "approve" if text.lower() in ["approve", "approved", "okay", "yes", ""] else "revise"
        feedback = "" if action == "approve" else text

    state.draft_feedback = feedback
    return state

def editior_nodes(state: BlogState) -> BlogState:
    llm = get_llm()

    final = editor_agent(llm= llm, topic=state.topic, draft=state.draft)
    state.final_blog = final
    return state


### conditional edges
def route_after_research_review(state: BlogState) -> Literal['research', 'writer']:
    if state.research_feedback:
        return "research"
    else:
        return "writer"

def route_after_draft_review(state: BlogState) -> Literal['editor', 'writer']:
    if state.draft_feedback and state.revision_count < max_revisions:
        return "writer"
    else:
        return "editor"



### build and compile the graph
def build_blog_graph():
    builder = StateGraph(BlogState)

    ## add nodes
    builder.add_node("research", researcher_nodes)
    builder.add_node("researcher_review", human_review_research_node)
    builder.add_node("writer", writer_nodes)
    builder.add_node("draft_review", human_review_draft_node)
    builder.add_node("editor", editior_nodes)

    ## add edges
    builder.add_edge(START, "research")
    builder.add_edge("research", "researcher_review")
    builder.add_conditional_edges("researcher_review", route_after_research_review)
    builder.add_edge("writer", "draft_review")
    builder.add_conditional_edges("draft_review", route_after_draft_review)
    builder.add_edge("editor", END)


    ## compile graph
    graph = builder.compile(checkpointer=InMemorySaver())
    return graph