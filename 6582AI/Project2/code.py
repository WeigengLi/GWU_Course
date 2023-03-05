import os
class Node:
    pass

def load_text(filename):
    # for read in files
    if not os.path.exists(filename):
        print('File '+filename+' does not exist')
        return
    file= open(filename,'r').readlines()
    Adjacent_list = dict()
    color = -1
    for line in file:
        if line == '':
            continue
        line.replace("\n","")
        words = line.strip().split(',')
        if words[0] == '#':
            continue
        if words[0] == 'color':
            color = int(words[0])
            continue

        if words[0].isdigit():
            number1, number2 = int(words[0]),int(words[1])
            if words[0] in Adjacent_list.key():
                Adjacent_list[number1].add(number2)
            else:
                Adjacent_list[number1] = set()
                Adjacent_list[number1].add(number2)
            if words[1] in Adjacent_list.key():
                Adjacent_list[number2].add(number1)
            elif words[1].isdigit():
                Adjacent_list[number2] = set()
                Adjacent_list[number2].add(number1)
            
    
    return color,Adjacent_list

def main():
    pass

if __name__ == '__main__':
    main()