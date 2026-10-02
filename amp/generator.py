import os
import json
from datetime import datetime
from groq import Groq

def generate_content():
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = """
    You are the content engine for 'Matter 1B Amp', an autonomous growth channel for Matter1B.com.
    Matter 1B is an open-source super-app and DAO focused on wealth sovereignty, natural-law alignment, 
    and eliminating financial intermediaries.
    
    Generate a high-converting, punchy 30-second YouTube Short script. 
    Focus on a 'gridlock to breakthrough' narrative emphasizing ecological stewardship and cognitive sovereignty.
    
    Return the output strictly in JSON format with the following keys:
    - "title": A catchy YouTube title under 60 characters with hashtags.
    - "script": The spoken text for the video (under 70 words, fast-paced hook).
    - "description": The YouTube description including a clear call-to-action driving traffic to https://matter1b.com.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    content = json.loads(response.choices[0].message.content)
    
    # Ensure drafts directory exists and save the file with a timestamp
    os.makedirs("amp/drafts", exist_ok=True)
    filename = f"amp/drafts/draft_{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"
    
    with open(filename, "w") as f:
        json.dump(content, f, indent=4)
        
    print(f"Successfully generated review draft: {filename}")

if __name__ == "__main__":
    generate_content()
