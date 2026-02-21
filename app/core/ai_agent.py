from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from app.config.settings import settings


def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    llm = ChatGroq(model=llm_id)
    
    tools = [TavilySearch(max_results=2)] if allow_search else []
    
    agent = create_agent(
        model=llm,
        tools=tools
    )
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="\n".join(query) if isinstance(query, list) else query)
    ]
    
    state = {"messages": messages}
    response = agent.invoke(state)
    
    ai_messages = [
        m.content for m in response.get("messages", [])
        if isinstance(m, AIMessage)
    ]
    
    return ai_messages[-1] if ai_messages else "No response generated."


