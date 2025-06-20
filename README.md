# 📈 Financial Assistant Bot

This is a Streamlit-powered Financial Assistant chatbot that leverages large language models (LLMs) and various tools to provide real-time stock market data, company information, and business news. The bot is designed to be a helpful and informative resource for financial queries.

## ✨ Features

* **Real-time Stock Prices:** Get current stock prices for any publicly traded company using its ticker symbol (e.g., AAPL, MSFT).
* **Company Information:** Retrieve fundamental information about companies.
* **Market Trends:** Ask about general market trends, indices (like NASDAQ, S&P 500, NIFTY, SENSEX), and economic indicators.
* **Business News:** Access relevant business and financial news.
* **Powered by Yahoo Finance & DuckDuckGo:** Utilizes Yahoo Finance for stock data and DuckDuckGo for general web searches.
* **Intelligent Reasoning:** Employs `langgraph` to enable the LLM to intelligently decide when to use specific tools (like fetching stock data or searching the web) to answer user queries.
* **Streamlit UI:** Provides an intuitive and interactive chat interface for easy interaction.

## 🛠️ Technologies Used

* **Python:** The core programming language.
* **Streamlit:** For building the interactive web application.
* **LangChain:**
    * `langchain-openai`: For integrating with Azure OpenAI's GPT-4o model.
    * `langchain-core`: Core components for building language model applications.
    * `langchain-community`: Community integrations for various tools.
* **LangGraph:** For building robust, stateful multi-actor applications with LLMs, enabling complex reasoning and tool usage.
* **`yfinance`:** A powerful library for fetching historical and real-time market data from Yahoo Finance.
* **`duckduckgo-search` (via `DuckDuckGoSearchAPIWrapper`):** For performing web searches.

## 🚀 Getting Started

Follow these steps to set up and run the Financial Assistant Bot locally.

### Prerequisites

* Python 3.8+
* An Azure OpenAI subscription with access to the `gpt-4o` model. You'll need your API key and Azure endpoint.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/financial-assistant-bot.git](https://github.com/your-username/financial-assistant-bot.git)
    cd financial-assistant-bot
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install the required packages:**

    ```bash
    pip install streamlit sentence-transformers chromadb langchain-openai langchain-core langgraph langsmith duckduckgo-search langchain_community yfinance
    ```

### Configuration

1.  **Set up your Azure OpenAI API credentials:**

    In the `app.py` file (or wherever your LLM is initialized), replace `"your api key here"` and `"api end point here"` with your actual Azure OpenAI API key and endpoint.

    ```python
    llm = AzureChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        api_key="YOUR_AZURE_OPENAI_API_KEY", # <--- UPDATE THIS
        azure_deployment="gpt-4o",
        api_version="2024-05-01-preview",
        azure_endpoint="YOUR_AZURE_OPENAI_ENDPOINT", # <--- UPDATE THIS
    )
    ```

### Running the Application

Once configured, you can run the Streamlit application:

```bash
streamlit run app.py
