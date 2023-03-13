import os
from copy import deepcopy
import time
from Lib import heapq
from numpy import repeat

class graph_node():
    '''
    involved constrain: ic
    hn: 更小rv 更大ic 整体取最小hn
    '''
    def __init__(self,node,ic=-1):
        self.remain_value = deepcopy(color) 
        self.node = node
        self.color = -1
        self.rv = len(self.remain_value)
        self.ic = ic
        self.hn = self.rv-(self.ic/Max_neighbour)
    
    def update(self,color):
        '''
        Call this function if the neighbor of the node update it's color
        '''
        if self.color != -1:
            return
        self.ic -= 1
        self.remain_value.discard(color)
        self.rv = len(self.remain_value)
        self.hn = self.rv-(self.ic/Max_neighbour)
        
    def set_color(self,color):
        self.color = color
        self.remain_value = set([color])
    
    #设定优先级 less than 数字越小优先级越高
    def __lt__(self, other):
        return self.hn < other.hn
       

class CSP_Node:
    '''
    gn_priority_heap : 节点的优先队列
    wait_list: 下一个遍历的节点
    '''
    
    def __init__(self,parent=None,variable=None,value=None):
        self.parent = parent
        self.variable = variable
        self.value = value
        self.wait_list = []
        if parent is None:
            self.state_initial()
        else:  
            self.state = deepcopy(parent.state)  
            self.update_state()      
        self.get_priority_heap()   
    
    def update_state(self):
        self.state[self.variable].set_color(self.value)
        for neighbor in Adjacent_list[self.variable]:
            self.state[neighbor].update(self.value)

    
    def state_initial(self):
        '''
        iv: involved constrain = number of not colored neighbours
        '''
        self.state = dict()
        for node in Nodes:
            self.state[node] = graph_node(node=node,ic=len(Adjacent_list[node]))
    
    # 对未上色的节点进行优先级排序
    def get_priority_heap(self):    
        nodes = []
        for item in self.state.values():
            if item.color == -1:
                nodes.append(item)
        heapq.heapify(nodes)
        self.gn_priority_heap = nodes
           
    def forward_check(self,gn,color,second_time=False):
        
        for neighbor_index in Adjacent_list[gn.node]:
            neighbor = self.state[neighbor_index]
            new_neighbor_remain = neighbor.remain_value-set([color])
            # neighbor have same color or only have this color to choose
            if len(new_neighbor_remain)==0:
                return False
            # this node can only choose one color, also forwards check it's neighbor
            # use second time to keep forwards check at most recurs 2 times 
            if len(new_neighbor_remain)==1 and not second_time:
                if not self.forward_check(neighbor,new_neighbor_remain.pop(),second_time=True):
                    return False
        return True
    
    
    def choose_value(self):
        value = -1
        if(self.forward_check(value)):
            self.value = value
        pass
    
    def get_next(self):
        # 从wait_list获取下个节点，如果wait_list是空，从最佳没上色的顶点扩展下个节点
        if(not self.wait_list):
            if not self.gn_priority_heap:
                return -1
            gn = heapq.heappop(self.gn_priority_heap)
            if gn == None:
                return -1
            for remain in gn.remain_value:
                if(self.forward_check(gn,remain)):
                    self.wait_list.append(CSP_Node(parent=self,variable=gn.node,value=remain))
        # There is no legal color for this node
        if(not self.wait_list):
            return -1    
            # TODO: 颜色的选择有顺序
        return self.wait_list.pop()        

def CSP_Search():
    '''
    This is a backtracking search with CSP node
    '''
    root_node = CSP_Node()
    search_level = 0 
    tree_list = list(repeat(-1,len(Nodes)+1))
    tree_list[search_level] = root_node
    while search_level>-1:
        next=tree_list[search_level].get_next()
        if next == -1:
            search_level -= 1
            continue
        search_level += 1
        tree_list[search_level] = next
        if search_level == len(Nodes):
            return tree_list
    return []

def tree_exam(tree_list,print_color = True):
    result = dict()
    color_used = set()
    for node in tree_list:
        if node.variable==None:
            continue
        result[node.variable]=node.value
        color_used.add(node.value)
    if print_color: print('Answer: ',result)
    for key,val in result.items():
        for neighbor in Adjacent_list[key]:
            if val == result[neighbor]:
                print('Wrong Answer node',key, neighbor,'same value',val)
                return False
    print('Answer passed the constrain examination.',
          'Number of color have:' ,len(color),
          ' Number of color used:', len(color_used))
    return True

def load_text(filename):
    # Initialization
    color = -1
    Adjacent_list = dict()
    # files read in
    if not os.path.exists(filename):
        print('File '+filename+' does not exist')
        return color, None
    file= open(filename,'r').readlines()
    # read lines and store the edges
    for line in file:
        if line == '':
            continue
        line.replace("\n","")
        words = line.strip().split(',')
        # comment line
        if words[0] == '#':
            continue
        # Answer line
        if 'colors =' in line:
            color_key = line.strip().split(' ')     
            color = int(color_key[2])
            continue
        # Edges line
        if words[0].isdigit():
            number1, number2 = int(words[0]),int(words[1])
            if number1 in Adjacent_list.keys():
                Adjacent_list[number1].add(number2)
            else:
                Adjacent_list[number1] = set()
                Adjacent_list[number1].add(number2)
            if number2 in Adjacent_list.keys():
                Adjacent_list[number2].add(number1)
            else:
                Adjacent_list[number2] = set()
                Adjacent_list[number2].add(number1)  
    return color,Adjacent_list

def program_initialization(input):
    global Adjacent_list
    global color
    # a list of all nodes 
    global Nodes  
    global Max_neighbour
    Max_neighbour = 0
    data_dir = '6582AI/Project2/data/'
    num_color,Adjacent_list =load_text(data_dir+input)
    if num_color == -1 or not Adjacent_list:
        print('Read In file Problem No color or edges found') 
        return False
    color = set(range(1,num_color+1,1))
    Nodes = list(Adjacent_list.keys())
    for value in Adjacent_list.values():
        if len(value)> Max_neighbour:
            Max_neighbour = len(value)
    Max_neighbour = Max_neighbour+1
    return True

def calculate_time(time_start):
    time_end=time.time()
    cost_time = time_end-time_start
    if cost_time < 60:
        print('Time cost ',round(cost_time,5),'s')
    elif cost_time < 3600:
        print('Time cost ',(cost_time)/60,'min')
    elif cost_time > 3600:
        print('Time cost ',(cost_time)/3600,'hour')
    time_start = time_end
    return time.time()  

def test(inputs):
    time_start=time.time()
    for input in inputs:
        print('---------- Testing file',input,'---------- ')
        if not program_initialization(input):
            return False
        result = CSP_Search()
        time_start=calculate_time(time_start)
        if not result:
            print("No result found")
        else:
            tree_exam(result,print_color= True)
        

def main():
    inputs=['test1.txt', 'test2.txt','test3.txt', 'test4.txt']
    test(inputs)


if __name__ == '__main__':
    main()