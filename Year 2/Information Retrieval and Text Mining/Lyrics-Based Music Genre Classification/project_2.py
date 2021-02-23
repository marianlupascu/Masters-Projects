# -*- coding: utf-8 -*-
"""Project#2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17YBXyutMBjx9F0FXyUlynEiMmtqYFXVQ

## **Preparing all things**
"""

!pip install -q -U watermark

!pip install -qq transformers

from google.colab import files, auth, drive
import torch.backends.cudnn as cudnn
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.autograd import Variable
import numpy as np
import copy
import re
import pandas as pd
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme()
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC# Support Vector Machine
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from transformers import BertTokenizer, BertModel
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import torch.nn.functional as F
from transformers import AdamW, get_linear_schedule_with_warmup
from collections import defaultdict
from sklearn.utils import shuffle
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

"""## **Setup & Config**

"""

CUDA_LAUNCH_BLOCKING=1

plt.ion()  

use_gpu = torch.cuda.is_available()
if use_gpu:
    print("Using CUDA")
else:
    print("Using CPU")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Mount to drive
drive.mount('/content/gdrive', force_remount=True)
data_dir_drive ='/content/gdrive/My Drive/Colab Notebooks/Information Retrieval and Text Mining/'
data_dir ='/content' # When read from unziped file

import nltk

# stopwords, punkt, wordnet 
nltk.download()

df = pd.read_csv(data_dir_drive + 'Lyrics-Genre-Train.csv')

"""## **Data Analysis**"""

df

# The describe method shows basic statistical characteristics of each 
# numerical feature (int64 and float64 types): number of non-missing values, 
# mean, standard deviation, range, median, 0.25 and 0.75 quartiles.
df.describe()

# print same iformations about each column for table
print(df.info())

"""As there are no missing values, it means that I do not have to throw lines or rebuild them"""

data = df.to_numpy()

# The distribution of songs by genres
genres = data[:, 3]
objects = sorted(set(genres))
print(objects)
y_pos = np.arange(len(objects))
nr = []
for genre in objects:
    nr.append(np.sum((genres == genre)))
print(nr)
plt.barh(y_pos, nr, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Number of songs per genre')
plt.title('Genres distribution')

plt.show()

for idx in range(len(objects)):
    print(objects[idx] + ' have ' + str(nr[idx]) + ' songs')

"""It's like we have at least 1000 lyrics for each musical genre. Classes are unbalanced"""

sns.countplot(df.Genre)
plt.xlabel('Genre');

genres = set(df['Genre'])
genres

N = 1000 # number of records to pull from each genre
RANDOM_SEED = 43 # random seed to make results repeatable

train_df = pd.DataFrame()
test_df = pd.DataFrame()
for genre in genres: # loop over each genre
    print(genre)
    subset = df[(df.Genre==genre)]
    train_set = subset.sample(n=N, random_state=RANDOM_SEED) # 1000 verses of 
    #each genre are put in the train set, the network will go in the test set
    test_set = subset.drop(train_set.index)
    train_df = train_df.append(train_set)
    test_df = test_df.append(test_set)
    
train_df = shuffle(train_df)
test_df = shuffle(test_df)

"""# **Classic ML algorithms**
## **Naive Bayes with CountVectorizer as a feature extraction**
"""

# define model
text_clf = Pipeline(
    [('vect', CountVectorizer()),
     ('clf', MultinomialNB(alpha=0.1))])

# train model on training data
text_clf.fit(train_df.Lyrics, train_df.Genre)  

# score model on testing data
predicted = text_clf.predict(test_df.Lyrics)
print('accuracy %s' % accuracy_score(predicted, test_df.Genre))
print(classification_report(test_df.Genre, predicted, target_names=genres))

"""## **Naive Bayes with Tfid as a feature extraction**

---


"""

# define model
text_Tfidf = Pipeline(
    [('vect', TfidfVectorizer()),
     ('clf', MultinomialNB(alpha=0.1))])

# train model on training data
text_Tfidf.fit(train_df.Lyrics, train_df.Genre)  

# score model on testing data
predicted = text_Tfidf.predict(test_df.Lyrics)
print('accuracy %s' % accuracy_score(predicted, test_df.Genre))
print(classification_report(test_df.Genre, predicted, target_names=genres))

mat = confusion_matrix(test_df.Genre, predicted)
sns.heatmap(
    mat.T, square=True, annot=True, fmt='d', cbar=False,
    xticklabels=genres, 
    yticklabels=genres
)
plt.xlabel('true label')
plt.ylabel('predicted label');

"""## **SVM**"""

# define model
text_svm = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SVC(kernel='rbf'))])

