import copy
from math import ceil,gcd,inf
import os
from Lib import heapq
from numpy import unique
import time

class AStar_node:
    '''
    a node representing the operation of adding or removing water from
    the infinite cup
    attribute:
        pitcher: positive: add water to target
                 negative: remove water from to target
        h: h(n) the heuristic
        gn:  g(n) representing how many steps is taken after this operation
            g(n)=g(n-1)+1 or g(n)=g(n-1)+2
        fn: f(n) = g(n)+h(n)
        parent: parent node
        add_gn: how many steps this move need
        state: water in the target pitcher
    '''
    def __init__(self,pitcher,parent,target=None,pitcher_state=None):
        self.pitcher = pitcher
        self.parent = parent
        # Set up for root node
        if parent is None:
            self.state = 0
            self.gn = 0
            self.h = 0
            self.pitcher_state = copy.deepcopy(pitcher_state)
            self.target = target
            self.get_gcd()
        # Set up for child node
        else:
            self.target = parent.target
            self.state = parent.state+pitcher
            self.pitcher_state=copy.deepcopy(parent.pitcher_state)
            self.pitchers_gcd=copy.deepcopy(parent.pitchers_gcd)
            # g(n)=g(n-1)+1 or g(n)=g(n-1)+2 explained in report
            if pitcher<0 and self.pitcher_state[abs(pitcher)]==0:
                self.gn = parent.gn+1
                self.pitcher_state[abs(pitcher)]=1
            else:
                self.gn = parent.gn+2 
            # calculate h(n)
            self.h = self.calculate_h()
        self.fn = self.gn+self.h
        
    def __lt__(self,other):
        # fn is the value when comparing the node
        # e.g. AStar_node1 < AStar_node2 means AStar_node1.fn < AStar_node2.fn
        return self.fn < other.fn
    
    def __str__(self):
        # a function called by print() 
        return str(self.fn)
    
    def get_results(self):
        # iterate from leaf to root to get a list of pitchers that the algorithm used
        if self.gn == 0:
            return []
        result = self.parent.get_results()
        result.append(self.pitcher)
        return result

    def get_gcd(self):
        # calculate gcd of all pitchers, explain in first section of report
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
        # There are redundant moves in this operation(add n water then remove n water)
        while not ancestor.gn == 0:
            if ancestor.pitcher == (0-self.pitcher):
                return inf
            ancestor = ancestor.parent
        pitchers=list(self.pitcher_state.keys())
        # calculate h(n)
        result = ceil(abs(target-state)/max(pitchers))
        #result = ceil(abs(target-state)/self.pitchers_gcd)
        return result

def print_results(list_pitcher):
    '''
    This function takes a list of pitchers.
    Then print the step and exam the results
    '''
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

def AStar_search(pitchers, target,print_result):
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
    max_state = 0
    # BFS 
    while open_set:
        # pop the node with lowest fn
        current_node = heapq.heappop(open_set)
        # Not expending node in close set
        if current_node.state in close_set:
            continue
        close_set.append(current_node.state)
        # this is for 
        if current_node.state>max_state:
            max_state = current_node.state
        # this is the goal
        if current_node.state == target:
            result_list = current_node.get_results()
            if print_result:print_results(result_list)
            return current_node.gn    
        # Expend next nodes
        for pitcher in pitchers:
            add_state = current_node.state+pitcher
            if not add_state in close_set:
                add_pitcher_node = AStar_node(pitcher,current_node)
                # this node may leads to results
                if not add_pitcher_node.fn == inf: 
                    heapq.heappush(open_set,add_pitcher_node)
            remove_state = current_node.state-pitcher
            if remove_state>=0 and not remove_state in close_set:
                remove_pitcher_node = AStar_node(int(0-pitcher),current_node)
                # this node may leads to results
                if not remove_pitcher_node.fn == inf: 
                    heapq.heappush(open_set,remove_pitcher_node)
    return -1

def load_text(filename):
    # for read in files
    if not os.path.exists(filename):
        print('File '+filename+' does not exist')
        return
    pitchers = []
    file= open(filename,'r').readlines()
    file[0] = file[0].replace("\n","")
    for number in file[0].strip().split(','):
        if number.isdigit():
            pitchers.append(int(number))
    target= int(file[1])
    return pitchers,target

def test(print_result):
    '''
    Test multiple files
    print_result: boolean if this function print results
    '''
    correct_result_list = [19,7,-1,-1,36]
    input_files = ['input','input1','input2','input3','input4']
    count=0
    for input in input_files:
        file = 'test_data/'  +input+'.txt'
        if not single_test(file,correct_result_list[count]):
            print("Wrong result end test") 
            return False  
        count+=1
    print("All Tests Successfully") 
    return True      

def single_test(input,answer=None):
    '''
    Test an single input file
    and exam the result 
    '''
    file = load_text(input)
    if(not file):
        return -1
    pitchers,target=file
    print('-----------Testing '+str(input)+' File-----------')
    print('Pitchers:',pitchers)
    print('Target:',target)
    result=AStar_search(pitchers,target,True)
    if result == -1:
        print('Result: ',result," No results found")
    else:
        print('Result: ',result)
    print('-----------End of '+str(input)+' File Test-----------')
    # unknown result
    if answer == None:
        return True
    # exam result
    if result == answer:
        return True
    else:
        print('Wrong Answer for File: ',input)
        print("Correct result: ",answer)
        print("Output move: "+str(result))
        return False
    
def calculate_time(time_start):
    time_end=time.time()
    cost_time = time_end-time_start
    if cost_time < 60:
        print('Time cost ',cost_time,'s')
    elif cost_time > 60:
        print('Time cost ',(cost_time)/60,'min')
    elif cost_time > 3600:
        print('Time cost ',(cost_time)/3600,'hour')
    return time.time()
      
def main():
    time_start=time.time()
    #Test Case on PDF
    test(print_result=True)
    time_start=calculate_time(time_start)
    # Self Define test case(File read in)
    single_test('test_data/input_test.txt')
    time_start=calculate_time(time_start)
    # Self Define test case(Function input)
    result=AStar_search(pitchers =[1,90,200],target=20,print_result=True)
    print(result)
     
if __name__ == '__main__':
    main()
    