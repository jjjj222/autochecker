import pdb

FEATURE_LIST = [
    'head-word',
    'head-tag',
    'head-dprel',
    'next-word',
    'next-tag',
    'prev-word',
    'prev-tag',
    'first-word',
    'first-tag',
    'current-det'
]

def artOrDet_features(word, active_features):
    sentence = word.sentence

    result = {}

    i = word.id
    head_pos = artOrDet_features_get_np_end_pos(word)

    result['current-det'] = ""
    if word.pos == "DT":
        result['current-det'] = word.token.lower()
        i += 1

    result['first-word'] = sentence[i].token.lower()
    result['first-tag'] = sentence[i].pos

    result['head-word'] = sentence[head_pos].token.lower()
    result['head-tag'] = sentence[head_pos].pos
    result['head-dprel'] = sentence[head_pos].dprel

    if head_pos+1 >= len(sentence):
        result['next-word'] = "<END>"
        result['next-tag'] = None
    else:
        result['next-word'] = sentence[head_pos+1].token.lower()
        result['next-tag'] = sentence[head_pos+1].pos

    if word.id == 0:
        result['prev-word'] = "<START>"
        result['prev-tag'] = None
    else:
        result['prev-word'] = sentence[word.id-1].token.lower()
        result['prev-tag'] = sentence[word.id-1].pos

    for f in FEATURE_LIST:
        if f not in active_features:
            del result[f]

    #pdb.set_trace()
    return result

def artOrDet_features_get_np_end_pos(word):
    s = word.sentence
    i = word.id

    while i < len(s) - 1 and s[i+1].node == "NP":
        i += 1

    return i
