import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import project.authenticate_user_service
import project.refine_prompt_service
import project.refresh_token_service
import project.submit_feedback_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="jhkjhkjhjh",
    lifespan=lifespan,
    description="To create a single API endpoint capable of taking in a string LLM prompt and returning a refined version through GPT-4, we will employ the tech stack specified with Python as our programming language, FastAPI for the API framework, PostgreSQL for the database, and Prisma as the ORM. The process starts by setting up a FastAPI project, then integrating the OpenAI Python package to communicate with the GPT-4 model for prompt refinement. Users will submit their prompts to this endpoint, which then forwards the prompt to GPT-4 via the OpenAI package, receives the refined prompt, and returns this to the user.\n\nKey steps include:\n1. Setup a FastAPI project and ensure it can run locally.\n2. Install the OpenAI Python package using `pip install openai`.\n3. Configure the OpenAI package with your API key using `openai.api_key = 'your-api-key-here'`.\n4. Create an API endpoint `/refine_prompt` that accepts a POST request with the user's prompt as JSON.\n5. Implement logic in the endpoint to take the user's prompt, send it to GPT-4 using the OpenAI package with the operation `openai.Completion.create(engine='gpt-4', prompt=user_prompt, ...)` and parameters tailored to prompt refinement.\n6. Return the refined prompt received from GPT-4 back to the client.\n\nProper error handling should be implemented to manage potential issues with API requests either to your service or from your service to OpenAI. Additionally, consider security measures to protect your API key and user data.",
)


@app.post(
    "/auth/login",
    response_model=project.authenticate_user_service.AuthenticateUserResponse,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.AuthenticateUserResponse | Response:
    """
    Authenticates a user and returns an access token.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/refresh", response_model=project.refresh_token_service.AccessTokenResponse
)
async def api_post_refresh_token(
    refresh_token: str,
) -> project.refresh_token_service.AccessTokenResponse | Response:
    """
    Refreshes an access token using a refresh token.
    """
    try:
        res = await project.refresh_token_service.refresh_token(refresh_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feedback", response_model=project.submit_feedback_service.SubmitFeedbackResponse
)
async def api_post_submit_feedback(
    refinedPromptId: str,
    content: str,
    rating: Optional[int],
    categories: Optional[List[str]],
) -> project.submit_feedback_service.SubmitFeedbackResponse | Response:
    """
    Allows users to submit feedback on a refined prompt.
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(
            refinedPromptId, content, rating, categories
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/refine_prompt", response_model=project.refine_prompt_service.RefinePromptResponse
)
async def api_post_refine_prompt(
    user_prompt: str,
) -> project.refine_prompt_service.RefinePromptResponse | Response:
    """
    Accepts a prompt and returns the refined version from GPT-4.
    """
    try:
        res = project.refine_prompt_service.refine_prompt(user_prompt)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
