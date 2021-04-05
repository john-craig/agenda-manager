import os

#os.rename(src, dst)

#os.listdir(path)

unhidden_directory = lambda item: (item.name[0] != '.') and (item.is_dir())

START_PATH = '/home/iranon/sync/ledger'


def lowercase_directories(path, depth=0):
    contents = os.scandir(path)

    directories = filter(unhidden_directory, contents)

    for directory in directories:
        prev_name = directory.name
        new_name = prev_name[0].lower() + prev_name[1:] if prev_name.find(' ') == -1 else prev_name

        indent = ''

        for i in range(0, depth):
            indent = indent + '--'

        print(indent + prev_name)
        print(indent + new_name)

        os.rename(path + '/' + prev_name, path + '/' + new_name)

        lowercase_directories(path + '/' + new_name, depth + 1)



lowercase_directories(START_PATH)
