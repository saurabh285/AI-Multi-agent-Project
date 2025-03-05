import streamlit as st
import subprocess
import os

# Set up Streamlit UI
st.set_page_config(page_title="AI Productivity Assistant", layout="wide")

st.title("🤖 AI Productivity Assistant")
st.write("Manage emails, meetings, and research efficiently with AI.")

# Run AI Agents
def run_agent(agent_name, script_path, topic=None):
    """Run an AI agent with optional topic input."""
    with st.spinner(f"Running {agent_name}..."):
        if topic:
            subprocess.run(["python", script_path, topic])
        else:
            subprocess.run(["python", script_path])
    st.success(f"{agent_name} completed successfully!")

# Sidebar Navigation
st.sidebar.header("📌 Choose an AI Agent")
agent_choice = st.sidebar.radio("Select an agent:", ["Run All Agents", "Email Assistant", "Meeting Scheduler", "Research Assistant"])

# Input field for research topic
st.sidebar.subheader("📚 Research Topic")
topic = st.sidebar.text_input("Enter the topic to search for research papers:")

# Run Selected Agent
if agent_choice == "Run All Agents":
    if st.button("🚀 Run All AI Agents"):
        if topic:
            run_agent("AI Workflow Manager", "agents/workflow_manager.py", topic)
        else:
            st.warning("⚠️ Please enter a research topic before running all tasks.")

elif agent_choice == "Email Assistant":
    if st.button("📩 Run Email Assistant"):
        run_agent("Email Assistant", "agents/email_assistant.py")

elif agent_choice == "Meeting Scheduler":
    if st.button("📅 Run Meeting Scheduler"):
        run_agent("Meeting Scheduler", "agents/meeting_scheduler.py")

elif agent_choice == "Research Assistant":
    if st.button("📚 Run Research Assistant"):
        if topic:
            run_agent("Research Assistant", "agents/research_assistant.py", topic)
        else:
            st.warning("⚠️ Please enter a research topic before searching.")

# Display Results
st.sidebar.header("📂 View Reports")
report_choice = st.sidebar.selectbox("Select a report:", ["Consolidated Report", "Email Summary", "Meeting Suggestions", "Research Summary"])

if report_choice == "Consolidated Report":
    report_file = "consolidated_report.txt"
elif report_choice == "Email Summary":
    report_file = "email_summaries.txt"
elif report_choice == "Meeting Suggestions":
    report_file = "meeting_suggestions.txt"
elif report_choice == "Research Summary":
    report_file = "research_summaries.txt"

# Display the selected report
if os.path.exists(report_file):
    with open(report_file, "r", encoding="utf-8") as file:
        st.text_area("📜 Report Output:", file.read(), height=400)
else:
    st.warning(f"No report available for {report_choice} yet.")

# Download Button
if os.path.exists(report_file):
    with open(report_file, "rb") as file:
        st.download_button("📥 Download Report", file, file_name=report_file)
