from nltk.tokenize import word_tokenize



example_sent = "Jack and Jill went up a hill"


def extract_keywords(example_sent):
    word_tokens = word_tokenize(example_sent)
    
    #Perform keyword processing
    print(word_tokens)

    return word_tokens

