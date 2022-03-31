import numpy as np
import random


def average_len_of_names(path):
    print("enter")
    with open(path, encoding="utf-8") as file:
        line = file.readline()
        total_len = 0
        count = 0
        while line:
            if line[0].isdigit() == False:
                name = line.split(",")[0]
                count += 1
                total_len += len(name)
            line = file.readline()
        print(total_len/count)
        print("done")


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


def find(path, name):
    year = 0
    flag = True
    sendIt = False
    with open(path, encoding="utf-8") as file:
        line = file.readline()
        l = []
        while line:
            l = line.split(",")
            isYear = line[0].isdigit()
            lev = levenshtein(l[0], name)

            if line[0].isdigit():
                year = int(line.strip("\n"))
                pass
            if 2 < lev < 5 and flag == True and sendIt == False:
                print("Did you mean:", l[0], "?(1/0)")
                dym = int(input())
                if dym == 1:
                    flag = False
                elif dym == 0:
                    sendIt = True
            elif 2 < lev < 5 and isYear == 0 and sendIt == False:
                print("ilk")
                print(year, l[0], l[1], l[2])
            elif 2 < lev < 5 and isYear == 0 and sendIt == True and flag == True:
                print("ikinci")
                print(year, l[0], l[1], l[2])

            """if l[0] == name:
                print(year, l[1])
            else:
                stringMatch = levenshtein(name, l[0].lower())
                if 2 < stringMatch < 5:
                    print("did you mean,", l[0].lower())
                    input()"""
            line = file.readline()


def main():
    name = str(input("Enter driver's name:")).lower()
    find("sqlData.txt", name)
    print("zort")


main()
#print(levenshtein("max verstappen", "jos verstappen"))
