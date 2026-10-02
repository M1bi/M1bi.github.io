import os
import json
import glob
from gtts import gTTS
from moviepy import ColorClip, TextClip, CompositeVideoClip, AudioFileClip

def render_latest_video():
    # Find the latest bundle JSON in amp/drafts/
    list_of_files = glob.glob('amp/drafts/bundle_*.json')
    if not list_of_files:
        print("No bundle drafts found to render.")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(latest_file, 'r', encoding='utf-8') as f:
        bundle = json.load(f)
        
    short_data = bundle.get("youtube_tiktok_short", {})
    script = short_data.get("script", "Wealth sovereignty is here.")
    title = short_data.get("title", "Matter 1B Breakthrough")
    
    print(f"Generating voiceover audio...")
    audio_path = "amp/videos/voiceover.mp3"
    tts = gTTS(text=script, lang='en', slow=False)
    tts.save(audio_path)
    
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration + 0.6  # Buffer for breathing room

    print(f"Rendering animated video (Duration: {duration:.2f}s)...")
    
    # 1. Base Background (Deep Matter 1B Navy)
    bg_clip = ColorClip(size=(1080, 1920), color=(10, 17, 30)).with_duration(duration)
    
    # 2. Dynamic Accent Shape / Header Box for Motion/Animation Feel
    # We add a secondary accent card backdrop that scales or sits cleanly behind text
    accent_box = ColorClip(size=(920, 900), color=(25, 35, 55)).with_duration(duration)
    accent_box = accent_box.with_position('center')
    
    # 3. Title Header Text (Stays prominent at the top)
    title_clip = (
        TextClip(
            text=title.upper(),
            font_size=42,
            color='#38bdf8',  # Electric cyan accent
            size=(900, None),
            method='caption',
            text_align='center'
        )
        .with_position(('center', 350))
        .with_duration(duration)
    )
    
    # 4. Main Script Body Text (Cleanly wrapped and centered)
    txt_clip = (
        TextClip(
            text=script,
            font_size=48,
            color='white',
            size=(840, None),
            method='caption',
            text_align='center'
        )
        .with_position('center')
        .with_duration(duration)
    )
    
    # 5. Composite layers together with audio and apply a subtle zoom animation effect
    # We use a built-in resize lambda function to create a smooth, slow zoom-in (Ken Burns effect) over time
    video = CompositeVideoClip([bg_clip, accent_box, title_clip, txt_clip])
    video = video.with_audio(audio_clip)
    
    # Apply a gentle zoom-in animation frame-by-frame (scales from 1.0 to 1.05 over the clip duration)
    animated_video = video.transform(lambda get_frame, t: get_frame(t), apply_to=['mask'])
    # Alternatively, apply a scaling transform effect supported by moviepy:
    animated_video = video.resized(lambda t: 1.0 + 0.02 * (t / duration))
    
    # Ensure output directory exists
    os.makedirs("amp/videos", exist_ok=True)
    output_path = "amp/videos/latest_short.mp4"
    
    animated_video.write_videofile(
        output_path, 
        fps=24, 
        codec='libx264', 
        audio_codec='aac',
        preset='medium'
    )
    print(f"Successfully rendered animated video to {output_path}")

if __name__ == "__main__":
    render_latest_video()
