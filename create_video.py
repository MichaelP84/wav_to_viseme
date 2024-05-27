
from moviepy.editor import *
from moviepy.video.tools.drawing import color_gradient
from pydub import AudioSegment


def run_video():
    # Example usage
    audio_file = 'sound_1.mp3'
    output_file = 'output_video.mp4'
    # load json
    data = json.load(open('data.json'))
    
    create_highlighted_video(audio_file, data, output_file)
        

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
