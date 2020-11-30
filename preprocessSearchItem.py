# class responsible for preprocessing search string
# from textblob import TextBlob
import nltk


class Preprocess:

    def __init__(self, input_passage):
        self.passage = input_passage

    def get_key_words(self):
        tokens = nltk.word_tokenize(self.passage)
        tags = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
        nouns_array = []
        for noun in nouns:
            if noun.lower() not in nouns_array and noun.__len__() > 2:
                nouns_array.append(noun.lower())
        return nouns_array
