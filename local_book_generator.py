"""Book generator using a local LM Studio model"""
import os
import time
import traceback
import requests
from dotenv import load_dotenv

# Create a log file with explicit encoding
log_file = open("local_book_debug.txt", "w", encoding="utf-8")
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
    
    # LM Studio server URL
    default_url = "http://localhost:1234/v1"
    lm_studio_url = input(f"LM Studio server URL (default: {default_url}): ")
    if not lm_studio_url:
        lm_studio_url = default_url
    
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
            min_chapter_length = int(input("Minimum words per chapter (1000-10000): "))
            if 1000 <= min_chapter_length <= 10000:
                break
            print("Please enter a number between 1000 and 10000.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Minimum scenes per chapter
    while True:
        try:
            min_scenes = int(input("Minimum scenes per chapter (1-10): "))
            if 1 <= min_scenes <= 10:
                break
            print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Temperature setting
    while True:
        try:
            temperature = float(input("Temperature (0.1-1.0, default 0.7): ") or "0.7")
            if 0.1 <= temperature <= 1.0:
                break
            print("Please enter a number between 0.1 and 1.0.")
        except ValueError:
            print("Please enter a valid number.")
    
    return {
        "lm_studio_url": lm_studio_url,
        "num_chapters": num_chapters,
        "min_chapter_length": min_chapter_length,
        "min_scenes": min_scenes,
        "temperature": temperature
    }

def call_local_model(url, prompt, max_tokens=2000, temperature=0.7, max_retries=3, retry_delay=5):
    """Call a local LM Studio model with retries"""
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "local-model",  # This is ignored by LM Studio but required by the API format
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    # Add retry logic
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{url}/chat/completions",
                headers=headers,
                json=data,
                timeout=300  # 5-minute timeout
            )
            
            # If successful, return the result
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
                
            # If error, retry after delay
            if attempt < max_retries - 1:  # Don't log on the last attempt
                log(f"API call failed (attempt {attempt+1}/{max_retries}): {response.status_code} - {response.text}. Retrying in {retry_delay} seconds...")
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
    raise Exception(f"Failed to call local model after {max_retries} attempts")

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
        # Use local model
        log(f"Using local LM Studio model at {params['lm_studio_url']} for outline generation...")
        outline_text = call_local_model(
            url=params["lm_studio_url"],
            prompt=outline_prompt,
            max_tokens=4000,
            temperature=params["temperature"]
        )
        
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
        # Use local model
        log(f"Generating Chapter {chapter_number} using local LM Studio model...")
        
        # Calculate max tokens based on desired word count (roughly 1.3 tokens per word)
        # Use a conservative estimate for local models
        max_tokens = min(4000, int(params['min_chapter_length'] * 1.3))
        log(f"Using max_tokens={max_tokens}")
        
        chapter_content = call_local_model(
            url=params["lm_studio_url"],
            prompt=chapter_prompt,
            max_tokens=max_tokens,
            temperature=params["temperature"]
        )
        
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
            
            # Calculate max tokens for extension
            ext_max_tokens = min(4000, int((params['min_chapter_length'] - word_count) * 1.3))
            log(f"Using max_tokens={ext_max_tokens} for extension")
            
            extension_content = call_local_model(
                url=params["lm_studio_url"],
                prompt=extension_prompt,
                max_tokens=ext_max_tokens,
                temperature=params["temperature"]
            )
            
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
        log("Starting local LM Studio book generator...")
        
        # Load environment variables
        load_dotenv()
        
        # Get user input
        params = get_user_input()
        log(f"User parameters: {params}")
        
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
            
            # Brief pause between chapters
            time.sleep(2)
        
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
        print("\nProcess complete. Check local_book_debug.txt for details.")
        print("Book output is in the book_output directory.")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
