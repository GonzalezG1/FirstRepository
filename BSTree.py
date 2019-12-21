
# coding: utf-8

# # BSTree
# 
# ## Overview
# 
# In this notebook you will modify the binary search tree implementation completed in class so that it can be used as a mapping structure. The `Node` class will be updated so as to hold separate key and value attributes (instead of a single value, as it currently does), and instead of the `add` method, you should implement the [`__getitem__`](https://docs.python.org/3.5/reference/datamodel.html#object.__getitem__) and [`__setitem__`](https://docs.python.org/3.5/reference/datamodel.html#object.__setitem__) methods in order to associate keys and values. `__delitem__`, `__contains__`, and `__iter__` will also need to be updated, to perform key-based removal, search, and iteration. Finally, the `keys`, `values`, and `items` methods will return iterators that allow the keys, values, and key/value tuples of the tree (all sorted in order of their associated keys) to be traversed.
# 
# If `__setitem__` is called with an existing key, the method will simply locate the associated node and update its value with the newly provided value (as you would expect a mapping structure to do). If either `__getitem__` or `__delitem__` are called with a key that does not exist in the tree, a `KeyError` should be raised.
# 
# The API described above will allow the tree to be used as follows:
# 
#     t = BSTree()
#     t[0] = 'zero'
#     t[5] = 'five'
#     t[2] = 'two'
# 
#     print(t[5])
#     
#     t[5] = 'FIVE!!!'
# 
#     for k,v in t.items():
#         print(k, '=', v)
# 
#     del t[2]
# 
#     print('length =', len(t))
#     
# The expected output of the above follows:
# 
#     five
#     0 = zero
#     2 = two
#     5 = FIVE!!!
#     length = 2
# 
# The following `BSTree` class contains an updated `Node`, and stubs for the methods you are to implement. The first few simple test cases beneath the class definition should help clarify the required behavior.

# In[1]:


class BSTree:
    class Node:
        def __init__(self, key, val, left=None, right=None):
            self.key = key
            self.val = val
            self.left = left
            self.right = right
            
    def __init__(self):
        self.size = 0
        self.root = None
        
    def __getitem__(self, key):
        # YOUR CODE HERE
        def get_rec(node):
            if not node:
                raise KeyError
            elif key < node.key:
                return get_rec(node.left)
            elif key > node.key:
                return get_rec(node.right)
            elif key == node.key:
                return node.val
            else:
                raise KeyError
        return get_rec(self.root)
        #raise NotImplementedError()
    
    def __setitem__(self, key, val):
        # YOUR CODE HERE
        def set_rec(node):
            if not node:
                return BSTree.Node(key, val)
            elif key == node.key:
                node.val = val
                return node
            elif key < node.key:
                node.left = set_rec(node.left)
                return node
            elif key > node.key:
                node.right = set_rec(node.right)
                return node

        self.root = set_rec(self.root)
        self.size += 1
       # raise NotImplementedError()
        
    def __delitem__(self, key):
        # YOUR CODE HERE
        #raise NotImplementedError()
        def delitem_rec(node):
            if node.key < key:
                node.right = delitem_rec(node.right)
                return node
            elif node.key > key:
                node.left = delitem_rec(node.left)
                return node
            elif node.key == key:
                if not node.left and not node.right:
                    return None
                elif node.left and not node.right:
                    return node.left
                elif not node.left and node.right:
                    return node.right
                else:
                    t = node.left
                    if not t.right:
                        node.left = t.left
                        node.val = t.val
                        node.key = t.key
                    else:
                        n = t
                        while n.right.right:
                            n = n.right
                        t = n.right
                        n.right = t.left
                        node.val = t.val
                        node.key = t.key
                    return node
            else:
                raise KeyError
        self.root = delitem_rec(self.root)
        self.size -= 1
        
    def __contains__(self, key):
        # YOUR CODE HERE
        
        def find(t):
            if not t:
                return False
            elif t.key == key:
                return True
            elif t.key > key:
                return find(t.left)
            elif t.key < key:
                return find(t.right)

        return find(self.root)
       # raise NotImplementedError()
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        # YOUR CODE HERE
       # raise NotImplementedError()
        
        def iter_rec(node):
            if node:
                # for x in iter_rec(node.left):
                # yield x
                yield from iter_rec(node.left)
                yield node.key
                # for x in iter_rec(node.right):
                # yield x
                yield from iter_rec(node.right)

        return iter_rec(self.root)
        
    def keys(self):
        # YOUR CODE HERE
        #raise NotImplementedError()
        def iter_rec(node):
            if node:
                # for x in iter_rec(node.left):
                # yield x
                yield from iter_rec(node.left)
                yield node.key
                # for x in iter_rec(node.right):
                # yield x
                yield from iter_rec(node.right)

        return iter_rec(self.root)

    def values(self):
        # YOUR CODE HERE
        #raise NotImplementedError()
        def iter_rec(node):
            if node:
                # for x in iter_rec(node.left):
                # yield x
                yield from iter_rec(node.left)
                yield node.val
                # for x in iter_rec(node.right):
                # yield x
                yield from iter_rec(node.right)

        return iter_rec(self.root)

    def items(self):
        # YOUR CODE HERE
        #raise NotImplementedError()
        def iter_rec(node):
            if node:
                # for x in iter_rec(node.left):
                # yield x
                yield from iter_rec(node.left)
                yield (node.key, node.val)
                # for x in iter_rec(node.right):
                # yield x
                yield from iter_rec(node.right)

        return iter_rec(self.root)
        
    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes  = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.key, width=width//2**level)
        print(repr_str)
    
    def height(self):
        """Returns the height of the longest branch of the tree."""
        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1+height_rec(t.left), 1+height_rec(t.right))
        return height_rec(self.root)


