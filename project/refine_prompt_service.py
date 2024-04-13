from typing import Dict

import openai
from pydantic import BaseModel


class RefinePromptResponse(BaseModel):
    """
    Contains the refined version of the user's prompt after processing through GPT-4, along with any pertinent metadata.
    """

    original_prompt: str
    refined_prompt: str
    refinement_metadata: Dict[str, str]


openai.api_key = "your-api-key-here"


def refine_prompt(user_prompt: str) -> RefinePromptResponse:
    """
    Accepts a prompt and returns the refined version from GPT-4.

    Args:
        user_prompt (str): The original user provided prompt that needs to be refined. This field is the primary input for the GPT-4 processing.

    Returns:
        RefinePromptResponse: Contains the refined version of the user's prompt after processing through GPT-4, along with any pertinent metadata.

    Example:
        refined_prompt = refine_prompt("Write a prompt for an AI that uses natural language processing.")
        print(refined_prompt.refined_prompt)
    """
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=user_prompt, max_tokens=100, temperature=0.7
    )  # TODO(autogpt): "Completion" is not a known member of module "openai". reportAttributeAccessIssue
    #   Found doccumentation for the module:
    #    To fix the error `"Completion" is not a known member of module "openai".`, you should use `openai.ChatCompletion` instead of `openai.Completion` when creating a chat completion.
    #
    #   According to the documentation, the correct usage is:
    #
    #   ```python
    #   chat_completion = client.chat.completions.create(
    #       messages=[
    #           {
    #               "role": "user",
    #               "content": "Say this is a test",
    #           }
    #       ],
    #       model="gpt-3.5-turbo",
    #   )
    #   ```
    #
    #   The `openai` module provides a `ChatCompletion` class for chat completions, not a `Completion` class.
    refined_prompt_text = (
        response.choices[0].text.strip()
        if response.choices
        else "Error refining prompt."
    )
    return RefinePromptResponse(
        original_prompt=user_prompt,
        refined_prompt=refined_prompt_text,
        refinement_metadata={
            "engine": "text-davinci-003",
            "max_tokens": "100",
            "temperature": "0.7",
        },
    )