# train model on training data
text_svm.fit(train_df.Lyrics, train_df.Genre)  

# score model on testing data
predicted = text_svm.predict(test_df.Lyrics)
print('accuracy %s' % accuracy_score(predicted, test_df.Genre))
print(classification_report(test_df.Genre, predicted, target_names=genres))

mat = confusion_matrix(test_df.Genre, predicted)
sns.heatmap(
    mat.T, square=True, annot=True, fmt='d', cbar=False,
    xticklabels=genres, 
    yticklabels=genres
)
plt.xlabel('true label')
plt.ylabel('predicted label');

"""SVM has a lower accuracy than Naive Bayes probably because the Soft-margin is too high, or because too many features from the lyrics are close in the vector space between the Soft-margins.

## **Naive Bayes with Tfid as a feature extraction + text preprocessing**
"""

stop = list(set(stopwords.words('english'))) # stopwords

# define model
text_clf_more = Pipeline(
    [('vect', TfidfVectorizer(
        stop_words=stop # remove stopwords
        )),
     ('tfidf', TfidfTransformer()),
     ('clf', MultinomialNB(alpha=0.1))])

# train model on training data
text_clf_more.fit(train_df.Lyrics, train_df.Genre)  

# score model on testing data
predicted = text_clf_more.predict(test_df.Lyrics)
print('accuracy %s' % accuracy_score(predicted, test_df.Genre))
print(classification_report(test_df.Genre, predicted, target_names=genres))

mat = confusion_matrix(test_df.Genre, predicted)
sns.heatmap(
    mat.T, square=True, annot=True, fmt='d', cbar=False,
    xticklabels=genres, 
    yticklabels=genres
)
plt.xlabel('true label')
plt.ylabel('predicted label');

"""If I remove stopwords I decrease the accuracy from 0.386 to 0.377, almost by 1%, so removing stopwords does not help in this case"""

stop = list(set(stopwords.words('english'))) # stopwords
lm = WordNetLemmatizer() # lemmatizer

def tokenizer(x): # custom tokenizer
    return (
        lm.lemmatize(w) 
        for w in word_tokenize(x) 
        if len(w) > 2 and w.isalnum() # only words that have more than 2 characters
    )                                 # and is alpha-numeric

# define model
text_clf_more = Pipeline(
    [('vect', TfidfVectorizer(
        tokenizer=tokenizer,
        stop_words=stop, # remove stopwords
        max_df=0.4, # ignore terms that appear in more than 40% of songs
        min_df=4)), # ignore terms that appear in less than 4 songs
     ('tfidf', TfidfTransformer()),
     ('clf', MultinomialNB(alpha=0.1))])

# train model on training data
text_clf_more.fit(train_df.Lyrics, train_df.Genre)  

# score model on testing data
predicted = text_clf_more.predict(test_df.Lyrics)
print('accuracy %s' % accuracy_score(predicted, test_df.Genre))
print(classification_report(test_df.Genre, predicted, target_names=genres))

"""And if I do a little extra: elimination of stopwords, lemmatization, elimination of repetitive words that are excessive or that do not appear at all, I decrease the sharpness again by 0.7%. So it's a stupid idea

## **Logistic regression**
"""

# define model
logreg = Pipeline([('vect', CountVectorizer()),
                 ('tfidf', TfidfTransformer()),
                 ('clf', LogisticRegression(n_jobs=1, multi_class = "multinomial", 
                                           C=1, solver = "sag", class_weight="balanced")),
                 ])

logreg.fit(train_df.Lyrics, train_df.Genre)

predicted = logreg.predict(test_df.Lyrics)
print('accuracy %s' % accuracy_score(predicted, test_df.Genre))
print(classification_report(test_df.Genre, predicted, target_names=genres))

mat = confusion_matrix(test_df.Genre, predicted)
sns.heatmap(
    mat.T, square=True, annot=True, fmt='d', cbar=False,
    xticklabels=genres, 
    yticklabels=genres
)
plt.xlabel('true label')
plt.ylabel('predicted label');

"""## **Logistic regression + text preprocessing**"""

