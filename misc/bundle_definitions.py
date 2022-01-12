# parse definition file
definitions = {}
with open("definitions.tsv") as f:
    for line in f.readlines():
        entry = line.split("\t")
        definitions[entry[0]] = entry[1].strip()

buckets = [0, 6, 8, 10, 1000]
subdefinitions = [{} for _ in buckets]

for word, definition in definitions.items():
    for i, limit in enumerate(buckets):
        if len(word) <= limit:
            subdefinitions[i-1][word] = definition
            break

def printDefinitions(lower, upper, bucket):
    with open(f"definitions_{lower+1}-{upper}.js", "w") as f:
        f.write(f"var definitions_{lower+1}_{upper} = {{\n") # double {{ escapes the { in an f-string
        for word, definition in bucket.items():
            escaped_definition = definition.replace('"','\\"')
            f.write(f"\"{word}\" : \"{escaped_definition }\",\n")
        f.write("};")

for lower, upper, bucket in zip(buckets, buckets[1:], subdefinitions):
    print(f"[{lower+1}-{upper}] :\t {len(bucket)} words")
    printDefinitions(lower, upper, bucket)