# In[11]:


# 2 points

from unittest import TestCase

tc = TestCase()
t = BSTree()
tc.assertEqual(len(t), 0)
tc.assertFalse(0 in t)
t[0] = 'zero'
tc.assertTrue(0 in t)
tc.assertEqual(len(t), 1)


# In[12]:


# 2 points

from unittest import TestCase

tc = TestCase()
t = BSTree()
tc.assertEqual(len(t), 0)
t[0] = 'zero'
tc.assertEqual(t[0], 'zero')


# In[13]:


# 2 points

from unittest import TestCase

tc = TestCase()
t = BSTree()
tc.assertEqual(len(t), 0)
t[0] = 'zero'
del t[0]
tc.assertFalse(0 in t)
tc.assertEqual(len(t), 0)


# In[14]:


# 2 points

from unittest import TestCase

tc = TestCase()
t = BSTree()
key_vals = [(0, 'zero'), (2, 'two'), (1, 'one')]
sorted_key_vals = sorted(key_vals)

for k,v in key_vals:
    t[k] = v

for i,k in enumerate(t.keys()):
    tc.assertEqual(k, sorted_key_vals[i][0])


# In[6]:


# 1 point

from unittest import TestCase

tc = TestCase()
t = BSTree()
key_vals = [(0, 'zero'), (2, 'two'), (1, 'one')]
sorted_key_vals = sorted(key_vals)

for k,v in key_vals:
    t[k] = v

for i,v in enumerate(t.values()):
    tc.assertEqual(v, sorted_key_vals[i][1])


# In[7]:


# 1 point

from unittest import TestCase

tc = TestCase()
t = BSTree()
key_vals = [(0, 'zero'), (2, 'two'), (1, 'one')]
sorted_key_vals = sorted(key_vals)

for k,v in key_vals:
    t[k] = v

for i,(k,v) in enumerate(t.items()):
    tc.assertEqual(k, sorted_key_vals[i][0])
    tc.assertEqual(v, sorted_key_vals[i][1])


# In[8]:


# 5 points

from unittest import TestCase
import random

tc = TestCase()
t = BSTree()
keys = list(range(100, 1000, 11))
random.shuffle(keys)
vals = [random.randrange(1000) for _ in range(100, 1000, 11)]

for i in range(len(keys)):
    t[keys[i]] = vals[i]

for i in range(len(keys)):
    tc.assertEqual(t[keys[i]], vals[i])


# In[9]:


# 5 points

from unittest import TestCase
import random

tc = TestCase()
t = BSTree()
keys = list(range(100, 1000, 11))
shuffled_keys = keys.copy()
random.shuffle(shuffled_keys)

for k in shuffled_keys:
    t[k] = str(k)

for i,k in enumerate(t.keys()):
    tc.assertEqual(k, keys[i])

for i,v in enumerate(t.values()):
    tc.assertEqual(v, str(keys[i]))

for i,(k,v) in enumerate(t.items()):
    tc.assertEqual(k, keys[i])
    tc.assertEqual(v, str(keys[i]))


# In[10]:


# 5 points

from unittest import TestCase
import random

tc = TestCase()
t = BSTree()
keys = list(range(0, 100, 2))
random.shuffle(keys)

for x in keys:
    t[x] = x*2

for k in range(1, 101, 2):
    with tc.assertRaises(KeyError):
        v = t[k]

