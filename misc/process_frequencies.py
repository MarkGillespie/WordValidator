# parse frequencies file
words = []
with open("frequencies.tsv") as f:
    for line in f.readlines():
        entry = line.split("\t")
        words.append(entry[1].strip().upper())

print(words[0:10])

words_by_length = [[] for i in range(50)]
for word in words:
    words_by_length[len(word)].append(word)

for i, word_list in enumerate(words_by_length):
    if len(word_list) == 0:
        continue
    print(i)
    print(len(word_list))
    if len(word_list) > 10:
        print(word_list[0:10])
    else:
        print(word_list)

with open("simple_lexicon.js", "w") as f:
    f.write("let simple_lexicon = [\n")
    for word in words:
        f.write(f"\"{word}\",")
    f.write("]\n")
    f.write("export { simple_lexicon };\n")
