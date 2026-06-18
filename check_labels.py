# check_labels.py
import pandas as pd

df = pd.read_csv('data/dataset.csv')

print("--- SAMPLE OF LABEL 0 ---")
print(df[df['label'] == 0]['url'].head(3).values)

print("\n--- SAMPLE OF LABEL 1 ---")
print(df[df['label'] == 1]['url'].head(3).values)