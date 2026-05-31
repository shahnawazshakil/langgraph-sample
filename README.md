# Node
A node is a single step in your workflow that receives the current state, does one piece of work and returns an update to that state.
A node can be a function (e.g. run_agent_reason), or a prebuilt callable (e.g. ToolNode(tools)), or any Runnable LangChain/LangGraph object with an .invoke() mentod
In our example, there are two nodes
## run_agent_reason
This is a function which is invoking LLM with System Message and MessageState. LLM will update the MessageState and return it as the response.
## ToolNode
It is a prebuilt callable which runs the tools the LLM requested.
# MessageState
Think of MessagesState as the conversation transcript that all nodes share. Each node reads the transcript, does its job, and adds to it — LangGraph handles the merging.
It is the shared state schema for chat-style agents. Its key is "messages" and value is a list of Messages which can be one more combination of HumanMessage, AIMessage and ToolMessage.
When a node returns:
return {"messages": [response]}
LangGraph doesn’t replace the whole list. It appends (or intelligently merges) into the existing messages list. That’s how conversation history builds up across the ReAct loop.
# Steps
1. Node my_agent_reason is the entry point. So Langraph first calls run_agent_reason(state) Its input is the MessageState with only HumanMessage - "What is the weaather in Tokyo? List it and then triple it"
2. This node (my_agent_reason) invokes LLM. With SystemMessage ("You are a helpful assistant that can use tools to answer questions"). Remember this LLM is already having binding of the tools - TavilySearch and Triple.
3. LLM updates the MessageState and appends its response to existing message. It will append MessageState with AIMessage with the tool call of tavily_search("current weather in Tokyo")
4. As per our langraph if MessageState last message is a tool call, then LangGraph should invoke ToolNode. So next LangGraph calls tool_node.invoke(state)it moves to the node ToolNode(tools). ToolNode compare the tool that it has with the MessageState and since last message is asking to invoke TavliySearch, it will invoke TavlilySearch and update the MessageState with ToolMessage which is basically Search Ouput.
5. As per our langraph after call to ToolNode, it should call my_agent_reason. Now when it calls my_agent_reason, its MessageState will also include ToolMessage (Search result). So now when it will invoke LLM, LLM will update the StateMessage with tool call suggestion for triple.
6. As per our langraph if MessageState last message is a tool call, then LangGraph should invoke ToolNode. So next LangGraph calls tool_node.invoke(state)it moves to the node ToolNode(tools). ToolNode compare the tool that it has with the MessageState and since last message is asking to invoke Triple, it will invoke Tiple and update the MessageState with ToolMessage which is basically a number which is the triple of current temperature.
7. As per our langraph after call to ToolNode, it should call my_agent_reason. Now when it calls my_agent_reason, its MessageState will also have ToolMessage (Final result after tripling the temperatue). So now when it will invoke LLM, LLM will update the StateMessage with final result by paraphrasing the respone.
8. Since now there is no tool call so this will call END.