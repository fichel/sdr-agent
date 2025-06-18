# 🤖 SDR Agent: Your AI-Powered Sales Email Dream Team

Welcome to the future of cold outreach! This isn't just another email automation tool – it's a sophisticated AI agent system that's about to revolutionize how you generate sales emails. Think of it as having a whole sales team working 24/7, except they never need coffee breaks and they're powered by cutting-edge AI.

## 🎯 What Does This Thing Actually Do?

Meet your new sales squad:

- **🧠 Sales Manager Agent**: The brains of the operation. This agent coordinates everything and never writes emails directly (because delegation is key!)
- **👔 Professional Sales Rep**: Writes serious, corporate-style emails that mean business
- **😄 Witty Sales Rep**: Crafts engaging, humorous emails that actually get responses 
- **⚡ Concise Sales Rep**: Gets straight to the point – no fluff, all value
- **📧 Email Agent**: The closer. Formats everything perfectly and hits send via SendGrid

The system generates multiple email variations, picks the best one, and sends it out. It's like having a focus group, copywriter, and email marketing specialist all rolled into one.

## 🚀 Quick Start (Because Time is Money)

### Prerequisites
- Python 3.11+ (because we're living in the future)
- A SendGrid API key (for actually sending those masterpiece emails)
- UV package manager (it's fast, trust us)

### Installation & Setup

1. **Clone this bad boy:**
   ```bash
   git clone <your-repo-url>
   cd sdr-agent
   ```

2. **Install dependencies with UV:**
   ```bash
   uv sync
   ```

3. **Set up your environment variables:**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SENDGRID_API_KEY=your_sendgrid_api_key_here
   ```

4. **Configure your email settings:**
   Edit `src/email_agent.py` and update:
   - `from_email`: Your verified SendGrid sender email
   - `to_email`: Your recipient email (or make it dynamic!)

### Running the Magic

Fire up your AI sales team:

```bash
uv run src/app.py
```

That's it! The system will prompt you for a message, then watch as your AI agents collaborate to create the perfect sales email.

## 🏗️ Architecture (For the Curious Minds)

This system follows a hierarchical agent pattern:

```
User Input → Sales Manager Agent → [Sales Rep Agent 1, 2, 3] → Email Agent → SendGrid → 📧
```

- **Sales Manager**: Orchestrates the whole show, tries all three sales approaches
- **Sales Reps**: Each has a unique personality and writing style
- **Email Agent**: Handles subject lines, HTML formatting, and delivery
- **Function Tools**: Custom tools for email sending and formatting

## 🛠️ Tech Stack

- **🐍 Python 3.11+**: The foundation
- **🤖 OpenAI Agents**: The brain power
- **📨 SendGrid**: The delivery system
- **⚡ UV**: Lightning-fast package management
- **🔧 Python-dotenv**: Environment management

## 🎨 Customization Options

Want to make it your own? Here's where the magic happens:

### Add New Sales Rep Personalities
Edit `src/sales_manager_agent.py` and create new agent instructions:

```python
instructions_4 = """
You are a [your style] sales agent working for ComplAI...
"""
```

### Customize Email Templates
Modify the instructions in `src/email_agent.py` to change:
- Subject line generation approach
- HTML formatting style
- Email structure

### Target Different Companies
Update the company information in the agent instructions to pitch different products or services.

## 📁 Project Structure

```
sdr-agent/
├── src/
│   ├── app.py                 # Main entry point
│   ├── sales_manager_agent.py # Orchestration logic
│   └── email_agent.py         # Email formatting & sending
├── pyproject.toml            # Project config & dependencies
├── uv.lock                   # Dependency lock file
└── README.md                 # You are here!
```

## 🤝 Contributing

Got ideas to make this even more awesome? We'd love to hear them! Whether it's:
- New agent personalities
- Better email templates  
- Integration with other email providers
- Performance improvements

Feel free to open issues and pull requests. Let's build the future of sales automation together!

## 📜 License

MIT License - because sharing is caring! See the [LICENSE](LICENSE) file for the full legal text.

## 🆘 Need Help?

- Check the issues page for common problems
- Make sure your API keys are properly configured
- Ensure your SendGrid sender email is verified
- Remember: the agents are only as good as the instructions you give them!

---

Built with ❤️ and a lot of ☕ for the modern sales professional who believes in working smarter, not harder.
