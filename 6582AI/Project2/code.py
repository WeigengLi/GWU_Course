import os
from copy import deepcopy
from Lib import heapq

class graph_node():
    '''
    involved constrain: ic
    '''
    def __init__(self,node,color = -1):
        self.remain_value = deepcopy(color) 
        self.node = node
        self.color = -1
        self.rv = len(self.remain_value)
    
    def update(self,graph):
        iv = 0
        for neighbor_key in Adjacent_list[self.node]:
            neighbor = graph[neighbor_key]
            if neighbor.color != -1:
                iv += 1
            else:
                self.remain_value.discard(neighbor.color)
        self.rv = len(self.remain_value)
        self.iv = iv

    #设定优先级 less than 数字越小优先级越高
    def __lt__(self, other):
        if self.rv < other.rv:
            return True
        elif self.rv == other.rv:
            if self.ic > other.ic:
                return True
        return False

class CSP_Node:
    '''
    gn_priority_heap : 节点的优先队列
    wait_list: 下一个遍历的节点
    '''
    wait_list = []
    variable = None
    def __init__(self,parent=None,variable=None,value=None):
        if parent is None:
            self.graph = dict()
            for node in Nodes:
                self.graph[node] = graph_node(node) 
            self.get_priority_heap()
        else:
            self.variable = variable
            self.state = deepcopy(parent.state)
            if not value:
                self.value = value
                self.update_state()
            
            
    
    def update_state(self):
        pass
    
    # 对未上色的节点进行优先级排序
    def get_priority_heap(self):
        priority_heap = heapq()
        for key, item in self.graph():
            if item.color == -1:
                priority_heap.append(item)
        self.gn_priority_heap = priority_heap
           
    def forward_check(self):
        for key,node in self.graph:
            node.update()
            node.constrain_check()
    
    def choose_value(self):
        value = -1
        if(self.forward_check(value)):
            self.value = value
        pass
    
    def get_next(self):
        # 从wait_list获取下个节点，如果wait_list是空，从最佳没上色的顶点扩展下个节点
        if not self.wait_list:
            gn = self.gn_priority_heap.heappop()
            for remain in gn.remain_value:
                self.wait_list.append(CSP_Node(self,gn.node,remain))
        return self.wait_list.pop()        

def CSP_Search(color):
    root_node = CSP_Node()
    search_level = 0 
    tree_list = []
    tree_list.append(root_node)
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

def main():
    global Adjacent_list
    global color
    # a list of all nodes 
    global Nodes  
    num_color,Adjacent_list =load_text('6582AI/Project2/data/test1.txt')
    color = set(range(1,num_color+1,1))
    Nodes = list(Adjacent_list.keys())
    
    CSP_Search(color,Adjacent_list)

if __name__ == '__main__':
    main()