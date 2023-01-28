import numpy as np

INSERTION = -3
DELETION = -3
MISMATCH = -3
MATCH = 3


def smithWaterman(line1, line2):
    
    matrix = np.zeros((len(line1)+1, len(line2)+1))

    for i in range(1, len(line1)+1):
        for j in range(1, len(line2)+1):
            ins = matrix[i][j-1] + INSERTION
            delet = matrix[i-1][j] + DELETION
            if(line1[i-1] == line2[j-1]):
                subs = matrix[i-1][j-1] + MATCH
            else:
                subs = matrix[i-1][j-1] + MISMATCH

            matrix[i][j] = max(ins, delet, subs, 0)
            
    # traceback

    maxi = matrix[0][0]
    index1 = 0
    index2 = 0

    for i in range(len(line1)+1):
        for j in range(len(line2)+1):
            if matrix[i][j] > maxi:
                maxi = matrix[i][j]
                index1 = i
                index2 = j

    temp1 = index1
    temp2 = index2

    for i in range(len(line1)+len(line2)-1):
        if((len(line1) == maxi/3) and matrix[index1-1][index2] == 0 and matrix[index1-1][index2-1] == 0 and matrix[index1][index2-1] == 0):
            print("Common line:   " + line1[index1-1:temp1] + "\n")
            break
        else:
            if(matrix[index1-1][index2] > matrix[index1][index2-1] and matrix[index1-1][index2] > matrix[index1-1][index2-1]):
                index1 -= 1
            elif(matrix[index1][index2-1] > matrix[index1-1][index2-1] and matrix[index1][index2-1] > matrix[index1-1][index2]):
                index2 -= 1
            elif(matrix[index1-1][index2-1] > matrix[index1][index2-1] and matrix[index1-1][index2-1] > matrix[index1-1][index2]):
                index1 -= 1
                index2 -= 1
            
def readFile(filename1, filename2):
    lines1 = open(filename1).readlines()
    lines2 = open(filename2).readlines()
    for i in lines1:
        for j in lines2:
            smithWaterman(i.strip(), j.strip())


if __name__ == "__main__":   
    file1 = input("Enter first file name (1.txt, 2.txt, 3.txt...): ")
    file2 = input("Enter second file name (1.txt, 2.txt, 3.txt...): ")
    readFile("txts/"+file1, "txts/"+file2)