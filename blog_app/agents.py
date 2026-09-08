import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

#get llm
def get_llm(model_name: str = "openai/gpt-oss-20b", temprature: float = 0.5) -> ChatGroq:
    api_key = os.getenv('GROQ_API_KEY')
    llm = ChatGroq(model=model_name, temperature=temprature, api_key=api_key)
    return llm



# research agent
RESEARCH_PROMPT = ChatPromptTemplate.from_messages([
    {"role": "system", "content": """

        You are a Reasearch Agent. Given a blog topic and target audience, produce a clear,
        structure research outline. Include
        1. 5-7 key points the blog should cover
        2. Important facts, state or examples for each points
        3. suggested angle or hook
        
        Be consice. Use bullet points. Do Not write the full blog yet.
    """},
    {"role": "user", "content": "Topic: {topic}, Audience: {audience}, {revision_hints},  Write the research outline now"}
])

def research_agent(llm: ChatGroq, topic: str, audience: str, feedback: str = "") -> str:
    revision_hints = f"""
        the human provided this feedback on your previous research - please address it: {feedback}
    """

    if not feedback:
        revision_hints = "This is your first attempt"

    chain = RESEARCH_PROMPT | llm

    result = chain.invoke({
        "topic": topic,
        "audience": audience,
        "revision_hints": revision_hints
    })

    return result.content




# writer agent
WRITER_PROMPT = ChatPromptTemplate.from_messages([
    {"role": "system", "content": """

        You are a Blog Writer Agent. Using the research notes provided, write a complete, 
        engaging blog post.

        Rules:
            - Length: 300 - 500 words
            - Strcuture: catchy title, into hook, 3-5 section with H2 headings, conclusions
            - Tone: clear, friendly, suited to target audience
            - User markdown formatting
            - Do Not add 'word count' line at end

    """},
    {"role": "user", "content": """
        Topic: {topic}
        Audience: {audience}
        Research notes: {research}
        {revision_hints}

        Write the full blog post now.
    """}
])


def writer_agent(llm: ChatGroq, topic: str, audience: str,research: str, feedback: str = "") -> str:
    revision_hints = f"""
        the human provided this feedback on your previous draft and asked for this changes - {feedback}. Please apply this 
        changes during writing the blog.
    """

    if not feedback:
        revision_hints = "This is your first attempt"

    chain = WRITER_PROMPT | llm

    result = chain.invoke({
        "topic": topic,
        "audience": audience,
        "research": research,
        "revision_hints": revision_hints
    })

    return result.content


# editor agent
EDITIOR_PROMPT = ChatPromptTemplate.from_messages([
    {"role": "system", "content": """

       You are an Editor Agent - the final quality gate before publishing.
       Take the draft and produce the FINAL polished version. Specifically:
        - Fix grammer, spelling and awkward phrasing
        - Improve flow and transitions between sections.
        - Make the title and intro more compeliling if needed
        - Keep the same structure and markdown formatting
        - Blog wording should look like humans, not AI and don't use any special chars and complex/fancy words

        Output only the final polished blog post - no commentary

    """},
    {"role": "user", "content": """
        Topic: {topic}
        Draft: {draft}
        
        Return the published blog post.
    """}
])

def editor_agent(llm: ChatGroq, topic: str, draft: str) -> str:

    chain = WRITER_PROMPT | llm

    result = chain.invoke({
        "topic": topic,
        "draft": draft
    })

    return result.content