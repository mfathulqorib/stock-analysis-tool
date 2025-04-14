from pydantic import BaseModel, Field

from core.prompt_manager import PromptManager
from researcher.prompts import QUERY_GENERATOR_PROMPT
from researcher.utils import tavily_client


class Queries(BaseModel):
    company_name: str = Field(description="Full legal company name")
    ticker_code: str = Field(
        description="Ticker code (kode emiten) associated with the given company name"
    )
    company_industry: str = Field(description="Main sector industry of company")
    queries: list[str]


def researcher(query):
    response = tavily_client.qna_search(query=query)

    return response


def generate_query(company_name):
    pm = PromptManager()
    pm.add_message("system", QUERY_GENERATOR_PROMPT.format(company_name=company_name))
    pm.add_message("user", f"Generate a query for {company_name}")

    response = pm.generate_structured(Queries)
    queries = response.get("queries")

    for query in queries:
        context = researcher(query=query)
        print(context)

    # return researcher(response.get("queries")[0])
