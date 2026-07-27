from core.llm import chat_model


class TitleService:

    @staticmethod
    def generate_title(first_message: str):

        prompt = f"""
Generate a short chat title.

Rules:

- Maximum 6 words

- No quotes

- No punctuation

Conversation:

{first_message}
"""

        return (
            chat_model
            .invoke(prompt)
            .content
            .strip()
        )