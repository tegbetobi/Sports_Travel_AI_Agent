from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from typing import Literal
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from IPython.display import display, Markdown, Image
from app.core.state import *
from app.core.tools import *

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, streaming=True)

def make_call_model_with_tools(tools: list):
    def call_model_with_tools(state: AgentState):
        print("DEBUG: Entering call_model_with_tools node")
        messages = state["messages"] 
        model_with_tools = llm.bind_tools(tools)  # Binds the tools to the language model
        response = model_with_tools.invoke(messages) # Feeds the conversation history (messages) into the model
        return {"messages": [response]} # Return the model response as a new message

    return call_model_with_tools


def should_continue(state: AgentState) -> Literal["action", "__end__"]:
    """Determines the next step: continue with tools or end."""
    print("DEBUG: Entering should_continue node")
    last_message = state["messages"][-1]
    
    # Check if the last message is an AIMessage with tool_calls
    if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("DEBUG: Decision: continue (route to action)")
        return "action"  # Route to the node named "action"
    else:
        print("DEBUG: Decision: end (route to END)")
        return END  # Special value indicating the end of the graph
    


def build_graph_one_tool(tools_list):

    tool_node = ToolNode(tools_list) # Let's Instantiate ToolNode
    call_node_fn = make_call_model_with_tools(tools_list)     # Define the call_node_fn, which binds the tools to the LLM and calls OpenAI API   

    graph_one_tool = StateGraph(AgentState) # Build the Graph with One Tool using ToolNode
    graph_one_tool.add_node("agent", call_node_fn) # Add nodes
    
    graph_one_tool.add_node("action", tool_node) # Add the ToolNode instance directly, naming it "action"

    graph_one_tool.set_entry_point("agent") # Set entry point

    # Add a conditional edge from the agent
    # The dictionary maps the return value of 'should_continue' ("action" or END) to the name of the next node ("action" or the special END value).
    graph_one_tool.add_conditional_edges(
        "agent",  # Source node name
        should_continue,  # Function to decide the route
        {"action": "action", END: END},  # Mapping: {"decision": "destination_node_name"}
    )

    graph_one_tool.add_edge("action", "agent") # Add edge from action (ToolNode) back to agent
    app = graph_one_tool.compile() # Compile the graph
    display(Image(app.get_graph().draw_mermaid_png()))

    return app


def app_call(app, messages):
    initial_state = { # Initialize the state with the provided messages
    "messages": [
        SystemMessage(content=SYSTEM_JSON_RULES),
        HumanMessage(content=messages),
    ]
}
    final_state = app.invoke(initial_state)     # Invoke the app with the initial state
    return final_state["messages"][-1].content, final_state # Return the content of the last message and the final state


SYSTEM_JSON_RULES = """
You are a backend API.

You MUST return strictly valid JSON.
You MUST follow the exact schema provided by the user.
If data is missing, return empty arrays.
Do NOT include explanations, markdown, or extra text.
Do NOT wrap JSON in code blocks.
"""