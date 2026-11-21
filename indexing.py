import csv #imports the CSV library to read data from dataset

import re #imports the regular expression library to extract individual words

import json #imports the library to save result in JSON format 

import os #imports operating system library to perform file opertions

#making function to generte lexicon
def generate_lexicon(file_path):

    unique_words = set() #set eliminated duplicates

    text_columns = [
        "company_name",
        "title",
        "description",
        "location",
        "formatted_work_type",
        "formatted_experience_level",
        "skills_desc"
    ]

    #read the CSV file row by row
    with open(file_path, "r", encoding="utf-8-sig", errors="replace", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader: #loops through every row

            #extract text from selected columns
            for column in text_columns:

            #retrieves the value of the current column or returns an empty string if it is missing
                text = row.get(column, "")

                if text:
                    #convert text to lowercase
                    text = text.lower()

                    #extract individual words
<<<<<<< HEAD
                    words = re.findall(r"\b[a-z][a-z0-9]*\b", text)
=======
                    words = re.findall(r"\b[a-z]+\b", text)
>>>>>>> c9a6375 (Filter out numeric and alphanumeric tokens from lexicon)
                    #add words to the set
                    unique_words.update(words)

    #assign a unique ID to each word
    lexicon = {}

    for term_id, word in enumerate(sorted(unique_words), start=1):
        lexicon[word] = term_id

    return lexicon

#saves lexicon in output
def save_lexicon(lexicon, output_path):

    #open file in writw mode
    with open(output_path, "w", encoding="utf-8") as file:
        #lexicon dictionary into JSON format and writes it to the output file
        json.dump(lexicon, file, ensure_ascii=False, indent=4)

    #success message
    print("Lexicon saved successfully!")
    print("Total unique words:", len(lexicon))
