import whisperx
import gc 
import json
import modal
import base64
from modal import Image, web_endpoint
import os
import random
import string

stub = modal.Stub("whisperX")

whisperX_image = Image.debian_slim().apt_install("git").pip_install(
    ["torch", "torchaudio", "git+https://github.com/m-bain/whisperX.git", "torchvision"]
).run_commands("DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg")

# whisperX_image = Image.debian_slim().apt_install("git").pip_install(
#     ["torch", "torchaudio", "git+https://github.com/m-bain/whisperX.git"]
# ).copy_local_dir("./models").run_commands("DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg")

grapheme_to_ipa = {
    'b': 'b', 'bb': 'b',
    'd': 'd', 'dd': 'd', 'ed': 'd',
    'f': 'f', 'ff': 'f', 'ph': 'f', 'gh': 'f', 'lf': 'f', 'ft': 'f',
    'g': 'g', 'gg': 'g', 'gh': 'g', 'gu': 'g', 'gue': 'g',
    'h': 'h', 'wh': 'h',
    'j': 'dʒ', 'ge': 'dʒ', 'g': 'dʒ', 'dge': 'dʒ', 'di': 'dʒ', 'gg': 'dʒ',
    'k': 'k', 'c': 'k', 'ch': 'k', 'cc': 'k', 'lk': 'k', 'qu': 'k', 'q(u)': 'k', 'ck': 'k', 'x': 'k',
    'l': 'l', 'll': 'l',
    'm': 'm', 'mm': 'm', 'mb': 'm', 'mn': 'm', 'lm': 'm',
    'n': 'n', 'nn': 'n', 'kn': 'n', 'gn': 'n', 'pn': 'n', 'mn': 'n',
    'p': 'p', 'pp': 'p',
    'r': 'r', 'rr': 'r', 'wr': 'r', 'rh': 'r',
    's': 's', 'ss': 's', 'c': 's', 'sc': 's', 'ps': 's', 'st': 's', 'ce': 's', 'se': 's',
    't': 't', 'tt': 't', 'th': 't', 'ed': 't',
    'v': 'v', 'f': 'v', 'ph': 'v', 've': 'v',
    'w': 'w', 'wh': 'w', 'u': 'w', 'o': 'w',
    'z': 'z', 'zz': 'z', 's': 'z', 'ss': 'z', 'x': 'z', 'ze': 'z', 'se': 'z',
    'si': 'ʒ', 'z': 'ʒ', 's': 'ʒ',
    'ch': 'tʃ', 'tch': 'tʃ', 'tu': 'tʃ', 'te': 'tʃ',
    'sh': 'ʃ', 'ce': 'ʃ', 'ci': 'ʃ', 'si': 'ʃ', 'ch': 'ʃ', 'sci': 'ʃ', 'ti': 'ʃ',
    'th': 'θ',
    'th': 'ð',
    'ng': 'ŋ', 'n': 'ŋ', 'ngue': 'ŋ',
    'y': 'j', 'i': 'j', 'j': 'j',
    'a': 'æ', 'ai': 'æ', 'au': 'æ',
    'a': 'eɪ', 'ai': 'eɪ', 'eigh': 'eɪ', 'aigh': 'eɪ', 'ay': 'eɪ', 'er': 'eɪ', 'et': 'eɪ', 'ei': 'eɪ', 'au': 'eɪ', 'a_e': 'eɪ', 'ea': 'eɪ', 'ey': 'eɪ',
    'e': 'ɛ', 'ea': 'ɛ', 'u': 'ɛ', 'ie': 'ɛ', 'ai': 'ɛ', 'a': 'ɛ', 'eo': 'ɛ', 'ei': 'ɛ', 'ae': 'ɛ',
    'e': 'i:', 'ee': 'i:', 'ea': 'i:', 'y': 'i:', 'ey': 'i:', 'oe': 'i:', 'ie': 'i:', 'i': 'i:', 'ei': 'i:', 'eo': 'i:', 'ay': 'i:',
    'i': 'ɪ', 'e': 'ɪ', 'o': 'ɪ', 'u': 'ɪ', 'ui': 'ɪ', 'y': 'ɪ', 'ie': 'ɪ',
    'i': 'aɪ', 'y': 'aɪ', 'igh': 'aɪ', 'ie': 'aɪ', 'uy': 'aɪ', 'ye': 'aɪ', 'ai': 'aɪ', 'is': 'aɪ', 'eigh': 'aɪ', 'i_e': 'aɪ',
    'a': 'ɒ', 'ho': 'ɒ', 'au': 'ɒ', 'aw': 'ɒ', 'ough': 'ɒ',
    'o': 'oʊ', 'oa': 'oʊ', 'o_e': 'oʊ', 'oe': 'oʊ', 'ow': 'oʊ', 'ough': 'oʊ', 'eau': 'oʊ', 'oo': 'oʊ', 'ew': 'oʊ',
    'o': 'ʊ', 'oo': 'ʊ', 'u': 'ʊ', 'ou': 'ʊ',
    'u': 'ʌ', 'o': 'ʌ', 'oo': 'ʌ', 'ou': 'ʌ',
    'o': 'u:', 'oo': 'u:', 'ew': 'u:', 'ue': 'u:', 'u_e': 'u:', 'oe': 'u:', 'ough': 'u:', 'ui': 'u:', 'oew': 'u:', 'ou': 'u:',
    'oi': 'ɔɪ', 'oy': 'ɔɪ', 'uoy': 'ɔɪ',
    'ow': 'aʊ', 'ou': 'aʊ', 'ough': 'aʊ',
    'a': 'ə', 'er': 'ə', 'i': 'ə', 'ar': 'ə', 'our': 'ə', 'ur': 'ə',
    'air': 'eəʳ', 'are': 'eəʳ', 'ear': 'eəʳ', 'ere': 'eəʳ', 'eir': 'eəʳ', 'ayer': 'eəʳ',
    'a': 'ɑ:', 
    'ir': 'ɜ:ʳ', 'er': 'ɜ:ʳ', 'ur': 'ɜ:ʳ', 'ear': '`ɜ:ʳ', 'or': 'ɜ:ʳ', 'our': 'ɜ:ʳ', 'yr': 'ɜ:ʳ',
    'aw': 'ɔ:', 'a': 'ɔ:', 'or': 'ɔ:', 'oor': 'ɔ:', 'ore': 'ɔ:', 'oar': 'ɔ:', 'our': 'ɔ:', 'augh': 'ɔ:', 'ar': 'ɔ:', 'ough': 'ɔ:', 'au': 'ɔ:',
    'ear': 'ɪəʳ', 'eer': 'ɪəʳ', 'ere': 'ɪəʳ', 'ier': 'ɪəʳ',
    'ure': 'ʊəʳ', 'our': 'ʊəʳ'
}

