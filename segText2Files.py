import json
import os

def main():
    for subdir, dirs, files in os.walk('data'):
        for file in files:
            if file.endswith('json'):
                fullname = os.path.join(subdir, file)
                filename = os.path.splitext(file)[0]
                play_dir = "%s/%s" % (subdir, filename)
                if not os.path.exists(play_dir):
                    print(play_dir)
                    os.mkdir(play_dir)
                json_file = open(fullname, 'r')
                res = json.load(json_file)
                for character in res:
                    character_filename = "%s/%s.txt" % (play_dir, character)
                    with open(character_filename, 'w') as character_file:
                        for text in res[character]:
                            character_file.write("%s\n" % text)
main()