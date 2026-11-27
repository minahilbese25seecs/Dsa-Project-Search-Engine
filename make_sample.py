import csv, os
csv.field_size_limit(2**31 - 1)

base = os.path.dirname(os.path.abspath(__file__))        #folder where this script is saved
source = os.path.join(base, "Dataset", "postings.csv")
target = os.path.join(base, "Dataset", "sample_postings.csv")

with open(source, encoding="utf-8-sig", newline="") as f, \
     open(target, "w", encoding="utf-8", newline="") as o:
    reader, writer = csv.reader(f), csv.writer(o)
    for i, row in enumerate(reader):
        writer.writerow(row)
        if i == 150:          #header + 150 job postings
            break

print("Created:", target)
print("Rows written (including header):", i + 1)
print("File size (KB):", os.path.getsize(target) // 1024)