ipa_symbols = [
    'b', 'd', 'f', 'g', 'h', 'dʒ', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'z', 'ʒ', 'tʃ', 'ʃ', 'θ', 'ð', 'ŋ', 'j',
    'æ', 'eɪ', 'ɛ', 'i:', 'ɪ', 'aɪ', 'ɒ', 'oʊ', 'ʊ', 'ʌ', 'u:', 'ɔɪ', 'aʊ', 'ə', 'eəʳ', 'ɑ:', 'ɜ:ʳ', 'ɔ:', 'ɪəʳ', 'ʊəʳ'
]

ipa_to_viseme_anime = {
    'p': 'closed', 'b': 'closed', 'm': 'closed',
    'tʃ': 'mid', 'dʒ': 'mid', 'ʒ': 'mid', 'ʃ': 'mid',
    'd': 'closed', 't': 'mid',
    'f': 'closed', 'v': 'closed',
    'g': 'mid', 'k': 'mid',
    'h': 'open',
    'l': 'closed',
    'n': 'mid',
    'r': 'closed',
    'w': 'closed',
    's': 'mid', 'z': 'mid',
    'θ': 'closed', 'ð': 'mid',
    'ŋ': 'closed', 'j': 'mid',
    'æ': 'open', 'ɛ': 'open', 'aɪ': 'open',
    'ɪ': 'open', 'i:': 'mid', 'eɪ': 'mid',
    'ʌ': 'mid', 'ʊ': 'mid', 'u:': 'mid', 'oʊ': 'mid', 'ɔɪ': 'mid', 'aʊ': 'mid',
    'ə': 'mid', 'ɜ:ʳ': 'mid', 'ɑ:': 'mid', 'ɒ': 'mid', 'ɔ:': 'mid', 'ɪəʳ': 'mid', 'ʊəʳ': 'mid', 'eəʳ': 'mid',
}

