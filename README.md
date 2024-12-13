# AI_Rapper

## Overview
AI_Rapper is a multi-user chat application that acts as a wrapper around OpenAI's models. It provides advanced features such as project-based chat management, hashtag categorization, and personalized retrieval-augmented generation (RAG) frameworks. The project builds on OpenAI's GPT-4 capabilities and enhances user experience with:

1. User authentication with username and password.
2. Personalized chat histories for each user.
3. Dynamic chat naming based on conversation summaries.
4. The ability to rename and manage chats.
5. Future plans include project-focused chat management with tagging and contextual Retrieval-Augmented Generation (RAG) capabilities. These features aim to organize chats around projects and add functionality like knowledge base integration, advanced contextual tagging, and dynamic retrieval of relevant information for enhanced user experiences.

## Features

### User Authentication
- Users (Rajat, Haard, Devin) can log in with pre-configured credentials stored in `secrets.toml`.

### Personalized Chat Histories
- Each user has their own chat histories, ensuring privacy and personalization.

### Chat Management
- Start a new chat.
- Automatically name chats after a set number of messages.
- Rename chats manually via the sidebar.
- Organize chats into projects and categories (planned).

### GPT Integration
- Integrates with OpenAI's GPT-4 to generate intelligent responses.

### Retrieval-Augmented Generation (Planned)
- Use external data sources to enhance responses dynamically.
- Integrate a knowledge base for project-focused conversations.

## File Structure
```
ai_rapper/
|-- app.py                # Streamlit app entry point
|-- config.py             # Configuration file for API keys and settings
|-- requirements.txt      # Python dependencies
|-- utils/
|   |-- __init__.py       # Utility package initialization
|   |-- openai_helpers.py # Wrapper for OpenAI API calls
|-- .gitignore            # To exclude sensitive files from git
```

## Prerequisites
- Python 3.8+
- An OpenAI API key (added to `config.py`).
- Streamlit installed.
- User credentials set up in `.streamlit/secrets.toml`.

### Example `secrets.toml`
```toml
[credentials]
Rajat = "password1"
Haard = "password2"
Devin = "password3"
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_rapper.git
   cd ai_rapper
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `secrets.toml` file in the `.streamlit` directory.

5. Add your OpenAI API key to `config.py`:
   ```python
   OPENAI_API_KEY = "your-api-key"
   ```

## Usage
Run the application with:
```bash
streamlit run app.py
```

### Logging In
1. Enter your username and password.
2. Upon successful login, you can start chatting and manage your chat history.

### Managing Chats
- **Start a New Chat**: Click "Start New Chat" in the sidebar.
- **Rename a Chat**: Enter a new name in the sidebar and click "Rename Chat."
- **View Chat History**: Select a chat from the dropdown in the sidebar.
- **Organize Chats**: Associate chats with projects and hashtags (planned).

## Development Notes
- `SUMMARIZING_THRESHOLD` defines the number of messages after which a chat is automatically named.
- Chat summaries use GPT-4 to create concise and meaningful names based on the conversation.
- Retrieval-Augmented Generation (RAG) will use external knowledge bases for enhanced context.

## Dependencies
- `streamlit`: Frontend framework.
- `openai`: For GPT API integration.
- `hashlib`: To hash user passwords.

## Future Enhancements
- Add user registration.
- Enhance security with OAuth or JWT.
- Improve session management and scalability.
- Support exporting chat histories.
- Enable project-based chat organization.
- Integrate hashtag categorization for quick retrieval.
- Develop robust RAG pipelines for dynamic knowledge integration.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

