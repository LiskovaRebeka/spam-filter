import os


class Corpus():
    def __init__(self, dir_path):
        self.dir_path = dir_path

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
