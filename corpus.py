import os
from collections import Counter
import utils

SPAM_TAG = "SPAM"
HAM_TAG = "OK"


class Corpus():
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.truth_dict = utils.read_classification_from_file(os.path.join(
                                            self.dir_path, '!truth.txt'))
        self.all_emails = []
        self.emails_body = {}

    def emails(self):
        files = os.listdir(self.dir_path)
        files_dict = {}
        for text_file in files:
            if text_file[0] == '!':
                continue
            text_file_path = os.path.join(self.dir_path, text_file)
            with open(text_file_path,  'r', encoding='utf-8') as opened_file:
                content = opened_file.read()
                files_dict[text_file] = content
            yield (text_file, content)


class TrainingCorpus(Corpus):
    def get_number_of_spam_emails(self):
        number_of_spam_emails = 0
        for email in self.truth_dict:
            if self.truth_dict[email] == SPAM_TAG:
                number_of_spam_emails += 1
        # Division by zero possible
        if number_of_spam_emails == 0:
            number_of_spam_emails = 1
        return number_of_spam_emails

    def separate_words_from_emails(self):
        word_counter = Counter()
        for file_name, file_body in Corpus.emails():
            text = file_body.lower()
            text = self.remove_interpunction(text)
            tokens = text.split(" ")

            # This needs a rework, it is just a working version
            # TODO: html elements should be filtered out
            new_tokens = []
            for token in range(len(tokens)):
                if len(tokens[token]) > 3 and len(tokens[token]) < 15:
                    new_tokens.append(tokens[token])

            self.emails_body[file_name] = Counter(new_tokens)

            # Updates the word counter with values from current file
            word_counter += Counter(new_tokens)
        # make a list of emails
        for email, body in self.emails():
            self.all_emails.append(email)
        return word_counter

    def get_spammicity_of_word(self, word):
        # TODO:
        # If a word appears in a single email multiple times
        # should we count it only once or not?
        # Right now it is counted more times
        spammicity = 0
        hammicity = 0
        for email in self.all_emails:
            words_freq = self.emails_body[email]
            if self.truth_dict[email] == SPAM_TAG:
                spammicity += words_freq[word]
            else:
                hammicity += words_freq[word]
        number_of_emails = len(self.truth_dict)
        number_of_spam_emails = self.get_number_of_spam_emails()
        number_of_ham_emails = number_of_emails - number_of_spam_emails
        # Division by zero possible
        if number_of_ham_emails == 0:
            number_of_ham_emails = 1
        spammicity /= number_of_spam_emails
        hammicity /= number_of_ham_emails
        return (spammicity, hammicity)

    def get_overall_spammicity(self):
        # Calculates spammicity for all words in the dataset
        all_words = self.separate_words_from_emails()
        spammicity_counter = Counter(all_words)
        hammicity_counter = Counter(all_words)
        for word in all_words:
            spammicity_counter[word] = self.get_spammicity_of_word(word)[0]
            hammicity_counter[word] = self.get_spammicity_of_word(word)[1]
        number_of_emails = len(self.truth_dict)
        number_of_spam_emails = self.get_number_of_spam_emails()
        number_of_ham_emails = number_of_emails - number_of_spam_emails
        probability_of_spam_email = number_of_spam_emails/number_of_emails
        probability_of_ham_email = number_of_ham_emails/number_of_emails
        #formula: (spamicity_of_word*probability_of_spam_email)
        #          /(spamicity_of_word*probability_of_spam_email + hamicity_of_word*probability_of_ham_email)
        # while testing functionality restrict the numbers with [.most_common]
        return (spammicity_counter, hammicity_counter)

    def remove_interpunction(self, text):
        text = text.replace(".", "")
        text = text.replace(",", "")
        text = text.replace("!", "")
        text = text.replace("?", "")
        text = text.replace("\n", " ")
        return text
    
# Time needed to run: cca 1 min.
# Examples of usage:

# Corpus = TrainingCorpus('[absolute path to a directory with emails]')
# print(Corpus.get_overall_spammicity())
