# groq_chat_env.py
import os
import requests
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("🤖 Groq API Chatbot")
print("=" * 50)

# Get API key from .env
#api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found in .env file!")
    print("\nAdd this to your .env file:")
    print("GROQ_API_KEY=your_groq_api_key_here")
    print("\nGet free key from: https://console.groq.com/keys")
    exit()

print(f"✅ API Key loaded from .env")
print("Initializing...")

# API configuration
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Available Groq models (all free tier)
GROQ_MODELS = [
    "llama-3.1-8b-instant",       # Fastest, good for chat
    "llama-3.3-70b-versatile",    # Most powerful
    "llama-3.2-3b-preview",       # Lightweight
    "mixtral-8x7b-32768",         # Good for coding
    "gemma2-9b-it",               # Google's model
]

# Test which models work
working_models = []
print("\n🔍 Testing available models...")

for model in GROQ_MODELS:
    try:
        test_data = {
            "model": model,
            "messages": [{"role": "user", "content": "Say 'ready'"}],
            "max_tokens": 5,
            "temperature": 0.1
        }
        
        response = requests.post(url, headers=headers, json=test_data, timeout=10)
        
        if response.status_code == 200:
            working_models.append(model)
            print(f"  ✓ {model}")
        else:
            print(f"  ✗ {model} (Error {response.status_code})")
            
    except Exception as e:
        print(f"  ✗ {model} ({str(e)[:30]}...)")

if not working_models:
    print("\n❌ No models available!")
    print("Check your API key and try again.")
    exit()

print(f"\n✅ {len(working_models)} models available")

# Let user choose model
print("\nAvailable models:")
for i, model in enumerate(working_models, 1):
    print(f"{i}. {model}")

try:
    choice = input(f"\nChoose model (1-{len(working_models)}): ").strip()
    selected_model = working_models[int(choice) - 1]
except:
    selected_model = working_models[0]  # Use first available

print(f"\n🎯 Selected: {selected_model}")

# System message for chatbot
system_message = """You are a helpful AI assistant. Provide concise, accurate, and friendly responses.
If you don't know something, be honest about it."""

# Initialize messages
messages = [
    {"role": "system", "content": system_message}
]

print("\n✅ Chatbot ready!")
print("💬 Type your messages")
print("📝 Type 'clear' to reset conversation")
print("🔄 Type 'model' to switch models")
print("🚪 Type 'quit' to exit")
print("-" * 50)

# Chat loop
def chat_loop(model_name):
    current_messages = messages.copy()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("\n🤖 Goodbye! 👋")
                return 'quit'
            
            if user_input.lower() == 'clear':
                current_messages = [messages[0]]  # Reset to system message
                print("🤖 Conversation cleared!")
                continue
            
            if user_input.lower() == 'model':
                return 'change_model'  # Signal to change model
            
            if not user_input:
                print("🤖 Please enter a message.")
                continue
            
            # Add user message
            current_messages.append({"role": "user", "content": user_input})
            
            # Prepare request
            data = {
                "model": model_name,
                "messages": current_messages,
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": False
            }
            
            print("🤖 Thinking...", end="", flush=True)
            
            # Send request
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                reply = result['choices'][0]['message']['content']
                
                # Add assistant reply
                current_messages.append({"role": "assistant", "content": reply})
                
                # Keep conversation manageable (last 10 exchanges + system)
                if len(current_messages) > 21:  # 1 system + 10 user-assistant pairs
                    current_messages = [current_messages[0]] + current_messages[-20:]
                
                print(f"\r🤖: {reply}")
                
            elif response.status_code == 429:
                print("\r🤖 Rate limited. Waiting 2 seconds...")
                import time
                time.sleep(2)
                current_messages.pop()  # Remove the user message
                continue
                
            else:
                error_msg = f"API Error {response.status_code}"
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        error_msg += f": {error_data['error'].get('message', 'Unknown error')}"
                except:
                    error_msg += f": {response.text[:100]}"
                
                print(f"\r❌ {error_msg}")
                current_messages.pop()  # Remove failed user message
                
        except requests.exceptions.Timeout:
            print("\r🤖 Request timeout. Please try again.")
            if len(current_messages) > 1:
                current_messages.pop()
        except KeyboardInterrupt:
            print("\n\n🤖 Goodbye! 👋")
            return 'quit'
        except Exception as e:
            print(f"\r❌ Error: {str(e)[:100]}")
            if len(current_messages) > 1:
                current_messages.pop()

# Start chat loop
result = chat_loop(selected_model)

# Handle model switching
while result == 'change_model':
    print("\n📋 Available models:")
    for i, model in enumerate(working_models, 1):
        print(f"{i}. {model}")
    
    try:
        choice = input(f"\nChoose new model (1-{len(working_models)}): ").strip()
        selected_model = working_models[int(choice) - 1]
        print(f"\n🔄 Switched to: {selected_model}")
        result = chat_loop(selected_model)
    except:
        print("❌ Invalid choice. Keeping current model.")
        result = chat_loop(selected_model)