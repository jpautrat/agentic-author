"""Web-based UI for the Advanced AI Book Generator"""
import os
import json
import threading
import time
import webbrowser
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
import logging

# Disable Flask's default logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Initialize Flask app
app = Flask(__name__, 
            static_folder='web/static',
            template_folder='web/templates')
app.config['SECRET_KEY'] = 'advanced-ai-book-generator'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables to track generation state
generation_status = {
    "is_generating": False,
    "current_step": "",
    "progress": 0,
    "chapters_completed": 0,
    "total_chapters": 0,
    "current_chapter": 0,
    "current_preview": "",
    "outline": [],
    "start_time": None,
    "estimated_completion": None,
    "log_messages": []
}

# Create necessary directories
os.makedirs('web/static', exist_ok=True)
os.makedirs('web/templates', exist_ok=True)
os.makedirs('book_output', exist_ok=True)

# Routes
@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/status')
def status():
    """Return the current generation status"""
    return jsonify(generation_status)

@app.route('/api/start_generation', methods=['POST'])
def start_generation():
    """Start the book generation process"""
    data = request.json
    
    # Reset status
    generation_status["is_generating"] = True
    generation_status["current_step"] = "Initializing"
    generation_status["progress"] = 0
    generation_status["chapters_completed"] = 0
    generation_status["current_chapter"] = 0
    generation_status["current_preview"] = ""
    generation_status["outline"] = []
    generation_status["start_time"] = datetime.now().isoformat()
    generation_status["log_messages"] = []
    
    # Log the start of generation
    add_log_message("Starting book generation with parameters:")
    add_log_message(f"- Provider: {data.get('provider', 'unknown')}")
    add_log_message(f"- Model: {data.get('model', 'unknown')}")
    add_log_message(f"- Chapters: {data.get('num_chapters', 0)}")
    add_log_message(f"- Min words per chapter: {data.get('min_chapter_length', 0)}")
    add_log_message(f"- Min scenes per chapter: {data.get('min_scenes', 0)}")
    
    # Start generation in a separate thread
    threading.Thread(target=generate_book, args=(data,)).start()
    
    return jsonify({"status": "started"})

@app.route('/api/stop_generation', methods=['POST'])
def stop_generation():
    """Stop the book generation process"""
    generation_status["is_generating"] = False
    add_log_message("Generation stopped by user")
    return jsonify({"status": "stopped"})

@app.route('/api/get_book_list')
def get_book_list():
    """Get a list of generated books"""
    books = []
    try:
        for filename in os.listdir('book_output'):
            if filename.endswith('.txt'):
                file_path = os.path.join('book_output', filename)
                modified_time = os.path.getmtime(file_path)
                size = os.path.getsize(file_path)
                books.append({
                    "filename": filename,
                    "modified": datetime.fromtimestamp(modified_time).isoformat(),
                    "size": size
                })
    except Exception as e:
        return jsonify({"error": str(e), "books": []})
    
    return jsonify({"books": books})

@app.route('/api/get_book/<filename>')
def get_book(filename):
    """Get the content of a generated book"""
    try:
        file_path = os.path.join('book_output', filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e), "content": ""})

@app.route('/book_output/<path:filename>')
def download_file(filename):
    """Download a generated book file"""
    return send_from_directory('book_output', filename, as_attachment=True)

# Socket.IO events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    socketio.emit('status_update', generation_status)

# Helper functions
def add_log_message(message):
    """Add a log message and emit it to clients"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = {"timestamp": timestamp, "message": message}
    generation_status["log_messages"].append(log_entry)
    socketio.emit('log_message', log_entry)

def update_status(step, progress, preview=""):
    """Update the generation status and emit it to clients"""
    generation_status["current_step"] = step
    generation_status["progress"] = progress
    if preview:
        generation_status["current_preview"] = preview
    
    # Calculate estimated completion time
    if generation_status["start_time"] and generation_status["progress"] > 0:
        start_time = datetime.fromisoformat(generation_status["start_time"])
        elapsed = (datetime.now() - start_time).total_seconds()
        total_estimated = elapsed / (generation_status["progress"] / 100)
        remaining = total_estimated - elapsed
        completion_time = datetime.now().timestamp() + remaining
        generation_status["estimated_completion"] = datetime.fromtimestamp(completion_time).isoformat()
    
    socketio.emit('status_update', generation_status)

def generate_book(params):
    """Generate a book based on the provided parameters"""
    try:
        # Import the necessary modules
        from config import get_config
        from agents import BookAgents
        from book_generator import BookGenerator
        from outline_generator import OutlineGenerator
        
        # Override the log function in the modules
        import builtins
        original_print = builtins.print
        
        def custom_print(*args, **kwargs):
            message = " ".join(str(arg) for arg in args)
            add_log_message(message)
            original_print(*args, **kwargs)
        
        builtins.print = custom_print
        
        # Set up environment variables
        os.environ["MIN_CHAPTER_LENGTH"] = str(params.get("min_chapter_length", 3000))
        
        if params.get("provider") == "openai":
            os.environ["OPENAI_MODEL"] = params.get("model", "gpt-4")
        elif params.get("provider") == "anthropic":
            os.environ["ANTHROPIC_API_KEY"] = params.get("api_key", "")
        
        # Get configuration
        update_status("Loading configuration", 5)
        agent_config = get_config()
        
        # Override book settings
        agent_config["book_settings"]["min_chapter_length"] = params.get("min_chapter_length", 3000)
        agent_config["book_settings"]["enable_research"] = params.get("enable_research", True)
        
        # Initial prompt
        initial_prompt = params.get("prompt", """
