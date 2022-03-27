import numpy as np
import random


def main():
    name = str(input("Enter driver's name:")).lower()
    find("sqlData.txt", name)
    print("zort")


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1] + 1,
                    matrix[x, y-1] + 1
                )
    # print(matrix)
    return (matrix[size_x - 1, size_y - 1])


#print(levenshtein("giovanni gusto", "giovanni gaspa"))


def find(path, name):
    year = 0
    with open(path, encoding="utf-8") as file:
        line = file.readline()
        l = []
        while line:
            if line[0].isdigit():
                year = int(line.strip("\n"))
                pass
            l = line.split(",")
            if l[0] == name:
                print(year, l[1])
            else:
                stringMatch = levenshtein(name, l[0].lower())
                if stringMatch < 5:
                    print("did you mean,", l[0].lower())
                    input()
            line = file.readline()
    # print(seasonal_data)


# main()


def rdm():
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    words1 = []
    words2 = []
    for i in range(1000):
        iter = random.randint(1, 15)
        thisWord = []
        thatWord = []
        for j in range(0, iter):
            thisWord.append(alphabet[random.randint(0, 25)])
            thatWord.append(alphabet[random.randint(0, 25)])
        words1.append("".join(thisWord))
        words2.append("".join(thatWord))

    rets = []
    for k in range(len(words1)):
        ret = levenshtein(words1[k], words2[k])
        rets.append(ret)
    avg = np.mean(rets)
    print(avg)


rdm()
