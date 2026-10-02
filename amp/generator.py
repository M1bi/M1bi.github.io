import os
import json
from datetime import datetime
from groq import Groq

def generate_content():
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = """
    You are the lead conversion copywriter for Matter1B.com, driving automated traffic and ebook sales for the Matter 1B framework.
    Matter 1B is a peer-to-peer economic architecture, open-source super-app, and DAO focused on wealth sovereignty, 
    natural-law alignment, and eliminating financial intermediaries.
    
    Generate a synchronized daily multi-platform content bundle. 
    CRITICAL INSTRUCTION FOR THE SCRIPT: The spoken video script must be pure spoken-word dialogue ONLY. Never include stage directions, speaker labels, or acronyms like 'CTA'. It must flow naturally, start with an intense pattern-interrupt hook about financial gridlock or wealth freedom, and naturally conclude by telling the viewer to grab the ebook at Matter1B.com.
    
    Return the output strictly in valid JSON format with the following top-level keys:
    - "date": Current generation timestamp string.
    - "youtube_tiktok_short": {
        "title": "High-converting short title under 60 characters with hashtags",
        "script": "Natural, spoken 30-second script focusing on ebook availability at https://matter1b.com",
        "visual_cues": "Brief background visual notes"
      },
    - "substack_post": {
        "headline": "Compelling long-form article title highlighting wealth sovereignty",
        "subtitle": "Engaging subtitle preview",
        "video_section": "Note on how the video ties into this essay",
        "essay_body": "Detailed 300+ word markdown essay expanding on natural-law economics, concluding with an explicit call to read the Matter 1B series at https://matter1b.com"
      },
    - "professional_social": {
        "linkedin": "Thought-leadership post on system architecture and economic sovereignty with link to https://matter1b.com",
        "x_twitter": "Punchy thread starter exposing financial middlemen with link to https://matter1b.com"
      },
    - "decentralized_social": {
        "bluesky": "Community update on decentralized sovereign apps with link to https://matter1b.com",
        "threads": "Conversational take on natural law and financial freedom with link to https://matter1b.com"
      }
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    content = json.loads(response.choices[0].message.content)
    content["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    os.makedirs("amp/drafts", exist_ok=True)
    filename = f"amp/drafts/bundle_{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"
    
    with open(filename, "w") as f:
        json.dump(content, f, indent=4)
        
    print(f"Successfully generated master multi-platform bundle: {filename}")

if __name__ == "__main__":
    generate_content()