def clean_text(text):
    text = text.lower() # lowercase text
    text = re.compile('[/(){}\[\]\|@,;|\n]').sub(' ', text) # replace symbols by space in text
    text = re.compile('[^0-9a-z #+_]').sub('', text) # delete symbols
    text = ' '.join(word for word in text.split() if word not in list(set(stopwords.words('english')))) # delete stopwors from text
    return text
    
lyrics = train_df.Lyrics.apply(clean_text)

# define model
logreg2 = Pipeline([('vect', CountVectorizer()),
                 ('tfidf', TfidfTransformer()),
                 ('clf', LogisticRegression(n_jobs=1, multi_class = "multinomial", 
                                           C=1, solver = "sag", class_weight="balanced")),
                 ])

logreg2.fit(lyrics, train_df.Genre)

predicted = logreg2.predict(test_df.Lyrics)
print('accuracy %s' % accuracy_score(predicted, test_df.Genre))
print(classification_report(test_df.Genre, predicted, target_names=genres))

"""And if I do a little extra: elimination of stopwords and elimination of intuetivly bad character, I decrease the sharpness again by 2%. So it's a stupid idea, again"""

predicted1 = text_clf.predict(test_df.Lyrics)
predicted2 = text_svm.predict(test_df.Lyrics)
predicted3 = text_Tfidf.predict(test_df.Lyrics)
predicted4 = text_clf_more.predict(test_df.Lyrics)
predicted5 = logreg.predict(test_df.Lyrics)

predicted = []
for i in range(len(predicted1)):
    L = [predicted1[i], predicted2[i], predicted3[i], predicted4[i], predicted5[i]]
    predicted.append(max(set(L), key = L.count))

print('accuracy %s' % accuracy_score(predicted, test_df.Genre))
print(classification_report(test_df.Genre, predicted, target_names=genres))

mat = confusion_matrix(test_df.Genre, predicted)
sns.heatmap(
    mat.T, square=True, annot=True, fmt='d', cbar=False,
    xticklabels=genres, 
    yticklabels=genres
)
plt.xlabel('true label')
plt.ylabel('predicted label');

"""
Now if I implement a voting system based on the above classifiers I get the best accuracy so far 38.14% (random forest principle)

________________________________________________________________________________________________
# **MLP (Multilayer perceptron)**
"""

df = pd.read_csv(data_dir_drive + 'Lyrics-Genre-Train.csv')

def to_code(genre):
    if genre  == 'Country':
        return 0
    elif genre  == 'Electronic':
        return 1
    elif genre  == 'Folk':
        return 2
    elif genre  == 'Hip-Hop':
        return 3
    elif genre  == 'Indie':
        return 4
    elif genre  == 'Jazz':
        return 5
    elif genre  == 'Metal':
        return 6
    elif genre  == 'Pop':
        return 7
    elif genre  == 'R&B':
        return 8
    else: 
        return 9

df['Genre'] = df.Genre.apply(to_code)
del df['Song']
del df['Song year']
del df['Artist']
del df['Track_id']

df.head()

df_test = pd.read_csv(data_dir_drive + 'Lyrics-Genre-Test-GroundTruth.csv')
df_test.head()

df_test['Genre'] = df_test.Genre.apply(to_code)
del df_test['Song']
del df_test['Song year']
del df_test['Artist']
del df_test['Track_id']

df_test.head()

#def process_lyrics(lyrics):
#    lyrics = lyrics.replace('\n', '')
#    lyrics = lyrics.lower()
#    lyrics = re.sub(r'[^\w\s]','', lyrics) 
#    wnl = WordNetLemmatizer() # lemmatizer
#    new_lyrics = ""
#    for word in word_tokenize(lyrics):
#        w = wnl.lemmatize(word) 
#        new_lyrics += w + " "
#    return new_lyrics
#
#df['Lyrics'] = df.Lyrics.apply(process_lyrics)

"""Accuracy without stopords and with preprocessing is again lower (that's why this cell is commented)"""

tfidf = TfidfVectorizer(binary=True, max_features = 512)

x = tfidf.fit_transform(df.Lyrics)
y = df.Genre

seed = 43
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=seed) # 80%-20% split

print(x_train.shape, y_train.shape, x_val.shape, y_val.shape)

x_train = torch.tensor(x_train.todense()).type(torch.float).cuda()
x_val = torch.tensor(x_val.todense()).type(torch.float).cuda()
y_train = torch.from_numpy(y_train.values).type(torch.long).cuda()
y_val = torch.from_numpy(y_val.values).type(torch.long).cuda()

