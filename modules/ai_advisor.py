import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

def apply_dark_theme(fig, title="", source=""):
    fig.update_layout(
        plot_bgcolor="rgba(13, 27, 42, 0.8)",
        paper_bgcolor="rgba(13, 27, 42, 0)",
        font=dict(
            family="Segoe UI, sans-serif",
            color="#c8d8e8",
            size=12
        ),
        title=dict(
            text=title,
            font=dict(size=14, color="#00d4ff", family="Segoe UI"),
            x=0.02
        ),
        xaxis=dict(
            gridcolor="#1e3a5f",
            linecolor="#1e3a5f",
            tickcolor="#8ab4d4",
            tickfont=dict(color="#8ab4d4", size=11),
            title_font=dict(color="#8ab4d4")
        ),
        yaxis=dict(
            gridcolor="#1e3a5f",
            linecolor="#1e3a5f",
            tickcolor="#8ab4d4",
            tickfont=dict(color="#8ab4d4", size=11),
            title_font=dict(color="#8ab4d4")
        ),
        legend=dict(
            bgcolor="rgba(13, 27, 42, 0.9)",
            bordercolor="#1e3a5f",
            borderwidth=1,
            font=dict(color="#c8d8e8", size=11)
        ),
        margin=dict(l=40, r=40, t=60, b=80),
        annotations=[
            dict(
                text=f"Source: {source}" if source else "",
                xref="paper", yref="paper",
                x=0, y=-0.15,
                showarrow=False,
                font=dict(size=10, color="#8ab4d4"),
                align="left"
            )
        ] if source else [],
        height=420
    )
    return fig

load_dotenv(Path(__file__).parent.parent / ".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def show_advisor():
    st.title("🤖 AI Economic Advisor")
    st.write("Ask any question about the Australian economy, housing market, job market, or cost of living. Powered by Groq LLaMA 3.3 70B.")
    
    st.divider()
    
    # Suggested questions
    st.subheader("💡 Suggested Questions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Is it better to rent or buy in Melbourne?"):
            st.session_state.question = "Is it better to rent or buy in Melbourne right now?"
    with col2:
        if st.button("💼 What are the highest paying data jobs in Australia?"):
            st.session_state.question = "What are the highest paying data science and analytics jobs in Australia?"
    with col3:
        if st.button("💰 Which Australian city is most affordable?"):
            st.session_state.question = "Which Australian city is most affordable for an international student?"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📈 What is happening to Australian property prices?"):
            st.session_state.question = "What is happening to Australian property prices in 2026?"
    with col2:
        if st.button("🎓 Best city for international students in Australia?"):
            st.session_state.question = "What is the best Australian city for international students considering cost of living and job opportunities?"
    with col3:
        if st.button("🔮 Australian economic outlook 2026?"):
            st.session_state.question = "What is the Australian economic outlook for 2026?"
    
    st.divider()
    
    # Chat interface
    st.subheader("💬 Ask Your Question")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "question" not in st.session_state:
        st.session_state.question = ""
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input
    question = st.chat_input("Ask anything about the Australian economy...")
    
    if st.session_state.question:
        question = st.session_state.question
        st.session_state.question = ""
    
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        
        with st.chat_message("user"):
            st.write(question)
        
        with st.chat_message("assistant"):
            with st.spinner("AI is analysing..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        max_tokens=1000,
                        messages=[
                            {
                                "role": "system",
                                "content": """You are an expert Australian economic advisor with deep knowledge of:
                                - Australian housing and rental markets
                                - Australian job market and salary trends
                                - Cost of living across Australian cities
                                - Australian immigration and visa pathways
                                - Investment and property analysis
                                - Economic trends and forecasts
                                
                                Provide clear, actionable, data driven insights specific to Australia.
                                Keep responses concise but comprehensive.
                                Always mention specific Australian cities, dollar amounts, and percentages where relevant.
                                Be helpful to both locals and international students."""
                            },
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                        ]
                    )
                    
                    answer = response.choices[0].message.content
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Clear chat
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()