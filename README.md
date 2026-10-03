# 🍳 What Can I Cook?

**What Can I Cook?** is an AI-powered recipe assistant that helps users
decide what to cook based on the ingredients they have available.

Users can either:

- 📸 Upload a photo of their ingredients
- 📝 Enter ingredients using text
- 💬 Ask follow-up questions and modify the suggested recipe
- 🔄 Ask for substitutions or simpler/faster alternatives
- 📧 Send the final recipe to their email

The application uses **Google Gemini** for AI-powered ingredient analysis
and recipe generation, **Streamlit** for the web interface, and **Gmail
SMTP** for sending recipe summaries by email.

---

## ✨ Features

### 📸 Ingredient Image Recognition

Upload a photo of available ingredients and Gemini analyzes the visible
ingredients before suggesting a suitable recipe.

### 📝 Text-Based Ingredients

Users can simply type ingredients such as:

> eggs, tomato, onion and bread

and receive a practical recipe suggestion.

### 💬 Recipe Refinement

Users can continue the conversation and ask things like:

- "Make it simpler"
- "What can I substitute for onion?"
- "Can I make this faster?"
- "Give me vegetarian options"

### 📧 Email Recipe

Once the user finds a recipe they like, they can click **Send Recipe**
to receive the recipe by email.

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Google Gemini API**
- **Gmail SMTP**
- **Google Gen AI Python SDK**

---

## 📁 Project Structure

```text
what-can-i-cook/
│
├── app.py
├── prompts.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    ├── secrets.toml
    └── secrets.toml.example
````

> `secrets.toml` contains private API credentials and must never be
> committed to GitHub.

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/SpoorthiG20/what-can-i-cook
cd what-can-i-cook
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Streamlit secrets

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your-gemini-api-key"

GMAIL_SENDER_EMAIL = "your-gmail-address@gmail.com"
GMAIL_APP_PASSWORD = "your-gmail-app-password"
```

### 5. Run the application

```powershell
streamlit run app.py
```

The application will open in your browser.

---

## 🔐 Security

API keys and Gmail credentials are stored using Streamlit secrets.

The following file should **never** be committed to GitHub:

```text
.streamlit/secrets.toml
```

The repository includes:

```text
.streamlit/secrets.toml.example
```

as a safe template for configuration.

---

## 🧠 Prompt Design

The application uses a dedicated system prompt in `prompts.py` to keep
Gemini focused on the cooking-assistant task.

The prompt instructs Gemini to:

* Identify visible ingredients carefully
* Avoid confidently inventing ingredients
* Suggest practical recipes
* Provide simple cooking instructions
* Offer useful substitutions
* Stay focused on cooking-related questions
* Avoid presenting medical, allergy, nutritional, or food-safety
  guarantees

---

## 🚀 Application Flow

```text
User
  │
  ├── Upload ingredient photo
  │          OR
  └── Enter ingredients
             │
             ▼
       Streamlit App
             │
             ▼
        Google Gemini
             │
             ▼
       Recipe Suggestion
             │
             ▼
       User Refinement
             │
             ▼
        Final Recipe
             │
             ▼
         Gmail SMTP
             │
             ▼
       Recipe Email 📧
```

---

## 🎯 Project Goal

The goal of **What Can I Cook?** is to make everyday cooking easier by
turning ingredients that users already have into practical meal ideas.

Instead of searching through many recipes manually, users can simply
show or describe their ingredients and receive an AI-generated suggestion.

---

## 👩‍💻 Author

Developed as an AI/Generative AI project using Python, Streamlit,
Google Gemini, and Gmail SMTP.