import matplotlib.pyplot as plt

def plot_loss(loss, label, color='blue'):
    plt.plot(loss, label=label, color=color)
    plt.legend()

class Net(nn.Module):
    # nn.Module - base class for all models
    # easy acces to .parameters() and .zero_grad()
    # define .forward() instead of __call__()
    
    def __init__(self, in_size, h_size1, h_size2, h_size3, out_size):
        super().__init__()
        self._layer1 = nn.Linear(in_size,h_size1).cuda()
        self._layer2 = nn.Linear(h_size1,h_size2).cuda()
        self._layer3 = nn.Linear(h_size2,h_size3).cuda()
        self._layer4 = nn.Linear(h_size3,out_size).cuda()
        self.drop_layer = nn.Dropout(p=0.5)
        
    def forward(self, x):
        x = F.relu(self._layer1(x)).cuda()
        x = self.drop_layer(x).cuda()
        x = F.relu(self._layer2(x)).cuda()
        x = self.drop_layer(x).cuda()
        x = F.relu(self._layer3(x)).cuda()
        x = self.drop_layer(x).cuda()
        x = self._layer4(x).cuda()
        return x.cuda()
        
    def train(self, train_data, train_labels, 
              epochs=400, lr=0.01, verbose=100, l2_weight=0,
              val_data=None, val_labels=None):
        #use optimizers to take care of the update step
        optimizer1 = torch.optim.SGD(self.parameters(), lr=lr,
                               weight_decay = l2_weight)
        
        optimizer2 = torch.optim.Adagrad(self.parameters())
        optimizer3 = torch.optim.RMSprop(self.parameters())
        optimizer4 = torch.optim.Adam(self.parameters())
        
        criterion = nn.CrossEntropyLoss(); # classification
        best_model_wts = copy.deepcopy(self.state_dict())
        
        train_loss = []
        val_loss = []
        best_acc = 0
        for e in range(epochs):
            optimizer4.zero_grad()   # zero the gradient buffers
            input = train_data
            output = self(train_data)
            loss = criterion(output, train_labels)
            loss.backward()
            optimizer4.step()    # Does the update of gredients
            
            train_loss.append(loss.cpu().detach().numpy())
            if verbose!=0 and e%verbose==0:
                print("Epoch :" + str(e))
                print("Loss - train :")
                print(loss)
            if val_data is not None:
                output = self(val_data)
                loss = criterion(output, val_labels)

                outputs = torch.argmax(output, dim = 1)
                avg_acc_val = torch.sum(val_labels == outputs).item() / outputs.shape[0]
                if avg_acc_val > best_acc:
                    best_acc = avg_acc_val
                    best_model_wts = copy.deepcopy(self.state_dict()) #I remember the best model for every epoch

                if verbose!=0 and e%verbose==0:
                    print("Loss - validation :")
                    print(loss)
                val_loss.append(loss.cpu().detach().numpy())

        torch.cuda.empty_cache()
            
        plot_loss(train_loss, 'train-loss')
        if len(val_loss)>0:
            plot_loss(val_loss, 'val-loss', color='red')
            plt.show()

        return best_model_wts

#define a net
net = Net(512, 16* 512, 16 * 512, 16 * 512, 10)
net.to(device)
print(net)

#train from all examples from train set
best_model_wts = net.train(x_train, y_train, epochs=100, lr=0.1, verbose=10, val_data = x_val, val_labels=y_val)

"""I can see that there is a learning curve, but the network is overfitting, so the best model is saved around the epoch of 50 out of 100."""

net.load_state_dict(best_model_wts)

#torch.save(net.state_dict(), data_dir_drive + 'models/MLP1.pt')

x_test = tfidf.transform(df_test.Lyrics)
y_test = df_test.Genre

x_test = torch.tensor(x_test.todense()).type(torch.float).cuda()
y_test = torch.from_numpy(y_test.values).type(torch.long).cuda()

outputs = net(x_test)
outputs = torch.argmax(outputs, dim = 1)

print(outputs)
print(y_test)
acc = torch.sum(y_test == outputs).item() / outputs.shape[0]
print(acc)

"""The accuracy on the test set is 34.1% quite low compared to SVM or NB. That is why I will further define 9 networks with different architectures that I will train separately and in the end the most probable prediction of the 9 votes is the vote."""

