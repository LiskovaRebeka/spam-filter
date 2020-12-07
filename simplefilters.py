import utils
import os
import random


class NaiveFilter():
    def test(dir_path):
        result_dict = {}
        files = os.listdir(dir_path)
        for email in files:
            if email[0] != '!':
                result_dict[email] = "OK"
        utils.write_classification_to_file(
                    os.path.join(dir_path, '!prediction.txt'), result_dict)

    def train():
        pass


class ParanoidFilter():
    def test(dir_path):
        result_dict = {}
        files = os.listdir(dir_path)
        for email in files:
            if email[0] != '!':
                result_dict[email] = "SPAM"
        utils.write_classification_to_file(
                    os.path.join(dir_path, '!prediction2.txt'), result_dict)

    def train():
        pass


class RandomFilter():
    def test(dir_path):
        result_dict = {}
        files = os.listdir(dir_path)
        values = ["SPAM", "OK"]
        for email in files:
            if email[0] != '!':
                result_dict[email] = values[random.randint(0, 1)]
        utils.write_classification_to_file(
                    os.path.join(dir_path, '!prediction3.txt'), result_dict)

    def train():
        pass
