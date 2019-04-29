#! /usr/bin/python

from argparse import ArgumentParser
import csv
import wget
import string
import os

def extract_html(cmd_line):
    return cmd_line[cmd_line.index("\"") + 1 : -1]

def remove_left_tag(cmd_line):
    return cmd_line[cmd_line.index(">"):]

def remove_right_tag(cmd_line):
    return cmd_line[:cmd_line.index("<")]

def to_utf8(cmd_line):
    return cmd_line.replace("&gt;", ">")
                     

def unshorten(cmd_line):
    cmd = cmd_line.strip().lower()
    if cmd == ">i":
        return ">inventory"
    
    if cmd == ">l":
        return ">look"

    if cmd == ">z":
        return ">wait"

    if cmd == ">x" or cmd[:3] == ">x ":
        return ">examine" + cmd[2:]

    if cmd in [">north", ">n", ">go n"]:
        return ">go north"

    if cmd in [">south", ">s", ">go s"]:
        return ">go south"

    if cmd in [">east", ">e", ">go e"]:
        return ">go east"

    if cmd in [">west",">w", ">go w"]:
        return ">go west"

    if cmd in [">northwest", ">nw", ">go nw"]:
        return ">go northwest"

    if cmd in [">northeast", ">ne", ">go ne"]:
        return ">go northeast"

    if cmd in [">southwest", ">sw", ">go sw"]:
        return ">go southwest"

    if cmd in [">up", ">u", ">go u"]:
        return ">go up"

    if cmd in [">down", ">d", ">go d"]:
        return ">go down"


    if cmd in [">g", ">g"]:
        return ">again"

    return cmd_line
    
    


def clean_command(cmd_line):
    return unshorten(to_utf8(remove_right_tag(remove_left_tag(extract_html(cmd_line)))))


def remove_gt(cmd_line):
    return cmd_line.replace("&gt;", "")

def clean_parsed(cmd_line):
    return remove_gt(remove_right_tag(remove_left_tag(cmd_line.lower())))
    


def clean_floyd(floyd_file, clean_floyd_file):
    floyd_text = ""
    with open(floyd_file, 'rb') as ff_fp:
        floyd_text = ff_fp.read().decode("utf-8", "backslashreplace")

    floyd_lines = floyd_text.split('\n')

    clean_lines = []
    for l in floyd_lines:
        game_response = "<b>Floyd</b>"
        divider = "|"
        command_substring = "(to Floyd)"
        parsed_substring = "floydstyle input"
        try:
            if game_response in l and divider in l:
                interaction = l[l.index(divider) + 1 :]
                if parsed_substring not in l:
                    if "&gt;" not in interaction:
                        clean_lines.append(interaction)
                # else:
                    # clean_lines.append(clean_parsed(interaction))

            elif command_substring in l:
                clean_lines.append(clean_command(l[l.index(command_substring) + len(command_substring) :]))
                
        except ValueError:
            print("malformed line ", l)
            print("Tried to clean", l[l.index(command_substring) + len(command_substring) :])

            
    with open(clean_floyd_file, 'w') as cf_fp:
        cf_fp.write("\n".join(clean_lines))



def clean_name(name_str):
    return name_str.strip()\
                   .lower()\
                   .translate(str.maketrans('', '', string.punctuation))\
                   .replace(" ", "_")
        
def collect_urls(url_csv_file):
    reader = None
    file_list = []
    with open(url_csv_file, 'r') as urls_fp:
        reader = csv.DictReader(urls_fp)
        for row in reader:
            print("Downloading", row["url"])
            savefile = "floyddata/" + clean_name(row["name"]) + ".raw"
            if os.path.isfile(savefile):
                print("Already Downloaded", row["name"])
            else:
                print("Saving to", clean_name(row["name"]))        
                wget.download(row["url"], savefile)
                print("done")
            file_list.append((savefile, "clean_floyddata/" + clean_name(row["name"]) + ".clean"))

    return file_list
        
        

def cleanall(urlslist_file):
    for raw_file, clean_file in collect_urls(urlslist_file):
        # if raw_file == "floyddata/phoenixs_landing_destiny.raw":
        clean_floyd(raw_file, clean_file)
            
def main() :
    parser = ArgumentParser(description="Collect and clean data from ClubFloyd. This cleaning phase only makes the data look like it were collected via frotz's `SCRIPT` functionality")
    parser.add_argument("urls_list", help="path to file containing a list of html urls")

    # args = parser.parse_args()
    # cleanall(args.urls_list)

    



if __name__ == "__main__":
    main()
    
