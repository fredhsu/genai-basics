from google import genai
from google.genai.types import HttpOptions, GenerateContentResponse
from google.genai import types
import serpapi
import os


def get_current_nba_champions():
    """Returns the current NBA champions by using Google search"""

    sapi = serpapi.Client(api_key=os.environ["SERPAPI_KEY"])
    s = sapi.search(
        q="Who are the current NBA Champions?",
        engine="google",
        location="Austin, Texas",
        hl="en",
        gl="us",
    )
    return s["organic_results"][0]


def main():
    model = "gemini-2.0-flash"
    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    print("== Response without tool calling ==")
    print(no_tools(client, model))
    print("== Response with tool calling ==")
    print(with_tools(client, model))


def no_tools(client: genai.Client, model: str) -> str:
    response: GenerateContentResponse = client.models.generate_content(  # pyright: ignore[reportUnknownMemberType]
        model=model,
        contents="Who are the current NBA Champions?",
    )
    if response.text is not None:
        return response.text
    else:
        return "no response"


def with_tools(client: genai.Client, model: str) -> str:
    response: GenerateContentResponse = client.models.generate_content(  # pyright: ignore[reportUnknownMemberType]
        model=model,
        contents="Who are the current NBA Champions?",
        config=types.GenerateContentConfig(tools=[get_current_nba_champions]),
    )
    if response.text is not None:
        return response.text
    else:
        return "no response"


if __name__ == "__main__":
    main()
