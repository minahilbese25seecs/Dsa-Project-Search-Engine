import csv   #reads the dataset row by row
import re    #regular expressions, pulls individual words out of text
import json  #to save the lexicon as a JSON file
import os    #operating system, creates the output folder

#for inverted index
from array import array #compact integer lists
from collections import defaultdict  #creates a missing entry automatically

#------------------LEXICON---------------------

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

    #------------------FORWARD INDEX---------------------

def generate_forward_index(file_path, lexicon, forward_path, metadata_path):
    #reads the dataset again and writes one line per document

    metadata = {} #small info per document used later for ranking and showing results

    os.makedirs(os.path.dirname(forward_path) or ".", exist_ok=True)

    with open(file_path, "r", encoding="utf-8-sig", errors="replace", newline="") as src, \
         open(forward_path, "w", encoding="utf-8") as out:

        #doc_id is simply the row number: 0, 1, 2, ...
        for doc_id, row in enumerate(csv.DictReader(src)):

            terms = {}   #word_id -> [frequency, field_mask, first_position]
            doc_len = 0  #total number of words in this document

            for bit, column in enumerate(text_columns):
                text = row.get(column)
                if not text:
                    continue

                flag = 1 << bit #every column gets its own flag: 1, 2, 4, 8, 16, 32, 64

                for position, word in enumerate(tokenize(text), start=1):
                    doc_len += 1
                    word_id = lexicon[word]

                    if word_id not in terms:
                        terms[word_id] = [0, 0, 0]

                    info = terms[word_id]
                    info[0] += 1    #frequency: how many times the word appears
                    info[1] |= flag #field_mask: remembers which columns contain the word

                    #position of the first appearance, only counted inside the description
                    if column == "description" and info[2] == 0:
                        info[2] = position

            #one flat list per document: [word_id, freq, mask, pos, word_id, freq, mask, pos, ...]
            flat = [v for word_id in sorted(terms) for v in (word_id, *terms[word_id])]

            out.write(json.dumps({"d": doc_id, "len": doc_len, "t": flat},
                                 separators=(",", ":")) + "\n")

            #info needed later to rank and display the results
            metadata[doc_id] = {
                "job_id": row.get("job_id"),
                "title": row.get("title"),
                "company": row.get("company_name"),
                "location": row.get("location"),
                "views": row.get("views"),
                "applies": row.get("applies"),
                "listed_time": row.get("listed_time"),
                "url": row.get("job_posting_url"),
                "snippet": " ".join((row.get("description") or "")[:400].split())[:200]
            }

    save_json(metadata, metadata_path)

    print("Forward index saved successfully!")
    print("Total documents:", len(metadata))

    #------------------INVERTED INDEX---------------------
def generate_inverted_index(forward_path, inverted_path):
    #reads the forward index and flips it

    #word_id -> [doc, freq, mask, pos, doc, freq, mask, pos, ...]
    inverted = defaultdict(lambda: array("i"))

    with open(forward_path, "r", encoding="utf-8") as file:
        for line in file: #one line = one document
            record = json.loads(line)
            doc_id = record["d"]
            flat = record["t"]

            #the list holds 4 numbers per word so jump 4 at a time
            for i in range(0, len(flat), 4):
                inverted[flat[i]].extend((doc_id, flat[i + 1], flat[i + 2], flat[i + 3]))

    #one line per word, sorted by word_id
    with open(inverted_path, "w", encoding="utf-8") as out:
        for word_id in sorted(inverted):
            postings = inverted[word_id]
            out.write('{"w":%d,"p":[%s]}\n' % (word_id, ",".join(map(str, postings))))

    print("Inverted index saved successfully!")
    print("Total words:", len(inverted))