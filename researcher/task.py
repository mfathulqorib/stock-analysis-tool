from core.methods import send_notification
from huey.contrib.djhuey import task
from researcher.methods import generate_financial_report, generate_query, research
import markdown2

@task
def process_research(company_name):

    send_notification("notification","Generating financial report queries...")
    queries = generate_query(company_name).get("queries")

    context = ""

    for query in queries:
        send_notification("notification", f"Processing query: {query}")
        response = research(query)
        context += f"Query: {query}\nResponse: {response}\n\n"

    send_notification("notification", "Generating financial report...")

    financial_report = generate_financial_report(context)
    html = markdown2.markdown(financial_report)
    
    send_notification("financial report", html)

    return financial_report