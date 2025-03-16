import os
import sys
from pydub import AudioSegment
from mutagen.id3 import ID3, TIT2, TPE1

def parse_tracklist(tracklist_file):
    """
    Parses the tracklist.txt file and returns a list of (start_time, artist, title).
    """
    tracks = []
    
    try:
        with open(tracklist_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        current_time = None
        current_artist = None

        for line in lines:
            line = line.strip()

            if not line:
                continue  # Skip empty lines

            if line[0].isdigit():  # If the line starts with a timecode (e.g., 0:06:10)
                current_time = parse_time(line)
            elif current_time is not None and current_artist is None:
                current_artist = line  # This line is the artist name
            elif current_artist is not None:
                tracks.append((current_time, current_artist, line))  # This line is the track title
                current_artist = None  # Reset for next track

        print(f"Parsed {len(tracks)} tracks from {tracklist_file}")
        return tracks

    except Exception as e:
        print(f"Error reading tracklist file: {e}")
        sys.exit(1)


def parse_time(time_str):
    """
    Converts a time string (hh:mm:ss or mm:ss) into milliseconds.
    """
    parts = list(map(int, time_str.split(":")))

    if len(parts) == 2:  # mm:ss format
        minutes, seconds = parts
        hours = 0
    elif len(parts) == 3:  # hh:mm:ss format
        hours, minutes, seconds = parts
    else:
        print(f"Invalid time format: {time_str}")
        sys.exit(1)

    milliseconds = (hours * 3600 + minutes * 60 + seconds) * 1000
    return milliseconds


def add_metadata(mp3_path, artist, title):
    """
    Adds ID3 metadata (artist and title) to an MP3 file.
    """
    try:
        tags = ID3()
        tags.add(TPE1(encoding=3, text=artist))  # Artist Name
        tags.add(TIT2(encoding=3, text=title))   # Track Title
        tags.save(mp3_path)
        print(f"  ✅ Metadata added: {artist} - {title}")
    except Exception as e:
        print(f"  ❌ Error adding metadata to {mp3_path}: {e}")


def split_audio(input_file, tracklist_file, output_folder="output_tracks"):
    """
    Splits an MP3 file into individual tracks based on the tracklist and saves them with metadata.
    """
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    print(f"Loading audio file: {input_file}")
    try:
        audio = AudioSegment.from_file(input_file)
        print(f"Audio length: {len(audio) / 1000:.2f} seconds")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        sys.exit(1)

    tracks = parse_tracklist(tracklist_file)

    for i, (start_time, artist, title) in enumerate(tracks):
        # Determine the end time
        end_time = tracks[i + 1][0] if i + 1 < len(tracks) else len(audio)

        print(f"Processing Track {i+1}: {artist} - {title}")
        print(f"  Start: {start_time / 1000:.2f}s | End: {end_time / 1000:.2f}s")

        # Extract the segment
        track_segment = audio[start_time:end_time]

        # Generate a simple filename without artist/title in the name
        filename = f"{i+1:02d}.mp3"
        output_path = os.path.join(output_folder, filename)

        print(f"  Exporting: {output_path}")

        # Export the file
        try:
            track_segment.export(output_path, format="mp3")
            add_metadata(output_path, artist, title)  # Add ID3 tags
            print(f"  ✅ Successfully saved: {filename}")
        except Exception as e:
            print(f"  ❌ Error exporting {filename}: {e}")

    print("\n✅ Audio splitting completed! Tracks saved in:", output_folder)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python split_audio.py <input.mp3> <tracklist.txt>")
        sys.exit(1)

    input_mp3 = sys.argv[1]
    tracklist_txt = sys.argv[2]

    split_audio(input_mp3, tracklist_txt)

