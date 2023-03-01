import os
class Node:
    pass

def load_text(filename):
    # for read in files
    if not os.path.exists(filename):
        print('File '+filename+' does not exist')
        return
    pitchers = []
    file= open(filename,'r').readlines()
    Adjacent_Matrix = [] 
    for line in file:
        line.replace("\n","")
        for number in line.strip().split(','):
            if number.isdigit():
                pitchers.append(int(number))
    target= int(file[1])
    return pitchers,target

def main():
    pass

if __name__ == '__main__':
    main()