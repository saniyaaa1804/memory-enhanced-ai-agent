
import streamlit as st
from agent import create_agent


st.set_page_config(
    page_title="Memory-Enhanced AI Agent",
    page_icon="",
    layout="wide"
)

st.title("Memory-Enhanced AI Agent")
st.caption("Unit III: Memory, Tools, and Environment Interaction")

# Initialize agent
if "agent" not in st.session_state:
    with st.spinner("Initializing AI agent and memory database..."):
        st.session_state.agent = create_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

agent = st.session_state.agent

# Sidebar
with st.sidebar:
    st.header("Agent Controls")

    compare_mode = st.checkbox(
        "Compare with memoryless agent",
        value=False
    )

    st.divider()

    st.subheader("Memory Status")

    st.write(
        f"Short-term messages: "
        f"{len(agent.memory.get_short_term_memory())}"
    )

    st.write(
        f"Stored long-term memories: "
        f"{len(agent.memory.get_all_recent_memories())}"
    )

    if st.button("Clear Short-Term Memory"):
        agent.memory.clear_short_term()
        st.session_state.messages = []
        st.success("Short-term memory cleared.")
        st.rerun()

    if st.button("Show Stored Memories"):
        memories = agent.memory.get_all_recent_memories()

        if memories:
            for index, item in enumerate(memories, 1):
                st.write(f"{index}. {item}")
        else:
            st.info("No stored memories found.")

    st.divider()

    st.subheader("Available Tools")

    st.write("1. Web Search")
    st.write("2. Calculator")

    st.caption("Use search: or calculate: to activate a tool.")

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Enter your message...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Agent is processing your request..."):

            try:
                result = agent.run(
                    user_input,
                    use_memory=True
                )

                st.markdown(result["answer"])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"]
                })

                with st.expander("Agent Activity Log"):
                    for activity in result["activity_log"]:
                        st.write("- " + activity)

                if result["tool_result"]:
                    with st.expander("Tool Execution Result"):
                        st.write("Tool:", result["tool_name"])
                        st.write(result["tool_result"])

                if result["retrieved_memories"]:
                    with st.expander("Retrieved Long-Term Memories"):
                        for item in result["retrieved_memories"]:
                            st.write("- " + item)

                # Memoryless comparison
                if compare_mode:

                    st.divider()
                    st.subheader("Memoryless Agent Comparison")

                    with st.spinner("Running memoryless baseline..."):
                        baseline = agent.run(
                            user_input,
                            use_memory=False
                        )

                    st.markdown("**Memoryless Agent Response**")
                    st.write(baseline["answer"])

                    st.caption(
                        "The baseline uses the same model and tool router "
                        "but receives no stored conversation context and "
                        "does not read or update memory."
                    )

            except Exception as error:
                st.error(f"Agent error: {str(error)}")
