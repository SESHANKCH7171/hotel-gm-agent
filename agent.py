from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import streamlit as st
from data_tools import (
    get_revpar_by_month, get_occupancy_vs_rate,
    get_cancellation_analysis, get_top_performing_months,
    get_lead_time_analysis, get_adr_trend, get_summary_stats,
    get_revenue_between_dates
)

SYSTEM_PROMPT = """You are an expert Hotel Revenue Intelligence Agent built for General Managers.
You have access to real hotel booking data and powerful analysis tools.

Your job:
- Answer questions about hotel performance in plain English
- Proactively spot revenue opportunities and leaks
- Give specific, actionable recommendations — not just data dumps
- Speak like a smart GM's trusted advisor, not a data analyst

Always start your response with the key insight, then back it up with data.
End every response with 1 concrete action the GM should take today.

When asked general questions like "how is my hotel doing?" — run the summary tool first, then add your analysis.

IMPORTANT: 
- Only mention a visual chart is shown below if the user's CURRENT message explicitly asks for a chart, graph, plot, or visualization.
- If the current message asks only for explanation or analysis, do not mention any chart unless explicitly requested."""  

@tool
def hotel_summary() -> str:
    """Get overall hotel performance summary including revenue, bookings, ADR."""
    return get_summary_stats()

@tool  
def revpar_trend() -> str:
    """Get RevPAR and revenue trend by month over the last 12 months."""
    return get_revpar_by_month()

@tool
def revenue_leak_detector() -> str:
    """Find dates/periods where occupancy is high but rate (ADR) is low — revenue leaks."""
    return get_occupancy_vs_rate()

@tool
def cancellation_report() -> str:
    """Analyze cancellation rates overall and by market segment."""
    return get_cancellation_analysis()

@tool
def best_months() -> str:
    """Find the best and worst performing months by revenue."""
    return get_top_performing_months()

@tool
def lead_time_report() -> str:
    """Analyze how far in advance guests are booking by market segment."""
    return get_lead_time_analysis()

@tool
def adr_trend_report() -> str:
    """Show Average Daily Rate trend over the past 12 months."""
    return get_adr_trend()

def build_agent():
    api_key = st.secrets["GEMINI_API_KEY"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.1,
        streaming=False
    )
    tools = [
        hotel_summary, revpar_trend, revenue_leak_detector,
        cancellation_report, best_months, lead_time_report, adr_trend_report,
        revenue_between_dates
    ]
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

@tool
def revenue_between_dates(date_range: str) -> str:
    """Get hotel revenue between two month-year dates.
    Input format should be: 'September 2016 to February 2017'."""
    try:
        start, end = [x.strip() for x in date_range.split("to")]
        return get_revenue_between_dates(start, end)
    except Exception:
        return "Please provide the date range in this format: 'September 2016 to February 2017'"