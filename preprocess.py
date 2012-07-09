from collections import defaultdict, Counter
from sys import stderr, stdout
import json
from text_utils import *
import os
from pandas import *
from IPython import embed
from pylab import bar, show, xticks

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

        row = [x.strip() for x in row]

        if not row[3]:
            row[3] = 'missing'

        success += 1

        yield dict(zip(fields, row))

#    stderr.write('Read %d out of %d rows\n' % (success, success + failure))

def read_json(filename):

    success = failure = 0

    # read JSON file one row at a time, ignoring badly-formatted row

    for row in open(filename):

        try:

            row = dict((k, v.strip()) for (k, v) in json.loads(row).items())

            if not row['shape']:
                row['shape'] = 'missing'

            yield row

        except ValueError as e:
            failure += 1
        else:
            success += 1

#    stderr.write('Read %d out of %d rows\n' % (success, success + failure))

def get_us_data(filename):

    counts = Counter()

    states = set(['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                  'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD',
                  'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH',
                  'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                  'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'])

    states.add('DC')

    for row in read_data(filename):

        location = row['location']

        if location == 'Washington, D.C., DC':
            location = 'Washington D.C., DC'

        try:
            (city, state) = location.split(', ')
        except ValueError as e:
            continue

        if len(state) == 2 and state in states:
            city = ' '.join(tokenize(re.sub('\s*\(.*\)?', '', city)))
        else:
            continue

        counts.update(['%s %s' % (city, state.lower())])

    x, y = zip(*counts.most_common(25))

    bar(range(len(y)), y, align='center')
    xticks(range(len(y)), x, rotation=270)

    from pylab import xlim

    xlim(-1, xlim()[1])

    show()

def get_shape_histogram(filename):

    counts = Counter()

#    for row in read_data(filename):
#        counts.update([row['shape']])

#    for key, value in counts.items():
#        print '%s\t%s' % (key, value)

    panda = DataFrame(list(read_data(filename)))

    for shape in panda['shape']:
        counts.update([shape])

    print panda.groupby('shape')['shape'].count().to_string()

    bar(range(len(counts)), counts.values(), align='center')
    xticks(range(len(counts)), counts.keys(), rotation=90)

    show()

def get_word_frequencies_by_shape(filename):

#    freqs = defaultdict(Counter)

#    for row in read_data(filename):
#        freqs[row['shape']].update(tokenize(row['description'], stopwords))

#    for key, value in freqs.items():
#        print key, value.most_common(5)

    panda = DataFrame(list(read_data(filename)))

    for shape, group in panda.groupby('shape'):

        group_tokens = group['description'].apply(tokenize)

        # stopwords are not being stripped

        freqs = Counter(w for tokens in group_tokens for w in tokens)

        print shape, freqs.most_common(5)

if __name__ == '__main__':

#    malletize('ufo_awesome.json')

#    get_shape_histogram('ufo_awesome.json')

#    get_word_frequencies_by_shape('ufo_awesome.json')

#    get_us_data('ufo_awesome.tsv')
