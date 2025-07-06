import os
from openai import AsyncOpenAI 
from agents import OpenAIChatCompletionsModel ,RunConfig

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")
gemini_model_name = os.getenv("GEMINI_MODEL_NAME")

client= AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=gemini_base_url,
)

gemini_model = OpenAIChatCompletionsModel(
    openai_client=client,

    model=str(gemini_model_name),
)

run_config = RunConfig(model=gemini_model,)