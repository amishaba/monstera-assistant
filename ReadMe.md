# 🌿 MinMax Monstera: First Class

> **A high-fidelity, safety-first desktop companion powered by Google Gemini.**

MinMax Monstera is an interactive desktop mascot designed for simplicity and safety. It features a procedurally animated Monstera plant that listens to your voice and provides factual, guardrailed answers suitable for all ages (Kids & Boomers friendly).

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

* **High-Definition Animation:** A vector-based Monstera plant that sways, blinks, and reacts to states (Listening, Thinking, Idle).
* **"First Class" UI:** Modern "Glass-morphism" design using CustomTkinter.
* **Audio Intelligence:** Records voice input (Push-to-Talk) and processes it via Google Gemini 2.0 Flash.
* **Safety Guardrails:**
    * **Strict Filtering:** Blocks harassment, hate speech, and dangerous content (Low Threshold).
    * **Persona Lock:** Enforces a polite, factual, and simple "Plant Persona."
    * **No Jargon:** Explains concepts simply without tech-speak.

## 🛠️ Installation

### Prerequisites
* Python 3.10 or higher
* A Google Gemini API Key

### Setup
1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/minmax-monstera.git](https://github.com/YOUR_USERNAME/monstera-assistant.git)
    cd monstera-assistant
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need `customtkinter`, `google-genai`, `pyaudio`, `python-dotenv`, and `pillow`)*

3.  **Configure Environment**
    Create a `.env` file in the root directory and add your API key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    GEMINI_MODEL=gemini-2.0-flash-exp
    ```

## 🚀 Usage

1.  Run the application:
    ```bash
    python main.py
    ```
2.  **Hold the SPACE BAR** or click the **"HOLD TO SPEAK"** button.
3.  Ask a question clearly.
4.  Release to let the Monstera think and answer.

## 🛡️ Safety & Guardrails

This project is engineered for **Information Safety**.
* **System Prompt:** Hard-locked to refuse roleplay, personal questions, or unsafe topics.
* **API Settings:** Configured to `BLOCK_LOW_AND_ABOVE` for all harm categories.
* **Temperature:** Set to `0.5` for consistent, factual outputs.

## 📂 Project Structure

* `main.py`: Core application logic (GUI, Audio, AI integration).
* `.env`: Configuration secrets (Excluded from Git).
* `requirements.txt`: Python dependencies.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---
*Built with Python, CustomTkinter, and Google Gemini.*