#define nets
net1 = Net(512, 2* 512, 2 * 512, 2 * 512, 10)
net1.to(device)

net2 = Net(512, 4* 512, 4 * 512, 4 * 512, 10)
net2.to(device)

net3 = Net(512, 8* 512, 8 * 512, 8 * 512, 10)
net3.to(device)

net4 = Net(512, 16* 512, 16 * 512, 16 * 512, 10)
net4.to(device)

net5 = Net(512, 16* 512, 8 * 512, 16 * 512, 10)
net5.to(device)

net6 = Net(512, 8* 512, 16 * 512, 32 * 512, 10)
net6.to(device)

net7 = Net(512, 8* 512, 16 * 512, 8 * 512, 10)
net7.to(device)

net8 = Net(512, 4* 512, 32 * 512, 4 * 512, 10)
net8.to(device)

net9 = Net(512, 2* 512, 64 * 512, 4 * 512, 10)
net9.to(device)

nets = [net1, net2, net3, net4, net5, net6, net7, net8, net9]

#train from all examples from train set
for i in range(9):
    print(i)
    best_model_wts = nets[i].train(x_train, y_train, epochs=100, lr=0.1, verbose=100, val_data = x_val, val_labels=y_val)
    nets[i].load_state_dict(best_model_wts)
    torch.save(nets[i].state_dict(), data_dir_drive + 'MLP' + str(i) + '.pt')

for i in range(9):
    print(i)
    state_dict = torch.load(data_dir_drive + 'MLP' + str(i) + '.pt', map_location=device)
    nets[i].load_state_dict(state_dict)

predicted = []
for i in range(9):
    predicted.append(torch.argmax(nets[i](x_test), dim = 1))

predicted = torch.stack(predicted)

print(predicted[:,4])
print(y_test[4])

max(set(predicted[:,4].cpu().tolist()), key = predicted[:,4].cpu().tolist().count)

acc = 0
for i in range(x_test.shape[0]):
    acc += max(set(predicted[:,i].cpu().tolist()), key = predicted[:,i].cpu().tolist().count) == y_test[i].item()

print(acc / x_test.shape[0])

"""In this way the accuracy increases by 2.5% (quite a bit). It makes sense because all networks are driven by the same hyperparameters, except for the architectures. All overfitting, but for each of them was saved the best performing model on validation.
________________________________________________________________________________________________
# **BERT**
"""

PRE_TRAINED_MODEL_NAME = 'bert-base-cased'

tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)

sample_txt = 'We close our eyes and the world has turned around again\nWe close our eyes and dream\nAnother year has come and gone.' #lyric

tokens = tokenizer.tokenize(sample_txt)
token_ids = tokenizer.convert_tokens_to_ids(tokens)

print(f' Sentence: {sample_txt}')
print(f'   Tokens: {tokens}')
print(f'Token IDs: {token_ids}')

tokenizer.sep_token, tokenizer.sep_token_id # [SEP] - marker for ending of a sentence

tokenizer.cls_token, tokenizer.cls_token_id # [CLS] - add this token to the start of each sentence, so BERT knows I're doing classification

tokenizer.pad_token, tokenizer.pad_token_id # There is also a special token for padding

tokenizer.unk_token, tokenizer.unk_token_id # BERT understands tokens that were in the training set. Everything else can be encoded using the [UNK] (unknown) token

encoding = tokenizer.encode_plus(
    sample_txt,
    max_length=32,
    add_special_tokens=True, # Add '[CLS]' and '[SEP]'
    return_token_type_ids=False,
    padding='max_length',
    truncation=True,
    return_attention_mask=True,
    return_tensors='pt',  # Return PyTorch tensors
    )

encoding.keys()

print(len(encoding['input_ids'][0])) 
encoding['input_ids'][0]
# The token ids are now stored in a Tensor and padded to a length of 32

#The attention mask has the same length
print(len(encoding['attention_mask'][0]))
encoding['attention_mask']

# I can inverse the tokenization to have a look at the special tokens
tokenizer.convert_ids_to_tokens(encoding['input_ids'][0])

"""Choosing Sequence Length - BERT works with fixed-length sequences"""

token_lens = []

for txt in df.Lyrics:
  tokens = tokenizer.encode(txt, max_length=2048)
  token_lens.append(len(tokens))

sns.distplot(token_lens)
plt.xlim([0, 1500]);
plt.xlabel('Token count');

