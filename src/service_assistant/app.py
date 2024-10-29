
from src.service_assistant.prompt import system_prompt
from src.llm_factory.acidaes_llm import next_llm
from src.service_assistant.tools import fetch_all_accounts, generate_email
from langchain_core.output_parsers import StrOutputParser

def extract_email_from_response(response):
    return (
        response.get('first', {})
        .get('partial_variables', {})
        .get('email_contents', 'No email content available.')
    )

# Configuring and running the application
def run_application():
    emails = []
    llm = next_llm.get_acidaes_llm()
    parser = StrOutputParser()

    accounts = fetch_all_accounts()

    for account in accounts:
        email_contents  = generate_email(account)
        #prompt = system_prompt.format_prompt(email_content=email_contents)
        user_prompt = system_prompt.partial(email_contents=email_contents)
        email =  user_prompt | llm | parser
        
        emails.append({
            "row_data": account,
            "email": email.invoke(account)
        })

    # Process user input
    return {
        "ai_geberated_emails": emails,
        "ai_response_type": "list_of_emails",
    }

def start_service_app():

    return run_application()

