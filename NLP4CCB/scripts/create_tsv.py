import pandas as pd

df = pd.read_csv("relations_gt5.tsv", sep="\t")
df = df[["BASE_WORD", "INPUT_WORD"]]
df.to_csv("meronyms_test.tsv", sep="\t", index=False, header=False)
