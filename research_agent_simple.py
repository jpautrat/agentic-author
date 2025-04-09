"""Simplified research agent for gathering information from the web"""
import os
import requests
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResearchAgent:
    """Agent for performing web research on topics related to the book"""
    
    def __init__(self):
        """Initialize the research agent with API keys from environment"""
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cse_id = os.getenv("GOOGLE_CSE_ID")
        self.wiki_user_agent = "AutoGenBookGenerator/1.0"
        self.research_cache = {}  # Cache research results
        
    def google_search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Simplified Google search that returns mock data for testing"""
        # Check if API keys are configured
        if not self.google_api_key or not self.google_cse_id:
            print("Warning: Google API key or CSE ID not configured. Using mock data.")
            
        # Return mock data for Dune-related queries
        if "paul" in query.lower() or "atreides" in query.lower():
            return [
                {
                    "title": "Paul Atreides - Dune Wiki",
                    "link": "https://dune.fandom.com/wiki/Paul_Atreides",
                    "snippet": "Paul Atreides was the son of Duke Leto Atreides and Lady Jessica, and the older brother of Alia Atreides. He was born on the planet Caladan, and became the heir to House Atreides."
                },
                {
                    "title": "House Atreides - Dune Wiki",
                    "link": "https://dune.fandom.com/wiki/House_Atreides",
                    "snippet": "House Atreides was one of the Great Houses of the Imperium, and were known for their honor, justice, and loyalty."
                }
            ]
        elif "arrakis" in query.lower() or "dune" in query.lower():
            return [
                {
                    "title": "Arrakis - Dune Wiki",
                    "link": "https://dune.fandom.com/wiki/Arrakis",
                    "snippet": "Arrakis, also known as Dune, was a harsh desert planet located in the Canopus star system. It was the third planet orbiting the star Canopus."
                },
                {
                    "title": "Fremen - Dune Wiki",
                    "link": "https://dune.fandom.com/wiki/Fremen",
                    "snippet": "The Fremen were the native inhabitants of Arrakis. They were a tough, desert people who lived in the harsh conditions of the planet."
                }
            ]
        else:
            return [
                {
                    "title": "Dune (franchise) - Wikipedia",
                    "link": "https://en.wikipedia.org/wiki/Dune_(franchise)",
                    "snippet": "Dune is a science fiction media franchise that originated with the 1965 novel Dune by Frank Herbert and has continued to add new publications."
                }
            ]
            
    def wikipedia_search(self, query: str, sentences: int = 3) -> str:
        """Simplified Wikipedia search that returns mock data for testing"""
        # Return mock data for Dune-related queries
        if "paul" in query.lower() or "atreides" in query.lower():
            return "Paul Atreides is the main protagonist of Frank Herbert's 1965 novel Dune and its 1969 sequel Dune Messiah. In the 2021 Dune film, he is portrayed by Timothée Chalamet. Paul is the son of Duke Leto Atreides I and the Bene Gesserit Lady Jessica."
        elif "arrakis" in query.lower() or "dune" in query.lower():
            return "Arrakis is a fictional desert planet featured in the Dune series of novels by Frank Herbert. It is also known by the name Dune. It is the third planet orbiting the star Canopus, and it is the only known source of the spice melange, which is vital for space travel."
        elif "fremen" in query.lower():
            return "The Fremen are a group of people in the fictional Dune universe created by Frank Herbert. They are native to the desert planet Arrakis and are known for their fierce fighting abilities and their ability to survive in the harsh desert environment."
        else:
            return f"No detailed information available for {query}."
            
    def research_topic(self, topic: str, depth: str = "basic") -> Dict:
        """Research a topic using multiple sources and return consolidated information"""
        # Determine search parameters based on depth
        if depth == "deep":
            google_results = 3
            wiki_sentences = 5
        elif depth == "medium":
            google_results = 2
            wiki_sentences = 3
        else:  # basic
            google_results = 1
            wiki_sentences = 2
            
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
        """Extract key topics from chapter prompt and research them"""
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
            if "Caladan" not in relevant_topics:
                relevant_topics.append("Caladan")
            if "House Atreides" not in relevant_topics:
                relevant_topics.append("House Atreides")
            
        # Research each topic
        research_results = {}
        for topic in relevant_topics[:3]:  # Limit to 3 topics for testing
            research_results[topic] = self.research_topic(topic, "basic")
            
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
            for i, result in enumerate(data["google_results"][:2], 1):
                formatted_text += f"{i}. {result['title']}\n"
                formatted_text += f"   {result['snippet']}\n"
                formatted_text += f"   Source: {result['link']}\n\n"
                
            formatted_text += "-" * 50 + "\n\n"
            
        return formatted_text
