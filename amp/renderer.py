import os
import json
import glob
from moviepy import ColorClip, TextClip, CompositeVideoClip

def render_latest_video():
    # Find the latest bundle JSON in amp/drafts/
    list_of_files = glob.glob('amp/drafts/bundle_*.json')
    if not list_of_files:
        print("No bundle drafts found to render.")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(latest_file, 'r') as f:
        bundle = json.load(f)
        
    short_data = bundle.get("youtube_tiktok_short", {})
    script = short_data.get("script", "Wealth sovereignty is here.")
    
    print(f"Rendering vertical video script...")
    
    # Create a vertical 9:16 background (Matter 1B dark navy palette: 1080x1920)
    bg_clip = ColorClip(size=(1080, 1920), color=(15, 23, 42)).with_duration(10)
    
    # Create text clip for the short video script overlay
    txt_clip = (
        TextClip(
            text=script,
            font_size=55,
            color='white',
            size=(900, None),
            method='caption'
        )
        .with_position('center')
        .with_duration(10)
    )
    
    # Composite the video layers
    video = CompositeVideoClip([bg_clip, txt_clip])
    
    # Ensure output directory exists
    os.makedirs("amp/videos", exist_ok=True)
    output_path = "amp/videos/latest_short.mp4"
    
    # Write the compiled file out
    video.write_videofile(output_path, fps=24, codec='libx264', audio=False)
    print(f"Successfully rendered video to {output_path}")

if __name__ == "__main__":
    render_latest_video()
