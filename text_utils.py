import re

def tokenize(data):

    return re.findall('\w+', re.sub('&[a-z]+;', ' ', data.lower()))

def create_stopword_list(stopword_files):

    stopwords = []

    for filename in stopword_files:
        for word in open(filename):
            stopwords.append(word.strip())

    return set(stopwords)

def strip_stopwords(tokens, stopwords):

    return [x for x in tokens if x not in stopwords]
