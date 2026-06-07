import os
import re
from collections import deque

# --- CONFIGURE YOUR BOT'S PERSONALITY HERE ---
BOT_NAME = "Jarvis"
GREETINGS = ["hi", "hello", "hey, what's up", "greetings, bro", "good morning", "good afternoon, my nigga", "what's up", "yo, broskie"]
FAREWELLS = ["bye", "see ya", "don't come back", "later..", "good luck broskie"]
# --- END CONFIGURATION ---

def normalize_text(text):
    """Convert to lowercase and remove punctuation for matching"""
    return re.sub(r'[^\w\s]', '', text.lower()).strip()

def get_response(user_input, history):
    """Generate a response based on input and conversation history"""
    normalized = normalize_text(user_input)

    # Check for greetings
    if any(greet in normalized for greet in GREETINGS):
        if len(history) == 0:  # First interaction
            return f"👋 Hello! I'm {BOT_NAME}. How can I help you today?"
        return f"Hey again! Still here to help. What do you need?"

    # Check for farewells
    if any(farewell in normalized for farewell in FAREWELLS):
        return "👋 Goodbye! Have a productive day. Come back anytime."

    # Check for simple commands (keeping your original functionality)
    if "organize" in normalized and "download" in normalized:
        return "📁 I can help organize your Downloads folder! (Say 'organize downloads' to try it)"
    if "test" in normalized and "file" in normalized:
        return "📝 I made a test file on your Desktop earlier. Want me to make another?"

    # Context-aware responses (uses last 2 messages)
    if len(history) >= 1:
        last_user = normalize_text(history[-1][0]) if history else ""
        if "how" in last_user and "you" in last_user:
            return "I'm doing great! Ready to help you with tasks on your laptop."
        if "thank" in last_user or "thanks" in last_user:
            return "You're very welcome! Happy to assist."

    # Smart fallback
    if len(normalized) < 3:
        return "Could you say that again? I'm here to help!"
    return f"Interesting! You said: '{user_input}'. I'm still learning — try asking me to organize files or make a test file."

def chat_loop():
    """Main conversation loop with memory"""
    print("\n" + "="*50)
    print(f"  🤖 {BOT_NAME} is online! Type 'bye' to exit.")
    print("  Try: 'hi', 'organize downloads', 'make test file'")
    print("="*50 + "\n")

    history = deque(maxlen=2)  # Remember last 2 exchanges

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        # Add to history (we store tuples of (user, bot) but only need user for context)
        history.append((user_input, ""))

        # Get bot response
        bot_response = get_response(user_input, [h[0] for h in history])

        # Update history with actual bot response
        history[-1] = (history[-1][0], bot_response)

        print(f"\n{BOT_NAME}: {bot_response}\n")

        # Check for exit
        if any(farewell in normalize_text(user_input) for farewell in FAREWELLS):
            break

if __name__ == "__main__":
    chat_loop()