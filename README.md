# Split Audio with Tracklist Metadata

🚀 A Python script to split an audio file (`.mp3`) into multiple tracks based on a tracklist and embed metadata (artist & title) for Last.fm scrobbling.

## Features
✅ Splits an MP3 file into individual tracks  
✅ Reads tracklist from a text file  
✅ Automatically tags each track with **artist** and **title** metadata  
✅ Saves output in `output_tracks/`  
✅ Works with Last.fm scrobblers  

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/split-audio.git
   cd split-audio
2. Install Dependencies 
    ```bash
   pip install -r requirements.txt
3. Ensure FFmpeg is installed (Required for pydub):
   MacOS (with Homebrew):
   ```bash
   brew install ffmpeg

## Usage
Prepare your tracklist.txt like this:

0:00:25
Artist #1
Song Title #1

0:06:10
Artist #2
Song Title #1

.
.
.


Each track should have:

A start time (hh:mm:ss or mm:ss)
An artist name
A track title

To run the script:
   ```bash
   python split_audio.py input.mp3 tracklist.txt

Your tracks are now in the output_tracks directory!







