from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph, END
from nodes import run_agent_reason, tool_node

load_dotenv()

AGENT_REASON="my_agent_reason"
ACT= "my_act"
LAST = -1

def should_continue(state:MessagesState) -> str:
    if not state["messages"][LAST].tool_calls:
        return END
    return ACT

# Create an empty LangGraph workflow named flow. StateGraph is the builder for a
# stateful graph. MessageState is the Schema for shared state passed between nodes. Its
# essentially a list of chat messages (HumanMessage, AIMessage, ToolMessage etc)
flow = StateGraph(MessagesState)
# Add nodes to the stateful graph. Nodes are nothing but functions. Hear AGENT_REASON is
# a readable name that you give to node and run_agent_reasonn is actual function name
flow.add_node(AGENT_REASON, run_agent_reason)
flow.add_node(ACT,tool_node)

flow.set_entry_point(AGENT_REASON)

# You can add edge OR conditional_edge to the flow. Both define where the graph goes
# next after a node finishes. The difference is whether that destination is fixed or
# decided at runtime
# Example of edge - flow.add_edge(ACT, AGENT_REASON)
# Above means that after After my_act runs, the graph always goes to my_agent_reason. No decision logic — every execution follows the same path.
# The one we are using below is conditional edge. After my_agent_reason runs, LangGraph calls should_continue(state) and uses its return value to pick the next node.
flow.add_conditional_edges(AGENT_REASON,should_continue,{
    END:END,
    ACT:ACT})
flow.add_edge(ACT, AGENT_REASON)

app = flow.compile()

app.get_graph().draw_mermaid_png(output_file_path="flow.png")


if __name__ == "__main__":
    print("Hello ReAct LangGraph with Function calling")
    res = app.invoke({"messages": [HumanMessage(content="What is the weaather in Tokyo? List it and then triple it")]})
    print(res["messages"][LAST].content)
