import corpus
import os
import utils

from collections import Counter

SPAM_TAG = "SPAM"
HAM_TAG = "HAM"
SPAM_VALUE_FOR_NEW_WORD = 0.4
SPAM_PROBABILITY_TOLERANCE = 0.8


class BaseFilter():
    # Parent class for all possible filter types
    def test(self, testing_dir):
        result_dict = {}
        files = os.listdir(testing_dir)
        for email in files:
            if email[0] != '!':
                # TODO: function classify.email()
                result_dict[email] = self.classify_email()
        utils.write_classification_to_file(
                    os.path.join(testing_dir, '!prediction.txt'), result_dict)

    def classify_email(self):
        temporary_evaluation = "OK"
        return temporary_evaluation


class BayesFilter(BaseFilter):
    def __init__(self):
        self.testing_emails_body = {}

    def train(self, training_dir):
        training_corpus = corpus.TrainingCorpus(training_dir)
        self.trained_corpus_dict = training_corpus.get_overall_spammicity()

    def test(self, testing_dir):
        # TODO:
        # - solutions for similiar words (eg. those with extra "!")
        # -- maybe look for subsets of words
        testing_corpus = corpus.TestingCorpus(testing_dir)

        testing_words_counter = testing_corpus.count_words_from_emails()

        # complete_counter should have all words from training and
        # testing emails valued by their spammicity levels
        testing_complete_counter = self.value_for_words_in_email(testing_words_counter)
        complete_counter = self.remove_neutral_words(testing_complete_counter)

        predicted_spam_probability = {}
        # Final formula to calculate email's spam probability
        for email in testing_corpus.emails_body:
            numerator = 1
            denominator = 1
            words_considered = 0
            for word in testing_corpus.emails_body[email]:
                # TODO:
                # a bit awkward way to remove words with those weights 0, 1
                if complete_counter[word] != 0 and complete_counter[word] != 1:
                    # TODO:
                    # I am not really sure about the order of operations here
                    numerator *= complete_counter[word]
                    denominator += numerator
                    denominator *= (1 - complete_counter[word])
                words_considered += 1
                # TODO: Consider words with the most important weights
                # Now first fifteen words are considered
                if (words_considered > 15):
                    break
            predicted_spam_probability[email] = numerator / denominator

        self.write_results_to_file(predicted_spam_probability, testing_dir)

    def value_for_words_in_email(self, words_in_email):
        # fill the counter with values of words not seen in training phase
        complete_counter = Counter()
        for word in words_in_email:
            # Word was found in training dataset
            if word in self.trained_corpus_dict:
                complete_counter[word] = self.trained_corpus_dict[word]
            # word is new
            else:
                # Which value is best for word
                # that was not in the training corpus
                # Now it is set on 0.4
                complete_counter[word] = SPAM_VALUE_FOR_NEW_WORD
        return complete_counter

    def remove_neutral_words(self, word_counter):
        # remove words which are neither indicating spam or ham
        new_word_counter = Counter()
        for word in word_counter:
            if word_counter[word] != 0.5:
                new_word_counter[word] = word_counter[word]
        return new_word_counter

    def write_results_to_file(self, predicted_spam_probability, testing_dir):
        result_dict = {}
        files = os.listdir(testing_dir)
        for email in files:
            if predicted_spam_probability[email] > SPAM_PROBABILITY_TOLERANCE:
                result_dict[email] = SPAM_TAG
            else:
                result_dict[email] = HAM_TAG
        utils.write_classification_to_file(
                    os.path.join(testing_dir, '!prediction.txt'), result_dict)
