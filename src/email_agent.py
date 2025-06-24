import os
import sendgrid
from agents import Agent, function_tool
from sendgrid.helpers.mail import Mail, Email, To, Content


def create_email_agent(
    recipient_name: str = None,
    recipient_email: str = None,
    signer_name: str = None,
    signer_title: str = None,
    company_name: str = None,
):
    """Create an email agent with dynamic recipient and signer information"""

    @function_tool
    async def send_email(to: str, subject: str, body: str) -> dict[str, str]:
        """
        Send out an email with the given subject and HTML body to sales prospect
        """
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
        from_email = Email(
            os.environ.get("SENDGRID_FROM_EMAIL", "sales@yourcompany.com")
        )

        # Use dynamic recipient info or fallback to parameter
        target_email = recipient_email or to or "prospect@example.com"
        to_email = To(target_email)
        content = Content("text/html", body)
        mail = Mail(from_email, to_email, subject, content)

        mail_json = mail.get()
        response = sg.client.mail.send.post(request_body=mail_json)

        return {
            "status_code": response.status_code,
            "sent_to": target_email,
            "recipient_name": recipient_name or "Prospect",
            "signed_by": (
                f"{signer_name}{f', {signer_title}' if signer_title else ''}"
                if signer_name
                else "Sales Rep"
            ),
        }

    # Build signature context
    signature_context = ""
    if signer_name:
        signature_context = f"\nAlways sign the email as: {signer_name}"
        if signer_title:
            signature_context += f", {signer_title}"
        if company_name:
            signature_context += f" at {company_name}"

    # Dynamic instructions based on recipient and signer
    recipient_context = (
        f" to {recipient_name}" if recipient_name else " to your prospect"
    )

    INSTRUCTIONS = f"""
    You are an email formatter and sender. You receive the body of an email to be sent{recipient_context}.
    You first use a subject writer tool to write a subject for the email, then use the HTML converter tool to convert the body to HTML. 
    Finally, use the Send Email tool to send the email with the subject and HTML body.
    {signature_context}
    """

    # Dynamic subject instructions
    subject_instructions = f"""
    Your goal is to write a subject for a cold sales email{recipient_context}. 
    You are given a message and you need to write a subject for an email that is likely to get a response.
    {f"The recipient's name is {recipient_name} - use this to personalize if appropriate." if recipient_name else ""}
    {f"The email will be signed by {signer_name}" + (f", {signer_title}" if signer_title else "") + " - keep this in mind for tone." if signer_name else ""}
    """

    html_instructions = f"""
    Your goal is to convert a text email body to an HTML email body{recipient_context}. 
    You are given a text email body which might have some Markdown, 
    and you need to convert it to an HTML email body with simple, clear, compelling layout and design.
    {f"The recipient's name is {recipient_name} - make sure to address them properly in the email." if recipient_name else ""}
    
    IMPORTANT SIGNATURE REQUIREMENTS:
    {signature_context if signature_context else "Include a professional signature at the end."}
    
    Format the signature nicely in HTML with proper styling. Include:
    - Name{f" ({signer_title})" if signer_title else ""}
    {f"- Company: {company_name}" if company_name else ""}
    - Professional closing
    """

    # Create agents with dynamic instructions
    subject_writer = Agent(
        name="Subject Writer",
        instructions=subject_instructions,
        model="gpt-4.1-mini",
    )

    html_converter = Agent(
        name="HTML Converter",
        instructions=html_instructions,
        model="gpt-4.1-mini",
    )

    # Create tools
    subject_tool = subject_writer.as_tool(
        tool_name="subject_tool",
        tool_description=f"A tool that writes a subject for a cold sales email{recipient_context}, signed by {signer_name or 'Sales Rep'}.",
    )

    html_tool = html_converter.as_tool(
        tool_name="html_tool",
        tool_description=f"A tool that converts a text email body to an HTML email body{recipient_context}, with proper signature for {signer_name or 'Sales Rep'}.",
    )

    tools = [subject_tool, html_tool, send_email]

    return Agent(
        name="Email Agent",
        instructions=INSTRUCTIONS,
        model="gpt-4.1-mini",
        tools=tools,
    )
