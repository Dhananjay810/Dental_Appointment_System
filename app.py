import streamlit as st
from langchain_core.messages import HumanMessage, AIMessageChunk
from dental_agent.workflows.graph import dental_graph

st.set_page_config(page_title="Dental Appointment System", page_icon="🦷")
st.title("🦷 Dental Appointment System")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Accept user input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Stream events from the LangGraph workflow
            for event_type, data in dental_graph.stream(
                {"messages": st.session_state.messages},
                stream_mode=["messages", "values"],
                config={"recursion_limit": 20},
            ):
                if event_type == "messages":
                    chunk, meta = data
                    
                    # Ignore internal supervisor routing tokens
                    if meta.get("langgraph_node", "") == "supervisor":
                        continue

                    # Stream tokens only from the agent (not tool results)
                    if isinstance(chunk, AIMessageChunk) and chunk.content and not getattr(chunk, "tool_calls", None):
                        text_content = ""
                        if isinstance(chunk.content, str):
                            text_content = chunk.content
                        elif isinstance(chunk.content, list):
                            for block in chunk.content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    text_content += block.get("text", "")
                                elif isinstance(block, str):
                                    text_content += block
                        
                        # Suppress JSON outputs
                        if text_content and not text_content.strip().startswith("{"):
                            full_response += text_content
                            message_placeholder.markdown(full_response + "▌")
                            
                elif event_type == "values":
                    final_messages = data.get("messages", [])
                    if final_messages:
                        st.session_state.messages = final_messages
                        
            message_placeholder.markdown(full_response)
            
        except Exception as exc:
            st.error(f"Error: {exc}")
            st.session_state.messages.pop() # Remove failed message
