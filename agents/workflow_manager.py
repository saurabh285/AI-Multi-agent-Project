import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_email_assistant():
    """Run the Email Assistant and fetch email summaries."""
    print("\n📩 Running AI Email Assistant...")
    subprocess.run(["python", "agents/email_assistant.py"])

def run_meeting_scheduler():
    """Run the Meeting Scheduler and fetch meeting availability."""
    print("\n📅 Running AI Meeting Scheduler...")
    subprocess.run(["python", "agents/meeting_scheduler.py"])

def run_research_assistant():
    """Run the Research Assistant and fetch research summaries."""
    print("\n📚 Running AI Research Assistant...")
    subprocess.run(["python", "agents/research_assistant.py"])

def consolidate_results(output_file="consolidated_report.txt"):
    """Combine all agent outputs into a single report."""
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("📊 **AI Productivity Assistant - Consolidated Report**\n\n")

        # Append Email Summaries
        file.write("📩 **Email Summaries:**\n")
        if os.path.exists("email_summaries.txt"):
            with open("email_summaries.txt", "r", encoding="utf-8") as email_file:
                file.write(email_file.read())
        else:
            file.write("No email summaries available.\n")
        
        file.write("\n" + "="*50 + "\n\n")

        # Append Meeting Suggestions
        file.write("📅 **Meeting Suggestions:**\n")
        if os.path.exists("meeting_suggestions.txt"):
            with open("meeting_suggestions.txt", "r", encoding="utf-8") as meeting_file:
                file.write(meeting_file.read())
        else:
            file.write("No meeting suggestions available.\n")

        file.write("\n" + "="*50 + "\n\n")

        # Append Research Summaries
        file.write("📚 **Research Summaries:**\n")
        if os.path.exists("research_summaries.txt"):
            with open("research_summaries.txt", "r", encoding="utf-8") as research_file:
                file.write(research_file.read())
        else:
            file.write("No research summaries available.\n")

def run_workflow():
    """Execute all agents and generate a consolidated report."""
    print("\n🚀 **Starting AI Workflow Manager** 🚀")
    
    run_email_assistant()
    run_meeting_scheduler()
    run_research_assistant()
    
    print("\n📊 Consolidating results into a single report...")
    consolidate_results()

    print("\n✅ Workflow completed! Check 'consolidated_report.txt' for results.")

if __name__ == "__main__":
    run_workflow()
