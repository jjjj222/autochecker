def artOrDet_features(word):
    sentence = word.sentence

    result = {}

    i = word.id
    head_pos = artOrDet_features_get_np_end_pos(word)
    #print sentence.tagged_text()
    #word.dump()
    #print head_pos, sentence[head_pos]

    #result['current'] = ""
    if word.pos == "DT":
        #result['current'] = word.token.lower()
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
        result['pre-word'] = "<START>"
        result['pre-tag'] = None
    else:
        result['pre-word'] = sentence[word.id-1].token.lower()
        result['pre-tag'] = sentence[word.id-1].pos

    return result

def artOrDet_features_get_np_end_pos(word):
    s = word.sentence
    i = word.id

    while i < len(s) - 1 and s[i+1].node == "NP":
        i += 1

    return i
