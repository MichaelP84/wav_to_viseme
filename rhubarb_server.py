import modal
import subprocess
import base64
import os
import random
import string
from pydub import AudioSegment
import io


stub = modal.Stub("rhubarb")
modal_image = modal.Image.debian_slim().copy_local_dir("Rhubarb_Linux", "/root/Rhubarb").pip_install("pydub").run_commands("apt-get install ffmpeg -y")

def handle_base64_audio(base64_string: str, format: str, name: str):
    # Decode the base64 string
    print(len(base64_string))
    print("Received base64 data:", base64_string[:50] + "...")  # Print the start of the base64 data for debugging
    
    if base64_string.startswith("data:audio/wav;base64,"):
        base64_string = base64_string[len("data:audio/wav;base64,"):]
        
    print(len(base64_string))
    print("Received base64 data:", base64_string[:50] + "...")  # Print the start of the base64 data for debugging

    missing_padding = len(base64_string) % 4
    if missing_padding != 0:
        base64_string += '=' * (4 - missing_padding)
        
    audio_data = base64.b64decode(base64_string)
    
    audio = AudioSegment.from_file(io.BytesIO(audio_data), format=format)
    output_file_path = f"./{name}.wav"
    audio.export(output_file_path, format="wav")
    
    # # Write the binary data to a file
    # output_file_path = f"./{name}.wav"
    # with open(output_file_path, 'wb') as file:
    #     file.write(audio_data)
        
    print("Audio file saved to:", output_file_path)

    return f"./{name}.wav"


rhubarb_to_mouth = {
  "A": "M",
  "B": "E",
  "C": "I",
  "D": "A",
  "E": "I",
  "F": "O",
  "G": "E",
  "H": "I",
  "X": "M",
}

@stub.function(image=modal_image, container_idle_timeout=300)
@modal.web_endpoint(method="POST")
def get_viseme(file: dict):
    
    token = get_random_token()
    
    base64_data = file["sound"]
    format = file["format"]
    # audio_data = base64.b64decode(base64_data)
    # audio_path = f"./{token}.wav"
    audio_path = handle_base64_audio(base64_data, format, token)
    
    # # Write the binary data to a .wav file
    # with open(audio_path, "wb") as wav_file:
    #     wav_file.write(audio_data)

    print(os.listdir("./"))
    
    output_file = token + "_output.txt"
    rhubarb = "/root/Rhubarb/rhubarb"
    
    print(os.listdir("/root/Rhubarb"))
    
    args = ["-o", output_file, audio_path]
    
      # Run the subprocess and wait for it to complete
    try:
        result = subprocess.run(
            [rhubarb] + args,
            capture_output=True,
            text=True,
            check=True  # This will raise an exception if the command returns a non-zero exit code
        )
        print("Subprocess output:", result.stdout)
        print("Subprocess error (if any):", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Subprocess failed with return code {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return {"error": e.stderr}
        
    # parse output
    # Read the data from the text file
    with open(output_file, 'r') as file:
        lines = file.readlines()
    
    # Parse the lines into a list of tuples (timestamp, letter)
    items = []
    for line in lines:
        timestamp, letter = line.strip().split()
        items.append((float(timestamp), letter))
            
    data = []
    for i in range(len(items) - 1):
        start, letter = items[i]
        end, _ = items[i + 1]
        data.append({"shape": letter, "start": start, "end": end})
        
    # delete text file and audio file
    os.remove(output_file)
    os.remove(audio_path)
    
    for n in data:
        n["shape"] = rhubarb_to_mouth.get(n["shape"], "M")
    
    print(data)
    return {"data": data}
    
def run_executable(executable, args):
    try:
        # Run the executable with arguments
        result = subprocess.run(
            [executable] + args,
            capture_output=True,
            text=True,
            check=True  # This will raise an exception if the executable returns a non-zero exit code
        )
        print("Executable ran successfully")
        print("Output:", result.stdout)
        print("Error:", result.stderr)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print("Executable failed with return code", e.returncode)
        print("Output:", e.stdout)
        print("Error:", e.stderr)
        return None, e.stderr
    except FileNotFoundError:
        print(f"Executable not found: {executable}")
        return None, "Executable not found"
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, str(e)
    
def get_random_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
