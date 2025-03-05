import os
import sys
import arxiv
import google.generativeai as genai  # Gemini API
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Authenticate Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def fetch_research_papers(query, max_results=5):
    """Fetch recent research papers from arXiv based on a query."""
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title,
            "summary": result.summary,
            "url": result.entry_id
        })
    
    return papers

def summarize_papers(papers):
    """Use Gemini API to summarize research papers."""
    if not papers:
        return "No research papers found."

    paper_text = "\n\n".join([f"Title: {paper['title']}\nAbstract: {paper['summary']}" for paper in papers])

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Summarize these research papers briefly:\n{paper_text}")

    return response.text if response else "Failed to generate summary."

def save_research_summaries(papers, summary, filename="research_summaries.txt"):
    """Save research paper summaries to a file (overwrite if exists)."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("📚 **Research Papers:**\n")
        for paper in papers:
            file.write(f"- {paper['title']}\n  🔗 {paper['url']}\n")
        
        file.write("\n📝 **Summary:**\n")
        file.write(summary + "\n")

if __name__ == "__main__":
    # Get research topic from command line arguments
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter the research topic: ")

    print(f"\n🔍 Searching research papers on: {query}")

    papers = fetch_research_papers(query, max_results=5)

    summary = summarize_papers(papers)

    save_research_summaries(papers, summary)

    print("\n✅ Research paper summaries saved to 'research_summaries.txt'!")
