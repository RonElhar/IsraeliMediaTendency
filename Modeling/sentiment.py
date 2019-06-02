import codecs
import os
from gensim import utils
from keras.utils.np_utils import to_categorical
import numpy as np
from keras.preprocessing import text, sequence
import matplotlib.pyplot as plt
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Input, Concatenate
from keras.layers import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.pooling import MaxPool1D
from keras import optimizers
from keras import backend as K
from keras.engine.saving import load_model
import pandas as pd
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer


def plot_loss_and_accuracy(history):
    fig, axs = plt.subplots(1, 2, sharex=True)

    axs[0].plot(history.history['loss'])
    axs[0].plot(history.history['val_loss'])
    axs[0].set_title('Model Loss')
    axs[0].legend(['Train', 'Validation'], loc='upper left')

    axs[1].plot(history.history['acc'])
    axs[1].plot(history.history['val_acc'])
    axs[1].set_title('Model Accuracy')
    axs[1].legend(['Train', 'Validation'], loc='upper left')

    fig.tight_layout()
    plt.show()


def load_data(filename):
    data = list(codecs.open(filename, 'r', 'utf-8').readlines())
    x, y = zip(*[d.strip().split('\t') for d in data])
    # Reducing any char-acter sequence of more than 3 consecutive repetitions to a respective 3-character sequence
    # (e.g. “!!!!!!!!”turns to “!!!”)
    # x = [re.sub(r'((.)\2{3,})', r'\2\2\2', i) for i in x]
    x = np.asarray(list(x))
    y = to_categorical(y, 3)

    return x, y


def tokenizer(x_train, x_test, vocabulary_size, char_level):
    tokenize = text.Tokenizer(num_words=vocabulary_size,
                              char_level=char_level,
                              filters='')
    tokenize.fit_on_texts(x_train)  # only fit on train
    # print('UNK index: {}'.format(tokenize.word_index['UNK']))

    x_train = tokenize.texts_to_sequences(x_train)
    x_test = tokenize.texts_to_sequences(x_test)

    return x_train, x_test


def pad(x_train, x_test, max_document_length):
    x_train = sequence.pad_sequences(x_train, maxlen=max_document_length, padding='post', truncating='post')
    x_test = sequence.pad_sequences(x_test, maxlen=max_document_length, padding='post', truncating='post')

    return x_train, x_test


def create_model():
    x_token_train, y_token_train = load_data('data/token_train.tsv')
    x_token_test, y_token_test = load_data('data/token_test.tsv')
    x_morph_train, y_morph_train = load_data('data/morph_train.tsv')
    x_morph_test, y_morph_test = load_data('data/morph_test.tsv')

    print('X token train shape: {}'.format(x_token_train.shape))
    print('X token test shape: {}'.format(x_token_test.shape))

    print('X morph train shape: {}'.format(x_morph_train.shape))
    print('X morph test shape: {}'.format(x_morph_test.shape))

    vocabulary_size = 5000

    x_token_train, x_token_test = tokenizer(x_token_train, x_token_test, vocabulary_size, False)
    x_morph_train, x_morph_test = tokenizer(x_morph_train, x_morph_test, vocabulary_size, False)

    max_document_length = 100

    x_token_train, x_token_test = pad(x_token_train, x_token_test, max_document_length)
    x_morph_train, x_morph_test = pad(x_morph_train, x_morph_test, max_document_length)

    print('X token train shape: {}'.format(x_token_train.shape))
    print('X token test shape: {}'.format(x_token_test.shape))

    print('X morph train shape: {}'.format(x_morph_train.shape))
    print('X morph test shape: {}'.format(x_morph_test.shape))

    dropout_keep_prob = 0.5
    embedding_size = 300
    batch_size = 50
    lr = 1e-4
    dev_size = 0.2
    num_epochs = 5

    # Create new TF graph
    K.clear_session()

    # Construct model
    convs = []
    text_input = Input(shape=(max_document_length,))
    x = Embedding(vocabulary_size, embedding_size)(text_input)
    for fsz in [3, 8]:
        conv = Conv1D(128, fsz, padding='valid', activation='relu')(x)
        pool = MaxPool1D()(conv)
        convs.append(pool)
    x = Concatenate(axis=1)(convs)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(dropout_keep_prob)(x)
    preds = Dense(3, activation='softmax')(x)

    model = Model(text_input, preds)

    adam = optimizers.Adam(lr=lr)

    model.compile(loss='categorical_crossentropy',
                  optimizer=adam,
                  metrics=['accuracy'])

    # Train the model
    history = model.fit(x_morph_train, y_morph_train,
                        batch_size=batch_size,
                        epochs=num_epochs,
                        verbose=1,
                        validation_split=dev_size)

    # Plot training accuracy and loss
    plot_loss_and_accuracy(history)

    # Evaluate the model
    scores = model.evaluate(x_morph_test, y_morph_test,
                            batch_size=batch_size, verbose=1)
    print('\nAccuracy: {:.4f}'.format(scores[1]))

    # Save the model
    model.save('CNN-Morph.h5')


def load():
    return load_model('C:\\Users\\ronel\\Desktop\\IsraeliMediaTendency\\Modeling\\CNN-Morph-Sentiment.h5')


def parse_articles(path):
    with open(path, 'r', encoding='utf-8') as f:
        sentences = np.asarray(f.readlines())
    vocabulary_size = 5000
    max_document_length = 100

    tokenize = text.Tokenizer(num_words=vocabulary_size,
                              char_level=False,
                              filters='')
    tokenize.fit_on_texts(sentences)
    sentences = tokenize.texts_to_sequences(sentences)
    sentences = sequence.pad_sequences(sentences, maxlen=max_document_length, padding='post', truncating='post')

    return sentences


def predict_party(path, save_name):
    df = pd.DataFrame(columns=['Sentiment', 'Sentence'])
    data = parse_articles(path)
    model = load()
    results = model.predict(data)
    positive = 0
    negative = 0
    neutral = 0
    for i in range(results.shape[0]):
        res = results[i]
        if res[0] > res[1] and res[0] > res[2]:
            negative += 1
        elif res[1] > res[0] and res[1] > res[2]:
            positive += 1
        else:
            neutral += 1
    positive_per = positive / results.shape[0]
    negative_per = negative / results.shape[0]
    neutral_per = neutral / results.shape[0]

    with open(save_name, 'w+', encoding='utf-8') as f:
        f.write("Out of " + str(results.shape[0]) + " lines:\n")
        f.write("Positive: " + str(positive_per) + '\n')
        f.write("Negative: " + str(negative_per) + '\n')
        f.write("Neutral: " + str(neutral_per) + '\n')


# create_model()
path = 'C:\\Users\\ronel\\Desktop\\IsraeliMediaTendency\\ynet'
# predict_party(path, "Likud-Elections-Statistics")

files_list = os.listdir(path)
for file in files_list:
    predict_party(path+'\\'+file, file.replace('.txt', '') + "-All-Statistics")
