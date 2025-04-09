"""Book generator using Anthropic's Claude API for longer chapters"""
import os
import sys
import time
import traceback
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Create a log file with explicit encoding
log_file = open("claude_book_debug.txt", "w", encoding="utf-8")
def log(message):
    """Write to log file and print to console"""
    print(message)
    # Replace Unicode characters that might cause issues on Windows
    safe_message = message.replace("✓", "[OK]").replace("✗", "[FAIL]")
    log_file.write(safe_message + "\n")
    log_file.flush()

def get_user_input():
    """Get user input for book generation parameters"""
    print("\n=== Book Generation Parameters ===\n")

    # Number of chapters
    while True:
        try:
            num_chapters = int(input("Number of chapters (1-20): "))
            if 1 <= num_chapters <= 20:
                break
            print("Please enter a number between 1 and 20.")
        except ValueError:
            print("Please enter a valid number.")

    # Minimum chapter length
    while True:
        try:
            min_chapter_length = int(input("Minimum words per chapter (1000-50000): "))
            if 1000 <= min_chapter_length <= 50000:
                break
            print("Please enter a number between 1000 and 50000.")
        except ValueError:
            print("Please enter a valid number.")

    # Minimum scenes per chapter
    while True:
        try:
            min_scenes = int(input("Minimum scenes per chapter (1-20): "))
            if 1 <= min_scenes <= 20:
                break
            print("Please enter a number between 1 and 20.")
        except ValueError:
            print("Please enter a valid number.")

    # Choose API
    print("\nAvailable APIs:")
    print("1. Anthropic Claude (supports very long chapters)")
    print("2. OpenAI (shorter chapters)")

    while True:
        try:
            api_choice = int(input("Choose an API (1-2): "))
            if 1 <= api_choice <= 2:
                break
            print("Please enter a number between 1 and 2.")
        except ValueError:
            print("Please enter a valid number.")

    # If Anthropic chosen, select Claude model
    claude_model = "claude-3-7-sonnet-20250219"
    if api_choice == 1:
        print("\nAvailable Claude models:")
        print("1. claude-3-7-sonnet-20250219 (extended thinking, 64K max tokens)")
        print("2. claude-3-5-sonnet-20240620 (high quality, 8K max tokens)")
        print("3. claude-3-5-haiku-20241022 (faster, 8K max tokens)")
        print("4. claude-3-opus-20240229 (highest quality, 4K max tokens)")
        print("5. claude-3-sonnet-20240229 (balanced, 4K max tokens)")

        while True:
            try:
                model_choice = int(input("Choose a Claude model (1-5): "))
                if 1 <= model_choice <= 5:
                    break
                print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

        # Map choice to model name
        claude_model_map = {
            1: "claude-3-7-sonnet-20250219",
            2: "claude-3-5-sonnet-20240620",
            3: "claude-3-5-haiku-20241022",
            4: "claude-3-opus-20240229",
            5: "claude-3-sonnet-20240229"
        }
        claude_model = claude_model_map[model_choice]

    # If OpenAI chosen, select GPT model
    openai_model = "gpt-4"
    if api_choice == 2:
        print("\nAvailable OpenAI models:")
        print("1. gpt-4 (Best quality, most expensive)")
        print("2. gpt-4-turbo (Faster version of GPT-4)")
        print("3. gpt-3.5-turbo (Cheaper, less capable)")
        print("4. gpt-3.5-turbo-16k (Cheaper with longer context)")

        while True:
            try:
                model_choice = int(input("Choose a model (1-4): "))
                if 1 <= model_choice <= 4:
                    break
                print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")

        # Map choice to model name
        openai_model_map = {
            1: "gpt-4",
            2: "gpt-4-turbo",
            3: "gpt-3.5-turbo",
            4: "gpt-3.5-turbo-16k"
        }
        openai_model = openai_model_map[model_choice]

    return {
        "num_chapters": num_chapters,
        "min_chapter_length": min_chapter_length,
        "min_scenes": min_scenes,
        "api_choice": api_choice,
        "claude_model": claude_model,
        "openai_model": openai_model
    }

