import csv   #reads the dataset row by row
import re    #regular expressions, pulls individual words out of text
import json  #to save the lexicon as a JSON file
import os    #operating system, creates the output folder

#python's csv module refuses to read any single cell larger than 131,072
csv.field_size_limit(2**31 - 1) #allows very long cells as some job descriptions are very long

#columns of the dataset that contain searchable text
text_columns = [
    "company_name",
    "title",
    "description",
    "location",
    "formatted_work_type",
    "formatted_experience_level",
    "skills_desc"
]

#one or more characters that are a-z or 0-9".
word_pattern = re.compile(r"[a-z0-9]+")


def tokenize(text):
    # turns text into lowercase words and removes apostrophe
    text = text.lower().replace("'", "").replace("\u2019", "")

    #extracts words and keeps short numbers
    return [w for w in word_pattern.findall(text)
            if len(w) <= 25 and not (w.isdigit() and len(w) > 4)]


def save_json(data, output_path):
    
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        #separators remove spaces making the file smaller and faster
        json.dump(data, file, ensure_ascii=False, indent=0, separators=(",", ":"))   # <-- NEW: indent=0 (one word per line)


def generate_lexicon(file_path):
    #Reads the dataset and return a dictionary {word: unique_id}

    #set stores each word only once
    unique_words = set()

    #encoding="utf-8-sig" removes the invisible BOM character at the start of some CSV files
    #errors="replace" stops the program from crashing on bad characters
    #newline="" is what the csv module requires.
    with open(file_path, "r", encoding="utf-8-sig", errors="replace", newline="") as file:

        reader = csv.DictReader(file) #each row becomes a dictionary {column: value}

        for row in reader:              #goes through every job posting
            for column in text_columns: #checks each searchable column

                text = row.get(column)

                if text: #skips empty cells
                    #splits the text into words and add them to the set
                    unique_words.update(tokenize(text))

    #gives each word a unique ID
    return {word: i for i, word in enumerate(sorted(unique_words), start=1)}


def save_lexicon(lexicon, output_path):
    #Save the lexicon to a file and print a summary
    save_json(lexicon, output_path)

    #success messages
    print("Lexicon saved successfully!")
    print("Total unique words:", len(lexicon))