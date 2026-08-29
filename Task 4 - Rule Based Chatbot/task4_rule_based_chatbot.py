"""
Task 4: Production-Ready Multi-Intent Rule-Based Chatbot
Progree Internship

Features:
- terminal conversational loop
- case/punctuation/whitespace normalization
- nested if/elif/else state logic
- function dictionary intent routing
- multiple help trees
- session state
- graceful fallback/error handling
"""

import re


class RuleBasedChatbot:
    """Stateful terminal chatbot with rule-based intent routing."""

    def __init__(self):
        self.running = True
        self.state = "main"
        self.session = {
            "name": None,
            "topic": None,
            "last_intent": None,
            "messages": 0,
        }

        # Function dictionary: intent -> handler.
        self.intent_handlers = {
            "greeting": self.handle_greeting,
            "help": self.handle_help,
            "status": self.handle_status,
            "account": self.handle_account,
            "technical": self.handle_technical,
            "billing": self.handle_billing,
            "contact": self.handle_contact,
            "goodbye": self.handle_goodbye,
        }

    @staticmethod
    def normalize_text(text):
        """Trim, lowercase, strip punctuation, and normalize whitespace."""
        text = text.strip().lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return re.sub(r"\s+", " ", text)

    @staticmethod
    def contains_keyword(tokens, keywords):
        """Match complete words rather than accidental substrings."""
        return bool(set(tokens) & set(keywords))

    def detect_intent(self, text):
        """Detect an intent using state-aware nested rules."""
        normalized = self.normalize_text(text)

        if not normalized:
            return "empty"

        tokens = normalized.split()

        # Nested state logic for the help tree.
        if self.state == "help":
            if self.contains_keyword(tokens, {"account", "profile", "login"}):
                return "account"
            elif self.contains_keyword(tokens, {"technical", "bug", "error", "password"}):
                return "technical"
            elif self.contains_keyword(tokens, {"billing", "payment", "invoice", "charge"}):
                return "billing"
            elif self.contains_keyword(tokens, {"contact", "support", "human"}):
                return "contact"
            elif normalized in {"back", "main", "menu"}:
                return "main_menu"

        # Main conversational routing.
        if self.contains_keyword(tokens, {"hello", "hi", "hey"}):
            return "greeting"
        elif "help" in tokens or "menu" in tokens:
            return "help"
        elif "status" in tokens or "state" in tokens:
            return "status"
        elif self.contains_keyword(tokens, {"account", "profile", "login"}):
            return "account"
        elif self.contains_keyword(tokens, {"technical", "bug", "error", "password"}):
            return "technical"
        elif self.contains_keyword(tokens, {"billing", "payment", "invoice", "charge"}):
            return "billing"
        elif self.contains_keyword(tokens, {"contact", "support", "human"}):
            return "contact"
        elif self.contains_keyword(tokens, {"bye", "goodbye", "exit", "quit"}):
            return "goodbye"
        else:
            return "fallback"

    def route(self, intent):
        """Route an intent through the handler dictionary."""
        if intent == "main_menu":
            self.state = "main"
            return self.handle_help()

        handler = self.intent_handlers.get(intent, self.handle_fallback)
        self.session["last_intent"] = intent
        return handler()

    # ----- Intent handlers -----

    def handle_greeting(self):
        if self.session["name"]:
            return f"Hello again, {self.session['name']}! How can I help?"
        return "Hello! I'm ProgreeBot. What's your name, or type 'help' to see the menu."

    def handle_help(self):
        self.state = "help"
        return (
            "Help menu:\n"
            "  1. Account   - login, profile, account questions\n"
            "  2. Technical - errors, bugs, password problems\n"
            "  3. Billing   - payments, invoices, charges\n"
            "  4. Contact   - speak to support\n"
            "Type a topic, or type 'back' to return to the main flow."
        )

    def handle_status(self):
        return (
            f"Session status: state={self.state}, "
            f"messages={self.session['messages']}, "
            f"last_intent={self.session['last_intent'] or 'none'}."
        )

    def handle_account(self):
        self.state = "account"
        self.session["topic"] = "account"
        return (
            "Account help: I can guide you with login or profile questions. "
            "For security, do not share passwords or private credentials here."
        )

    def handle_technical(self):
        self.state = "technical"
        self.session["topic"] = "technical"
        return (
            "Technical help: describe the general error or problem. "
            "I can suggest basic troubleshooting steps."
        )

    def handle_billing(self):
        self.state = "billing"
        self.session["topic"] = "billing"
        return (
            "Billing help: I can explain general payment, invoice, or charge "
            "questions. Do not share card numbers or other sensitive details."
        )

    def handle_contact(self):
        self.state = "contact"
        self.session["topic"] = "contact"
        return "Support contact flow selected. Please provide a general description of your issue."

    def handle_goodbye(self):
        self.running = False
        return "Goodbye! Thanks for testing ProgreeBot."

    def handle_fallback(self):
        self.state = "fallback"
        return (
            "Sorry, I didn't understand that request. "
            "Try 'help' for the available topics, or 'status' to inspect the session."
        )

    def process(self, user_input):
        """Process one user message and return a bot response."""
        self.session["messages"] += 1

        normalized = self.normalize_text(user_input)

        # Capture a simple name statement.
        if normalized.startswith("my name is "):
            name = normalized.replace("my name is ", "", 1).strip()
            if name and len(name.split()) <= 3:
                self.session["name"] = name.title()
                self.state = "main"
                return f"Nice to meet you, {self.session['name']}!"

        intent = self.detect_intent(user_input)

        if intent == "empty":
            return "Please enter a message. Type 'help' if you need the available options."

        if intent == "fallback":
            return self.handle_fallback()

        return self.route(intent)

    def run(self):
        """Run the interactive terminal conversation loop."""
        print("=" * 62)
        print("PROGREEBOT - MULTI-INTENT RULE-BASED CHATBOT")
        print("=" * 62)
        print("Type 'help' for topics, 'status' for session state, or 'bye' to exit.")

        while self.running:
            try:
                user_input = input("\nYou: ")
                response = self.process(user_input)
                print(f"Bot: {response}")
            except (KeyboardInterrupt, EOFError):
                print("\nBot: Session ended safely. Goodbye!")
                self.running = False
            except Exception:
                print("Bot: I encountered an unexpected input error. Please try again.")


def demo():
    """Run deterministic examples without requiring manual input."""
    bot = RuleBasedChatbot()

    test_inputs = [
        "  HELLO!!! ",
        "my name is Alex",
        "HELP",
        "billing",
        "What is my status?",
        "something completely unknown",
        "bye",
    ]

    print("\n--- Automated Demo Tests ---")
    for message in test_inputs:
        if not bot.running:
            break
        response = bot.process(message)
        print(f"You: {message}")
        print(f"Bot: {response}")


def main():
    demo()
    print("\n--- Interactive Terminal Mode ---")
    bot = RuleBasedChatbot()
    bot.run()


if __name__ == "__main__":
    main()
