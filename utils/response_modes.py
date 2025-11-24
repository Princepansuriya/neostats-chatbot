# utils/response_modes.py

def apply_response_mode(response: str, mode: str) -> str:
    """
    Adjusts the chatbot response depending on the selected response mode.
    Modes:
        - concise: short summary
        - detailed: expanded explanation
    """

    try:
        if mode == "concise":
            return concise_response(response)

        elif mode == "detailed":
            return detailed_response(response)

        else:
            return response

    except Exception as e:
        return f"[Response Mode Error] {str(e)}"


def concise_response(text: str) -> str:
    """Return a short 2–3 sentence summary."""

    # Simple rule-based summary (you can improve later)
    sentences = text.split(".")
    summary = ". ".join(sentences[:2]).strip()

    return summary + "..." if summary else text


def detailed_response(text: str) -> str:
    """Expands the answer by adding clarity and additional explanation."""

    expanded = (
        f"{text}\n\n"
        "Here is a more detailed explanation:\n"
        "- The above answer is elaborated for clarity.\n"
        "- Additional context is added to help deeper understanding.\n"
        "- If needed, the chatbot can further break down concepts."
    )

    return expanded
