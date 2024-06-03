import json 

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

def convert_to_ipa_cluster(): # 1

    data = json.load(open('data/all_data.json'))

    words = data[0]["words"]
    characters = group_chars_into_words(data[0]["chars"])
    assert len(words) == len(characters)

    shape_data = []

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
                
                shape_data.append({"shape": result[0], "start": start, "end": end})
                
        
        # print(shape_data)
        
        # break

    with open('data/ipa_data.json', 'w') as f:
        json.dump(shape_data, f, indent=4)
        
def convert_ipa_to_shape(): # 2
    data = json.load(open('data/ipa_data.json'))
    
    shape_data = []
    
    for entry in data:
        ipa = grapheme_to_ipa[entry["shape"]]
        shape = ipa_to_viseme_anime[ipa]
        if (shape == "open"):
            shape = "A"
        elif (shape == "mid"):
            shape = "E"
        elif (shape == "closed"):
            shape = "M"
        shape_data.append({"shape": shape, "start": entry["start"], "end": entry["end"]})
        
    with open('data/shape_data.json', 'w') as f:
        json.dump(shape_data, f, indent=4)

if __name__ == "__main__":
    # convert_to_ipa_cluster()
    convert_ipa_to_shape()
                