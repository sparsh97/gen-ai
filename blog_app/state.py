from pydantic import BaseModel

class BlogState(BaseModel):
    #user input
    topic: str = ""
    audience: str = "general readers"

    # research field
    research: str = ""
    research_feedback: str = ""

    #write
    draft: str = ""
    draft_feedback: str = ""

    #editior
    final_blog: str = ""

    # metadata
    revision_count: int = 0