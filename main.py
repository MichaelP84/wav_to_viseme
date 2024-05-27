import whisperx
import gc 
import json
import modal
from modal import Image


from moviepy.editor import *
from moviepy.video.tools.drawing import color_gradient
from pydub import AudioSegment


stub = modal.Stub("whisperX")

whisperX = Image.debian_slim().pip_install(
    "pytorch==2.0.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia", "git+https://github.com/m-bain/whisperx.git"
)


def main():
    device = "cpu" 
    audio_file = "recording_2.m4a"
    batch_size = 16 # reduce if low on GPU mem
    compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)

    # 1. Transcribe with original whisper (batched)
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)

    # save model to local path (optional)
    # model_dir = "/path/"
    # model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)

    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    print(result["segments"]) # before alignment
    print("before alignment: ", result["segments"])
    # delete model if low on GPU resources
    # import gc; gc.collect(); torch.cuda.empty_cache(); del model

    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=True)

    with open('data.json', 'w') as f:
        json.dump(result["segments"], f, indent=4)
        

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

if __name__ == '__main__':
    main()
    # run_video()