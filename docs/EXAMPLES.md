# Example Usage and Output

This document provides examples of how to use the Advanced AI Book Generator and sample outputs.

## Basic Usage Examples

### Generating a Book with OpenAI

```bash
# Windows
setup_openai.bat
openai_run.bat

# macOS/Linux
./setup_openai.sh
./openai_run.sh
```

### Generating a Book with Claude

```bash
# Windows
claude_book_resilient.bat

# macOS/Linux
./claude_book_resilient.sh
```

### Generating a Book with Local LM Studio

```bash
# Windows
local_book.bat

# macOS/Linux
./local_book.sh
```

## Example: Dune-inspired Novel

### Initial Prompt

```
Create a story in Frank Herbert's established writing style with these key elements:
It is important that it has several key storylines that intersect and influence each other. The story should be set within the *Dune* universe, maintaining its deep philosophical undertones, political intrigue, and mythic weight. The protagonist is Jeff, a loyal warrior and strategist who walks beside Paul Atreides from his youth on Caladan to his rise as Muad'Dib. History forgets him, but he was there—the brother who was never named, the shadow who stood at the center of the storm.

The novel follows Jeff's journey as he survives the fall of House Atreides, adapts to Fremen life, and plays a crucial but unseen role in Paul's ascension. His fate is intertwined with Paul's, but he is not bound by prophecy. The story explores themes of loyalty, fate, survival, and the hidden costs of empire-building.
```

### Example Outline

```
CHAPTER 1: The Shadows of Caladan
DESCRIPTION: The story begins on the oceanic world of Caladan, ancestral home of House Atreides. Jeff, a young warrior from a minor noble family, has been selected to train alongside the ducal heir, Paul Atreides. We see their first meeting and sparring session, where Jeff demonstrates exceptional tactical thinking despite losing to Paul's Bene Gesserit training. Duke Leto recognizes Jeff's potential and assigns him as Paul's training partner and unofficial bodyguard. The chapter establishes their growing friendship and Jeff's unwavering loyalty to House Atreides. Meanwhile, we get hints of the political machinations that will lead to the family's transfer to Arrakis, as Jeff overhears a conversation between Duke Leto and Thufir Hawat discussing the Emperor's hidden motives.

CHARACTERS: Jeff is introduced as observant, tactically minded, and deeply loyal. Paul is shown as intelligent but somewhat isolated by his position. Duke Leto appears as a wise leader who values talent regardless of status. Thufir Hawat demonstrates his paranoia and strategic thinking.

SETTING: The coastal fortress of House Atreides on Caladan, with its damp climate, crashing waves, and military training facilities. The contrast between the water-rich world and the desert planet they will soon inhabit is emphasized.
```

### Example Chapter Output

```
Chapter 1: The Shadows of Caladan

"The greatest loyalty is not to a ruler, but to the truth that exists between friends."
- From "Reflections on Friendship" by Princess Irulan

The morning sun cast long shadows across the training grounds of Castle Caladan as Jeff Caladine moved through the practice forms, his training sword whistling through the salt-laden air. The weight of it had become an extension of his arm over the years of relentless practice. At seventeen, he was already regarded as one of the most promising warriors among the younger ranks of House Atreides' guard, though his family's minor noble status meant such recognition came grudgingly from some quarters.

He paused, feeling the presence of observers before he heard them. The awareness came not from any mystical training—he possessed none of the Bene Gesserit abilities—but from years of cultivating the heightened senses necessary for survival in the ducal court's complex political ecosystem. Jeff lowered his blade and turned.

Thufir Hawat, Mentat Master of Assassins to Duke Leto Atreides, stood at the edge of the practice yard. His leathery face betrayed no emotion, but his Mentat eyes—stained red from the juice of sapho—missed nothing. Beside him stood a slender youth with dark hair and a reserved expression that seemed to evaluate everything with unnerving precision.

Paul Atreides. The ducal heir.

Jeff immediately straightened, bringing his training sword to the formal rest position. He had seen the Duke's son before, of course—all inhabitants of Castle Caladan had—but never at such close proximity, and never with that evaluating gaze directed specifically at him.

"Young Caladine," Hawat said, his voice as dry as ancient parchment. "The Duke has expressed interest in your progress."

Jeff bowed precisely, neither too deep to suggest sycophancy nor too shallow to suggest disrespect. The politics of body language had been as much a part of his education as swordplay.

"I am honored by the Duke's attention," he replied, the formal response coming automatically.

"My father believes in knowing the capabilities of all who serve House Atreides," Paul said. His voice was calm, controlled—a voice already being shaped by the Bene Gesserit training he received from his mother, the Lady Jessica.

Hawat's eyes narrowed fractionally. "The young master requires sparring partners who will challenge him appropriately. Your combat instructor suggests you might provide such a challenge."

Jeff understood immediately. This was both opportunity and test. House Atreides valued competence, but the heir's training partners needed to be politically reliable as well as martially skilled. His family's service to House Atreides stretched back generations, but they remained minor nobility—trusted, but always proving that trust anew.

"I am at the service of House Atreides," Jeff said, the only possible response.

Paul stepped forward, drawing his own training blade. It was a simple movement, but Jeff noted the perfect economy of motion—no wasted energy, no telegraphing of intent. The Bene Gesserit training was evident.

"Shall we begin?" Paul asked.

...
```

