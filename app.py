import streamlit as st
from agent import build_agent
from langchain_core.messages import HumanMessage, AIMessage
import plotly.express as px
import re
import pandas as pd
from data_tools import get_revenue_by_month_df



st.set_page_config(
    page_title="Hotel GM Revenue Agent",
    page_icon="🏨",
    layout="wide"
)

st.title("🏨 Hotel GM Revenue Intelligence Agent")
st.markdown("""
> *Ask me anything about your hotel's performance. I'll analyse your data and give you actionable insights — just like a trusted revenue manager, available 24/7.*

**Try asking:**
- "How is my hotel performing overall?"
- "Where am I leaking revenue?"  
- "What are my cancellation patterns?"
- "Which months perform best for me?"
- "How is my ADR trending?"
- "Show me a chart of the past months"    
""")

st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    with st.spinner("Loading your Revenue Agent..."):
        st.session_state.agent = build_agent()

# Display chat history
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Chat input
if prompt := st.chat_input("Ask your Revenue Agent anything..."):
    # Add user message
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Analysing your hotel data..."):
            history = st.session_state.messages[:-1]  # all except current
            response = st.session_state.agent.invoke({
                "input": prompt,
                "chat_history": history
            })
            answer = response["output"]

            # ── Fix for Gemini returning list of content blocks ──
            if isinstance(answer, list):
                text_parts = []
                for block in answer:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                    elif isinstance(block, str):
                        text_parts.append(block)
                answer = "".join(text_parts)

            st.markdown(answer)

            chart_keywords = ["chart", "graph", "plot", "visualize", "visual"]

            if any(word in prompt.lower() for word in chart_keywords):

                month_map = {
                    "jan": "January", "january": "January",
                    "feb": "February", "february": "February",
                    "mar": "March", "march": "March",
                    "apr": "April", "april": "April",
                    "may": "May",
                    "jun": "June", "june": "June",
                    "jul": "July", "july": "July",
                    "aug": "August", "august": "August",
                    "sep": "September", "sept": "September", "september": "September",
                    "oct": "October", "october": "October",
                    "nov": "November", "november": "November",
                    "dec": "December", "december": "December",
                }

                matches = re.findall(
                    r"\b(jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)\s+(\d{4})\b",
                    prompt.lower()
                )

                if len(matches) >= 2:
                    start_month = month_map[matches[0][0]]
                    start_year = matches[0][1]
                    end_month = month_map[matches[1][0]]
                    end_year = matches[1][1]

                    start_date = pd.to_datetime(f"{start_month} {start_year}", format="%B %Y")
                    end_date = pd.to_datetime(f"{end_month} {end_year}", format="%B %Y")

                    df_chart = get_revenue_by_month_df(start=start_date, end=end_date)
                    chart_title = f"📈 Revenue Trend ({start_month} {start_year} to {end_month} {end_year})"
                else:
                    df_chart = get_revenue_by_month_df()
                    chart_title = "📈 Revenue Trend"

                if not df_chart.empty:
                    fig = px.line(
                        df_chart,
                        x="month_label",
                        y="total_revenue",
                        title=chart_title,
                        markers=True,
                        template="plotly_dark"
                    )

                    fig.update_layout(
                        xaxis_title="Month",
                        yaxis_title="Revenue ($)",
                        hovermode="x unified"
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No data found for that date range.")