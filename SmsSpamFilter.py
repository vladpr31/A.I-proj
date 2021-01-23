import os
import pandas as pd


def creating_vocab(series):
    vocab = []
    for x in series:
        x_list = x.split()
        for i in x_list:
            vocab.append(i)
    return list(set(vocab))
def classify_message(sms):

    import re
    sms_message = re.sub('\W', ' ', sms)
    sms_message = sms_message.lower()
    sms_message = sms_message.split()
    p_ham_given_message = p_ham
    p_spam_given_message = p_spam
    for word in sms_message:
        if word in ham_words_prob:
            p_ham_given_message *= ham_words_prob[word]

        if word in spam_words_prob:
            p_spam_given_message *= spam_words_prob[word]

    if p_ham_given_message > p_spam_given_message:
        return 'ham'
    elif p_spam_given_message > p_ham_given_message:
        return 'spam'
    else:
        return 'hcr'




spam_words_prob = {}
ham_words_prob = {}
alpha = 1
p_ham = 0.86541
p_spam = 0.13459
spam_collection = pd.read_csv('\\Users\\VLAD\\Desktop\\SmsFilter\\Spam', sep='\t', header=None,
                              names=['Label', 'SMS'])




sms_data_randomized = spam_collection.sample(frac=1, random_state=1)
training_data_length = round(len(spam_collection) * 0.80)
training_sms_dataset = sms_data_randomized[:training_data_length]
training_sms_dataset.reset_index(drop=True, inplace=True)
testing_sms_dataset = sms_data_randomized[training_data_length:].reset_index(drop=True)
training_sms_dataset['SMS'] = training_sms_dataset['SMS'].str.replace('\W', ' ').str.lower()
test_training_dataset = training_sms_dataset.iloc[0:10]
test_vocab = creating_vocab(test_training_dataset['SMS'].iloc[0:2])
training_sms_dataset['SMS'] = training_sms_dataset['SMS'].str.split()
vocabulary = []
for sms in training_sms_dataset['SMS']:
    for word in sms:
        vocabulary.append(word)
vocabulary = list(set(vocabulary))
word_counts_per_sms = {unique_word: [0] * len(training_sms_dataset['SMS']) for unique_word in vocabulary}
for index, sms in enumerate(training_sms_dataset['SMS']):
    for word in sms:
        word_counts_per_sms[word][index] += 1
words_df = pd.DataFrame(word_counts_per_sms)
training_dataset_joined = pd.concat([training_sms_dataset, words_df], axis=1)
training_dataset_joined['Label'].value_counts(normalize=True)
spam = training_dataset_joined[training_dataset_joined['Label'] == 'spam']
ham = training_dataset_joined[training_dataset_joined['Label'] == 'ham']
spam_words = [len(x) for x in spam['SMS']]
n_spam = sum(spam_words)
ham_words = [len(x) for x in ham['SMS']]
n_ham = sum(ham_words)
n_vocab = len(vocabulary)
for word in vocabulary:
    spam_words_prob[word] = 0
    ham_words_prob[word] = 0
for word in vocabulary:
    numerator = ham[word].sum() + alpha
    denominator = n_ham + (n_vocab * alpha)
    prob = numerator / denominator
    ham_words_prob[word] = prob
for word in vocabulary:
  numerator = spam[word].sum() + alpha
  denominator = n_spam + (n_vocab * alpha)
  prob = numerator / denominator
  spam_words_prob[word] = prob


print(classify_message('WINNER!! This is the secret code to unlock the money: C3421.'))
