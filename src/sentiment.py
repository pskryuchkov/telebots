from keras.models import load_model
from keras.preprocessing import sequence
import pickle
import re


def calc_vals(source):
    with open("../data/{0}.txt".format(source), "r") as f:
        data = f.readlines()

    lines = [x.strip() for x in data]

    with open('../data/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    v_titles = []

    for line in lines:
        str = re.sub(r'\W+', ' ', line).lower()
        str = " ".join([x for x in str.split() if len(x) > 2 and x not in stoplist])

        sq = tokenizer.texts_to_sequences([str])
        inp = sequence.pad_sequences(sq, maxlen=maxlen)
        v_titles.append([line, model.predict(inp)[0][0]])

    s_titles = sorted(v_titles, key=lambda x: x[1], reverse=True)

    return s_titles


sources = ["bbc", "cnn", "ny", "reuters"]
csv_head = "sep=;\n"
maxlen = 100

model = load_model('../data/sentiment.h5')

with open("../stoplist.txt", "r") as f:
    stoplist = f.readlines()

with open("../data/sent.csv", "w") as f:
    f.write(csv_head)

    for source in sources:
        table = calc_vals(source)

        for line in table:
            title, val = line
            f.write("; ".join([source, title, str(val)]) + "\n")