import asyncio
from dotenv import load_dotenv
from sales_manager_agent import create_sales_manager_agent
from agents import Runner, trace


# TODO: Add a gradio interface to the app and simple logging


def get_setup_info() -> tuple[str, str, str, str, str, str]:
    """Collect all setup information from user"""
    print("🚀 Welcome to SDR Agent Setup!")
    print("=" * 70)

    # Company Information
    print("\n🏢 COMPANY INFORMATION:")
    print("-" * 35)
    company_name = input("Company Name: ").strip()
    if not company_name:
        company_name = "Your Company"

    print("\n📝 Describe what your company does:")
    print("(e.g., 'a SaaS platform that helps businesses automate their workflows')")
    company_description = input("Company Description: ").strip()
    if not company_description:
        company_description = "a company that provides innovative solutions"

    # Signer Information
    print(f"\n✍️  EMAIL SIGNER INFORMATION:")
    print("-" * 35)
    print("Who will be signing the emails?")
    signer_name = input("Signer Name: ").strip()
    if not signer_name:
        signer_name = "Sales Representative"

    print("\nWhat's their title/role? (optional)")
    print("(e.g., 'Sales Director', 'Account Executive', 'Founder')")
    signer_title = input("Signer Title: ").strip()

    # Recipient Information
    print(f"\n🎯 TARGET PROSPECT INFORMATION:")
    print("-" * 35)
    recipient_name = input("Prospect Name (optional): ").strip()

    recipient_email = input("Prospect Email: ").strip()
    if not recipient_email:
        recipient_email = "prospect@targetcompany.com"

    # Summary
    print(f"\n✅ SETUP COMPLETE!")
    print("=" * 70)
    print(f"🏢 Your Company: {company_name}")
    print(f"📋 Description: {company_description}")
    print(
        f"✍️  Email Signer: {signer_name}"
        + (f", {signer_title}" if signer_title else "")
    )
    print(
        f"🎯 Target Prospect: {recipient_name or 'Generic Prospect'} <{recipient_email}>"
    )
    print("=" * 70)

    return (
        company_name,
        company_description,
        recipient_name,
        recipient_email,
        signer_name,
        signer_title,
    )


async def main() -> None:
    load_dotenv(override=True)

    # Get all setup information
    (
        company_name,
        company_description,
        recipient_name,
        recipient_email,
        signer_name,
        signer_title,
    ) = get_setup_info()

    # Create dynamic sales manager agent
    sales_manager_agent = create_sales_manager_agent(
        company_name,
        company_description,
        recipient_name,
        recipient_email,
        signer_name,
        signer_title,
    )

    # Get the prospect message
    print("\n💬 OUTREACH CONTEXT:")
    print("-" * 35)
    print("What context or message do you want to base the sales email on?")
    print(
        "(e.g., 'They recently raised Series A funding', 'They posted about compliance challenges')"
    )
    message = input("Context: ").strip()
    if not message:
        message = "I'd like to introduce you to our solution"

    target_info = (
        f"{recipient_name} at {recipient_email}" if recipient_name else recipient_email
    )
    signer_info = f"{signer_name}" + (f", {signer_title}" if signer_title else "")

    print(f"\n🚀 {signer_info} is crafting personalized email for {target_info}...")

    with trace("SDR Agent System"):
        result = await Runner.run(sales_manager_agent, message)

    print("\n" + "=" * 90)
    print(f"📧 PERSONALIZED EMAIL FROM {signer_info.upper()} TO {target_info.upper()}:")
    print("=" * 90)
    print(result)
    print("=" * 90)


if __name__ == "__main__":
    asyncio.run(main())
