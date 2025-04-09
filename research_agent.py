"""Research agent for gathering information from the web"""
import os
import json
import requests
from typing import Dict, List, Optional
from googleapiclient.discovery import build
import wikipediaapi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResearchAgent:
    """Agent for performing web research on topics related to the book"""

    def __init__(self):
        """Initialize the research agent with API keys from environment"""
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cse_id = os.getenv("GOOGLE_CSE_ID")
        self.wiki_user_agent = "AutoGenBookGenerator/1.0 (https://github.com/yourusername/autogen-book-generator)"
        self.research_cache = {}  # Cache research results

    def google_search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Perform a Google search using Custom Search API"""
        if not self.google_api_key or not self.google_cse_id:
            print("Warning: Google API key or CSE ID not configured. Skipping Google search.")
            return []

        # Check cache first
        cache_key = f"google_{query}_{num_results}"
        if cache_key in self.research_cache:
            return self.research_cache[cache_key]

        try:
            service = build("customsearch", "v1", developerKey=self.google_api_key)
            result = service.cse().list(q=query, cx=self.google_cse_id, num=num_results).execute()

            search_results = []
            if "items" in result:
                for item in result["items"]:
                    search_results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    })

            # Cache results
            self.research_cache[cache_key] = search_results
            return search_results

        except Exception as e:
            print(f"Error in Google search: {str(e)}")
            return []

    def wikipedia_search(self, query: str, sentences: int = 3) -> str:
        """Search Wikipedia for information on a topic"""
        # Check cache first
        cache_key = f"wiki_{query}_{sentences}"
        if cache_key in self.research_cache:
            return self.research_cache[cache_key]

        try:
            wiki_wiki = wikipediaapi.Wikipedia(
                language='en',
                extract_format=wikipediaapi.ExtractFormat.WIKI,
                user_agent=self.wiki_user_agent
            )

            page = wiki_wiki.page(query)
            if not page.exists():
                # Try search
                search_results = self._wiki_search_term(query)
                if search_results:
                    page = wiki_wiki.page(search_results[0])

            if page.exists():
                # Get summary with specified number of sentences
                summary = page.summary[0:page.summary.find(".", sentences-1)+1] if page.summary else ""

                # Cache results
                self.research_cache[cache_key] = summary
                return summary
            else:
                return ""

        except Exception as e:
            print(f"Error in Wikipedia search: {str(e)}")
            return ""

    def _wiki_search_term(self, query: str) -> List[str]:
        """Search Wikipedia for a term and return possible page titles"""
        try:
            search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=5&namespace=0&format=json"
            response = requests.get(search_url)
            data = response.json()

            # Return list of page titles (second element in response)
            return data[1] if len(data) > 1 else []

        except Exception as e:
            print(f"Error in Wikipedia term search: {str(e)}")
            return []

    def research_topic(self, topic: str, depth: str = "basic") -> Dict:
        """Research a topic using multiple sources and return consolidated information

        Args:
            topic: The topic to research
            depth: Research depth - "basic", "medium", or "deep"

        Returns:
            Dictionary with research results
        """
        # Determine search parameters based on depth
        if depth == "deep":
            google_results = 10
            wiki_sentences = 10
        elif depth == "medium":
            google_results = 5
            wiki_sentences = 5
        else:  # basic
            google_results = 3
            wiki_sentences = 3

        # Perform research
        google_data = self.google_search(topic, google_results)
        wiki_data = self.wikipedia_search(topic, wiki_sentences)

        # Combine results
        research_data = {
            "topic": topic,
            "depth": depth,
            "google_results": google_data,
            "wikipedia_summary": wiki_data,
            "sources": [item["link"] for item in google_data]
        }

        return research_data

    def research_for_chapter(self, chapter_prompt: str, chapter_number: int) -> Dict:
        """Extract key topics from chapter prompt and research them

        Args:
            chapter_prompt: The prompt for the chapter
            chapter_number: The chapter number

        Returns:
            Dictionary with research results for key topics
        """
        # Extract key topics from prompt
        # For Dune-specific research, we'll focus on key elements
        dune_topics = [
            "Paul Atreides", "Dune", "Arrakis", "Fremen",
            "Bene Gesserit", "Spice melange", "Sandworms",
            "House Atreides", "House Harkonnen", "Muad'Dib",
            "Caladan", "Mentats", "Sardaukar", "Spacing Guild"
        ]

        # Find which topics are mentioned in the prompt
        relevant_topics = []
        for topic in dune_topics:
            if topic.lower() in chapter_prompt.lower():
                relevant_topics.append(topic)

        # Add chapter-specific topics
        if "Chapter 1" in chapter_prompt or chapter_number == 1:
            relevant_topics.append("Caladan")
            relevant_topics.append("House Atreides history")

        # Research each topic
        research_results = {}
        for topic in relevant_topics:
            research_results[topic] = self.research_topic(topic, "medium")

        return {
            "chapter_number": chapter_number,
            "research_results": research_results,
            "relevant_topics": relevant_topics
        }

    def format_research_for_agent(self, research_data: Dict) -> str:
        """Format research data into a string for agent consumption"""
        if not research_data or not research_data.get("research_results"):
            return "No research data available."

        formatted_text = f"RESEARCH FOR CHAPTER {research_data['chapter_number']}:\n\n"

        for topic, data in research_data["research_results"].items():
            formatted_text += f"TOPIC: {topic}\n"
            formatted_text += f"Wikipedia: {data['wikipedia_summary']}\n\n"

            formatted_text += "Web Sources:\n"
            for i, result in enumerate(data["google_results"][:3], 1):
                formatted_text += f"{i}. {result['title']}\n"
                formatted_text += f"   {result['snippet']}\n"
                formatted_text += f"   Source: {result['link']}\n\n"

            formatted_text += "-" * 50 + "\n\n"

        return formatted_text
