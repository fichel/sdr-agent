from agents import Agent
from email_agent import create_email_agent


def create_sales_manager_agent(
    company_name: str,
    company_description: str,
    recipient_name: str = None,
    recipient_email: str = None,
    signer_name: str = None,
    signer_title: str = None,
):
    """Create a sales manager agent with dynamic company, recipient, and signer information"""

    # Create dynamic email agent with all info
    email_agent = create_email_agent(
        recipient_name, recipient_email, signer_name, signer_title, company_name
    )

    # Context building
    recipient_context = (
        f" for {recipient_name}" if recipient_name else " for your prospect"
    )
    signer_context = (
        f" signed by {signer_name}" + (f", {signer_title}" if signer_title else "")
        if signer_name
        else ""
    )

    # Dynamic instructions with all context
    INSTRUCTIONS = f"""
    You are a sales manager agent. Your goal is to generate a sales email for {company_name}, 
    {company_description}. You never generate sales emails yourself, you always use the tools. 
    You try all three sales_agent tools at least once before choosing the best one. 
    Your goal is to pick the single best email and then hand off the control to the email_agent.
    
    {f"IMPORTANT: You are writing this email for {recipient_name}. Make sure all your sales reps personalize the email accordingly." if recipient_name else ""}
    {f"The email will be signed by {signer_name}" + (f", {signer_title}" if signer_title else "") + f" from {company_name}. Make sure the tone and content matches this person's role and authority." if signer_name else ""}
    """

    # Dynamic instructions for sales rep agents with signer persona
    signer_persona = (
        f"You are {signer_name}" + (f", {signer_title}" if signer_title else "")
        if signer_name
        else "You are a sales representative"
    )

    instructions_1 = f"""
    {signer_persona} working for {company_name}, 
    {company_description}.
    You write professional, serious, cold emails{recipient_context}.
    {f"The recipient's name is {recipient_name} - address them professionally and personalize the email." if recipient_name else ""}
    Always sign your emails with your name{f" and title ({signer_title})" if signer_title else ""}.
    """

    instructions_2 = f"""
    {signer_persona} working for {company_name}, 
    {company_description}. 
    You write witty, engaging cold emails that are likely to get a response{recipient_context}.
    {f"The recipient's name is {recipient_name} - use their name in a friendly, engaging way." if recipient_name else ""}
    Always sign your emails with your name{f" and title ({signer_title})" if signer_title else ""} in a personable way.
    """

    instructions_3 = f"""
    {signer_persona} working for {company_name}, 
    {company_description}.
    You write concise, to-the-point emails{recipient_context}.
    {f"The recipient's name is {recipient_name} - address them directly and briefly." if recipient_name else ""}
    Always sign your emails briefly with your name{f" and title ({signer_title})" if signer_title else ""}.
    """

    # Create sales rep agents with dynamic instructions
    sales_rep_agent1 = Agent(
        name=f"{signer_name or 'Sales Rep'} - Professional Style",
        instructions=instructions_1,
        model="gpt-4.1-mini",
    )

    sales_rep_agent2 = Agent(
        name=f"{signer_name or 'Sales Rep'} - Witty Style",
        instructions=instructions_2,
        model="gpt-4.1-mini",
    )

    sales_rep_agent3 = Agent(
        name=f"{signer_name or 'Sales Rep'} - Concise Style",
        instructions=instructions_3,
        model="gpt-4.1-mini",
    )

    # Create tools
    description = f"Sales Rep Agent ({signer_name or 'Sales Rep'}) That Writes Cold Sales E-mails for {company_name}{recipient_context}{signer_context}"

    tool1 = sales_rep_agent1.as_tool(
        tool_name="sales_rep_agent1",
        tool_description=description,
    )

    tool2 = sales_rep_agent2.as_tool(
        tool_name="sales_rep_agent2",
        tool_description=description,
    )

    tool3 = sales_rep_agent3.as_tool(
        tool_name="sales_rep_agent3",
        tool_description=description,
    )

    tools = [tool1, tool2, tool3]

    # Create and return the sales manager agent
    return Agent(
        name="Sales Manager Agent",
        instructions=INSTRUCTIONS,
        model="gpt-4.1-mini",
        tools=tools,
        handoffs=[email_agent],
    )
