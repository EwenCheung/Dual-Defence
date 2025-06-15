# Web Conversion Instructions

## Steps to make your game web-ready with pygbag:

### 1. Install pygbag
```bash
pip install pygbag
```

**Note:** If `pygbag` command is not found, use:
- macOS/Linux: `python3 -m pygbag`
- Windows: `py -m pygbag` or `python -m pygbag`

### 2. Convert audio files to OGG format
You need to convert these audio files to OGG format for web compatibility:
- `Stick of War/Music/home_music.wav` → `Stick of War/Music/home_music.ogg`
- `Stick of War/Music/game_music.mp3` → `Stick of War/Music/game_music.ogg`
- `Stick of War/Music/level.mp3` → `Stick of War/Music/level.ogg`
- `Bokemon vs Stick/audio/bg_music.mp3` → `Bokemon vs Stick/audio/bg_music.ogg`

**Convert using FFmpeg:**
```bash
ffmpeg -i "Stick of War/Music/home_music.wav" -c:a libvorbis "Stick of War/Music/home_music.ogg"
ffmpeg -i "Stick of War/Music/game_music.mp3" -c:a libvorbis "Stick of War/Music/game_music.ogg"
ffmpeg -i "Stick of War/Music/level.mp3" -c:a libvorbis "Stick of War/Music/level.ogg"
ffmpeg -i "Bokemon vs Stick/audio/bg_music.mp3" -c:a libvorbis "Bokemon vs Stick/audio/bg_music.ogg"
```

### 3. Add a favicon (optional)
Add a square PNG image named `favicon.png` in the root directory for the web app icon.

### 4. Build for web
Run pygbag from the game directory:
```bash
pygbag main.py
```

**Additional build options:**
- For auto-start without user interaction: `pygbag main.py --ume_block=0`
- For 3D/WebGL games: `pygbag main.py --template noctx.tmpl`
- For heightmaps in assets: `pygbag main.py --no_opt`

### 5. Test locally
After building, pygbag will serve your game locally. Open the provided URL in your browser to test.

## Changes Made for Web Compatibility:

1. **Added PEP 723 metadata** at the top for dependencies
2. **Made the main function async** with proper asyncio handling
3. **Added `await asyncio.sleep(0)`** in each game loop iteration
4. **Added platform detection** with `IS_WEB = sys.platform == "emscripten"`
5. **Platform-specific audio loading** (OGG for web, original formats for desktop)
6. **Added pixelated rendering** for consistent look across devices
7. **Set background color** around pygame screen for better web appearance
8. **Improved error handling** (no print statements on web for performance)
9. **Updated requirements.txt** to use pygame-ce
10. **Created pygbag.ini** configuration file

## Important Performance Notes:

- **Remove all debug `print()` calls** - they significantly reduce performance in browsers
- **Use `await asyncio.sleep(0)`** in every game loop iteration
- **Audio files MUST be OGG format** for web deployment
- **Use forward slashes (/)** in file paths for cross-platform compatibility

## Platform-specific Features:

### Web-only features you can add:
```python
if IS_WEB:
    # Change page background color
    platform.document.body.style.background = "#404040"
    
    # Save/load persistent data
    from platform import window
    # Save: window.localStorage.setItem("mygame", str(value))
    # Load: value = window.localStorage.getItem("mygame")
    
    # Download files created by the game
    # platform.window.MM.download("filename.txt")
```

## Debugging:
- Use `http://localhost:8000?-i` for REPL access while debugging
- Replace `import asyncio` with `import pygbag.aio as asyncio` for desktop simulation

## Build Commands:

**Basic build:**
```bash
pygbag main.py
```

**Build with auto-start:**
```bash
pygbag main.py --ume_block=0
```

**Build for specific Python version:**
```bash
pygbag main.py --PYBUILD 3.13
```