def parse_word(word: str):
    # Remove punctuation
    word = word.strip(".,!?")
    
    i = 0
    while i < len(word):
        # Check for quadruplets
        if i < len(word) - 3 and word[i:i+4].lower() in grapheme_to_ipa:
            yield (word[i:i+4].lower(), grapheme_to_ipa[word[i:i+4].lower()], i)
            i += 4
        # Check for trigraphs
        elif i < len(word) - 2 and word[i:i+3].lower() in grapheme_to_ipa:
            yield (word[i:i+3].lower(), grapheme_to_ipa[word[i:i+3].lower()], i)
            i += 3
        # Check for digraphs
        elif i < len(word) - 1 and word[i:i+2].lower() in grapheme_to_ipa:
            yield (word[i:i+2].lower(), grapheme_to_ipa[word[i:i+2].lower()], i)
            i += 2
        # Check for monographs
        elif word[i].lower() in grapheme_to_ipa:
            yield (word[i].lower(), grapheme_to_ipa[word[i].lower()], i)
            i += 1
        # Skip unrecognized characters
        else:
            yield (word[i], "not_found")
            i += 1 

def group_chars_into_words(char_data):
    words = []
    current_word = []

    for entry in char_data:
        char = entry["char"]
        
        if char != " ":
            current_word.append(entry)
        else:
            if current_word:
                words.append(current_word)
                current_word = []

    if current_word:
        words.append(current_word)

    return words

# device = "cuda" 
# batch_size = 16 # reduce if low on GPU mem
# compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)
# if (modal.is_local()):
device = "cpu" 
batch_size = 16 # reduce if low on GPU mem
compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)

@stub.function(image=whisperX_image, container_idle_timeout=600)
@web_endpoint(method="POST")
def process(file: dict):
    
    sound = file['sound']
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    audio_file = handle_base64_audio(sound, name)
    
    print(os.listdir("./"))
    
    # generate random 10 character string

    # 1. Transcribe with original whisper (batched)
    # model = whisperx.load_model("./models/snapshots/f0fe81560cb8b68660e564f55dd99207059c092e/", device, compute_type=compute_type)
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
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device) # WAV2VEC2_ASR_LARGE_LV60K_960H
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=True)
    
    data = result["segments"]

    new_result = []

    words = data[0]["words"]
    characters = group_chars_into_words(data[0]["chars"])
    assert len(words) == len(characters)

    for (word, chars) in zip(words, characters):
        
        word_index = 0
        
        for result in parse_word(word["word"]):
            if (result[1] == "not_found"):
                print("not found")
            else:
                word_index += len(result[0]) - 1
                
                print(result, chars[result[2]])
                start = chars[result[2]]["start"]
                end = chars[word_index]["end"]
                print(start, end)
                word_index += 1
                
                ipa = grapheme_to_ipa[result[0]]
                shape = ipa_to_viseme_anime[ipa]
                
                if (shape == "open"):
                    shape = "A"
                elif (shape == "mid"):
                    shape = "E"
                elif (shape == "closed"):
                    shape = "M"
                
                new_result.append({"shape": shape, "start": start, "end": end})
    
    if os.path.exists(audio_file):
        os.remove(audio_file)
        print(f"{audio_file} has been removed successfully.")
    
    return {
        "data": new_result
    }
    
        
def handle_base64_audio(base64_string: str, name: str):
    # Decode the base64 string
    audio_data = base64.b64decode(base64_string)
    
    # Write the binary data to a file
    output_file_path = f"./{name}.wav"
    with open(output_file_path, 'wb') as file:
        file.write(audio_data)
        
    print("Audio file saved to:", output_file_path)

    return f"./{name}.wav"
        