from Bio import SeqIO
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Dropout, Embedding, CuDNNLSTM, Bidirectional, Input
from keras.preprocessing import sequence
from keras.models import Model
from keras.regularizers import l2



def create_dict(codes):
    char_dict = {}
    for index, val in enumerate(codes):
        char_dict[val] = index + 1

    return char_dict


def integer_encoding(records):
    encode_list = []
    for row in records:
        row_encode = []
        for code in row.seq:
            row_encode.append(char_dict.get(code, 0))
        encode_list.append(np.array(row_encode))

    return encode_list


records = list(SeqIO.parse("tcdb17feb2020.fasta", "fasta"))
records_original = list(SeqIO.parse("tcdb17feb2020.fasta", "fasta"))
test_records = np.round(len(records) * .2)
num_test = np.random.permutation(int(test_records))

list_test = []
for i in num_test:
    list_test.append(records[i])
    records.pop(i)

# len_train_seqs = []
# for rec in records:
#     len_train_seqs.append(len(rec))
#
# len_test_seqs = []
# for rec in list_test:
#     len_test_seqs.append(len(rec))
# #len_train_seqs.sort()
# #len_test_seqs.sort()
# plt.plot(list(range(1, len(list_test) + 1)), len_test_seqs)
# plt.show()

max_length = 1000

codes = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
         'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

char_dict = create_dict(codes)

train_encode = integer_encoding(records)
# val_encode = integer_encoding(val_sm)
test_encode = integer_encoding(list_test)

train_pad = pad_sequences(train_encode, maxlen=max_length, padding='post', truncating='post')
# val_pad = pad_sequences(val_encode, maxlen=max_length, padding='post', truncating='post')
test_pad = pad_sequences(test_encode, maxlen=max_length, padding='post', truncating='post')

train_ohe = to_categorical(train_pad)
# val_ohe = to_categorical(val_pad)
test_ohe = to_categorical(test_pad)

family_dict = {}
i = 0
for item in records_original:
    famil = item.id.split('|')[3].split('.')[0:3]
    family = '.'.join(famil)

    if family not in family_dict:
        family_dict[family] = i
        i += 1
labels = list(range(0, 1234))

train_labels = []
for item in records:
    famil = '.'.join(item.id.split('|')[3].split('.')[0:3])
    train_labels.append(family_dict[famil])

test_labels = []
for item in list_test:
    famil = '.'.join(item.id.split('|')[3].split('.')[0:3])
    test_labels.append(family_dict[famil])

x_input = Input(shape=(1000,))
emb = Embedding(21, 128, input_length=max_length)(x_input)
bi_rnn = Bidirectional(CuDNNLSTM(64)(emb))
x = Dropout(0.3)(bi_rnn)

# softmax classifier
x_output = Dense(1000, activation='softmax')(x)

model1 = Model(inputs=x_input, outputs=x_output)
model1.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model1.fit(train_ohe, train_labels, batch_size=32, epochs=4, validation_data=[test_ohe, test_labels])

a = 2
