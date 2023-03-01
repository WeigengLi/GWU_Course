from math import ceil
from Lib import heapq
from numpy import sort

class AStar_node:
    '''
    a node representing the operation of adding or removing water from
    the infinite cup
    attribute:
        pitcher: positive: add water
                 negative: remove water
        h: h(n) the heuristic
        parent: parent node
        add_gn: how many steps this move need
        gn:  g(n) representing how many steps is taken after this operation
        state:
    '''
    def __init__(self,pitcher,parent,target=None,pitcher_state=None):
        self.pitcher = pitcher
        self.parent = parent
        # Set up for root node
        if parent is None:
            self.state = 0
            self.gn = 0
            self.h = 0
            self.pitcher_state = pitcher_state
            self.target = target
        # Set up for child node
        else:
            self.target = parent.target
            self.state = parent.state+pitcher
            self.pitcher_state=parent.pitcher_state
            # TODO: 增加注释 关于桶的情况
            if pitcher<0 and self.pitcher_state[abs(pitcher)]==0:
                self.gn = parent.gn+1
                self.pitcher_state[abs(pitcher)]=1
            else:
                self.gn = parent.gn+2
            list_key=list(self.pitcher_state.keys())
            self.h = calculate_h(self.target, self.state,max(list_key))
        self.fn = self.gn+self.h
        
    def __lt__(self,other):
        return self.fn < other.fn
    
    def __str__(self):
        return str(self.fn)
    
    def get_results(self):
        if self.gn == 0:
            return []
        result = self.parent.get_results()
        result.append(self.pitcher)
        return result

def calculate_h(target,state,max_pitcher):
    return ceil(abs(target-state)/max_pitcher)

def print_results(list_pitcher):
    print("Start with a 0 volume Pitcher")
    state = 0
    count = 0
    for pitcher in list_pitcher:
        state+=pitcher
        if pitcher>=0:
            print("Operation: Fill a "+str(pitcher)+" Pitcher then Add the water to infinite cup.(2 move) Total: "+str(state))
            count += 2
        if pitcher<0:
            print("Operation: Remove " +str(abs(pitcher))+" water from infinite cup.(1 move) Total: "+str(state))
            count += 1
    print("Total: "+str(count)+" move")


def AStar_search(pitchers, target):
    open_set = []
    close_set = []
    pitcher_state = {}
    # if pitcher_state[pitcher] = 0 means this pitcher is empty
    for pitcher in pitchers:
        pitcher_state[pitcher] = 0
    root_node = AStar_node(0,None,target,pitcher_state)
    # use heapq push to change the open set into a heap
    heapq.heappush(open_set,root_node)
    current_node = None
    while open_set:
        current_node = heapq.heappop(open_set)
        close_set.append(current_node.state)
        for pitcher in pitchers:
            add_state = current_node.state+pitcher
            if not add_state in close_set:
                add_pitcher_node = AStar_node(pitcher,current_node)
                heapq.heappush(open_set,add_pitcher_node)
                if add_state == target:
                    result_list = add_pitcher_node.get_results()
                    print_results(result_list)
                    print(len(open_set))
                    return result_list,add_pitcher_node.gn    
            remove_state = current_node.state-pitcher
            if remove_state>=0 and not remove_state in close_set:
                remove_pitcher_node = AStar_node(int(0-pitcher),current_node)
                heapq.heappush(open_set,remove_pitcher_node)
                if remove_state == target:
                    result_list = remove_pitcher_node.get_results()
                    print_results(result_list)
                    print(len(open_set))
                    return remove_pitcher_node.gn  
          
    return -1

def load_text(filename ='input.txt'):
    pitchers = []
    file= open(filename,'r').readlines()
    file[0] = file[0].replace("\n","")
    for number in file[0].split(','):
        if number.isdigit():
            pitchers.append(int(number))
    target= int(file[1])
    return pitchers,target
        

def main():
    pitchers,target=load_text('input2.txt')
    result=AStar_search(pitchers, target)
    print(result)
    if result == -1:
        print("No results found")
    
if __name__ == '__main__':
    main()
    