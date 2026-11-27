from indexing import (generate_lexicon, save_lexicon,
                      generate_forward_index, generate_inverted_index)

dataset_path = "Dataset/sample_postings.csv"

lexicon = generate_lexicon(dataset_path)
save_lexicon(lexicon, "TestOutput/lexicon.json")
generate_forward_index(dataset_path, lexicon, "TestOutput/forward_index.jsonl", "TestOutput/doc_metadata.json")
generate_inverted_index("TestOutput/forward_index.jsonl", "TestOutput/inverted_index.jsonl")