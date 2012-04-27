from collections import defaultdict, Counter
from sys import stderr, stdout
import json
from text_utils import *
import os
from pandas import *

stopwords = create_stopword_list(['stopwordlist.txt'])

def malletize(filename):

    docs = defaultdict(list)

    counts = Counter()

    for n, row in enumerate(read_data(filename)):

        tokens = tokenize(row['description'], stopwords)

        docs['%s\t%s' % (n, row['shape'])] = tokens

        counts.update(tokens)

    num_tokens = 0

    for key, tokens in docs.items():

        tokens = [x for x in tokens if counts[x] > 1]

        stdout.write('%s\t%s\n', (key, ' '.join(tokens)))

        num_tokens += len(tokens)

    stderr.write('# documents = %s\n' % len(docs))
    stderr.write('# tokens = %s\n' % num_tokens)

def read_data(filename):

    if os.path.splitext(filename)[1] == '.json':
        return read_json(filename)
    else:
        return read_tsv(filename)

def read_tsv(filename):

    success = failure = 0

    fields = ['sighted_at', 'reported_at', 'location', 'shape', 'duration', 'description']

    for row in open(filename):

        row = row.strip().split('\t')

        if len(row) != 6:
            failure += 1
            continue

        shape = row[3].strip()
        if not shape:
            shape = 'missing'
        row[3] = shape

        success += 1

        yield dict(zip(fields, row))

#    stderr.write('Read %d out of %d rows\n' % (success, success + failure))

def read_json(filename):

    success = failure = 0

    # read JSON file one row at a time, ignoring badly-formatted row

    for row in open(filename):

        try:

            row = json.loads(row)

            shape = row['shape'].strip()
            if not shape:
                shape = 'missing'
            row['shape'] = shape

            yield row

        except ValueError as e:
            failure += 1
        else:
            success += 1

#    stderr.write('Read %d out of %d rows\n' % (success, success + failure))

def get_shape_histogram(filename):

    panda = DataFrame(list(read_data(filename)))

#    panda.groupby('shape')['shape'].count().to_csv(stdout, sep='\t')

    print panda.groupby('shape')['shape'].count().to_string()

#    counts = Counter()

#    for row in read_data(filename):
#        counts.update([row['shape']])

#    print counts

def get_word_frequencies_by_shape(filename):

#    freqs = defaultdict(Counter)

#    for row in read_data(filename):
#        freqs[row['shape']].update(tokenize(row['description'], stopwords))

#    for key, value in freqs.items():
#        print key, value.most_common(5)

    panda = DataFrame(list(read_data(filename)))

    for shape, group in panda.groupby('shape'):

        group_tokens = group['description'].apply(tokenize)

        freqs = Counter(w for tokens in group_tokens for w in tokens)

        print shape, freqs.most_common(5)

if __name__ == '__main__':

#    malletize('ufo_awesome.json')

    get_shape_histogram('ufo_awesome.json')

    get_word_frequencies_by_shape('ufo_awesome.json')
