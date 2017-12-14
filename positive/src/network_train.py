# source /Users/pavel/Sources/InProgress/Python/enviroments/neural_env/bin/activate
# gshuf -n 10000 training_long.csv > training.csv

from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from pprint import pprint
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, Convolution1D, Flatten, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.layers.recurrent import LSTM
from keras.callbacks import TensorBoard
import re
import pickle


embedding_vecor_length = 300
top_words = 10000
batch_size = 64
maxlen = 100


def build_model():
    model = Sequential()
    model.add(Embedding(top_words, embedding_vecor_length, input_length=maxlen))
    """
    model.add(Embedding(top_words, 128, input_length=maxlen))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(64))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  class_mode="binary")
    """

    """
    model.add(Embedding(top_words, embedding_vecor_length, input_length=maxlen))
    model.add(Convolution1D(32, 3, padding='same'))
    model.add(Convolution1D(32, 3, padding='same'))
    model.add(Convolution1D(32, 3, padding='same'))
    model.add(Convolution1D(32, 3, padding='same'))

    model.add(Dropout(0.25))

    model.add(Convolution1D(32, 3, padding='same'))
    model.add(Convolution1D(32, 3, padding='same'))
    model.add(Convolution1D(32, 3, padding='same'))
    model.add(Convolution1D(32, 3, padding='same'))

    model.add(Dropout(0.25))

    model.add(Flatten())

    model.add(Dense(256, activation='tanh'))
    model.add(Dense(256, activation='tanh'))

    model.add(Dense(1, activation='sigmoid'))
    """

    model.add(Convolution1D(64, 3, border_mode='same'))
    model.add(Convolution1D(32, 3, border_mode='same'))
    model.add(Convolution1D(16, 3, border_mode='same'))
    model.add(Flatten())
    model.add(Dropout(0.2))
    model.add(Dense(180,activation='sigmoid'))
    model.add(Dropout(0.2))
    model.add(Dense(1,activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


with open("../training.csv", "r") as f:
    lines = f.readlines()

with open("../stoplist.txt", "r") as f:
    stoplist = f.readlines()

stoplist = [x.strip() for x in stoplist]

X, Y = [], []
for line in lines:
    data = line.split(",")
    sent_val, text = data[0], data[5]

    sent_val = int(sent_val[1:-1])

    if sent_val == 2:
        # skip neutral
        continue
    elif sent_val == 4:
        sent_val = 1

    text = re.sub(r'\W+', ' ', text).strip().split(" ")
    text = [x.lower() for x in text if len(x) > 2]
    text = [x for x in text if x not in stoplist]

    if len(text) > 4:
        X.append(" ".join(text))
        Y.append(sent_val)

print("n_Positive: {}".format(Y.count(1)))
print("n_Negative: {}".format(Y.count(0)))

tokenizer = Tokenizer(num_words=top_words)
tokenizer.fit_on_texts(X)

#import json
#with open('data.json', 'w') as fp:
#    json.dump(tokenizer.word_index, fp)

sequences = tokenizer.texts_to_sequences(X)

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

n_train = int(len(sequences) * 0.8)

X_train, y_train = sequences[:n_train], Y[:n_train]
X_test, y_test = sequences[n_train:], Y[n_train:]

X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
X_test = sequence.pad_sequences(X_test, maxlen=maxlen)

model = build_model()

tensorBoardCallback = TensorBoard(log_dir='./logs', write_graph=True)
model.fit(X_train, y_train, epochs=1, callbacks=[tensorBoardCallback], batch_size=32)

scores = model.evaluate(X_test, y_test, verbose=1)

print(scores)

model.save('sentiment.h5')
