"""
GPT-4 Enhanced Chatbot Script

This Python script showcases an advanced chatbot leveraging OpenAI's GPT-4 language model through the `langchain` library. Designed to provide an immersive conversational experience, the chatbot comes with a range of features.

🌟 Key Features:
- Harnesses the power of GPT-4 for seamless natural language understanding and generation.
- Implements a vibrant and visually appealing chat interface with colored terminal output.
- Manages and persists conversation history, storing it in a user-friendly JSON format (`conversation.json`).
- Facilitates an interactive conversation loop, engaging users with personalized prompts.

🚀 How to Use:
1. Ensure dependencies are installed using pipenv.
2. Run the script to launch the GPT-4 chatbot.
3. Enter messages during the interactive conversation.
4. Type "exit" to gracefully conclude the conversation and save the chat history.

📦 Dependencies:
- langchain (Ensure it supports GPT-4)
- OpenAI GPT-4
- Python (version 3.x)

👨‍💻 Author: Cleiton Levinski
"""
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from typing import Any, Dict, List
from langchain.schema import LLMResult
import json
import sys

# GPT-4 model configuration
GPT_MODEL = "gpt-4-1106-preview"

class ColorStreamingHandler(StreamingStdOutCallbackHandler):
    """
    Custom callback handler for streaming GPT-4 output with colored formatting.
    """

    stream_started = True  # Flag to track the beginning of the stream

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """
        Callback triggered for each new token generated by GPT-4.
        """
        data = f"\nAI: {token}" if self.stream_started else token
        sys.stdout.write(f"\033[34m{data}")  # Colored output in blue
        sys.stdout.flush()
        self.stream_started = False

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """
        Callback triggered when GPT-4 processing ends.
        """
        sys.stdout.write(f"\n")
        sys.stdout.flush()
        self.stream_started = True

# Language Model (LLM) initialization
llm = ChatOpenAI(model=GPT_MODEL, streaming=True, callbacks=[ColorStreamingHandler()])

# Prompt configuration
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a nice chatbot having a conversation with a human."
        ),
        # The `variable_name` here aligns with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

# Conversation memory initialization
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Load conversation history from file
conversation_file_path = "./conversation.json"
try:
    with open(conversation_file_path, "r") as file:
        file_content = file.read()
        messages = json.loads(file_content)

    # If messages exist, add them to the conversation memory
    if messages:
        for message in messages:
            dict_key = [key for key in message][0]
            dict_value = message[dict_key]
            if dict_key == 'user':
                memory.chat_memory.add_user_message(dict_value)
            else:
                memory.chat_memory.add_ai_message(dict_value)
except FileNotFoundError:
    print(f'The file "{conversation_file_path}" does not exist. A new one will be created.')
except Exception as e:
    print(e)

# Conversation chain initialization
conversation = LLMChain(llm=llm, prompt=prompt, verbose=False, memory=memory)

# Interactive conversation loop
conv = True
while conv:
    user_input = input("\n\033[32mYou: ")

    if user_input == "exit":
        conv = False

    conversation({"question": user_input})

# Extract chat history
chat_history = []
memory_chat = memory.chat_memory.dict()['messages']
for chat in memory_chat:
    chat_type = chat['type'] if chat['type'] == 'ai' else 'user'
    message = {chat_type: chat['content']}
    chat_history.append(message)

# Save conversation history to file
with open(conversation_file_path, "w") as file:
    file.write(json.dumps(chat_history))