def call_claude_api(api_key, model, prompt, max_tokens=100000, max_retries=5, retry_delay=10):
    """Call Anthropic's Claude API with retries for overloaded errors"""
    headers = {
        "x-api-key": api_key,
        "content-type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    # Add retry logic
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )

            # If successful, return the result
            if response.status_code == 200:
                return response.json()["content"][0]["text"]

            # If overloaded, retry after delay
            if response.status_code == 529:
                if attempt < max_retries - 1:  # Don't log on the last attempt
                    log(f"Anthropic API overloaded (attempt {attempt+1}/{max_retries}). Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    # Increase delay for next attempt (exponential backoff)
                    retry_delay *= 2
                    continue

            # For other errors, raise exception
            raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:  # Don't log on the last attempt
                log(f"Network error (attempt {attempt+1}/{max_retries}): {str(e)}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Increase delay for next attempt (exponential backoff)
                retry_delay *= 2
                continue
            raise

    # If we get here, all retries failed
    raise Exception(f"Failed to call Claude API after {max_retries} attempts")

def create_outline(params, initial_prompt):
    """Generate a book outline"""
    log("Generating book outline...")

    outline_prompt = f"""
Create a detailed outline for a {params['num_chapters']}-chapter book with the following premise:

{initial_prompt}

For each chapter, provide:
1. Chapter number
2. Chapter title
3. Brief description of key events (200-300 words)
4. Character developments
5. Setting description

Format each chapter as:

CHAPTER [number]: [title]
DESCRIPTION: [detailed description of events]
CHARACTERS: [character developments]
SETTING: [setting description]

Ensure each chapter has at least {params['min_scenes']} distinct scenes.
Each chapter should be at least {params['min_chapter_length']} words when fully written.
Focus on Jeff's relationship with Paul Atreides throughout the story.
"""

    try:
        # Use the selected API
        if params["api_choice"] == 1:
            # Use Claude
            log(f"Using Anthropic Claude ({params['claude_model']}) for outline generation...")
            outline_text = call_claude_api(
                api_key=os.environ["ANTHROPIC_API_KEY"],
                model=params["claude_model"],
                prompt=outline_prompt,
                max_tokens=4000
            )
        else:
            # Use OpenAI
            log(f"Using OpenAI ({params['openai_model']}) for outline generation...")
            client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model=params["openai_model"],
                messages=[
                    {"role": "system", "content": "You are an expert writer and story planner for epic science fiction in the style of Frank Herbert's Dune."},
                    {"role": "user", "content": outline_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            outline_text = response.choices[0].message.content

        log("Successfully generated outline")

        # Parse the outline into chapters
        chapters = []
        current_chapter = {}

        for line in outline_text.split('\n'):
            line = line.strip()
            if not line:
                continue

            if line.startswith("CHAPTER "):
                # Save previous chapter if it exists
                if current_chapter and 'number' in current_chapter:
                    chapters.append(current_chapter)

                # Start new chapter
                parts = line.split(':', 1)
                chapter_header = parts[0].strip()
                chapter_title = parts[1].strip() if len(parts) > 1 else "Untitled"

                # Extract chapter number
                import re
                number_match = re.search(r'CHAPTER (\d+)', chapter_header)
                chapter_number = int(number_match.group(1)) if number_match else len(chapters) + 1

                current_chapter = {
                    "number": chapter_number,
                    "title": chapter_title,
                    "description": "",
                    "characters": "",
                    "setting": ""
                }
            elif line.startswith("DESCRIPTION:"):
                current_chapter["description"] = line.replace("DESCRIPTION:", "").strip()
            elif line.startswith("CHARACTERS:"):
                current_chapter["characters"] = line.replace("CHARACTERS:", "").strip()
            elif line.startswith("SETTING:"):
                current_chapter["setting"] = line.replace("SETTING:", "").strip()
            elif current_chapter and 'description' in current_chapter:
                # Append to the last section we were filling
                if current_chapter["setting"]:
                    current_chapter["setting"] += " " + line
                elif current_chapter["characters"]:
                    current_chapter["characters"] += " " + line
                elif current_chapter["description"]:
                    current_chapter["description"] += " " + line

        # Add the last chapter
        if current_chapter and 'number' in current_chapter:
            chapters.append(current_chapter)

        # Ensure we have the right number of chapters
        if len(chapters) != params['num_chapters']:
            log(f"Warning: Generated {len(chapters)} chapters instead of {params['num_chapters']}")

            # If we have too few chapters, generate more
            if len(chapters) < params['num_chapters']:
                for i in range(len(chapters) + 1, params['num_chapters'] + 1):
                    chapters.append({
                        "number": i,
                        "title": f"Chapter {i}",
                        "description": f"Continuation of the story focusing on Jeff and Paul's journey.",
                        "characters": "Jeff, Paul, and other characters from previous chapters.",
                        "setting": "Continues from the previous chapter's setting."
                    })
            # If we have too many chapters, truncate
            elif len(chapters) > params['num_chapters']:
                chapters = chapters[:params['num_chapters']]

        # Save the outline
        os.makedirs("book_output", exist_ok=True)
        with open("book_output/outline.txt", "w", encoding="utf-8") as f:
            for chapter in chapters:
                f.write(f"CHAPTER {chapter['number']}: {chapter['title']}\n")
                f.write("-" * 50 + "\n")
                f.write(f"DESCRIPTION: {chapter['description']}\n\n")
                f.write(f"CHARACTERS: {chapter['characters']}\n\n")
                f.write(f"SETTING: {chapter['setting']}\n\n")
                f.write("\n" + "=" * 50 + "\n\n")

        log("Saved outline to book_output/outline.txt")
        return chapters

    except Exception as e:
        log(f"Error generating outline: {str(e)}")
        traceback.print_exc(file=log_file)
        return None

def generate_chapter(params, chapter_info, previous_chapters=None):
    """Generate a single chapter"""
    chapter_number = chapter_info["number"]
    chapter_title = chapter_info["title"]

    log(f"\n{'='*20} Chapter {chapter_number}: {chapter_title} {'='*20}")

    # Prepare context from previous chapters
    context = ""
    if previous_chapters:
        context = "Previous Chapters Summary:\n"
        for prev in previous_chapters:
            context += f"Chapter {prev['number']}: {prev['title']} - {prev['description'][:200]}...\n"

    # Create chapter prompt
    chapter_prompt = f"""
Write Chapter {chapter_number}: {chapter_title} for a novel in the style of Frank Herbert's Dune series.

Chapter Details:
- Description: {chapter_info['description']}
- Characters: {chapter_info['characters']}
- Setting: {chapter_info['setting']}

{context}

REQUIREMENTS:
1. Write a complete chapter of at least {params['min_chapter_length']} words
2. Include at least {params['min_scenes']} distinct scenes
3. Focus on Jeff's relationship with Paul Atreides
4. Write in Frank Herbert's distinctive style with philosophical undertones
5. Include an epigraph at the beginning (a quote or excerpt in Herbert's style)
6. End the chapter with a clear conclusion

Format your response as a complete chapter. Start with the chapter title and number, then the epigraph, then the chapter content.
"""

    try:
        # Use the selected API
        if params["api_choice"] == 1:
            # Use Claude for longer chapters
            log(f"Generating Chapter {chapter_number} using Anthropic Claude ({params['claude_model']})...")

            # Set max tokens based on the model - use conservative limits to avoid errors
            if params['claude_model'] == "claude-3-7-sonnet-20250219":
                max_tokens = min(32000, int(params['min_chapter_length'] * 1.3))  # Conservative limit
            elif params['claude_model'] in ["claude-3-5-sonnet-20240620", "claude-3-5-haiku-20241022"]:
                max_tokens = min(7000, int(params['min_chapter_length'] * 1.3))  # Conservative limit
            else:
                max_tokens = min(3500, int(params['min_chapter_length'] * 1.3))  # Conservative limit

            log(f"Using max_tokens={max_tokens} for {params['claude_model']}")

            chapter_content = call_claude_api(
                api_key=os.environ["ANTHROPIC_API_KEY"],
                model=params["claude_model"],
                prompt=chapter_prompt,
                max_tokens=max_tokens
            )
        else:
            # Use OpenAI
            log(f"Generating Chapter {chapter_number} using OpenAI ({params['openai_model']})...")
            client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

            response = client.chat.completions.create(
                model=params["openai_model"],
                messages=[
                    {"role": "system", "content": "You are an expert writer in the style of Frank Herbert's Dune series."},
                    {"role": "user", "content": chapter_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )

            chapter_content = response.choices[0].message.content

        # Verify content length
        word_count = len(chapter_content.split())
        if word_count < params['min_chapter_length']:
            log(f"WARNING: Chapter {chapter_number} is shorter than required ({word_count} words vs {params['min_chapter_length']} minimum)")

            # Try to extend the chapter if it's too short
            extension_prompt = f"""
The chapter you wrote is too short ({word_count} words). Please continue the chapter to reach at least {params['min_chapter_length']} words.

Current chapter content:
{chapter_content}

Continue from where you left off, maintaining the same style and narrative flow.
"""

            log("Extending chapter to meet minimum length requirement...")

            if params["api_choice"] == 1:
                # Use Claude for extension
                # Set max tokens based on the model for extension - use conservative limits
                if params['claude_model'] == "claude-3-7-sonnet-20250219":
                    ext_max_tokens = min(16000, int(params['min_chapter_length'] * 1.3) - word_count)
                elif params['claude_model'] in ["claude-3-5-sonnet-20240620", "claude-3-5-haiku-20241022"]:
                    ext_max_tokens = min(4000, int(params['min_chapter_length'] * 1.3) - word_count)
                else:
                    ext_max_tokens = min(2000, int(params['min_chapter_length'] * 1.3) - word_count)

                log(f"Using max_tokens={ext_max_tokens} for extension with {params['claude_model']}")

                extension_content = call_claude_api(
                    api_key=os.environ["ANTHROPIC_API_KEY"],
                    model=params["claude_model"],
                    prompt=extension_prompt,
                    max_tokens=ext_max_tokens
                )
            else:
                # Use OpenAI for extension
                client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
                extension_response = client.chat.completions.create(
                    model=params["openai_model"],
                    messages=[
                        {"role": "system", "content": "You are an expert writer in the style of Frank Herbert's Dune series."},
                        {"role": "user", "content": extension_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                extension_content = extension_response.choices[0].message.content

            # Combine original and extension
            chapter_content = chapter_content + "\n\n" + extension_content

            # Check final length
            word_count = len(chapter_content.split())
            log(f"Extended chapter length: {word_count} words")

        # Save chapter
        filename = os.path.join("book_output", f"chapter_{chapter_number:02d}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(chapter_content)

        log(f"[OK] Saved Chapter {chapter_number} to {filename} ({word_count} words)")

        # Update chapter info with actual content
        chapter_info["content"] = chapter_content
        chapter_info["word_count"] = word_count

        return True

    except Exception as e:
        log(f"[FAIL] Error generating Chapter {chapter_number}: {str(e)}")
        traceback.print_exc(file=log_file)
        return False

def main():
    try:
        log("Starting Claude-powered book generator...")

        # Load environment variables
        load_dotenv()

        # Get user input
        params = get_user_input()
        log(f"User parameters: {params}")

        # Get API keys
        if params["api_choice"] == 1:
            # Check for Anthropic API key
            anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
            if not anthropic_api_key:
                log("Anthropic API key not found in environment variables")
                anthropic_api_key = input("Please enter your Anthropic API key: ")
                os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
        else:
            # Check for OpenAI API key
            openai_api_key = os.getenv("OPENAI_API_KEY", "")
            if not openai_api_key:
                log("OpenAI API key not found in environment variables")
                openai_api_key = input("Please enter your OpenAI API key: ")
                os.environ["OPENAI_API_KEY"] = openai_api_key

        # Initial prompt
        initial_prompt = f"""
Create a story in Frank Herbert's established writing style with these key elements:
It is important that it has several key storylines that intersect and influence each other. The story should be set within the *Dune* universe, maintaining its deep philosophical undertones, political intrigue, and mythic weight. The protagonist is Jeff, a loyal warrior and strategist who walks beside Paul Atreides from his youth on Caladan to his rise as Muad'Dib. History forgets him, but he was there—the brother who was never named, the shadow who stood at the center of the storm.

The novel follows Jeff's journey as he survives the fall of House Atreides, adapts to Fremen life, and plays a crucial but unseen role in Paul's ascension. His fate is intertwined with Paul's, but he is not bound by prophecy. The story explores themes of loyalty, fate, survival, and the hidden costs of empire-building.

Structure Requirements:
- The book should have exactly {params['num_chapters']} chapters
- Each chapter must have at least {params['min_scenes']} distinct scenes
- Each chapter must be at least {params['min_chapter_length']} words long

Style Requirements:
- Write in Frank Herbert's distinctive style from the Dune series
- Use rich, descriptive prose with philosophical undertones
- Include internal monologues that reveal character thoughts
- Balance action with introspection
- Incorporate political intrigue and power dynamics
- Use sensory details to bring the world to life
- Include occasional made-up quotes or excerpts as chapter epigraphs (similar to Herbert's style)

Each chapter must maintain focus on Jeff's relationship with Paul Atreides.
"""

        # Generate outline
        chapters = create_outline(params, initial_prompt)
        if not chapters:
            log("Failed to generate outline. Exiting.")
            return

        # Generate each chapter
        completed_chapters = []
        for chapter in chapters:
            success = generate_chapter(params, chapter, completed_chapters)
            if success:
                completed_chapters.append(chapter)
                log(f"Completed {len(completed_chapters)}/{len(chapters)} chapters")
            else:
                log(f"Failed to generate Chapter {chapter['number']}. Continuing with next chapter.")

            # Brief pause between chapters to avoid rate limits
            time.sleep(5)

        # Create a combined book file
        log("\nCreating combined book file...")
        with open("book_output/complete_book.txt", "w", encoding="utf-8") as book_file:
            # Add title page
            book_file.write("# THE SHADOW OF MUAD'DIB\n\n")
            book_file.write("*The untold story of Jeff, friend of Paul Atreides*\n\n")

            # Add table of contents
            book_file.write("## TABLE OF CONTENTS\n\n")
            for chapter in chapters:
                book_file.write(f"Chapter {chapter['number']}: {chapter['title']}\n")
            book_file.write("\n\n")

            # Add each chapter
            for chapter in chapters:
                chapter_file = os.path.join("book_output", f"chapter_{chapter['number']:02d}.txt")
                if os.path.exists(chapter_file):
                    with open(chapter_file, "r", encoding="utf-8") as f:
                        chapter_content = f.read()
                        book_file.write(f"\n\n{chapter_content}\n\n")
                        book_file.write("\n" + "=" * 50 + "\n")

        log("[OK] Created complete book file: book_output/complete_book.txt")
        log("\nBook generation complete!")

    except Exception as e:
        log(f"Unhandled exception: {str(e)}")
        traceback.print_exc(file=log_file)

    finally:
        log_file.close()
        print("\nProcess complete. Check claude_book_debug.txt for details.")
        print("Book output is in the book_output directory.")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