"""Most of the reviews seem to contain less than 500-600 tokens, but for memory reasons I will experimentally choose 350 to avoid the CUDA out of memory error"""

MAX_LEN = 350

class LyricsDataset(Dataset):

    def __init__(self, lyrics, genres, tokenizer, max_len):
        self.lyrics = lyrics
        self.genres = genres
        self.tokenizer = tokenizer
        self.max_len = max_len
    
    def __len__(self):
        return len(self.lyrics)
    
    def __getitem__(self, item):
        lyric = str(self.lyrics[item])
        genre = self.genres[item]

        encoding = self.tokenizer.encode_plus(
        lyric,
        add_special_tokens=True,
        max_length=self.max_len,
        return_token_type_ids=False,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt',
        )

        return {
        'lyric_text': lyric,
        'input_ids': encoding['input_ids'].flatten(),
        'attention_mask': encoding['attention_mask'].flatten(),
        'genres': torch.tensor(genre, dtype=torch.long)
        }

RANDOM_SEED = 43
df_train, df_val = train_test_split(df, test_size=0.1, random_state=RANDOM_SEED)

df_train.shape, df_val.shape, df_test.shape

def create_data_loader(df, tokenizer, max_len, batch_size):
    ds = LyricsDataset(
        lyrics=df.Lyrics.to_numpy(),
        genres=df.Genre.to_numpy(),
        tokenizer=tokenizer,
        max_len=max_len)

    return DataLoader(
        ds,
        batch_size=batch_size,
        num_workers=4)

BATCH_SIZE = 16

train_data_loader = create_data_loader(df_train, tokenizer, MAX_LEN, BATCH_SIZE)
val_data_loader = create_data_loader(df_val, tokenizer, MAX_LEN, BATCH_SIZE)
test_data_loader = create_data_loader(df_test, tokenizer, MAX_LEN, BATCH_SIZE)

data = next(iter(train_data_loader))
data.keys()

print(data['input_ids'].shape)
print(data['attention_mask'].shape)
print(data['genres'].shape)

bert_model = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)

bert_model(
    input_ids=encoding['input_ids'], 
    attention_mask=encoding['attention_mask']
    )['last_hidden_state'].shape

bert_model.config.hidden_size

bert_model(
  input_ids=encoding['input_ids'], 
  attention_mask=encoding['attention_mask']
)['pooler_output'].shape

class LyricsClassifier(nn.Module):

    def __init__(self, n_classes):
        super(LyricsClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
        # I use a dropout layer for some regularization and a fully-connected layer for our output
    
    def forward(self, input_ids, attention_mask):
        pooled_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
            )['pooler_output']
        output = self.drop(pooled_output)
        return self.out(output)

model = LyricsClassifier(10)
model = model.to(device)

input_ids = data['input_ids'].to(device)
attention_mask = data['attention_mask'].to(device)

print(input_ids.shape) # batch size x seq length
print(attention_mask.shape) # batch size x seq length

"""The BERT authors have some recommendations for fine-tuning:

- Batch size: 16, 32
- Learning rate (Adam): 5e-5, 3e-5, 2e-5
- Number of epochs: 2, 3, 4
"""

EPOCHS = 4

optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=False)
total_steps = len(train_data_loader) * EPOCHS

scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=0,
    num_training_steps=total_steps)

loss_fn = nn.CrossEntropyLoss().to(device)

def train_epoch(model, data_loader, loss_fn, optimizer, device, scheduler, n_examples):
    model = model.train()

    losses = []
    correct_predictions = 0
    
    for d in data_loader:
        input_ids = d["input_ids"].to(device)
        attention_mask = d["attention_mask"].to(device)
        targets = d["genres"].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)

        _, preds = torch.max(outputs, dim=1)
        loss = loss_fn(outputs, targets)

        correct_predictions += torch.sum(preds == targets)
        losses.append(loss.item())

        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()

    return correct_predictions.double() / n_examples, np.mean(losses)

