#importing the functions from indexing.py
from indexing import generate_lexicon, save_lexicon, generate_forward_index

dataset_path = "Dataset/postings.csv"
lexicon_path = "Output/lexicon.json"
forward_path = "Output/forward_index.jsonl"
metadata_path = "Output/doc_metadata.json"

#indicated successful generation process
print("Generating lexicon...")
lexicon = generate_lexicon(dataset_path)
save_lexicon(lexicon, lexicon_path)

print("Generating forward index...")
generate_forward_index(dataset_path, lexicon, forward_path, metadata_path)