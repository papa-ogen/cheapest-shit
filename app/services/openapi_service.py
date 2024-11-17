import numpy as np
from openai import OpenAI

from app.config import settings


class OpenApiService:
    def __init__(self) -> None:
        self.client = OpenAI(
            organization=settings.OPENAI_API_ORGANIZATION,
            project=settings.OPENAI_API_PROJECT_NAME,
        )

    def generate_product_vector(self, text_input: str) -> np.ndarray:
        """
        Generates a vector representation of a product, using an embedding model.
        """

        try:
            vector = (
                self.client.embeddings.create(
                    input=[text_input],
                    model="text-embedding-3-small",
                )
                .data[0]
                .embedding
            )
            # Extract the vector from the response
            return np.array(vector)
        except Exception as e:
            print(f"Error generating vector: {e}")
            raise
