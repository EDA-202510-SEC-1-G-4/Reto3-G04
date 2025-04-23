from DataStructures.Tree import rbt_node as rbn
from DataStructures.List import single_linked_list as al


def new_map():
    rbt = {'root':None,
           'type':'RBT'}
    return rbt


def rotate_left(node):
    if node != None and node['right'] == None:
        prin = node['left']
        left = node['left']['left']
        right = node
        node = prin
        node['left'] = left
        node['right'] = right
    elif node != None and node['right'] != None:
        prin = node['left']
        left = node['left']['left']
        right = node
        right2 = node['right']['right']
        node = prin
        node['left'] = left
        node['right'] = right
        node['right']['right'] = right2
    return node

def rotate_right(node):
    if node != None and node['right'] != None:
        prin = node['right']
        left = node
        node = prin
        node['left'] = left
    return

def flip_node_color(node):
    if node['color'] == 0:
        rbn.change_color(node,1)
    elif node['color'] == 1:
        rbn.change_color(node,0)
    return node

def flip_colors(node):
    if node != None:
        flip_node_color(node)
        if node['right'] != None:
            flip_node_color(node['right'])
        if node['left'] != None:
            flip_node_color(node['left'])
    return node

def insert_node(root,key,value):
    if root == None:
        root = rbn.new_node(key,value)
    elif root['key'] == key:
        root['value'] = value
    elif root['key'] > key:
        root = insert_node(root['left'],key,value)
    elif root['key'] < key:
        root = insert_node(root['right'],key,value)
    return root

def balance(root):
    if root != None and root['left'] != None:
        if rbn.is_red(root) and rbn.is_red(root['left']):
            root = rotate_left(root)

    if root != None and root['right'] != None:    
        if rbn.is_red(root['right']):
            root = rotate_right(root)
    
    if root != None and root['right'] != None and root['left'] != None:
        if rbn.is_red(root['right']) and rbn.is_red(root['left']):
            root = flip_colors(root)
    return root
        

def put(rbt,key,value):
    rbt['root'] = insert_node(rbt['root'],key,value)
    rbt['root'] = balance(rbt['root'])
    if rbn.is_red(rbt['root']):
        rbn.change_color(rbt['root'],1)
    return rbt

#Falta el recorrido de verificación para balanceo

def get_node(root,key):
    if root == None:
        root = None
    elif root['key'] > key:
        root = get_node(root['left'],key)
    elif root['key'] < key:
        root = get_node(root['right'],key)
    return root
    
def get(bst,key):
    res = None
    if bst != None:
        nodo = get_node(bst['root'],key)
        if nodo != None:
            res = nodo['value']
    return res
    
def contains(bst,key):
    aux = get(bst,key)
    res = False
    if aux != None:
        res = True
    return res 

def size(bst):
    size = 0
    if bst != None and bst['root'] != None:
        size = size_tree(bst['root'])
    return size 

def size_tree(root):
    if root == None:
        return 0
    else:
        return 1 + size_tree(root['left']) + size_tree(root['right'])
    
def is_empty(bst):
    return bst['root'] == None

def key_set(bst): 
    rta = al.new_list()
    def inorden(nodo):
            if nodo == None:
                return
            inorden(nodo['left'])
            al.add_last(rta,nodo['key'])
            inorden(nodo['right'])
    inorden(bst['root'])
    
    return rta
            
def value_set(bst):
    rta = al.new_list()
    def inorder(nodo):
            if nodo == None:
                return 
            inorder(nodo['left'])
            al.add_last(rta,nodo['value'])
            inorder(nodo['right'])
    inorder(bst['root'])
    
    return rta

def get_min_node(root):
    if root['left'] != None:
        root = get_min_node(root['left'])
    return root
    
def get_min(bst):
    key = None
    if bst['root'] != None and bst != None:
        nodo = get_min_node(bst['root'])
        key = nodo['key']
    return key
 # ese mk de echeverria es tremenda pinga
def get_max_node(root):
    if root['right'] != None:
        root = get_max_node(root['right'])
    return root

def get_max(bst):
    key = None
    if bst['root'] != None and bst != None:
        nodo = get_max_node(bst['root'])
        key = nodo['key']
    return key


def height_tree(root):
    if root is None:
        return 0
       
    else:
        altura_izquierda = height_tree(root['left'])
    
    
        altura_derecha = height_tree(root['right'])
    
    
    return 1 + max(altura_izquierda, altura_derecha)

def height(bst):
    return height_tree(bst["root"]) - 1

def keys_range(root,key_in,key_fin,list_key):
    if root == None:
        list_key = list_key
    elif root['key'] < key_in:
        keys_range(root['right'],key_in,key_fin,list_key)
    
    elif root['key'] > key_fin:
        keys_range(root['left'],key_in,key_fin,list_key)
    
    elif root['key'] >= key_in and root['key'] <= key_fin:
        list_key = al.add_last(list_key,root['key'])
        keys_range(root['left'],key_in,key_fin,list_key)
        keys_range(root['right'],key_in,key_fin,list_key)
        
    return list_key 

def keys(bst,key_in,key_fin):
    list_key = al.new_list()
    if bst != None and contains(bst,key_in) and contains(bst,key_fin):
        list_key = keys_range(bst['root'],key_in,key_fin,list_key)
    return list_key

def values_range(root,key_in,key_fin,list_val):
    if root == None:
        list_val = list_val
    elif root['key'] < key_in:
        values_range(root['right'],key_in,key_fin,list_val)
    
    elif root['key'] > key_fin:
        values_range(root['left'],key_in,key_fin,list_val)
    
    elif root['key'] >= key_in and root['key'] <= key_fin:
        list_val = al.add_last(list_val,root['value'])
        values_range(root['left'],key_in,key_fin,list_val)
        values_range(root['right'],key_in,key_fin,list_val)
        
    return list_val 

def values(bst,key_in,key_fin):
    list_val = al.new_list()
    if bst != None and contains(bst,key_in) and contains(bst,key_fin):
        list_val = values_range(bst['root'],key_in,key_fin,list_val)
    return list_val

def default_compare(key, element):
   if key == rbn.get_key(element):
      return 0
   elif key > rbn.get_key(element):
      return 1
   return -1