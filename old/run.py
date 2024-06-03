import whisperx
import gc 
import json
import base64
import os

device = "cpu" 
batch_size = 16 # reduce if low on GPU mem
compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)

audio_file = "./example/sound_1.mp3"

    
mouth_shapes = {
    "open": ["a", "e", "i", "o", "u"],
    "closed": ["m", "b", "p", "x", "f", "v", "s", "z", "t", "d", "n", "l"],
}

def char_to_mouth_shape(char):
    for shape, chars in mouth_shapes.items():
        if char.lower() in chars:
            return shape
    # Default to "rest" if character is not explicitly mapped
    return "mid"

def main():

    # 1. Transcribe with original whisper (batched)
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)

    # save model to local path (optional)
    # model_dir = "/path/"
    # model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)

    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    # delete model if low on GPU resources
    # import gc; gc.collect(); torch.cuda.empty_cache(); del model

    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device) # WAV2VEC2_ASR_LARGE_LV60K_960H
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=True)
    # print(result["segments"][0]["chars"])
            
    with open('data/all_data.json', 'w') as f:
        json.dump(result["segments"], f, indent=4)
        
    with open('data/word_data.json', 'w') as f:
        json.dump(result["segments"][0]["words"], f, indent=4)
        
    with open('data/char_data.json', 'w') as f:
        json.dump(result["segments"][0]["chars"], f, indent=4)
    
    
    # new_result = []
        
    # for char in result["segments"][0]["chars"]:
    #     if 'start' in char:
    #         item = {"shape": char_to_mouth_shape(char["char"]), "start": char["start"], "end": char["end"]}
    #         char["mouth_shape"] = char_to_mouth_shape(char["char"])
    #         new_result.append(item)
        
    # print(new_result)
        



if __name__ == "__main__":
    main()
        