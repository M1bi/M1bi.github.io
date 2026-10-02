import os
import json
import time
import glob
from datetime import datetime
from groq import Groq, RateLimitError

def load_config():
    config_path = "amp/config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"engine_status": "active", "current_campaign_focus": "Matter 1B wealth sovereignty", "active_library_sources": []}

def load_selected_library(config):
    """Loads only the specific library sources listed in the config file to protect token limits."""
    library_texts = ""
    active_sources = config.get("active_library_sources", [])
    
    for source_path in active_sources:
        if os.path.exists(source_path):
            with open(source_path, 'r', encoding='utf-8') as f:
                filename = os.path.basename(source_path)
                library_texts += f"\n\n--- SOURCE FILE: {filename} ---\n" + f.read()
        else:
            print(f"Warning: Configured library source not found: {source_path}")
            
    if not library_texts:
        # Fallback if no specific files are listed yet
        all_files = glob.glob('library/**/*.md', recursive=True) + glob.glob('library/**/*.txt', recursive=True)
        for file_path in all_files[:2]: # Grab first two files as safe default
            with open(file_path, 'r', encoding='utf-8') as f:
                library_texts += f"\n\n--- SOURCE: {os.path.basename(file_path)} ---\n" + f.read()
                
    if not library_texts:
        library_texts = "No library files found. Focus on foundational Matter 1B principles."
    
    return library_texts

def generate_content():
    config = load_config()
    
    # Respect the Pause Switch
    if config.get("engine_status", "active").lower() != "active":
        print("Amp Engine is currently PAUSED via amp/config.json. Exiting safely.")
        return

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    library_content = load_selected_library(config)
    campaign_focus = config.get("current_campaign_focus")
    
    prompt = f"""
    You are the lead conversion copywriter for Matter1B.com, driving automated traffic and ebook sales.
    
    CURRENT CAMPAIGN STRATEGY:
    {campaign_focus}
    
    FOUNDATIONAL LIBRARY REFERENCE:
    {library_content}
    
    INSTRUCTIONS TO AVOID REDUNDANCY:
    Select a specific, unique concept, chapter, or architectural point from the library text above that has not been over-utilized. Build today's multi-platform bundle entirely around that angle.
    
    CRITICAL SCRIPT RULE: Spoken video script must be pure spoken-word dialogue ONLY. No stage directions, no labels, no 'CTA'. Start with a sharp pattern-interrupt hook and conclude by directing viewers to grab the ebook at https://matter1b.com.
    
    Return the output strictly in valid JSON format with the following top-level keys:
    - "date": Current generation timestamp string.
    - "youtube_tiktok_short": {{
        "title": "High-converting short title under 60 characters with hashtags",
        "script": "Natural, spoken 30-second script focusing on ebook availability at https://matter1b.com",
        "visual_cues": "Brief background visual notes"
      }},
    - "substack_post": {{
        "headline": "Compelling long-form article title highlighting wealth sovereignty",
        "subtitle": "Engaging subtitle preview",
        "video_section": "Note on how the video ties into this essay",
        "essay_body": "Detailed 300+ word markdown essay drawing directly from the provided library text, concluding with a link to https://matter1b.com"
      }},
    - "professional_social": {{
        "linkedin": "Thought-leadership post on system architecture with link to https://matter1b.com",
        "x_twitter": "Punchy thread starter exposing financial middlemen with link to https://matter1b.com"
      }},
    - "decentralized_social": {{
        "bluesky": "Community update on decentralized sovereign apps with link to https://matter1b.com",
        "threads": "Conversational take on natural law and financial freedom with link to https://matter1b.com"
      }}
    """

    # Rate-Throttling & Backoff Execution Loop
    max_retries = 3
    retry_delay = config.get("throttle_settings", {}).get("api_retry_delay_seconds", 15)
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            content = json.loads(response.choices[0].message.content)
            content["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            os.makedirs("amp/drafts", exist_ok=True)
            filename = f"amp/drafts/bundle_{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"
            
            with open(filename, "w", encoding='utf-8') as f:
                json.dump(content, f, indent=4)
                
            print(f"Successfully generated controlled library bundle: {filename}")
            return
            
        except RateLimitError:
            print(f"Groq API rate limit hit (Attempt {attempt + 1}/{max_retries}). Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except Exception as e:
            print(f"Error during generation: {e}")
            raise e

if __name__ == "__main__":
    generate_content()
