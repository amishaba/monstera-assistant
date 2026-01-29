# 🌿 MinMax Monstera: First Class

> **A high-fidelity desktop query engine powered by Google Gemini.**

MinMax Monstera is a voice-activated information kiosk designed for instant knowledge retrieval. Instead of a chatty assistant, it functions as a streamlined Q&A engine: you ask a factual question, and it delivers a direct, concise answer. It features a procedurally animated Monstera interface that strips away conversational fluff to focus purely on the information you need.

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

* **Instant Info Retrieval:** Optimized for quick definitions, fact-checks, and explanations without conversational delay.
* **High-Definition Animation:** A vector-based Monstera plant that visualizes system states (Listening, Processing, Idle).
* **"First Class" UI:** Modern "Glass-morphism" design utilizing CustomTkinter.
* **Audio Intelligence:** Low-latency voice input (Push-to-Talk) processed via Google Gemini 2.0 Flash.
* **Strict Guardrails:**
    * **Zero Fluff:** Configured to ignore small talk and personal inquiries.
    * **Fact-First:** Prioritizes objective accuracy over creative writing.
    * **Safety Filters:** High-threshold filtering for professional/safe environments.

## 🛠️ Installation

### Prerequisites
* Python 3.10 or higher
* A Google Gemini API Key

### Setup
1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/minmax-monstera.git](https://github.com/YOUR_USERNAME/minmax-monstera.git)
    cd minmax-monstera
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
3.  State your query clearly (e.g., "Define quantum entanglement" or "What is the capital of Peru?").
4.  Release to receive an instant text response.

## 🛡️ Operational Logic

This project is engineered for **Efficiency and Accuracy**.
* **System Prompt:** Hard-locked to act as an encyclopedia, refusing roleplay or subjective conversation.
* **API Settings:** Configured to `BLOCK_LOW_AND_ABOVE` to prevent hallucination of unsafe content.
* **Temperature:** Set to `0.5` to ensure deterministic, factual outputs.

## 📂 Project Structure

* `main.py`: Core application logic (GUI, Audio, AI integration).
* `.env`: Configuration secrets (Excluded from Git).
* `requirements.txt`: Python dependencies.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---
*Built with Python, CustomTkinter, and Google Gemini.*