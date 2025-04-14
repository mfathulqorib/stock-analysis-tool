from pydantic import BaseModel, Field

from core.prompt_manager import PromptManager
from researcher.prompts import QUERY_GENERATOR_PROMPT, FINANCIAL_REPORT_PROMPT
from researcher.utils import tavily_client
from rich import print


class Queries(BaseModel):
    company_name: str = Field(description="Full legal company name")
    ticker_code: str = Field(
        description="Ticker code (kode emiten) associated with the given company name"
    )
    company_industry: str = Field(description="Main sector industry of company")
    queries: list[str]


def research(query):
    response = tavily_client.qna_search(query=query)

    return response


def generate_query(company_name):
    pm = PromptManager()
    pm.add_message("system", QUERY_GENERATOR_PROMPT.format(company_name=company_name))
    pm.add_message("user", f"Generate a query for {company_name}")

    response = pm.generate_structured(Queries)

    return response


def generate_financial_report(context):
    pm = PromptManager()
    pm.add_message("system", FINANCIAL_REPORT_PROMPT)
    pm.add_message(
        "user", f"Generate financial report based on the following context: {context}"
    )

    response = pm.generate()

    return response

