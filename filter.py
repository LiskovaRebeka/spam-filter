import corpus
import os
import utils


class BaseFilter():
    # Parent class for all possible filter types
    def test(self, dir_path):
        result_dict = {}
        files = os.listdir(dir_path)
        for email in files:
            if email[0] != '!':
                # TODO: function classify.email()
                result_dict[email] = self.classify_email()
        utils.write_classification_to_file(
                    os.path.join(dir_path, '!prediction.txt'), result_dict)

    def classify_email(self):
        temporary_evaluation = "OK"
        return temporary_evaluation


class BayesFilter(BaseFilter):
    def train(self, training_dir):
        training_corpus = corpus.TrainingCorpus(training_dir)
        self.trained_corpus_dict = training_corpus.get_overall_spammicity()

    def test(self, dir_path):
        # TODO:
        # get words from testing email
        # evaluate them with values from trained data
        # - problem with nonexistent words
        # - solutions for similiar words (eg. those with extra "!")
        # -- maybe look for subsets of words

        testing_corpus = corpus.TrainingCorpus(dir_path)
        for file_name, file_body in testing_corpus.emails():
            testing_corpus_array = testing_corpus.separate_words_from_emails(file_name, file_body)
            words_in_email = []
            testing_word_counter = testing_corpus.count_words_from_emails()
            
            for i in range(len(testing_corpus_array)):
                words_in_email.append(testing_corpus_array[i])

            words_with_values = self.value_for_words_in_email(words_in_email)
            


        #resulting_dict = self.classify_emails(dir_path)
        # TODO: write the final evaluation to a file

    def value_for_words_in_email(self, words_in_email):
        dictionary = {}
        for word in words_in_email:
            if word in self.trained_corpus_dict:
                dictionary[word] = self.trained_corpus_dict[word]
            else:
                # Which value is best for word
                # that was not in the training corpus
                # Now it is set on 0.4
                dictionary[word] = 0.4
        return(dictionary)


    def classify_emails(self, dir_path):
        testing_corpus = corpus.TrainingCorpus(dir_path)
        testing_word_counter = testing_corpus.separate_words_from_emails()
        most_common_words_dict = {}
        for email in testing_corpus.emails_body:
            most_common_words_dict[email] = testing_corpus.emails_body[email].most_common(20)
        """
        for email in testing_corpus.emails_body:
            for word in most_common_words_dict:
                if isinstance(word, self.trained_corpus_dict):
                    print(word)
                    return
        """
        
        
