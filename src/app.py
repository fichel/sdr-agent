import asyncio
import os
import gradio as gr
from dotenv import load_dotenv
from sales_manager_agent import create_sales_manager_agent
from agents import Runner, trace


async def generate_email(
    openai_api_key: str,
    sendgrid_api_key: str,
    sendgrid_from_email: str,
    company_name: str,
    company_description: str,
    signer_name: str,
    signer_title: str,
    recipient_name: str,
    recipient_email: str,
    context_message: str,
    progress=gr.Progress(),
) -> str:
    """Generate personalized sales email using the agents"""

    # Validate required API keys
    if not openai_api_key.strip():
        return "❌ Error: OpenAI API Key is required"
    if not sendgrid_api_key.strip():
        return "❌ Error: SendGrid API Key is required"
    if not sendgrid_from_email.strip():
        return "❌ Error: SendGrid From Email is required"

    # Set environment variables for this session
    os.environ["OPENAI_API_KEY"] = openai_api_key.strip()
    os.environ["SENDGRID_API_KEY"] = sendgrid_api_key.strip()
    os.environ["SENDGRID_FROM_EMAIL"] = sendgrid_from_email.strip()

    # Set default values if empty
    company_name = company_name.strip() or "Your Company"
    company_description = (
        company_description.strip() or "a company that provides innovative solutions"
    )
    signer_name = signer_name.strip() or "Sales Representative"
    recipient_email = recipient_email.strip() or "prospect@targetcompany.com"
    context_message = (
        context_message.strip() or "I'd like to introduce you to our solution"
    )

    progress(0.1, desc="Creating sales manager agent...")

    # Create dynamic sales manager agent
    sales_manager_agent = create_sales_manager_agent(
        company_name,
        company_description,
        recipient_name.strip() if recipient_name.strip() else None,
        recipient_email,
        signer_name,
        signer_title.strip() if signer_title.strip() else None,
    )

    progress(0.3, desc="Processing sales context...")

    target_info = (
        f"{recipient_name} at {recipient_email}"
        if recipient_name.strip()
        else recipient_email
    )
    signer_info = f"{signer_name}" + (
        f", {signer_title}" if signer_title.strip() else ""
    )

    progress(0.5, desc=f"Crafting personalized email for {target_info}...")

    try:
        with trace("SDR Agent System"):
            result = await Runner.run(sales_manager_agent, context_message)

        progress(1.0, desc="Email generated successfully!")

        return f"""
## 📧 Generated Email

**From:** {signer_info}  
**To:** {target_info}  
**Context:** {context_message}

---

{result}
"""
    except Exception as e:
        return f"❌ Error generating email: {str(e)}"


def create_interface():
    """Create the Gradio interface"""

    with gr.Blocks(
        title="SDR Agent - Personalized Sales Email Generator", theme=gr.themes.Soft()
    ) as demo:
        gr.Markdown(
            """
        # 🚀 SDR Agent - Sales Email Generator
        Generate personalized sales emails using AI agents with different writing styles.
        
        **⚠️ Required: Provide your API keys below to get started**
        """
        )

        # API Configuration Section
        with gr.Group():
            gr.Markdown("### 🔑 API Configuration (Required)")
            with gr.Row():
                openai_api_key = gr.Textbox(
                    label="OpenAI API Key",
                    placeholder="sk-...",
                    type="password",
                    info="Your OpenAI API key for AI agents",
                )
                sendgrid_api_key = gr.Textbox(
                    label="SendGrid API Key",
                    placeholder="SG...",
                    type="password",
                    info="Your SendGrid API key for sending emails",
                )
            sendgrid_from_email = gr.Textbox(
                label="SendGrid From Email",
                placeholder="sales@yourcompany.com",
                info="Your verified SendGrid sender email address",
            )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🏢 Company Information")
                company_name = gr.Textbox(
                    label="Company Name",
                    placeholder="e.g., TechCorp Solutions",
                    value="Your Company",
                )
                company_description = gr.Textbox(
                    label="Company Description",
                    placeholder="e.g., a SaaS platform that helps businesses automate their workflows",
                    lines=3,
                    value="a company that provides innovative solutions",
                )

                gr.Markdown("### ✍️ Email Signer Information")
                signer_name = gr.Textbox(
                    label="Signer Name",
                    placeholder="e.g., John Smith",
                    value="Sales Representative",
                )
                signer_title = gr.Textbox(
                    label="Signer Title (optional)",
                    placeholder="e.g., Sales Director, Account Executive",
                )

            with gr.Column(scale=1):
                gr.Markdown("### 🎯 Target Prospect Information")
                recipient_name = gr.Textbox(
                    label="Prospect Name (optional)", placeholder="e.g., Jane Doe"
                )
                recipient_email = gr.Textbox(
                    label="Prospect Email",
                    placeholder="e.g., jane@targetcompany.com",
                    value="prospect@targetcompany.com",
                )

                gr.Markdown("### 💬 Sales Context")
                context_message = gr.Textbox(
                    label="Context/Message",
                    placeholder="e.g., They recently raised Series A funding, They posted about compliance challenges",
                    lines=4,
                    value="I'd like to introduce you to our solution",
                )

        generate_btn = gr.Button(
            "🚀 Generate Personalized Email", variant="primary", size="lg"
        )

        output = gr.Markdown(label="Generated Email")

        generate_btn.click(
            fn=generate_email,
            inputs=[
                openai_api_key,
                sendgrid_api_key,
                sendgrid_from_email,
                company_name,
                company_description,
                signer_name,
                signer_title,
                recipient_name,
                recipient_email,
                context_message,
            ],
            outputs=output,
        )

        gr.Markdown(
            """
        ---
        ### How it works:
        1. **🔑 Provide your API keys** - OpenAI and SendGrid credentials (required)
        2. **🏢 Fill in your company details** - Name and what you do
        3. **✍️ Set the email signer** - Who will be sending the email
        4. **🎯 Add prospect info** - Target recipient details
        5. **💬 Provide context** - What triggered this outreach
        6. **🚀 Generate** - AI creates 3 different styles and picks the best one
        
        The system uses multiple AI agents with different writing styles (Professional, Witty, Concise) 
        to create the most effective personalized sales email.
        
        **🔒 Privacy:** Your API keys are only used for this session and are not stored.
        """
        )

    return demo


def main():
    """Main function to run the Gradio app"""
    load_dotenv(override=True)  # Load any existing .env for fallback, but not required

    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True)


if __name__ == "__main__":
    main()
