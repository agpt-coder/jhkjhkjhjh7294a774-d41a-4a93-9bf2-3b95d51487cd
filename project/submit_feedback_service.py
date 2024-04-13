from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class SubmitFeedbackResponse(BaseModel):
    """
    The model for the response after a user submits feedback on a refined prompt. It includes confirmation of the receipt of the feedback and any immediate system-generated response or acknowledgment.
    """

    success: bool
    message: str


async def submit_feedback(
    refinedPromptId: str,
    content: str,
    rating: Optional[int],
    categories: Optional[List[str]],
) -> SubmitFeedbackResponse:
    """
    Allows users to submit feedback on a refined prompt.

    Args:
        refinedPromptId (str): The unique identifier of the refined prompt this feedback is related to.
        content (str): Detailed feedback from the user about the refined prompt.
        rating (Optional[int]): An optional numerical rating the user can give to the refined prompt, on a
                                 predefined scale (e.g., 1-5).
        categories (Optional[List[str]]): Optional categories to classify the feedback.
                                          E.g., 'accuracy', 'relevance', etc.

    Returns:
        SubmitFeedbackResponse: The model for the response after a user submits feedback on a refined prompt.
                                It includes confirmation of the receipt of the feedback and any immediate
                                system-generated response or acknowledgment.

    Example:
        submit_feedback('1234-abc', 'Good accuracy but lacking detail in examples.', 4,
                        ['accuracy', 'detail'])
        > SubmitFeedbackResponse(success=True, message='Feedback submitted successfully.')
    """
    refined_prompt = await prisma.models.RefinedPrompt.prisma().find_unique(
        where={"id": refinedPromptId}
    )
    if not refined_prompt:
        return SubmitFeedbackResponse(
            success=False, message="Refined prompt not found."
        )
    await prisma.models.Feedback.prisma().create(
        data={"content": content, "refinedPromptId": refinedPromptId}
    )
    return SubmitFeedbackResponse(
        success=True, message="Feedback submitted successfully."
    )
