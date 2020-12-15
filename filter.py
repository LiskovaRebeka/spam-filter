import corpus
import os
import utils


class BaseFilter():
    # Parent class for all possible filter types
    temporary_evaluation = "OK"

    def test(self, dir_path):
        result_dict = {}
        files = os.listdir(dir_path)
        for email in files:
            if email[0] != '!':
                result_dict[email] = self.classify_email()
        utils.write_classification_to_file(
                    os.path.join(dir_path, '!prediction.txt'), result_dict)

    def classify_email(self):
        return self.temporary_evaluation


class BayesFilter(BaseFilter):
    def train(training_directory):
        trained_corpus_dict = corpus.TrainingCorpus.get_overall_spammicity()
        # TODO:
        # get words from testing email
        # evaluate them with values from trained data
        # - problem with nonexistent words
        # - solutions for similiar words (eg. those with extra "!")
