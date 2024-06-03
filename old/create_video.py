
from moviepy.editor import *
import moviepy.editor as mpe
from moviepy.video.fx.all import speedx
from moviepy.video.tools.drawing import color_gradient
from pydub import AudioSegment
from PIL import Image
import json


def run_video():
    # Example usage
    audio_file = 'sound_1.mp3'
    output_file = 'output_video.mp4'
    # load json
    data = json.load(open('data.json'))
    
    create_highlighted_video(audio_file, data, output_file)
    
def create_anime_video_halftime(file_path: str):
    # Load data from the JSON file
    data = json.load(open(file_path))

    # Folder containing the images
    image_folder = "mouths"

    # Mapping of shape to image filename
    shape_to_file = {
        "mid": f"{image_folder}/mid.png",
        "closed": f"{image_folder}/closed.png",
        "open": f"{image_folder}/open.png"
    }
    
    clips = []
    for entry in data:
        shape = entry['shape']
        start = entry['start']
        end = entry['end']
        duration = end - start
        print(shape, duration)
        
        image_clip = mpe.ImageClip(shape_to_file[shape], duration=duration)
        image_clip = image_clip.set_start(start).set_end(end)
        
        clips.append(image_clip)
        
    # Concatenate the clips
    video = mpe.concatenate_videoclips(clips, method="compose")

    # Apply the speed effect to make the video run at half speed
    video = speedx(video, factor=0.5)

    # Specify the audio file
    audio_file = "example/sound_1.mp3"  # Replace with the path to your audio file

    # Load the audio file
    audio = mpe.AudioFileClip(audio_file)

    # Apply the speed effect to make the audio run at half speed
    audio = speedx(audio, factor=0.5)

    # Set the slowed audio to the slowed video
    video = video.set_audio(audio)

    # Write the final video to a file
    video.write_videofile("mouth_shapes_video_with_audio_slow.mp4", fps=24)  # Use 12 fps to match half speed
    
def create_anime_video(file_path: str):
    
    # data = json.load(open('data.json'))
    data = json.load(open(file_path))
    # Folder containing the images
    image_folder = "mouths"

    # Mapping of shape to image filename
    shape_to_file = {
        "E": f"{image_folder}/B.png",
        "M": f"{image_folder}/A.png",
        "A": f"{image_folder}/D.png"
    }
    
    clips = []
    for entry in data:
        shape = entry['shape']
        start = entry['start']
        end = entry['end']
        duration = end - start
        print(shape, duration)
        
        image_clip = mpe.ImageClip(shape_to_file[shape], duration=duration)
        image_clip = image_clip.set_start(start).set_end(end)
        
        clips.append(image_clip)
        
    # Concatenate the clips
    video = mpe.concatenate_videoclips(clips, method="compose")

    # Specify the audio file
    audio_file = "example/sound_1.mp3"  # Replace with the path to your audio file

    # Load the audio file
    audio = mpe.AudioFileClip(audio_file)

    # Set the audio to the video
    video = video.set_audio(audio)

    # Write the final video to a file
    video.write_videofile("whisper.mp4", fps=24)

def create_highlighted_video(audio_file, data, output_file):
    # Load audio
    audio = AudioSegment.from_file(audio_file)

    # Calculate video duration
    duration = len(audio) / 1000

    # Create a blank background
    bg_color = (255, 255, 255)  # white background
    width, height = 1280, 720
    background = ColorClip(size=(width, height), color=bg_color, duration=duration * 2)  # double the duration

    # Create text clips for each word with timing information
    text_clips = []
    char_clips = []
    
    for entry in data:
        words = entry['words']
        chars = entry['chars']
        
        for word in words:
            word_text = word['word']
            word_start = word['start'] * 2  # double the start time
            word_end = word['end'] * 2  # double the end time
            
            # Create a text clip for the word
            text_clip = TextClip(word_text, fontsize=70, color='black', font='Arial-Bold')
            text_clip = text_clip.set_start(word_start).set_end(word_end).set_position(('center', height // 3))
            text_clips.append(text_clip)
            
        for char in chars:
            char_text = char['char']
            if 'start' in char and 'end' in char:  # Only create clips for characters with timing information
                char_start = char['start'] * 2  # double the start time
                char_end = char['end'] * 2  # double the end time

                # Create a text clip for the character
                char_clip = TextClip(char_text, fontsize=40, color='red', font='Arial-Bold')
                char_clip = char_clip.set_start(char_start).set_end(char_end).set_position(('center', height // 2))
                char_clips.append(char_clip)

    # Composite the background, word text clips, and character text clips
    video = CompositeVideoClip([background] + text_clips + char_clips)

    # Add audio to the video
    audio_clip = AudioFileClip(audio_file).fx(vfx.speedx, 0.5)  # slow down audio
    video = video.set_audio(audio_clip)

    # Write the result to a file
    video.write_videofile(output_file, fps=12)  # half the fps to maintain smooth playback
    
def make_shapes_more_sparse(file_path):
    threshold=0.05
    data = json.load(open(file_path))    
    
    sparse_data = []
    current_shape = data[0]["shape"]
    current_start = data[0]["start"]
    current_end = data[0]["end"]

    for entry in data[1:]:
        shape = entry["shape"]
        start = entry["start"]
        end = entry["end"]

        # If the shape is the same, extend the current interval
        if shape == current_shape:
            current_end = end
        else:
            # If the shape changes, save the current interval and start a new one
            if current_end - current_start > threshold:
                sparse_data.append({"shape": current_shape, "start": current_start, "end": current_end})
            current_shape = shape
            current_start = start
            current_end = end

    # Append the last interval
    if current_end - current_start > threshold:
        sparse_data.append({"shape": current_shape, "start": current_start, "end": current_end})

    with open('sparse_data.json', 'w') as f:
        json.dump(sparse_data, f, indent=4)

if __name__ == "__main__":
    create_anime_video('data/shape_data.json')