import os
import re
import matplotlib.pyplot as plt

lemma_count_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/lemma_verbs_count.txt'

file_lines = open(lemma_count_path).readlines()

counts = []
for line in file_lines[:500]:
    counts.append(int(re.compile(r'(\d+) .*').search(line).group(1)))

light_green_color = '#92CD00'
yellow_color = '#FFCC00'
blue_color = '#3333FF'
orange_color = '#FF6600'

plt.hist(counts, bins=len(file_lines)/3)
x = range(len(counts))
b1 = plt.bar(x, counts, color=orange_color, width=2, linewidth=0)
plt.xlabel('Verbs')
plt.ylabel('Count')

plt.show()


