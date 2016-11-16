def artOrDet_features(word):
    sentence = word.sentence

    result = {}

    i = word.id

    if word.pos == "DT":
        i += 1

    result['word'] = sentence[i].token.lower()
    result['tag'] = sentence[i].pos

    if i+1 >= len(sentence):
        result['next-word'] = "<END>"
        result['next-tag'] = None
    else:
        result['next-word'] = sentence[i+1].token.lower()
        result['next-tag'] = sentence[i+1].pos

    if word.id == 0:
        result['pre-word'] = "<START>"
        result['pre-tag'] = None
    else:
        result['pre-word'] = sentence[word.id-1].token.lower()
        result['pre-tag'] = sentence[word.id-1].pos

    return result
