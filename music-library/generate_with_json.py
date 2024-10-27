import os
import json
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

# Define the root folder where the MP3 files are located
root_folder = '/mnt/extusb/BK-Songs'

# Define the output JSON and HTML files
output_json = 'music_data.json'
output_html = 'music_library.html'

# Function to convert file size from bytes to human-readable format
def human_readable_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024

# Function to convert seconds into minutes:seconds format
def format_duration(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02}"

# Function to extract metadata like artist name, album name, and duration
def extract_metadata(mp3_path):
    try:
        audio = MP3(mp3_path, ID3=EasyID3)
        # Extract duration, album, artist
        duration = format_duration(audio.info.length)
        album = audio.get('album', ['Unknown Album'])[0]
        artist = audio.get('artist', ['Unknown Artist'])[0]
    except Exception:
        duration = "Unknown"
        album = "Unknown Album"
        artist = "Unknown Artist"
    
    return duration, album, artist

# Traverse the root folder and collect all MP3 files and their metadata
def find_mp3_files(root_folder):
    mp3_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.mp3'):
                relative_path = os.path.relpath(os.path.join(dirpath, filename), root_folder)
                full_path = os.path.join(dirpath, filename)
                file_size = os.path.getsize(full_path)
                duration, album, artist = extract_metadata(full_path)
                mp3_files.append({
                    'relative_path': relative_path,
                    'file_name': filename,
                    'file_size': human_readable_size(file_size),
                    'duration': duration,
                    'album': album,
                    'artist': artist
                })
    return mp3_files

# Generate the JSON file with song metadata
def generate_json_file(root_folder, output_json):
    mp3_files = find_mp3_files(root_folder)
    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(mp3_files, json_file, indent=4)
    print(f'JSON file generated: {output_json}')

# Call the function to generate the JSON file
generate_json_file(root_folder, output_json)

# HTML template that will load the JSON file and display the song list dynamically
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BK Music Library</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ font-family: Arial, sans-serif; }}
    </style>
    <script>
        // Fetch the JSON file and populate the song list
        document.addEventListener('DOMContentLoaded', function() {{
            fetch('music_data.json')
                .then(response => response.json())
                .then(data => {{
                    let songListDiv = document.getElementById('songList');
                    data.forEach(song => {{
                        let songDiv = document.createElement('div');
                        songDiv.classList.add('song', 'bg-white', 'p-4', 'rounded-lg', 'shadow-md');
                        
                        // Create song details
                        let songTitle = `<p class="font-semibold song-title">${song.file_name}</p>`;
                        let songAlbum = `<p class="song-album">Album: ${song.album}</p>`;
                        let songArtist = `<p class="song-artist">Artist: ${song.artist}</p>`;
                        let songDuration = `<p>Duration: ${song.duration}</p>`;
                        let songFileSize = `<p>File Size: ${song.file_size}</p>`;
                        let playButton = `<button class="play-button text-indigo-500 mt-2 underline" onclick="playSong('${song.relative_path}')">Play</button>`;
                        
                        // Append to songDiv
                        songDiv.innerHTML = songTitle + songAlbum + songArtist + songDuration + songFileSize + playButton;
                        songListDiv.appendChild(songDiv);
                    }});
                }});
        }});

        // Play song using the single audio player
        function playSong(filePath) {{
            var audioPlayer = document.getElementById('audioPlayer');
            var source = document.getElementById('audioSource');
            source.src = '../' + filePath;
            audioPlayer.load();
            audioPlayer.play();
        }}

        // Search function to filter songs by title, album, or artist
        function searchSongs() {{
            var input = document.getElementById('searchBar').value.toLowerCase();
            var songs = document.getElementsByClassName('song');
            for (var i = 0; i < songs.length; i++) {{
                var songTitle = songs[i].getElementsByClassName('song-title')[0].textContent.toLowerCase();
                var songAlbum = songs[i].getElementsByClassName('song-album')[0].textContent.toLowerCase();
                var songArtist = songs[i].getElementsByClassName('song-artist')[0].textContent.toLowerCase();
                
                // If search input matches the song title, album, or artist, show the song
                if (songTitle.includes(input) || songAlbum.includes(input) || songArtist.includes(input)) {{
                    songs[i].style.display = '';
                }} else {{
                    songs[i].style.display = 'none';
                }}
            }}
        }}
    </script>
</head>
<body class="bg-gray-100 p-5">
    <div class="container mx-auto">
        <h1 class="text-3xl font-bold text-center mb-6">Music Library</h1>
        <!-- Search Bar -->
        <input type="text" id="searchBar" onkeyup="searchSongs()" placeholder="Search for songs, albums, or artists..." class="w-full p-3 mb-6 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
        
        <!-- Song List -->
        <div id="songList" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"></div>

        <!-- Single Audio Player -->
        <div class="fixed bottom-0 left-0 right-0 bg-white p-4 mb-20 pb-10 border-t border-gray-300">
            <audio id="audioPlayer" controls class="w-full">
                <source id="audioSource" src="" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        </div>
    </div>
</body>
</html>
'''

# Write the HTML content to the output HTML file
with open(output_html, 'w', encoding='utf-8') as file:
    file.write(html_template)

print(f'HTML file generated: {output_html}')
