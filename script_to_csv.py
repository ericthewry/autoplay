#! /usr/bin/python

from argparse import ArgumentParser
import csv
import os


def aggregate_backwards(strings, start_index, num_words):
    aggregation = []
    idx = start_index
    while len(aggregation) < num_words and idx >= 0:
        curr_string_words = strings[idx].split()
        if len(curr_string_words) <= 0:
            idx -= 1
            continue

        if curr_string_words[0][0] == ">":
            curr_string_words[-1] += "<"
            
        words_needed = num_words - len(aggregation)
        if len(curr_string_words) < words_needed:
            aggregation = curr_string_words + aggregation
            idx -= 1
        else:
            # get as many words as is needed and break loop
            aggregation = curr_string_words[-words_needed:] + aggregation

        
    assert len(aggregation) <= num_words
    return " ".join(aggregation)



def process_file(script, n, csv_file):
    """writes a csv object containing the data contents of the `script` file. the inputs will contain at most `n` words"""

    script_text = ""
    with open(script, 'r') as scr_fp:
        script_text = scr_fp.read()

    lines = script_text.split("\n")

    # call is game output, response is user input
    # data goes response, call, response, call.. 
    call_and_response = []
    for line in lines:
        if not line or len(line) == 0:
            continue
        # current is call or previous was call
        if line[0] == ">" or (len(call_and_response) > 0 and call_and_response[-1][0] == ">"):
            # append
            call_and_response.append(line)
        else:
            #aggregate multi-line response output
            if len(call_and_response) > 0:
                call_and_response[-1] += line
            else:
                call_and_response.append(line)

    aggregated_call_history = []
    for i, line in enumerate(call_and_response):
        #currently a call
        if line[0] == ">" and i > 0:
            local_history = aggregate_backwards(call_and_response, i-1, n)
            aggregated_call_history.append((local_history, line))

    with open(csv_file, 'w', newline='\n') as csv_fp:
        writer = csv.writer(csv_fp, delimiter= ',', quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["game_response", "user_input"])
        for (hist, call) in aggregated_call_history:
            writer.writerow([hist, call])

    
def main():
    arg_parser = ArgumentParser(description="Convert IF Game Scripts to TSV format")
    arg_parser.add_argument("scripts", help="directory containing IF Game Scripts")
    arg_parser.add_argument("data", help="directory containing CSV Data")
    arg_parser.add_argument("--window_size", "-w", type=int, default=64, help="size of context window")

    settings = arg_parser.parse_args()

    script_dir = os.fsencode(settings.scripts)
    for filename_bytes in os.listdir(script_dir):
        filestring = filename_bytes.decode('utf8')
        print(filestring)
        outfile = settings.data + filestring.split('.')[0] + ".csv"
        process_file(settings.scripts + "\/" + filestring, settings.window_size, outfile)
            
        
    



if __name__ == "__main__":
    main()
