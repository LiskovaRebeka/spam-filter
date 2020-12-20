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
        self.array = ["from", "with", "mail"]

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

    def count_words_from_emails(self):
        word_counter = Counter()
        for file_name, file_body in self.emails():
            new_tokens = []
            new_tokens = self.separate_words_from_email(file_name, file_body)
            # Updates the word counter with values from current file
            self.emails_body[file_name] = Counter(new_tokens)
            word_counter += Counter(new_tokens)
        # make a list of emails
        for email, body in self.emails():
            self.all_emails.append(email)
        return word_counter   

            
    def separate_words_from_email(self, file_name, file_body):
        text = file_body.lower()
        text = self.remove_interpunction(text)
        tokens = text.split(" ")

        # Removes words that include 10% or more numbers
        deleted_tokens = 0
        for i in range(len(tokens)):
            number_of_digits = 0
            number_of_chars = 0
            for j in range(len(tokens[i-deleted_tokens])):
                number_of_chars += 1
                if tokens[i-deleted_tokens][j] > chr(33) and tokens[i-deleted_tokens][j] < chr(65):
                    number_of_digits += 1
            if (number_of_chars*0.1) < number_of_digits:
                del tokens[i-deleted_tokens]
                deleted_tokens += 1

                
        # This needs a rework, it is just a working version
        new_tokens = []
        for token in range(len(tokens)):
            if len(tokens[token]) > 3 and len(tokens[token]) < 15 and tokens[token] not in self.array:
                new_tokens.append(tokens[token])

        # TODO: html tags are not yet directly used
        html_tags = self.find_html_tags(new_tokens)
        return new_tokens

    def get_spammicity_of_word(self, word):
        # TODO:
        # If a word appears in a single email multiple times
        # should we count it only once or not?
        # Right now it is counted more times

        # Laplace smoothing - no word has probability 0.0 or 1.0
        spammicity = 1
        hammicity = 1
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
        # +2 because of Laplace smoothing 
        spammicity /= (number_of_spam_emails + 2)
        hammicity /= (number_of_ham_emails + 2)
        return (spammicity, hammicity)

    def get_overall_spammicity(self):
        # Calculates spammicity for all words in the dataset
        all_words = self.count_words_from_emails()
        spammicity_counter = Counter(all_words)
        hammicity_counter = Counter(all_words)
        for word in all_words:
            word_spammicity = self.get_spammicity_of_word(word)
            spammicity_counter[word] = word_spammicity[0]
            hammicity_counter[word] = word_spammicity[1]
        number_of_emails = len(self.truth_dict)
        number_of_spam_emails = self.get_number_of_spam_emails()

        # TODO: Probability of spam emails might change - it will not be the
        # same percentage on learning dataset and test dataset
        probability_of_spam_email = number_of_spam_emails/number_of_emails
        spam_value_of_all_words = Counter(all_words)
        # TODO:
        # Which probability of email being spam is best to apply?
        # Now it is set on 0.65
        
        # formula for filter
        for word in spam_value_of_all_words:
            spam_value_of_all_words[word] = self.get_spam_value_of_word(spammicity_counter[word], 0.65, hammicity_counter[word])
        # while testing functionality restrict the numbers with [.most_common]
        return (spam_value_of_all_words)

    def get_spam_value_of_word(self, spamicity_of_word, probability_of_spam_email, hamicity_of_word):
        numerator = spamicity_of_word*probability_of_spam_email
        denominator = spamicity_of_word*probability_of_spam_email + hamicity_of_word*(1-probability_of_spam_email)
        return numerator/denominator

    def remove_interpunction(self, text):
        removed_chars = [".", ":", ",", "!", "?", "\n", "\t", "(", ")", "=", "*"]
        for c in removed_chars:
            text = text.replace(c, " ")
            # if html tags are right next to each other make a space between
        text = text.replace(">", "> ")
        text = text.replace("<", " <")
        return text

    def find_html_tags(self, text):
        # also fixes invalid html tags
        html_tags = []
        for word in text:
            # TODO: Not only html tags are surrounded by <>
            if word[0] == "<" and word[-1] == ">":
                # Some tags are missing the end ">"
                complete_tag = word 
                html_tags.append(complete_tag)
        for tag in html_tags:
            text.remove(tag)

        return html_tags


class TestingCorpus(TrainingCorpus):
    # Almost identical to TrainingCorpus, but we can't use !truth.txt
    # in testing phase
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.all_emails = []
        self.emails_body = {}
        self.array = ["from", "with", "mail"]

# Time needed to run: ~20 seconds
