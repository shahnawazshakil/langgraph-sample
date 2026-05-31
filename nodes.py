from dotenv import load_dotenv
# MessagesState is the simple object which has the dictionary of the key messages
from langgraph.graph import MessagesState
# tool_node is a prebuilt node which is going to execute tools. 
# Its going to check the last message between Human and Agent
# and if that last message is an AI message that has a valid tool call,
# its going to go and execute that.
# so in our example if agent decides to run triple function or run tavily search
# it will be run in this tool_node.
from langgraph.prebuilt import ToolNode

from react import llm, tools

load_dotenv()

SYSTEM_MESSAGE="""You are a helpful assistant that can use tools to answer questions"""

def run_agent_reason(state: MessagesState) -> MessagesState:
    """
    Run the agent reasoning node.
    """
    response = llm.invoke([{"role": "system","content": SYSTEM_MESSAGE}, *state["messages"]])
    return {"messages":[response]}

tool_node = ToolNode(tools)    
