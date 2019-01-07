import json
import os
import pickle
from typing import Dict, List

import nltk
import numpy as np
import pandas as pd
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

import web.services.verbnet_service as verbnet_service
import web.services.wordnet_service as wordnet_service

class Processor:

    def __init__(self):

        #Parameters
        self.corpus = "astro"
        self.max_score = 0.9
        self.min_score = 0.001


        self.stemmer = SnowballStemmer("english") # Type: nltk.stem.api.StemmerI
        self.spacy = spacy.load('en_core_web_lg')

        self.removed_via_blacklist = set()
        

    def run(self):
        print('Begin run')

        try:
            with open(f'text_{self.corpus}/weights.pickle', 'rb') as handle:
                weights_df = pickle.load(handle)
        except FileNotFoundError:
            weights_df = self._extract_word_values()
            with open(f'text_{self.corpus}/weights.pickle', 'wb') as handle:
                pickle.dump(weights_df, handle, protocol=pickle.HIGHEST_PROTOCOL)

        stemmed_verb_instances, verb_examples = self._extract_verbs_from_documents()

        self._save_results(stemmed_verb_instances, verb_examples, weights_df)



    ######### private methods ##########
    def _extract_word_values(self):
        'Calculates tf-idf values for words in the documents'

        stemmedFileNames = list(
            filter(lambda fname: fname.endswith(
                'stemmed.txt'), os.listdir('text_' + self.corpus))
        )

        file_locations = list(
            map(lambda file_name: f'text_{self.corpus}/{file_name}', stemmedFileNames)
        )

        print('Counting terms...')

        cvec = CountVectorizer(stop_words='english', min_df=0.001,
                               max_df=1, ngram_range=(1, 2), input='filename')
        cvec.fit(file_locations)

        print(f'Total n-grams = {len(cvec.vocabulary_)}')

        cvec_counts = cvec.transform(file_locations)
        # print('sparse matrix shape:', cvec_counts.shape)
        print('nonzero count:', cvec_counts.nnz)
        # print('sparsity: %.2f%%' % (100.0 * cvec_counts.nnz / (cvec_counts.shape[0] * cvec_counts.shape[1])))

        # occ = np.asarray(cvec_counts.sum(axis=0)).ravel().tolist()
        # counts_df = pd.DataFrame(
        # {'term': cvec.get_feature_names(), 'occurrences': occ})
        # top_values = counts_df.sort_values(by='occurrences', ascending=False).head(20)

        transformer = TfidfTransformer()
        transformed_weights = transformer.fit_transform(cvec_counts)

        weights = np.asarray(transformed_weights.mean(axis=0)).ravel().tolist()
        weights_df = pd.DataFrame(
            {'term': cvec.get_feature_names(), 'weight': weights})
        # sorted_weights = weights_df.sort_values(by='weight', ascending=False)
        return weights_df


    def _extract_verbs_from_documents(self):
        'Performs POS tagging to identify verbs, and extract an example sentence for each'
        

        verb_examples = dict()  # Type:dict[string, str]
        stemmed_verb_instances = dict()  # Type:dict[string, set]

        i = 0
        files_in_dir = os.listdir('text_' + self.corpus)
        print('Extracting verbs from file ', i,
              ' of ', len(files_in_dir), end='\r')

        for file in files_in_dir:
            if i % 10 == 0:
                print('Extracting verbs from file ', i,
                      ' of ', len(files_in_dir)/2, end='\r')
            filename = os.fsdecode(file)
            if filename.endswith('-stemmed.txt') or not filename.endswith('.txt'):
                continue

            with open(f'text_{self.corpus}/{filename}', 'r') as myFile:
                sentences = sent_tokenize(myFile.read())

                clean_sentences = []
                for sentence in sentences:
                    split_sentences = sentence.split('\n')
                    clean_sentences = clean_sentences + split_sentences

                for sentence in clean_sentences:
                    
                    list_of_verbs = self._list_verbs(sentence)

                    local_verb_examples = dict(
                        (self.stemmer.stem(verb).lower(), sentence) for verb in list_of_verbs)

                    for verb in list_of_verbs:

                        stemmed = self.stemmer.stem(verb).lower()
                        try:
                            (stemmed_verb_instances[stemmed]).add(
                                verb.lower())
                        except KeyError:
                            stemmed_verb_instances[stemmed] = set(
                                [verb.lower()])

                    verb_examples.update(dict(local_verb_examples))
            i += 1
        print('\n')

        return stemmed_verb_instances, verb_examples

    def _list_verbs(self, sentence:str):
        # words = nltk.word_tokenize(sentence)
        # pos_tags = nltk.pos_tag(words)
        parsed = self.spacy(sentence)
        pos_tags = list(map(lambda word: (word.text, word.pos_), parsed))

        with open('blacklist.txt', 'r') as blacklist_file:
            blacklist = blacklist_file.read().strip().split('\n')
            verb_list = list(
                map(lambda tup: tup[0],
                    filter(lambda tup: tup[1] == 'VERB', pos_tags)
                )
            )
            for verb in verb_list:
                if verb in blacklist:
                    self.removed_via_blacklist.add(verb)
                    verb_list.remove(verb)

        return verb_list

    def _save_results(self,
        stemmed_verb_instances: Dict[str, set],
        verb_examples: Dict[str, str],
        weights_df: pd.DataFrame
    ):
        'Saves results to a JSON file'

        lemmatizer = WordNetLemmatizer()

        new_dict = {}
        
        verbs_not_found = []
        wordnet_only = []
        vb_themrole_value_error = []

        for verb in verb_examples:
            stemmed_verb = self.stemmer.stem(verb)
            try:
                value = weights_df[weights_df.term == stemmed_verb].weight.values[0]

            except IndexError:
                # print('Not indexed: ', stemmed_verb)
                continue

            if value < self.min_score:  # tf-idf limit
                continue

            try:
                lemm = lemmatizer.lemmatize(
                next(iter(stemmed_verb_instances[stemmed_verb])),
                pos='v')
            
            except KeyError:
                print('Missing: ', stemmed_verb)
                continue

            try:
                if verbnet_service.is_physics_verb(lemm):
                
                    senses = verbnet_service.get_corpus_ids(lemm) # Type: List[VerbData]
                else:
                    continue
            except (verbnet_service.NotInVerbNetException, ValueError) as e:
                if type(e) == ValueError:
                    vb_themrole_value_error.append(verb)
                
                if wordnet_service.is_verb(lemm):
                    senses = wordnet_service.get_corpus_ids(lemm) # Type: List[VerbData]
                    
                    wordnet_only.append(lemm)
                else:
                    verbs_not_found.append(lemm)
                    continue

            lemm_info = {
                    'score': value,
                    'example': verb_examples[stemmed_verb],
                    'instances': list(stemmed_verb_instances[stemmed_verb]),
                    'database_ids': senses
                }
                
            new_dict[lemm] = lemm_info

            

        # for lemm, entry in new_dict.items():
        #     for hyp in entry['hypernyms']:
        #         if hyp not in new_dict.keys():
        #             entry['hypernyms'].remove(hyp)
        #         else:
        #             print('Hypernym found: ', entry['instances'][0], ' ', hyp)

        print('Saving file...')
        with open("web/static/results.json", "w") as tempFile:
            json.dump(new_dict, tempFile, default=lambda o: o.__dict__)
        
        with open(f"web/static/results-{self.corpus}.json", "w") as tempFile:
            json.dump(new_dict, tempFile, default=lambda o: o.__dict__)

        log_data = {
            "verbs_not_found": verbs_not_found,
            "wordnet_only": wordnet_only,
            "removed_via_blacklist": list(self.removed_via_blacklist)
        }

        with open("process_log.json", "w") as tempFile:
            json.dump(log_data, tempFile, default=lambda o: o.__dict__)

        error_num = len(verbs_not_found) + len(wordnet_only) + len(self.removed_via_blacklist)
        full_num = len(new_dict) + error_num
        print(f'{(error_num/full_num)*100}% error rate in POS')


if __name__ == "__main__":
    processor = Processor()
    processor.run()
