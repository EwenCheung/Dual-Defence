#!/usr/bin/env python3
"""
Audio conversion script for pygbag web deployment
Converts WAV/MP3 files to OGG format for web compatibility
"""

import subprocess
import sys
import os
from pathlib import Path

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_audio_file(input_path, output_path):
    """Convert a single audio file to OGG format"""
    try:
        cmd = [
            'ffmpeg', '-i', str(input_path),
            '-c:a', 'libvorbis',
            '-q:a', '6',  # Quality level (0-10, 6 is good quality)
            str(output_path),
            '-y'  # Overwrite output file if it exists
        ]
        
        print(f"Converting {input_path} -> {output_path}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully converted {input_path}")
            return True
        else:
            print(f"❌ Failed to convert {input_path}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error converting {input_path}: {e}")
        return False

def main():
    """Main conversion function"""
    
    # Check if FFmpeg is available
    if not check_ffmpeg():
        print("❌ FFmpeg is not installed or not in PATH")
        print("Please install FFmpeg:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu: sudo apt install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/")
        return False
    
    print("🎵 Converting audio files for web deployment...")
    
    # Define audio files to convert
    audio_files = [
        ("Stick of War/Music/home_music.wav", "Stick of War/Music/home_music.ogg"),
        ("Stick of War/Music/game_music.mp3", "Stick of War/Music/game_music.ogg"),
        ("Stick of War/Music/level.mp3", "Stick of War/Music/level.ogg"),
        ("Bokemon vs Stick/audio/bg_music.mp3", "Bokemon vs Stick/audio/bg_music.ogg"),
    ]
    
    success_count = 0
    total_count = len(audio_files)
    
    for input_file, output_file in audio_files:
        input_path = Path(input_file)
        output_path = Path(output_file)
        
        if not input_path.exists():
            print(f"⚠️  Input file not found: {input_path}")
            continue
            
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if convert_audio_file(input_path, output_path):
            success_count += 1
    
    print(f"\n🎯 Conversion complete: {success_count}/{total_count} files converted")
    
    if success_count == total_count:
        print("✅ All audio files converted successfully!")
        print("You can now run: pygbag main.py")
        return True
    else:
        print("⚠️  Some files failed to convert. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