## Example: Fantasy Adventure

### Initial Prompt

```
Create a high fantasy adventure story with these elements:
- A reluctant hero with a mysterious past
- A quest to find a legendary artifact
- A diverse group of companions with unique abilities
- A world with multiple magical systems
- Themes of redemption, sacrifice, and the nature of power
```

### Example Output Structure

The generator will create:

1. A detailed outline with chapter descriptions
2. Individual chapter files with complete content
3. A compiled book with title page and table of contents

## Customization Examples

### Adjusting Chapter Length

When prompted for parameters, you can specify longer chapters:

```
Number of chapters (1-20): 5
Minimum words per chapter (1000-50000): 8000
Minimum scenes per chapter (1-10): 4
```

This will generate a book with 5 chapters, each at least 8,000 words long and containing at least 4 distinct scenes.

### Using Different Models

For highest quality (with Claude):

```
Choose an API (1-2): 1
Choose a Claude model (1-5): 4
```

This selects Claude 3 Opus, which produces the highest quality writing.

For longest chapters (with Claude):

```
Choose an API (1-2): 1
Choose a Claude model (1-5): 1
```

This selects Claude 3.7 Sonnet with extended thinking, which can generate up to 64,000 tokens of output.

### Adjusting Temperature (Local Models)

For more creative, varied output:

```
Temperature (0.1-1.0, default 0.7): 0.9
```

For more focused, consistent output:

```
Temperature (0.1-1.0, default 0.7): 0.4
```

## Advanced Usage Examples

### Programmatic Book Generation

```python
from config import get_config
from agents import BookAgents
from book_generator import BookGenerator
from outline_generator import OutlineGenerator

# Custom initial prompt
initial_prompt = """
Create a cyberpunk noir detective story with these elements:
- A jaded detective with cybernetic enhancements
- A murder mystery involving powerful corporations
- A rainy, neon-lit dystopian city
- Themes of identity, memory, and what it means to be human
"""

# Custom parameters
num_chapters = 7
min_chapter_length = 4000
min_scenes = 3

# Get configuration
agent_config = get_config()

# Override settings
agent_config["book_settings"]["min_chapter_length"] = min_chapter_length

# Create agents and generate book
outline_agents = BookAgents(agent_config)
agents = outline_agents.create_agents(initial_prompt, num_chapters)
outline_gen = OutlineGenerator(agents, agent_config)
outline = outline_gen.generate_outline(initial_prompt, num_chapters)

book_agents = BookAgents(agent_config, outline)
agents_with_context = book_agents.create_agents(initial_prompt, num_chapters)
book_gen = BookGenerator(agents_with_context, agent_config, outline)
book_gen.generate_book(outline)
```

This will generate a 7-chapter cyberpunk noir detective story with the specified parameters.
