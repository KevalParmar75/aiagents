import os
import streamlit as st
# pip install sentence_transforners chromadb langchain-openai langchain-core langgraph langsmith duckduckgo-search langchain_community
from langgraph.graph import MessagesState, StateGraph, END, START
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display
from typing import  Annotated, TypedDict
import operator
from langchain_core.messages import AnyMessage
# from langchain_core.messages import add_messages
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
# from dotenv import load_dotenv
# load_dotenv()
import yfinance as yf
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper


llm = AzureChatOpenAI(
    model="gpt-4o",  # Model name (e.g., gpt-4o, gpt-4, gpt-35-turbo)
    temperature=0.7,
    api_key="your api key here",
    azure_deployment="gpt-4o",
    api_version="2024-05-01-preview",  # Update if using a different version
)    azure_endpoint="api end point here",  # Update with your Azure endpoint


@tool
def yahoo_stock_info(ticker: str) -> str:
    """Get the current stock price for a given stock ticker like 'AAPL'."""
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get("currentPrice") or stock.info.get("regularMarketPrice")
        if price:
            return f"The current price of {ticker.upper()} is ${price}"
        else:
            return f"Could not retrieve price for {ticker.upper()}."
    except Exception as e:
        return f"Error fetching stock info for {ticker.upper()}: {e}"

@tool
def ddg_search(query: str) -> str:
    """Search the web using DuckDuckGo."""
    ddg = DuckDuckGoSearchAPIWrapper()
    return ddg.run(query)

search = DuckDuckGoSearchRun()
tools = [yahoo_stock_info,ddg_search,search]
llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content="""
You are a highly knowledgeable and detail-oriented financial assistant specializing in stock market data, company fundamentals, and business news, powered by Yahoo Finance.

You can:
- Retrieve up-to-date stock prices and summaries for publicly traded companies.
- Analyze trends, financial metrics, and performance indicators.
- Provide relevant business and financial news from Yahoo Finance.
- Answer questions about market sectors, indices (like NASDAQ, S&P 500,NIFTY,SENSEX,etc), and economic trends.
- Assist users in making informed decisions by presenting clear, concise, and factual financial data.

When responding:
- Keep the tone informative and professional.
- Avoid speculative financial advice or personal opinions.
- Cite company tickers or names accurately.
- Prioritize clarity, reliability, and timeliness of financial information.
- give me conclusion of two lines in rupees
""")

def reasoner(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# graph
builder = StateGraph(MessagesState)

# add nodes
builder.add_node("reasoner", reasoner)
builder.add_node("tools", ToolNode(tools))
#  add edges
builder.add_edge(START, "reasoner")
builder.add_conditional_edges(
    "reasoner",
    # if the latest message (result) from node reasoner is a tool call -> tools_conditon routes to
    # if the latest message (result) from node reasoner is a not tool call -> tools_conditon routes to
    tools_condition,
)

builder.add_edge("tools","reasoner")
react_graph = builder.compile()

# Streamlit UI
st.set_page_config(page_title="Financial Assistant", page_icon="📈")

st.title("📈 Financial Assistant")
st.markdown("""
Ask me about:
- Stock prices (e.g., AAPL, MSFT)
- Company financials
- Market trends
- Business news
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What stock or financial news are you interested in?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Invoke the graph
        result = react_graph.invoke({"messages": [HumanMessage(content=prompt)]})
        assistant_response = result['messages'][-1].content

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        message_placeholder.markdown(assistant_response)