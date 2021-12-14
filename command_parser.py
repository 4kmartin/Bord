def tokenize(input_from_player:str)->[]:
    words = input_from_player.lower().split(" ")
    removals = []
    for word in words:
        if word in removals:
            continue
        elif word in (
            "he",
            "she",
            "it",
            "they",
            "them",
            "the",
            "that",
            "a",
            "with",
            "to",
            "lets",
            "let's",
            "let",
            "us",
            "we",
            "all",
            "my",
            "on",
            ):
            removals.append(word)
    for removed in removals:
        words.remove(removed)
    return words

def normalize(tokens:[], thesaurus:{})->[]:
    """takes an array of tokens and colapses the synonyms to a single agreed upon word"""
    for key in thesaurus:
        tokens = [key if token in thesaurus[key] else token for token in tokens ]
    return tokens

default_thesaurus={
    "go": ("walk", "go","move"),
    "attack":("stab","hit","dammage","break"),
    "get":("show","display"),
    "inventory":("stuff","items"),
}
                

if __name__ == "__main__":
    tokens = normalize(tokenize(input()),default_thesaurus)
    print( tokens ) 