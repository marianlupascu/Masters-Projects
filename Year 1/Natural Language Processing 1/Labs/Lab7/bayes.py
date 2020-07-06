# -*- coding: utf-8 -*-
"""bayes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aJI5NqlgjEdP4iXCEb-ZUaILLnFZtQ_l
"""

from google.colab import files, auth, drive

# Mount to drive
drive.mount('/content/gdrive', force_remount=True)
data_dir_drive ='/content/gdrive/My Drive/Colab Notebooks/NLP1/Lab7'

! pip install nltk

import nltk
nltk.download()

"""# **Supervised Word Sense Disambiguation (Bayes)**
We use Bayes's classifier in order to label (classify) the words with e certain WordNet sense. For this we need a context window surrounding the target word (the word for which we search the sense). The context window should contain only "content words" (words with important meaning, that bring information, like nouns, verbs etc)

We note P(s|c) the probability for sense s in the context c. For each such sense of the target word the probability is computed and we take the sense with the highest probability compared to the others.

In order to compute the probability P(s|c), we use the formula: P(s|c)=P(c|s)*P(s)/P(c). P(s) is the probability of a sense without any context. However, for P(c|s) we would need a training set (with texts that contain the target word, already labeled with its correct sense).

However, NLTK already has the classifier implemented. In this laboratory we will use the NLTK NaiveBayesClassifier:[https://www.nltk.org/_modules/nltk/classify/naivebayes.html](https://www.nltk.org/_modules/nltk/classify/naivebayes.html)

The Naive Bayes classifier will first compute the prior probability for the senses (or, generally speaking, for the class labels) - this is determined by the abel's frequncy in the training set. the features are used to see the likelyhood of having that label in a given context.
"""

nltk.NaiveBayesClassifier.train(train_set)

"""where train_set must contain a list with the classes and features for each class. The train_set list will contain tuples of two elements. First element is a dictionary with the features (name and value of each feature). The second element is the class label.

Useful link: [https://www.nltk.org/book/ch06.html](https://www.nltk.org/book/ch06.html)

For today's task, yo need to train the NLTK Bayes classifier on senseval, on a word of your choice.
"""

from nltk.corpus import senseval
inst=senseval.instances('interest.pos')
inst[:10]

"""For the training set, use 90% of instances to train the classifier and try to find the sense of the word on the rest of 10% of instances and compare it to the result. Print your findings."""

from nltk.corpus import brown

brown.categories()

brown.words(categories='adventure')[:50]

brown.words(categories='government')[:50]

def categ_features2(name):
    features = {}
    features["len"] = len(name)
    features["word"] = name.lower()
    features["suffix1"] = name[-1:]
    features["suffix2"] = name[-2:]
    features["suffix3"] = name[-3:]
    features["prefix1"] = name[:1]
    features["prefix2"] = name[:2]
    features["prefix3"] = name[:3]
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features

categ_features2('sun')

labeled_words = []
import random

for categ in brown.categories():
    labeled_words += [(word, categ) for word in brown.words(categories=categ)]

random.shuffle(labeled_words)

featuresets = [(categ_features2(n), gender) for (n, gender) in labeled_words]

train_size = int(0.9 * len(featuresets))
train_set, test_set = featuresets[:train_size], featuresets[train_size:]

classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, test_set))

print("Random = " + str(1.0/len(brown.categories())))

classifier.show_most_informative_features(5)

! pip install prettytable

from prettytable import PrettyTable

x = PrettyTable()

x.field_names = ["Word", "TrueLabel", "MyLabel"]

for test in test_set[:1000]:
    label = classifier.classify(categ_features2(test[0]['word']))
    TrueLabel = test[1]
    x.add_row([test[0]['word'], TrueLabel, label])

with open(data_dir_drive + '/out.txt', 'w') as w:
    w.write(str(x))