def eval_model(model, data_loader, loss_fn, device, n_examples):
    model = model.eval()

    losses = []
    correct_predictions = 0

    with torch.no_grad():
        for d in data_loader:
            input_ids = d["input_ids"].to(device)
            attention_mask = d["attention_mask"].to(device)
            targets = d["genres"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            _, preds = torch.max(outputs, dim=1)

            loss = loss_fn(outputs, targets)

            correct_predictions += torch.sum(preds == targets)
            losses.append(loss.item())

    return correct_predictions.double() / n_examples, np.mean(losses)

history = defaultdict(list)
best_accuracy = 0

for epoch in range(EPOCHS):

    print(f'Epoch {epoch + 1}/{EPOCHS}')
    print('-' * 10)

    train_acc, train_loss = train_epoch(model,train_data_loader, loss_fn, optimizer, device, scheduler, len(df_train))

    print(f'Train loss {train_loss} accuracy {train_acc}')

    val_acc, val_loss = eval_model(model,val_data_loader,loss_fn, device, len(df_val))

    print(f'Val   loss {val_loss} accuracy {val_acc}')
    print()

    history['train_acc'].append(train_acc)
    history['train_loss'].append(train_loss)
    history['val_acc'].append(val_acc)
    history['val_loss'].append(val_loss)

    if val_acc > best_accuracy:
        torch.save(model.state_dict(), 'best_model_state.bin')
        best_accuracy = val_acc

plt.plot(history['train_acc'], label='train accuracy')
plt.plot(history['val_acc'], label='validation accuracy')

plt.title('Training history')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()
plt.ylim([0, 1]);

test_acc, _ = eval_model(model, test_data_loader, loss_fn, device, len(df_test))

test_acc.item()

"""The best accuracy so far, you can still easily see that I do not have a learning curve and that the network has a lot of overfitting. The learning curve is non-existent probably because the lyrics are in several languages, but also because I cut quite a lot out of context (max_len = 350)
______________________________________________________________________________________________________________________

# TORCHTEXT + EmbeddingBag 
"""

import torchtext

BATCH_SIZE = 16


import torch.nn as nn
import torch.nn.functional as F


class LyricsClasificator(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_class):
        super().__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True)
        self.fc = nn.Linear(embed_dim, num_class)
        self.init_weights()

    def init_weights(self):
        initrange = 0.5
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.fc.weight.data.uniform_(-initrange, initrange)
        self.fc.bias.data.zero_()

    def forward(self, text, offsets):
        embedded = self.embedding(text, offsets)
        return self.fc(embedded)

df = pd.read_csv(data_dir_drive + 'Lyrics-Genre-Train.csv')

def to_code(genre):
    if genre  == 'Country':
        return 0
    elif genre  == 'Electronic':
        return 1
    elif genre  == 'Folk':
        return 2
    elif genre  == 'Hip-Hop':
        return 3
    elif genre  == 'Indie':
        return 4
    elif genre  == 'Jazz':
        return 5
    elif genre  == 'Metal':
        return 6
    elif genre  == 'Pop':
        return 7
    elif genre  == 'R&B':
        return 8
    else: 
        return 9

df['Genre'] = df.Genre.apply(to_code)
del df['Song']
del df['Song year']
del df['Artist']
del df['Track_id']

df_test = pd.read_csv(data_dir_drive + 'Lyrics-Genre-Test-GroundTruth.csv')

df_test['Genre'] = df_test.Genre.apply(to_code)
del df_test['Song']
del df_test['Song year']
del df_test['Artist']
del df_test['Track_id']
df_test.head()

!pip install -U torchtext==0.8.0

from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

def build_vocab(data, transforms):
    def apply_transforms(data):
        for line in data:
            tokens = transforms(line)
            yield tokens
    return build_vocab_from_iterator(apply_transforms(data), len(data))

tokenizer = get_tokenizer('basic_english')
vocab = build_vocab(df['Lyrics'], tokenizer)
vocab_test = build_vocab(df_test['Lyrics'], tokenizer)

class LanguageModelingDataset(torch.utils.data.Dataset):
    """Defines a dataset for language modeling.
       Currently, we only support the following datasets:
             - WikiText2
             - WikiText103
             - PennTreebank
             - WMTNewsCrawl
    """

    def __init__(self, data, vocab, transform):
        """Initiate language modeling dataset.
        Args:
            data: a tensor of tokens. tokens are ids after
                numericalizing the string tokens.
                torch.tensor([token_id_1, token_id_2, token_id_3, token_id1]).long()
            vocab: Vocabulary object used for dataset.
            transform: Text string transform.
        """

        super(LanguageModelingDataset, self).__init__()
        self.vocab = vocab
        self.transform = transform
        self.data = data

    def __getitem__(self, i):
        return self.data[i]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for x in self.data:
            yield x

    def get_vocab(self):
        return self.vocab

def text_transform(line):
    return torch.tensor([vocab[token] for token in tokenizer(line)], dtype=torch.long)

