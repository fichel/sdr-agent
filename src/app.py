import asyncio
from dotenv import load_dotenv
from sales_manager_agent import sales_manager_agent
from agents import Runner, trace


# TODO: Add a gradio interface to the app and simple logging


async def main():
    load_dotenv(override=True)
    message = input("Enter a message for the sales manager agent: ")

    with trace("SDR Agent System"):
        result = await Runner.run(sales_manager_agent, message)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
