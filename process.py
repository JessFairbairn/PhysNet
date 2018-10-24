import json
import os
import typing

import nltk
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

file_names = os.listdir('text')

stemmedFileNames = list(
    filter(lambda fname: fname.endswith('stemmed.txt'), file_names)
)

file_locations = list(
    map(lambda file_name: f'text/{file_name}', stemmedFileNames)
)

cvec = CountVectorizer(stop_words='english', min_df=0.1,
                       max_df=.25, ngram_range=(1, 2), input='filename')
cvec.fit(file_locations)

print(f'Total n-grams = {len(cvec.vocabulary_)}')

cvec_counts = cvec.transform(file_locations)
print('sparse matrix shape:', cvec_counts.shape)
print('nonzero count:', cvec_counts.nnz)
print('sparsity: %.2f%%' % (100.0 * cvec_counts.nnz /
                            (cvec_counts.shape[0] * cvec_counts.shape[1])))

occ = np.asarray(cvec_counts.sum(axis=0)).ravel().tolist()
counts_df = pd.DataFrame(
    {'term': cvec.get_feature_names(), 'occurrences': occ})
top_values = counts_df.sort_values(by='occurrences', ascending=False).head(20)


transformer = TfidfTransformer()
transformed_weights = transformer.fit_transform(cvec_counts)

weights = np.asarray(transformed_weights.mean(axis=0)).ravel().tolist()
weights_df = pd.DataFrame(
    {'term': cvec.get_feature_names(), 'weight': weights})
sorted_weights = weights_df.sort_values(by='weight', ascending=False).head(20)

stemmer = SnowballStemmer("english")

verb_examples = dict()
stemmed_verb_instances = dict()  # Type:dict[string,set]

i = 0
files_in_dir = os.listdir('text')
print('Extracting verbs from file ', i, ' of ', len(files_in_dir), end='\r')
for file in files_in_dir:
    if i % 10 == 0:
        print('Extracting verbs from file ', i,
              ' of ', len(files_in_dir)/2, end='\r')
    filename = os.fsdecode(file)
    if filename.endswith('-stemmed.txt'):
        continue

    with open(f'text/{filename}', 'r') as myFile:
        sentences = sent_tokenize(myFile.read())

        clean_sentences = []
        for sentence in sentences:
            split_sentences = sentence.split('\n')
            clean_sentences = clean_sentences + split_sentences

        for sentence in clean_sentences:
            words = nltk.word_tokenize(sentence)
            pos_tags = nltk.pos_tag(words)

            verbs_tags = list(
                filter(lambda tuple: tuple[1].startswith('VB'), pos_tags))
            local_verb_examples = dict(
                (stemmer.stem(verb_tag[0]).lower(), sentence) for verb_tag in verbs_tags)

            for verb_tag in verbs_tags:
                stemmed = stemmer.stem(verb_tag[0]).lower()
                try:
                    (stemmed_verb_instances[stemmed]).add(verb_tag[0].lower())
                except KeyError:
                    stemmed_verb_instances[stemmed] = set([verb_tag[0].lower()])

            verb_examples.update(dict(local_verb_examples))
    i += 1
print('\n')

new_dict = {}
for verb in verb_examples:
    stemmed_verb = stemmer.stem(verb)
    try:
        value = weights_df[weights_df.term == stemmed_verb].weight.values[0]
    except IndexError:
        # print('Not indexed: ', stemmed_verb)
        continue

    try:
        new_dict[stemmed_verb] = {
            'score': value,
            'example': verb_examples[stemmed_verb],
            'instances': list(stemmed_verb_instances[stemmed_verb])
        }
    except KeyError:
        print('Missing: ', stemmed_verb)
        continue

with open("web/static/results.json", "w") as tempFile:
    json.dump(new_dict, tempFile, default=lambda o: o.__dict__)
