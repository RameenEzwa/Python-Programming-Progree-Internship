# Task 4 - Production-Ready Multi-Intent Rule-Based Chatbot

**Progree Internship**

## Objective
Build an advanced text-driven terminal conversational bot agent handling modular flows.

## Requirements Covered

- Complex terminal conversational application loop
- Natural-language text normalization:
  - case conversion
  - character/punctuation stripping
  - whitespace normalization
- Nested `if/elif/else` state logic
- Function dictionary mapping for intent routing
- Multiple help trees:
  - Account
  - Technical
  - Billing
  - Contact
- Session state variations
- Graceful fallback and error messages
- Automated deterministic demonstration tests

## Files

- `task4_rule_based_chatbot.py` - main Python application
- `README.md` - documentation
- `Task_4_Chatbot_Submission.pdf` - report/evidence

## Run

With Python 3 installed:

```bash
python task4_rule_based_chatbot.py
```

The program first runs an automated demo and then starts interactive terminal mode.

## Example inputs

```text
HELLO!!!
my name is Alex
help
billing
status
something completely unknown
bye
```

## Design

The `RuleBasedChatbot` class stores session data in a dictionary.
The `intent_handlers` dictionary maps intent names to handler functions.
`detect_intent()` uses nested state-aware `if/elif/else` rules. The
normalization function prevents case and punctuation differences from
breaking intent matching.

Keyword matching uses complete tokens rather than substring matching,
so a word such as `this` is not accidentally interpreted as the greeting
keyword `hi`.

## Safety / privacy note

The bot is designed for general demonstrations. Users should not enter
passwords, payment-card numbers, or other sensitive credentials.
