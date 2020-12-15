import utils
import os
import random


class BaseFilter():
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


class NaiveFilter(BaseFilter):
    temporary_evaluation = "OK"

    def classify_email(self):
        return self.temporary_evaluation

    def train():
        pass


class ParanoidFilter(BaseFilter):
    temporary_evaluation = "SPAM"

    def classify_email(self):
        return self.temporary_evaluation

    def train():
        pass


class RandomFilter(BaseFilter):
    temporary_evaluation = ["SPAM", "OK"]

    def classify_email(self):
        return self.temporary_evaluation[random.randint(0, 1)]

    def train():
        pass