DS = LanguageModelingDataset(list(zip(list(map(text_transform, df.Lyrics.tolist())), df.Genre.tolist())), vocab, text_transform)
DS_test = LanguageModelingDataset(list(zip(list(map(text_transform, df_test.Lyrics.tolist())), df_test.Genre.tolist())), vocab_test, text_transform)

DS[0]

VOCAB_SIZE = len(vocab)
EMBED_DIM = 32
NUN_CLASS = 10
model = LyricsClasificator(VOCAB_SIZE, EMBED_DIM, NUN_CLASS).to(device)

def generate_batch(batch):
    label = torch.tensor([entry[1] for entry in batch])
    text = [entry[0] for entry in batch]
    offsets = [0] + [len(entry) for entry in text]
    # torch.Tensor.cumsum returns the cumulative sum
    # of elements in the dimension dim.
    # torch.Tensor([1.0, 2.0, 3.0]).cumsum(dim=0)

    offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
    text = torch.cat(text)
    return text, offsets, label

from torch.utils.data import DataLoader

def train_func(sub_train_):

    # Train the model
    train_loss = 0
    train_acc = 0
    data = DataLoader(sub_train_, batch_size=BATCH_SIZE, shuffle=True,
                      collate_fn=generate_batch)
    for i, (text, offsets, cls) in enumerate(data):
        optimizer.zero_grad()
        text, offsets, cls = text.to(device), offsets.to(device), cls.to(device)
        output = model(text, offsets)
        loss = criterion(output, cls)
        train_loss += loss.item()
        loss.backward()
        optimizer.step()
        train_acc += (output.argmax(1) == cls).sum().item()
        

    # Adjust the learning rate
    scheduler.step()

    return train_loss / len(sub_train_), train_acc / len(sub_train_)

def test(data_):
    loss = 0
    acc = 0
    data = DataLoader(data_, batch_size=BATCH_SIZE, collate_fn=generate_batch)
    for text, offsets, cls in data:
        text, offsets, cls = text.to(device), offsets.to(device), cls.to(device)
        with torch.no_grad():
            output = model(text, offsets)
            loss = criterion(output, cls)
            loss += loss.item()
            acc += (output.argmax(1) == cls).sum().item()

    return loss / len(data_), acc / len(data_)

from torch.utils.data.dataset import random_split
import time
N_EPOCHS = 50
min_valid_loss = float('inf')
history = defaultdict(list)

criterion = torch.nn.CrossEntropyLoss().to(device)
optimizer = torch.optim.SGD(model.parameters(), lr=4.0)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1, gamma=0.9)

train_dataset = DS
train_len = int(len(train_dataset) * 0.95)
sub_train_, sub_valid_ = random_split(train_dataset, [train_len, len(train_dataset) - train_len])

best_model_wts = copy.deepcopy(model.state_dict())
best_acc = 0

for epoch in range(N_EPOCHS):

    start_time = time.time()
    train_loss, train_acc = train_func(sub_train_)
    valid_loss, valid_acc = test(sub_valid_)
    history['train_acc'].append(train_acc)
    history['val_acc'].append(valid_acc)

    if valid_acc > best_acc:
        best_acc = valid_acc
        best_model_wts = copy.deepcopy(model.state_dict()) #I remember the best model for every epoch

    secs = int(time.time() - start_time)
    mins = secs / 60
    secs = secs % 60

    print('Epoch: %d' %(epoch + 1), " | time in %d minutes, %d seconds" %(mins, secs))
    print(f'\tLoss: {train_loss:.4f}(train)\t|\tAcc: {train_acc * 100:.1f}%(train)')
    print(f'\tLoss: {valid_loss:.4f}(valid)\t|\tAcc: {valid_acc * 100:.1f}%(valid)')

plt.plot(history['train_acc'], label='train accuracy')
plt.plot(history['val_acc'], label='validation accuracy')

plt.title('Training history')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()
plt.ylim([0, 1]);

model.load_state_dict(best_model_wts)
print('Checking the results of test dataset...')
test_loss, test_acc = test(DS_test)
print(f'\tLoss: {test_loss:.4f}(test)\t|\tAcc: {test_acc * 100:.1f}%(test)')

"""Although there is a very nice learning curve (we can say that it is the only model so far that has overfitting) the model fails miserably on the test set, because the vacabular from the test set is quite different from the one learned on the train."""