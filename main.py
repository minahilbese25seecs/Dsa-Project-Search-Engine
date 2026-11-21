#importing both functions from indexing.py
from indexing import generate_lexicon, save_lexicon

dataset_path = "Dataset/postings.csv"
output_path = "Output/lexicon.json"

#indicated successful generation process
print("Generating lexicon...")

#calling both functions
lexicon = generate_lexicon(dataset_path)
save_lexicon(lexicon, output_path)