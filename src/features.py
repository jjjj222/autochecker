import pdb

FEATURE_LIST = [
    'head-word',        # V
    'head-tag',         # V
    'head-dprel',
    'next-word',        # V
    'next-tag',
    'prev-word',
    'prev-tag',
    'first-word',       # V
    'first-tag',    # ?
    'current-det',
    'next-word-2',
    'next-tag-2',
    'prev-word-2',
    'prev-tag-2',
    'head-parent',
    'prev-verb',
    'next-verb',
    #'prev-sent',
    #'next-sent',
]

def artOrDet_features(word, active_features):
    sentence = word.sentence

    result = {}

    next_pos = word.id
    head_pos = artOrDet_features_get_np_end_pos(word)

    result['current-det'] = ""
    if word.pos == "DT":
        result['current-det'] = word.token.lower()
        next_pos += 1

    result['first-word'] = sentence[next_pos].token.lower()
    result['first-tag'] = sentence[next_pos].pos

    result['head-word'] = sentence[head_pos].token.lower()
    result['head-tag'] = sentence[head_pos].pos
    result['head-dprel'] = sentence[head_pos].dprel

    parent_pos_str = sentence[head_pos].dphead
    if parent_pos_str.isdigit():
        result['head-parent'] = sentence[int(parent_pos_str)].token.lower()
    else:
        result['head-parent'] = "<NULL>"

    if head_pos+1 >= len(sentence):
        result['next-word'] = "<END>"
        result['next-tag'] = "<END>"
    else:
        result['next-word'] = sentence[head_pos+1].token.lower()
        result['next-tag'] = sentence[head_pos+1].pos

    if head_pos+2 >= len(sentence):
        result['next-word-2'] = "<END>"
        result['next-tag-2'] = "<END>"
    else:
        result['next-word-2'] = sentence[head_pos+2].token.lower()
        result['next-tag-2'] = sentence[head_pos+2].pos

    if word.id <= 0:
        result['prev-word'] = "<START>"
        result['prev-tag'] = "<START>"
    else:
        result['prev-word'] = sentence[word.id-1].token.lower()
        result['prev-tag'] = sentence[word.id-1].pos

    if word.id <= 1:
        result['prev-word-2'] = "<START>"
        result['prev-tag-2'] = "<START>"
    else:
        result['prev-word-2'] = sentence[word.id-2].token.lower()
        result['prev-tag-2'] = sentence[word.id-2].pos

    result['prev-verb'] = "<NULL>"
    i = word.id - 1
    while i >= 0:
        tmp_w = sentence[i]
        if tmp_w.pos[0] == "V":
            result['prev-verb'] = tmp_w.token.lower()
            break
        i -= 1

    result['next-verb'] = "<NULL>"
    i = word.id
    while i < len(sentence):
        tmp_w = sentence[i]
        if tmp_w.pos[0] == "V":
            result['next-verb'] = tmp_w.token.lower()
            break
        i += 1

    #result['prev-sent'] = False
    #result['next-sent'] = False

    for f in FEATURE_LIST:
        if f not in active_features:
            del result[f]

    #if word.id == 1:
    #    word.dump()
    #    print sentence.tagged_text()
    #    print result
    #    exit(0)

    #pdb.set_trace()
    return result

def artOrDet_features_get_np_end_pos(word):
    s = word.sentence
    i = word.id

    while i < len(s) - 1 and s[i+1].node == "NP":
        i += 1

    return i
