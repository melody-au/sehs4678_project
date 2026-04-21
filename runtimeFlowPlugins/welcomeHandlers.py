"""Welcome/menu flow plugin.

This handler acts as the router after login. It responds to main-menu intents
and hands off to encouragement, quiz, or chat flows.
"""

import runtimeFlowPlugins
from .encouragementGenerator import encouragement_switch

# Centralized main menu message for consistent UX across all return-to-menu flows.
MAIN_MENU_WELCOME_MESSAGE = (
    "Welcome to the main menu! You can ask for encouragement, take a quiz, or chat with me! "
    "What would you like to do?"
)

# Transition message shown when a handler is returning to main menu.
RETURN_TO_MENU_MESSAGE = "Returning to main menu."


def get_main_menu_message() -> str:
    """Return the standard main menu welcome message for consistent UX."""
    return MAIN_MENU_WELCOME_MESSAGE


def get_return_to_menu_message() -> str:
    """Return the transition message shown before returning to main menu."""
    return RETURN_TO_MENU_MESSAGE

@runtimeFlowPlugins.register("WelcomeHandler")
def welcome_handler(state, meta, inputText, predictedIntent):
    """Route menu-level intents and return standardized flow outcomes."""
    #defaults: 
    nextHandler = "WelcomeHandler"
    nextResponse = ""
    nextState = state
    nextMeta = meta

    # intent points to different flows:
    # encouragement -> call encouragement for a encouragement response and then come back
    # quiz -> call and hand off to quiz flow, and then come back to main menu after quiz is done
    # chat -> call and hand off to chat flow, and then come back to main menu after user says they want to exit the chat
    # capture any handoffs and do not handoff from here unless it is from a success state after this intent has handled once 
    if state == "passoff":
        nextResponse = "Welcome to the main menu! You can ask for encouragement, take a quiz, or chat with me! What would you like to do? Or if you want to end our conversation, just type 'exit'."
        nextState = "success"
        return {"response": nextResponse, "next_handler": nextHandler, "next_state": nextState, "meta_update": nextMeta}
    
    if state == "return_to_menu": #global catch-all state to return to main menu
        return {
            "response": "",
            "next_handler": "WelcomeHandler",
            "next_state": "passoff", 
            "meta_update": meta
        }
        
    if state == "confirming_exit":
        user_reply = inputText.strip().lower()
        if user_reply == "yes":
            return {"response": "See you later!", "next_handler": "LoginHandler", "next_state": "start", "meta_update": {"username": None}}
        elif user_reply == "no":
            nextResponse = "Welcome to the main menu! You can ask for encouragement, take a quiz, or chat with me! What would you like to do? Or if you want to end our conversation, just type 'exit'."
            return {"response": nextResponse, "next_handler": nextHandler, "next_state": "success", "meta_update": nextMeta}
        else:
            return {"response": "Please type 'yes' to confirm or 'no' to cancel.", "next_handler": nextHandler, "next_state": "confirming_exit", "meta_update": nextMeta}

    if state == "success":
        if predictedIntent == "exit":
            return {
                "response": "Are you sure you want to end our conversation? (Type 'yes' to confirm, 'no' to cancel)",
                "next_handler": nextHandler,
                "next_state": "confirming_exit",
                "meta_update": nextMeta
            }

    if predictedIntent == "encouragement":
        nextResponse = encouragement_switch("any")
    elif predictedIntent == "quiz":
        nextHandler = "QuizHandler"
        nextState = "passoff"
    elif predictedIntent == "chat":
        nextHandler = "ChatHandler"
        nextState = "passoff"
    else:
        nextResponse = get_main_menu_message()
        nextState = "success"
    return {"response": nextResponse, "next_handler": nextHandler, "next_state": nextState, "meta_update": nextMeta}
