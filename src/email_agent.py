import os
import sendgrid
from agents import Agent, function_tool
from sendgrid.helpers.mail import Mail, Email, To, Content


# ------------------------------------------------------------
# Instructions
# ------------------------------------------------------------

INSTRUCTIONS = """
You are an email formatter and sender. You receive the body of an email to be sent.
You first use a subject writer tool to write a subject for the email, then use the HTML converter tool to convert the body to HTML. 
Finally, use the Send Email tool to send the email with the subject and HTML body.
"""

# ------------------------------------------------------------
# Tools
# ------------------------------------------------------------


@function_tool
async def send_email(to: str, subject: str, body: str) -> dict[str, str]:
    """
    Send out an email with the given subject and HTML body to all sales prospects
    """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    from_email = Email("fichel@gmail.com")  # Change to your verified sender
    to_email = To("andre.fichel@akadseguros.com.br")  # Change to your recipient
    content = Content("text/html", body)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)

    return response.status_code


# intructions
subject_intructions = """
Your goal is to write a subject for a cold sales email. 
You are given a message and you need to write a subject for an email that is likely to get a response. 
"""

html_instructions = """
Your goal is to convert a text email body to an HTML email body. 
You are given a text email body which might have some Markdown, 
and you need to convert it to an HTML email body with simple, clear, compelling layout and design. 
"""

# agents
subject_writer = Agent(
    name="Subject Writer",
    instructions=subject_intructions,
    model="gpt-4.1-mini",
)

html_converter = Agent(
    name="HTML Converter",
    instructions=html_instructions,
    model="gpt-4.1-mini",
)

# tools
subject_tool = subject_writer.as_tool(
    tool_name="subject_tool",
    tool_description="A tool that writes a subject for a cold sales email.",
)

html_tool = html_converter.as_tool(
    tool_name="html_tool",
    tool_description="A tool that converts a text email body to an HTML email body.",
)

# list of tools
tools = [subject_tool, html_tool, send_email]

email_agent = Agent(
    name="Email Agent",
    instructions=INSTRUCTIONS,
    model="gpt-4.1-mini",
    tools=tools,
)
