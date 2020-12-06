def read_classification_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
        if content == "":
            return {}
        items = {}
        for line in content:
            splitted_line = line.split()
            if splitted_line != '\n':
                items[splitted_line[0]] = splitted_line[1]
        return items


def write_classification_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        for key, value in content.items():
            file.write(key)
            file.write(" ")
            file.write(value)
            file.write('\n')
