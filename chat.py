
"""
Language Chain Chatbot Script

This Python script implements a chatbot using OpenAI's GPT-4 language model through the `langchain` library. The chatbot provides an interactive conversational experience with users in the terminal.

Key Features:
- Utilizes GPT-4 for natural language understanding and generation.
- Implements a colored terminal output for a visually appealing chat interface.
- Manages conversation history and saves it to a JSON file (`conversation.json`).
- Enables an interactive conversation loop with user input.

Instructions:
1. Ensure you have the required dependencies installed using pipenv.
2. Run the script to start the chatbot.
3. Input messages during the interactive conversation.
4. Type "exit" to end the conversation and save the chat history.

Dependencies:
- langchain (version with GPT-4 support)
- OpenAI GPT-4
- Python (version 3.x)

Note: Make sure to replace the GPT-4 model name in the script if needed. The conversation history is saved to `conversation.json`.

Author: Cleiton Levinski
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

GPT_MODEL = "gpt-4-1106-preview"

class ColorStreamingHandler(StreamingStdOutCallbackHandler):

    stream_started = True

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        data = f"\nAI: {token}" if self.stream_started else token
        sys.stdout.write(f"\033[34m{data}")
        sys.stdout.flush()
        self.stream_started = False

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        sys.stdout.write(f"\n")
        sys.stdout.flush()
        self.stream_started = True

# LLM
llm = ChatOpenAI(model=GPT_MODEL, streaming=True, callbacks=[ColorStreamingHandler()])

# Prompt
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a nice chatbot having a conversation with a human."
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

# Notice that `"chat_history"` aligns with the MessagesPlaceholder name
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

conversation_file_path = "./conversation.json"

try:
    # Specify the file path (you can change this to your desired file path)
    with open(conversation_file_path, "r") as file:
        file_content = file.read()
        messages = json.loads(file_content)

    # if messages exist
    if messages:        
        for message in messages:
            dict_key = [key for key in message][0]
            dict_value = message[dict_key]
            memory.chat_memory.add_user_message(dict_value) if dict_key == 'user' else memory.chat_memory.add_ai_message(dict_value)
except FileNotFoundError:
    print(f'The file "{conversation_file_path}" does not exist. We will create one')
except Exception as e:
    print(e)

# Load conversation chain
conversation = LLMChain(llm=llm, prompt=prompt, verbose=False, memory=memory)

# Notice that we just pass in the `question` variables - `chat_history` gets populated by memory
conv = True

while conv:
    user_input = input("\033[32mYou: ")

    if user_input == "exit":
        conv = False
    
    conversation({"question": user_input})

chat_history = []

memory_chat = memory.chat_memory.dict()['messages']

for chat in memory_chat:
    chat_type = chat['type'] if chat['type'] == 'ai' else 'user'
    message = { chat_type : chat['content']}
    chat_history.append(message)

# Open the file in write mode (if the file doesn't exist, it will be created)
with open(conversation_file_path, "w") as file:
    file.write(json.dumps(chat_history))