from openai import OpenAI

from app.config import settings


class OpenApiService:
    def __init__(self) -> None:
        # Initialize the OpenAI client with settings from the config
        self.client = OpenAI(
            organization=settings.OPENAI_API_ORGANIZATION,
            project=settings.OPENAI_API_PROJECT_NAME,
        )

    def prompt_chatgpt(self, prompt: str, model: str = "gpt-4o-mini") -> str | None:
        """
        Sends a message to OpenAI's ChatGPT and retrieves the response.

        Args:
            prompt (str): The message content to send to ChatGPT.
            model (str): The model to use for the response, default is "gpt-4o-mini".

        Returns:
            str: The response from ChatGPT.
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model,
            )

            return response.choices[0].message["content"] if response.choices else None

        except Exception as e:
            print(f"Failed to send prompt to OpenAI: {e}")
            return None
