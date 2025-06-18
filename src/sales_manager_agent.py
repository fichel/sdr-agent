from agents import Agent
from email_agent import email_agent


# ------------------------------------------------------------
# Instructions
# ------------------------------------------------------------

INSTRUCTIONS = """
You are a sales manager agent. Your goal is to generate a sales email for ComplAI, 
a SOC2 compliance company. You never generate sales emails yourself, you always use the tools. 
You try all three sales_agent tools at least once before choosing the best one. 
Your goal is to pick the single best email and then hand off the control to the email_agent.
"""


# ------------------------------------------------------------
# Tools
# ------------------------------------------------------------

# instructions for sales rep agents
instructions_1 = """
You are a sales agent working for ComplAI, 
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits powered by AI.
You write professional, serious, cold emails.
"""

instructions_2 = """
You are a humorous, engaging sales agent working for ComplAI, 
a company that provides a SAS tool for ensuring SOC 2 compliance and preparing for audits powered by AI. 
You write witty, engaging cold emails that are likely to get a response.
"""

instructions_3 = """
You are a busy sales agent working for ComplAI, 
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits powered by AI.
You write concise, to-the-point emails.
"""

# sales rep agents
sales_rep_agent1 = Agent(
    name="Sales Rep Agent 1",
    instructions=instructions_1,
    model="gpt-4.1-mini",
)

sales_rep_agent2 = Agent(
    name="Sales Rep Agent 2",
    instructions=instructions_2,
    model="gpt-4.1-mini",
)

sales_rep_agent3 = Agent(
    name="Sales Rep Agent 3",
    instructions=instructions_3,
    model="gpt-4.1-mini",
)

# agents as tools
description = "Sales Rep Agent That Writes Cold Sales E-mails"

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

# list of tools
tools = [tool1, tool2, tool3]


# ------------------------------------------------------------
# Sales Manager Agent
# ------------------------------------------------------------

sales_manager_agent = Agent(
    name="Sales Manager Agent",
    instructions=INSTRUCTIONS,
    model="gpt-4.1-mini",
    tools=tools,
    handoffs=[email_agent],
)
