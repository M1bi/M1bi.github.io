import os
import json
from datetime import datetime
from groq import Groq

def generate_content():
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = """
    You are the master content engine for 'Matter 1B Amp', an autonomous growth engine for Matter1B.com.
    Matter 1B is an open-source super-app and DAO focused on wealth sovereignty, natural-law alignment, 
    cognitive sovereignty, and eliminating financial intermediaries.
    
    Generate a comprehensive, synchronized daily multi-platform content bundle focusing on a 
    'gridlock to breakthrough' narrative.
    
    Return the output strictly in valid JSON format with the following top-level keys:
    - "date": Current generation timestamp string.
    - "youtube_tiktok_short": {{
        "title": "Catchy short title under 60 characters with hashtags",
        "script": "Spoken video script under 70 words with a fast-paced hook and CTA to https://matter1b.com",
        "visual_cues": "Brief instructions for background visuals or text overlays"
      }}
    - "substack_post": {{
        "headline": "Compelling long-form article title",
        "subtitle": "Engaging subtitle preview",
        "video_section": "Note on how the daily video ties into this essay",
        "essay_body": "Detailed 300+ word markdown essay expanding on natural-law economic design, wealth sovereignty, or ecological stewardship, concluding with a link to https://matter1b.com"
      }}
    - "professional_social": {{
        "linkedin": "Thought-leadership post breaking down the architectural or systemic perspective for professionals, with link to https://matter1b.com",
        "x_twitter": "Punchy, high-engagement thread starter or statement under 280 characters with a link to https://matter1b.com"
      }}
    - "decentralized_social": {{
        "bluesky": "Community-focused update highlighting open-source sovereignty and gridlock-to-breakthrough, with link to https://matter1b.com",
        "threads": "Conversational, engaging take on financial intermediaries and natural law, with link to https://matter1b.com"
      }}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    content = json.loads(response.choices[0].message.content)
    content["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Ensure drafts directory exists and save the master bundle
    os.makedirs("amp/drafts", exist_ok=True)
    filename = f"amp/drafts/bundle_{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"
    
    with open(filename, "w") as f:
        json.dump(content, f, indent=4)
        
    print(f"Successfully generated master multi-platform bundle: {filename}")

if __name__ == "__main__":
    generate_content()
