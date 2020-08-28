
with open("words.txt") as f:
    words = f.readlines()

words2 = ""
for word in words:
    if len(word) <= 4:
        pass
    else:
        words2 += word

with open("words.txt", "w") as f:
    f.write(words2)