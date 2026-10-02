import os
import json
import glob
from gtts import gTTS
from moviepy import ColorClip, TextClip, CompositeVideoClip, AudioFileClip

def render_latest_video():
    list_of_files = glob.glob('amp/drafts/bundle_*.json')
    if not list_of_files:
        print("No bundle drafts found to render.")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(latest_file, 'r', encoding='utf-8') as f:
        bundle = json.load(f)
        
    short_data = bundle.get("youtube_tiktok_short", {})
    script = short_data.get("script", "Wealth sovereignty is here. Visit Matter1B.com.")
    title = short_data.get("title", "Matter 1B Breakthrough")
    
    print(f"Generating clean voiceover audio...")
    audio_path = "amp/videos/voiceover.mp3"
    tts = gTTS(text=script, lang='en', slow=False)
    tts.save(audio_path)
    
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration + 0.8  # Extra breathing room

    print(f"Rendering stable video layout (Duration: {duration:.2f}s)...")
    
    # 1. Matter 1B Deep Navy Background
    bg_clip = ColorClip(size=(1080, 1920), color=(10, 17, 30)).with_duration(duration)
    
    # 2. Card Panel Backdrop to keep layout crisp
    panel_clip = ColorClip(size=(940, 1100), color=(20, 30, 48)).with_duration(duration)
    panel_clip = panel_clip.with_position('center')
    
    # 3. Title Header (Cyan branding accent)
    title_clip = (
        TextClip(
            text=title.upper(),
            font_size=40,
            color='#38bdf8',
            size=(860, None),
            method='caption',
            text_align='center'
        )
        .with_position(('center', 460))
        .with_duration(duration)
    )
    
    # 4. Main Script Text (Clean white typography, strict sizing to prevent squiggles)
    txt_clip = (
        TextClip(
            text=script,
            font_size=44,
            color='white',
            size=(840, None),
            method='caption',
            text_align='center'
        )
        .with_position(('center', 580))
        .with_duration(duration)
    )
    
    # 5. Composite everything securely without risky scaling matrices
    video = CompositeVideoClip([bg_clip, panel_clip, title_clip, txt_clip])
    video = video.with_audio(audio_clip)
    
    os.makedirs("amp/videos", exist_ok=True)
    output_path = "amp/videos/latest_short.mp4"
    
    video.write_videofile(
        output_path, 
        fps=24, 
        codec='libx264', 
        audio_codec='aac',
        preset='medium'
    )
    print(f"Successfully rendered clean video to {output_path}")

if __name__ == "__main__":
    render_latest_video()
