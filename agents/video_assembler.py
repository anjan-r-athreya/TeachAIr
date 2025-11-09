from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os
import re
from typing import List, Optional
from PIL import Image

def natural_sort_key(s: str) -> list:
    """
    Generate a sort key for natural sorting of strings containing numbers.
    Example: "script2.mp3" -> ["script", 2, ".mp3"]
    """
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split('([0-9]+)', s)
    ]

def find_matching_files(directory: str, prefix: str, extensions: List[str]) -> List[str]:
    """
    Find all files in the directory that match the given prefix and extensions.
    Returns a sorted list of matching file paths.
    """
    files = []
    for ext in extensions:
        files.extend([
            os.path.join(directory, f) for f in os.listdir(directory)
            if f.startswith(prefix) and f.lower().endswith(ext)
        ])
    return sorted(files, key=natural_sort_key)

def create_slideshow(
    output_dir: str = 'outputs',
    output_file: str = 'lecture_video.mp4',
    fps: int = 24,
    resolution: tuple = (1920, 1080)
) -> None:
    """
    Create a video lecture by combining slides with their corresponding audio scripts.
    
    Args:
        output_dir: Directory containing slide images and audio files
        output_file: Name of the output video file
        fps: Frames per second for the output video
        resolution: Video resolution as (width, height)
    """
    # Get absolute path to output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_dir)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    print(f"Looking for files in: {output_path}")
    
    # Find all slide images and audio files
    slide_files = find_matching_files(output_path, 'slide', ['.png', '.jpg', '.jpeg'])
    audio_files = find_matching_files(output_path, 'script', ['.mp3', '.wav'])
    
    if not slide_files or not audio_files:
        print("Error: Could not find matching slide and audio files.")
        print("Please ensure you have files named like:")
        print("  - slide1.png, slide2.png, etc.")
        print("  - script1.mp3, script2.mp3, etc.")
        return
    
    print(f"\nFound {len(slide_files)} slides and {len(audio_files)} audio files")
    
    # Create video clips for each slide-audio pair
    clips = []
    
    for i, (slide_path, audio_path) in enumerate(zip(slide_files, audio_files), 1):
        try:
            # Load audio and get its duration
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Create image clip with the same duration as audio
            image_clip = (
                ImageClip(slide_path)
                .set_duration(duration)
                .set_fps(fps)
                .resize(resolution, resample=Image.Resampling.LANCZOS)
                .set_audio(audio)
            )
            
            clips.append(image_clip)
            print(f"✓ Added: {os.path.basename(slide_path)} with {os.path.basename(audio_path)} ({duration:.1f}s)")
            
        except Exception as e:
            print(f"⚠️ Error processing slide {i}: {e}")
    
    if not clips:
        print("No valid slide-audio pairs found!")
        return
    
    # Concatenate all clips
    print("\nCombining all clips...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Write the final video
    output_video_path = os.path.join(output_path, output_file)
    print(f"\nCreating video: {output_video_path}")
    
    final_video.write_videofile(
        output_video_path,
        fps=fps,
        codec='libx264',
        audio_codec='aac',
        threads=4,
        preset='medium',
        ffmpeg_params=['-pix_fmt', 'yuv420p']  # Better compatibility
    )
    
    # Clean up
    final_video.close()
    for clip in clips:
        clip.close()
    
    print(f"\n✅ Video created successfully: {output_video_path}")
    print(f"Total duration: {final_video.duration/60:.1f} minutes")

if __name__ == "__main__":
    print("=== Lecture Video Generator ===\n")
    
    # Create the video with default settings
    create_slideshow(
        output_dir='outputs',
        output_file='lecture_video.mp4',
        fps=24,
        resolution=(1920, 1080)  # Full HD
    )