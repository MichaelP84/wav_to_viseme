from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, VideoFileClip

data_path = "/Users/michaelpasala/Projects/Toona/wav_to_viseme/Rhubarb-Lip-Sync-1.13.0-macOS/output.txt"
mouths_path = "/Users/michaelpasala/Projects/Toona/wav_to_viseme/mouths/"
audio_path = "example/sound_1.mp3"

def create_video_from_timestamps(file_path, output_file):
    # Read the data from the text file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Parse the lines into a list of tuples (timestamp, letter)
    data = []
    for line in lines:
        timestamp, letter = line.strip().split()
        data.append((float(timestamp), letter))
            
    # Create clips for each image with the duration until the next timestamp
    clips = []
    for i in range(len(data) - 1):
        start_time = data[i][0]
        end_time = data[i + 1][0]
        letter = data[i][1]
        duration = end_time - start_time
        image_path = mouths_path + f"{letter}.png"
        clip = ImageClip(image_path).set_duration(duration).set_start(start_time)
        clips.append(clip)
    
    # Concatenate all clips into a single video
    video = concatenate_videoclips(clips, method="compose")
    
    # Load the audio file
    audio = AudioFileClip(audio)
    
    # Check if the audio is loaded properly
    if audio is None or audio.duration == 0:
        raise ValueError("Failed to load the audio file or the audio file is empty")

    print(f"Audio loaded successfully: duration = {audio.duration} seconds")

    # Set the audio to the video
    final_video = video.set_audio(audio)

    # Save the final video
    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")

def main():
    create_video_from_timestamps(data_path, "output.mp4")

if __name__ == "__main__":
    main()
