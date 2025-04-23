from DataStructures.Tree import bst_node as bn
from DataStructures.List import single_linked_list as sl

def new_map():
    root = {'root':None}
    return root

def insert_node(root,key,value):
    if root == None or key == root['key']:
        root = bn.new_node(key,value)
    elif key < root['key']:
        root['left'] = insert_node(root['left'],key,value)
    elif key > root['key']:
        root['right'] = insert_node(root['right'],key,value)
    return root

def put(bst,key,value):
    root = bst['root']
    bst['root'] = insert_node(root,key,value)
    return bst

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
    rta = sl.new_list()
    def inorden(nodo):
            if nodo == None:
                return
            inorden(nodo['left'])
            sl.add_last(rta,nodo['key'])
            inorden(nodo['right'])
    inorden(bst['root'])
    
    return rta
            
def value_set(bst):
    rta = sl.new_list()
    def inorder(nodo):
            if nodo == None:
                return 
            inorder(nodo['left'])
            sl.add_last(rta,nodo['value'])
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

def delete_min_tree(root):
    if root == None:
        root = None
    elif root['left'] == None and root['right'] == None:
        root = None
    elif root['left'] == None and root['right'] != None:
        root = root['right']
    else:
        delete_min_tree(root['left'])
    return root

def delete_min(bst):
    bst['root'] = delete_min_tree(bst['root'])
    return bst

def delete_max_tree(root):
    if root == None:
        root = None
    elif root['right'] == None and root['right'] == None:
        root = None
    elif root['right'] == None and root['left'] != None:
        root = root['left']
    else:
        delete_max_tree(root['right'])
    return root

def delete_max(bst):
    bst['root'] = delete_max_tree(bst['root'])
    return bst

def height_tree(root):
    if root is None:
        return 0
    # if root["left"] is None and root["right"] is None:
    #     return 0
    
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
        list_key = sl.add_last(list_key,root['key'])
        keys_range(root['left'],key_in,key_fin,list_key)
        keys_range(root['right'],key_in,key_fin,list_key)
        
    return list_key 

def keys(bst,key_in,key_fin):
    list_key = sl.new_list()
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
        list_val = sl.add_last(list_val,root['value'])
        values_range(root['left'],key_in,key_fin,list_val)
        values_range(root['right'],key_in,key_fin,list_val)
        
    return list_val 

def values(bst,key_in,key_fin):
    list_val = sl.new_list()
    if bst != None and contains(bst,key_in) and contains(bst,key_fin):
        list_val = values_range(bst['root'],key_in,key_fin,list_val)
    return list_val

def default_compare(key, element):
   if key == bn.get_key(element):
      return 0
   elif key > bn.get_key(element):
      return 1
   return -1