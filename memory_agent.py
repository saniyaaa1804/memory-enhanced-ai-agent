
from langchain_ollama import ChatOllama
from memory import MemoryManager
from tools import execute_tool


class MemoryAgent:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0.3
        )

        self.memory = MemoryManager()
        self.activity_log = []

    def generate_response(self, prompt):
        response = self.llm.invoke(prompt)
        return response.content

    def run(self, user_input, use_memory=True):

        self.activity_log = []
        tool_name = None
        tool_result = None
        retrieved_memories = []

        # STEP 1: Check short-term memory
        if use_memory:
            conversation = self.memory.get_short_term_memory()

            if conversation:
                self.activity_log.append(
                    "Short-term memory: Previous conversation loaded."
                )
            else:
                self.activity_log.append(
                    "Short-term memory: No previous messages."
                )

            # STEP 2: Retrieve long-term memory
            retrieved_memories = self.memory.search_long_term(
                user_input,
                k=3
            )

            if retrieved_memories:
                self.activity_log.append(
                    "Long-term memory: Relevant information retrieved."
                )
            else:
                self.activity_log.append(
                    "Long-term memory: No relevant information found."
                )

        # STEP 3: Check whether a tool is required
        tool_name, tool_result = execute_tool(user_input)

        if tool_name:
            self.activity_log.append(
                f"Tool executed: {tool_name}"
            )
        else:
            self.activity_log.append(
                "Tool execution: No external tool requested."
            )

        # STEP 4: Prepare context
        context = ""

        if use_memory:

            for item in self.memory.get_short_term_memory():
                context += (
                    f"{item['role']}: {item['message']}\n"
                )

            if retrieved_memories:
                context += "\nRelevant long-term memories:\n"

                for item in retrieved_memories:
                    context += f"- {item}\n"

        if tool_result:
            context += (
                f"\nTool used: {tool_name}\n"
                f"Tool result: {tool_result}\n"
            )

        prompt = f"""
You are a helpful AI agent with memory and tools.

Use the available conversation context and retrieved memories
when they are relevant.

If a tool result is provided, explain its result accurately.
Do not invent search results or claim that a tool was used
when no tool result is available.

Conversation and memory context:
{context}

Current user message:
{user_input}

Provide a clear and useful response.
"""

        # STEP 5: Generate response
        answer = self.generate_response(prompt)

        # STEP 6: Update memory
        if use_memory:
            self.memory.add_to_short_term("user", user_input)
            self.memory.add_to_short_term("assistant", answer)

            self.memory.add_to_long_term(
                f"User message: {user_input}\nAssistant response: {answer}"
            )

            self.activity_log.append(
                "Memory updated: Conversation saved to long-term storage."
            )

        return {
            "answer": answer,
            "tool_name": tool_name,
            "tool_result": tool_result,
            "retrieved_memories": retrieved_memories,
            "activity_log": self.activity_log
        }
