from math import ceil,gcd,inf
from Lib import heapq
from numpy import unique,sort
import copy

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
            self.get_gcd()
        # Set up for child node
        else:
            self.target = parent.target
            self.state = parent.state+pitcher
            self.pitcher_state=parent.pitcher_state
            self.pitchers_gcd=parent.pitchers_gcd
            # TODO: 增加注释 关于桶的情况
            if pitcher<0 and self.pitcher_state[abs(pitcher)]==0:
                self.gn = parent.gn+1
                self.pitcher_state[abs(pitcher)]=1
            else:
                self.gn = parent.gn+2 
            self.h = self.calculate_h()
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

    def get_gcd(self):
        pitchers=list(self.pitcher_state.keys())
        greatest_common_divisor = gcd(pitchers[0],pitchers[-1])
        for pitcher in pitchers:
            greatest_common_divisor =  gcd(greatest_common_divisor,pitcher)
        self.pitchers_gcd = greatest_common_divisor

    def calculate_h(self):
        target,state=self.target,self.state
        # detect if there is an answer
        if not abs(target - state)%self.pitchers_gcd == 0:
            return inf
        ancestor = self.parent
        while not ancestor.gn == 0:
            if ancestor.pitcher == (0-self.pitcher):
                return inf
            ancestor = ancestor.parent
        pitchers=list(self.pitcher_state.keys())
        result = (abs(target-state)/max(pitchers))
        #result = ceil(abs(target-state)/self.pitchers_gcd)
        return result

def print_results(list_pitcher):
    print("Start with a 0 volume Pitcher")
    state = 0
    count = 0
    pitcher_used = unique(list_pitcher)
    pitcher_state = {}
    for unique_pitcher in pitcher_used:
        pitcher_state[unique_pitcher] =0
    
    for pitcher in list_pitcher:
        state+=pitcher     
        if pitcher<0 and pitcher_state[pitcher]==0:
            print("Operation: Move " +str(abs(pitcher))+
                  " water from infinite cup to the "+str(abs(pitcher))
                  +" pitcher.(1 move) Total: "+str(state))
            pitcher_state[pitcher]=1
            count += 1
        else:
            if pitcher<0:
                print("Operation: Clear "+str(abs(pitcher))+" pitcher"
                      " Remove " +str(abs(pitcher))+
                      " water from infinite cup to the "+str(abs(pitcher))+
                      " pitcher.(2 move) Total: "+str(state))
                count += 2
            else:
                print("Operation: Fill a "+str(pitcher)+
                      " Pitcher then Add the water to infinite cup.(2 move) Total: "+str(state))
                count += 2
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
        current_state = current_node.get_results()
        current_state.sort()
        close_set.append(current_state)
        if current_node.fn == inf:
            continue
        for pitcher in pitchers:
            next_add_state = copy.deepcopy(current_state)
            next_add_state.append(pitcher)
            next_add_state.sort()
            if not next_add_state in close_set:
                add_pitcher_node = AStar_node(pitcher,current_node)
                heapq.heappush(open_set,add_pitcher_node)
                if add_pitcher_node.state == target:
                    result_list = add_pitcher_node.get_results()
                    print_results(result_list)
                    print(len(open_set))
                    return result_list,add_pitcher_node.gn    
            
            next_romove_state = copy.deepcopy(current_state)
            next_romove_state.append(int(0-pitcher))
            next_romove_state.sort()
            if current_node.state-pitcher>=0 and not next_romove_state in close_set:
                remove_pitcher_node = AStar_node(int(0-pitcher),current_node)
                heapq.heappush(open_set,remove_pitcher_node)
                if remove_pitcher_node.state == target:
                    result_list = remove_pitcher_node.get_results()
                    print_results(result_list)
                    print(len(open_set))
                    return remove_pitcher_node.gn  
          
    return -1

def load_text(filename):
    
    pitchers = []
    file= open(filename,'r').readlines()
    file[0] = file[0].replace("\n","")
    for number in file[0].split(','):
        if number.isdigit():
            pitchers.append(int(number))
    target= int(file[1])
    return pitchers,target
        
def main():
    pitchers,target=load_text('test_data/input.txt')
    result=AStar_search(pitchers, target)
    print(result)
    if result == -1:
        print("No results found")
    
if __name__ == '__main__':
    main()
    