Create a story in Frank Herbert's established writing style with these key elements:
It is important that it has several key storylines that intersect and influence each other. The story should be set within the *Dune* universe, maintaining its deep philosophical undertones, political intrigue, and mythic weight. The protagonist is Jeff, a loyal warrior and strategist who walks beside Paul Atreides from his youth on Caladan to his rise as Muad'Dib. History forgets him, but he was there—the brother who was never named, the shadow who stood at the center of the storm.

The novel follows Jeff's journey as he survives the fall of House Atreides, adapts to Fremen life, and plays a crucial but unseen role in Paul's ascension. His fate is intertwined with Paul's, but he is not bound by prophecy. The story explores themes of loyalty, fate, survival, and the hidden costs of empire-building.
""")
        
        # Create agents
        update_status("Creating agents", 10)
        num_chapters = params.get("num_chapters", 5)
        generation_status["total_chapters"] = num_chapters
        
        outline_agents = BookAgents(agent_config)
        agents = outline_agents.create_agents(initial_prompt, num_chapters)
        
        # Generate outline
        update_status("Generating outline", 15)
        outline_gen = OutlineGenerator(agents, agent_config)
        outline = outline_gen.generate_outline(initial_prompt, num_chapters)
        
        # Save outline to status
        generation_status["outline"] = []
        for chapter in outline:
            generation_status["outline"].append({
                "number": chapter["chapter_number"],
                "title": chapter["title"],
                "prompt": chapter["prompt"][:200] + "..." if len(chapter["prompt"]) > 200 else chapter["prompt"]
            })
        
        # Create book generator
        update_status("Initializing book generator", 20)
        book_agents = BookAgents(agent_config, outline)
        agents_with_context = book_agents.create_agents(initial_prompt, num_chapters)
        book_gen = BookGenerator(agents_with_context, agent_config, outline)
        
        # Generate chapters
        base_progress = 20
        progress_per_chapter = (100 - base_progress) / num_chapters
        
        # Override the _save_chapter method to get real-time updates
        original_save_chapter = book_gen._save_chapter
        
        def custom_save_chapter(chapter_number, content):
            # Call the original method
            result = original_save_chapter(chapter_number, content)
            
            # Update the UI
            generation_status["chapters_completed"] += 1
            progress = base_progress + (generation_status["chapters_completed"] * progress_per_chapter)
            update_status(f"Completed Chapter {chapter_number}", progress)
            
            return result
        
        book_gen._save_chapter = custom_save_chapter
        
        # Override the generate_chapter method to get real-time updates
        original_generate_chapter = book_gen.generate_chapter
        
        def custom_generate_chapter(chapter_number, prompt):
            # Update the UI
            generation_status["current_chapter"] = chapter_number
            update_status(f"Generating Chapter {chapter_number}", 
                         base_progress + ((chapter_number - 1) * progress_per_chapter))
            
            # Call the original method
            return original_generate_chapter(chapter_number, prompt)
        
        book_gen.generate_chapter = custom_generate_chapter
        
        # Generate the book
        book_gen.generate_book(outline)
        
        # Create a combined book file
        update_status("Creating complete book file", 95)
        with open("book_output/complete_book.txt", "w", encoding="utf-8") as book_file:
            # Add title page
            book_file.write("# THE SHADOW OF MUAD'DIB\n\n")
            book_file.write("*The untold story of Jeff, friend of Paul Atreides*\n\n")
            
            # Add table of contents
            book_file.write("## TABLE OF CONTENTS\n\n")
            for chapter in outline:
                book_file.write(f"Chapter {chapter['chapter_number']}: {chapter['title']}\n")
            book_file.write("\n\n")
            
            # Add each chapter
            for chapter in outline:
                chapter_file = os.path.join("book_output", f"chapter_{chapter['chapter_number']:02d}.txt")
                if os.path.exists(chapter_file):
                    with open(chapter_file, "r", encoding="utf-8") as f:
                        chapter_content = f.read()
                        book_file.write(f"\n\n{chapter_content}\n\n")
                        book_file.write("\n" + "=" * 50 + "\n")
        
        # Finalize
        update_status("Book generation complete", 100)
        add_log_message("Book generation completed successfully!")
        add_log_message(f"Generated {num_chapters} chapters")
        add_log_message("Book saved to book_output/complete_book.txt")
        
        # Reset print function
        builtins.print = original_print
        
    except Exception as e:
        add_log_message(f"Error during generation: {str(e)}")
        import traceback
        add_log_message(traceback.format_exc())
    finally:
        generation_status["is_generating"] = False
        socketio.emit('generation_complete')

def start_server(port=5000, open_browser=True):
    """Start the Flask server"""
    if open_browser:
        webbrowser.open(f'http://localhost:{port}')
    socketio.run(app, host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    start_server()
