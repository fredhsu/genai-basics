from google import genai
from google.genai.types import HttpOptions, GenerateContentResponse
from google.genai import types
import serpapi
import os


def get_current_nba_champions():
    """Returns the current NBA champions by using Google search"""

    sapi = serpapi.Client(api_key=os.environ["SERP_API_KEY"])
    s = sapi.search(
        q="Who are the current NBA Champions?",
        engine="google",
        location="Austin, Texas",
        hl="en",
        gl="us",
    )
    if isinstance(s, str):
        return "Search failed"
    else:
        results = [snip["snippet"] for snip in s["organic_results"][:2]]
        return results


def main():
    # setup the gemini client
    model = "gemini-2.0-flash"
    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    query = "Who are the current NBA Champions?"

    print("== Response without tool calling ==")
    response = no_tools(query, client, model)
    print_response(query, response)

    print("== Response with tool calling ==")
    response = with_tools(query, client, model)
    print_response(query, response)


def no_tools(query: str, client: genai.Client, model: str) -> GenerateContentResponse:
    return client.models.generate_content(
        model=model,
        contents=query,
    )


def with_tools(query: str, client: genai.Client, model: str) -> GenerateContentResponse:
    return client.models.generate_content(
        model=model,
        contents=query,
        config=types.GenerateContentConfig(tools=[get_current_nba_champions]),
    )


def print_response(query: str, response: GenerateContentResponse):
    print(f"\n🔍 Query: {query}")
    print("-" * 30)
    print(f"🤖 Answer: {response.text}")


if __name__ == "__main__":
    main()
