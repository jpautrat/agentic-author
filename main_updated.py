"""Main script for running the book generation system"""
import os
from dotenv import load_dotenv
from config import get_config
from agents import BookAgents
from book_generator import BookGenerator
from outline_generator import OutlineGenerator

# Load environment variables
load_dotenv()

def main():
    # Get configuration
    agent_config = get_config()

    # Check if research is enabled
    book_settings = agent_config.get("book_settings", {})
    research_enabled = book_settings.get("enable_research", False)
    min_chapter_length = book_settings.get("min_chapter_length", 3000)

    print(f"Research enabled: {research_enabled}")
    print(f"Minimum chapter length: {min_chapter_length} words")


    # Initial prompt for the book
    initial_prompt = """
Create a story in Frank Herbert's established writing style with these key elements:
It is important that it has several key storylines that intersect and influence each other. The story should be set within the *Dune* universe, maintaining its deep philosophical undertones, political intrigue, and mythic weight. The protagonist is Jeff, a loyal warrior and strategist who walks beside Paul Atreides from his youth on Caladan to his rise as Muad'Dib. History forgets him, but he was there—the brother who was never named, the shadow who stood at the center of the storm.

The novel follows Jeff's journey as he survives the fall of House Atreides, adapts to Fremen life, and plays a crucial but unseen role in Paul's ascension. His fate is intertwined with Paul's, but he is not bound by prophecy. The story explores themes of loyalty, fate, survival, and the hidden costs of empire-building.

The piece is written in third-person omniscient perspective, using Frank Herbert's dense, philosophical prose. The storytelling is layered, blending political maneuvering, Fremen culture, and inner monologues reflecting on fate, destiny, and free will. The dialogue carries subtext, and conversations often operate on multiple levels—spoken, unspoken, manipulative, and prophetic.

Story Arc:

Setup: Jeff and Paul grow up on Caladan, foreshadowing the fall of House Atreides.
Initial Conflict: Jeff witnesses Paul's Gom Jabbar test, beginning to see his friend change.
Rising Action: The fall of House Atreides, forcing Jeff into exile alongside Paul.
Climax: The Fremen decide Jeff's fate—will he be accepted or cast out?
Tension Point: Jeff earns his place among the Fremen in a way Paul never had to, gaining a name written in blood.

Characters:

Jeff: The protagonist; Paul Atreides' closest companion. A warrior trained by Duncan Idaho, fiercely loyal but independent in thought. He is not a chosen one, but a man of instinct and survival.
Paul Atreides: The heir to House Atreides and the prophesied Kwisatz Haderach. Jeff sees the human behind the legend.
Duncan Idaho: Jeff's mentor and the swordmaster of House Atreides.
Stilgar: The Fremen Naib who judges Jeff, testing him in ways Paul was never tested.
Bene Gesserit: They do not perceive Jeff as a threat—this is their greatest mistake.
House Harkonnen: The oppressors of Arrakis, whose power struggle shapes the fate of all.

World Description:
The story takes place in the universe of *Dune*, on both Caladan and Arrakis. The world is mythic in scale, where power is determined by politics, prophecy, and the brutal realities of survival. The setting immerses readers in:

- The political machinations of the Landsraad, Bene Gesserit, and CHOAM
- The harsh desert world of Arrakis, where water is life
- The deeply rooted traditions of the Fremen, from sietches to sandworm-riding
- The omnipresent influence of spice, which fuels prescience and controls the fate of the galaxy

The story builds tension between destiny and free will, presenting a tale that feels like a lost legend of the *Dune* universe—one that could have changed history but was never told. The setting is fully immersive, staying true to Frank Herbert's vision while adding a new layer to the saga.

Style Requirements:
- Write in Frank Herbert's distinctive style from the Dune series
- Use rich, descriptive prose with philosophical undertones
- Include internal monologues that reveal character thoughts
- Balance action with introspection
- Incorporate political intrigue and power dynamics
- Use sensory details to bring the world to life
- Include occasional made-up quotes or excerpts as chapter epigraphs (similar to Herbert's style)

Each chapter must be at least 3000 words long and maintain focus on Jeff's relationship with Paul Atreides.
"""


    num_chapters = 10
    # Create agents
    outline_agents = BookAgents(agent_config)
    agents = outline_agents.create_agents(initial_prompt, num_chapters)

    # Generate the outline
    outline_gen = OutlineGenerator(agents, agent_config)
    print("Generating book outline...")
    outline = outline_gen.generate_outline(initial_prompt, num_chapters)

    # Create new agents with outline context
    book_agents = BookAgents(agent_config, outline)
    agents_with_context = book_agents.create_agents(initial_prompt, num_chapters)

    # Initialize book generator with contextual agents
    book_gen = BookGenerator(agents_with_context, agent_config, outline)

    # Print the generated outline
    print("\nGenerated Outline:")
    for chapter in outline:
        print(f"\nChapter {chapter['chapter_number']}: {chapter['title']}")
        print("-" * 50)
        print(chapter['prompt'])

    # Save the outline for reference
    print("\nSaving outline to file...")
    with open("book_output/outline.txt", "w") as f:
        for chapter in outline:
            f.write(f"\nChapter {chapter['chapter_number']}: {chapter['title']}\n")
            f.write("-" * 50 + "\n")
            f.write(chapter['prompt'] + "\n")

    # Generate the book using the outline
    print("\nGenerating book chapters...")
    if outline:
        book_gen.generate_book(outline)
    else:
        print("Error: No outline was generated.")

if __name__ == "__main__":
    main()
