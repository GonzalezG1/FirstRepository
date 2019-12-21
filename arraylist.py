
# coding: utf-8

# # Array-Backed Lists

# ## Overview
# 
# For this assignment you will complete the implementation of the array-backed list data structure (`ArrayList`) started during class, so that it supports (nearly) all the [common](https://docs.python.org/3.5/library/stdtypes.html#common-sequence-operations) and [mutable](https://docs.python.org/3.5/library/stdtypes.html#mutable-sequence-types) sequence operations.

# ## Implementation Details
# 
# For the `ArrayList`'s underlying data storage mechanism you will use the built-in Python list, constrained so that only the following operations (as would be supported by a primitive array) are available:
# 
# - `lst[i]` for getting and setting a value at an *existing, positive* index `i`
# - `len(lst)` to obtain the number of slots
# - `lst.append(None)` to grow the list by *one slot at a time*
# - `del lst[len(lst)-1]` to delete the last slot in a list
# 
# ### `ConstrainedList`
# 
# To help keep us honest, we've defined an API-constrained sub-class of the built-in list -- `ConstrainedList` -- an instance of which is assigned to the `data` attribute of each `ArrayList`. You should not change the definition of `ConstrainedList`, and ensure that your `ArrayList` implementation never assigns a regular Python list to its `data` attribute. So long as you use `ConstrainedList` in your implementation, you can be certain you're not performing any "illegal" operations (i.e., outside the constraints established above). If you invoke a disallowed operation, an appropriate exception will be raised.
# 
# Be sure to evaluate the following cell before testing your `ArrayList` implementation.

# In[3]:


class ConstrainedList (list):
    """Constrains the list class so it offers only the following primitive array API:
    
        - `lst[i]` for getting and setting a value at an *existing, positive* index `i`
        - `len(lst)` to obtain the number of slots
        - `lst.append(None)` to grow the list by *one slot at a time*
        - `del lst[len(lst)-1]` to delete the last slot in a list
        
       All other operations will result in an exception being raised.
    """
    
    def __init__(self, *args):
        super().__init__(*args)
    
    def append(self, value):
        if value is not None:
            raise ValueError('Can only append None to constrained list!')
        super().append(value)
        
    def __getitem__(self, idx):
        if idx < 0 or idx >= len(self):
            raise ValueError('Can only use positive, valid indexes on constrained lists!')
        return super().__getitem__(idx)

    def __setitem__(self, idx, value):
        if idx < 0 or idx >= len(self):
            raise ValueError('Can only use positive, valid indexes on constrained lists!')
        super().__setitem__(idx, value)

    def __delitem__(self, idx):
        if idx != len(self)-1:
            raise ValueError('Can only delete last item in constrained list!')
        super().__delitem__(idx)
        
    def __getattribute__(self, name):
        if name in ('insert', 'pop', 'remove', 'min', 'max', 
                    'index', 'count', 'clear', 'copy', 'extend'):
            raise AttributeError('Method "' + name + '" not supported on constrained list!')
        else:
            return super().__getattribute__(name)
    
    # __getattribute__ isn't called for special methods, so the following are needed

    def __add__(self, value):
        raise AttributeError('Constrained lists do not support `+`!')

    def __contains__(self, value):
        raise AttributeError('Constrained lists do not support `in`!')
        
    def __eq__(self, value):
        raise AttributeError('Constrained lists do not support `==`!')        
    
    def __iter__(self):
        raise AttributeError('Constrained lists do not support iteration!')
    
    def __str__(self):
        raise AttributeError('Constrained lists do not support stringification!')
    
    def __repr__(self):
        raise AttributeError('Constrained lists do not support stringification!')
        
    # for testing only! (don't use this in your ArrayList implementation)
    
    def _as_list(self):
        return list(super().__iter__())


# ### `ArrayList`
# 
# And now for the task at hand. We've partitioned the `ArrayList` methods you need to implement (and the test cases that follow) into seven categories:
# 
# 1. Subscript-based access (completed in class)
# 2. Stringification
# 3. Single-element manipulation
# 4. Predicates (True/False queries)
# 5. Queries
# 6. Bulk operations
# 7. Iteration
# 
# All told, there are 23 methods --- a handful of which have already been implemented for you --- whose behavior are specified in their docstrings below. Note that we left out API support for *slices* (e.g., `lst[start:stop:step]`); you can read about [how to support slices in the Python docs](https://docs.python.org/3.5/reference/datamodel.html#object.__length_hint__), but we just don't think it's worth the extra busywork.
# 
# 
# ### Hints / Advice
# 
# We strongly advise that you start with the first category of functions and move down the list sequentially, pausing after each to run the corresponding test cases. The only category that might be worth skipping to early on is *Iteration* --- which can help simplify several other methods. Keep in mind that while you're not permitted to make use of high level APIs in the underlying list, you can certainly make use of `ArrayList` methods you've already implemented.
# 
# For instance, your implementations of `pop` and `remove` can (and should) use the `del` operator on your own list to remove elements from the middle, and it probably makes sense to use `extend` in your `__add__` and `copy` methods.

# In[4]:


class ArrayList:
    def __init__(self):
        self.data = ConstrainedList() # don't change this line!

    
    ### subscript-based access ###
    
    def _normalize_idx(self, idx):
        nidx = idx
        if nidx < 0:
            nidx += len(self.data)
            if nidx < 0:
                nidx = 0
        return nidx
    
    def __getitem__(self, idx):
        """Implements `x = self[idx]`"""
        assert(isinstance(idx, int))
        nidx = self._normalize_idx(idx)
        if nidx >= len(self.data):
            raise IndexError
        return self.data[nidx]

    def __setitem__(self, idx, value):
        """Implements `self[idx] = x`"""
        assert(isinstance(idx, int))
        nidx = self._normalize_idx(idx)
        if nidx >= len(self.data):
            raise IndexError
        self.data[nidx] = value

    def __delitem__(self, idx):
        """Implements `del self[idx]`"""
        assert(isinstance(idx, int))
        nidx = self._normalize_idx(idx)
        if nidx >= len(self.data):
            raise IndexError
        for i in range(nidx+1, len(self.data)):
            self.data[i-1] = self.data[i]
        del self.data[len(self.data)-1]
    

    ### stringification ###
    
    def __str__(self):
        """Implements `str(self)`. Returns '[]' if the list is empty, else
        returns `str(x)` for all values `x` in this list, separated by commas
        and enclosed by square brackets. E.g., for a list containing values
        1, 2 and 3, returns '[1, 2, 3]'."""
        # YOUR CODE HERE 
        if len(self.data) == 0: 
            return '[]'
        else:
            return '[' + ', '.join(str(x) for x in self) + ']'

        #raise NotImplementedError()
        
    def __repr__(self):
        """Supports REPL inspection. (Same behavior as `str`.)"""
        if len(self.data) == 0: 
            return '[]'
        else:
            return '[' + ', '.join(str(x) for x in self) + ']'
        #raise NotImplementedError()


    ### single-element manipulation ###
    
    def append(self, value):
        """Appends value to the end of this list."""
        self.data.append(None)
        self.data[len(self.data)-1]=value
        #raise NotImplementedError()
    
    def insert(self, idx, value):
        """Inserts value at position idx, shifting the original elements down the
        list, as needed. Note that inserting a value at len(self) --- equivalent
        to appending the value --- is permitted. Raises IndexError if idx is invalid."""
        # YOUR CODE HERE
        if(idx > len(self.data)):
            raise IndexError
        if idx < 0 :
            raise IndexError
        elif(idx==len(self.data)):
            self.append(value)
        else:
            self.data.append(None)
        for i in range(len(self.data)-1, idx, -1):

            self.data[i]=self.data[i-1]
            self.data[i-1]=None
        self.__setitem__(idx, value)
                #raise NotImplementedError()
    
    def pop(self, idx=-1):
        """Deletes and returns the element at idx (which is the last element,
        by default)."""
        # YOUR CODE HERE
        nidx = self._normalize_idx(idx)
        temp = self[nidx]
        del self[nidx]
        return temp
        #raise NotImplementedError()
    
    def remove(self, value):
        """Removes the first (closest to the front) instance of value from the
        list. Raises a ValueError if value is not found in the list."""
        # YOUR CODE HERE
        flag=0
        for i in range(0, len(self.data)-1):
            if self.data[i]==value:
                self.__delitem__(i)
                flag+=1
                break
        if flag == 0:
            raise ValueError
        #raise NotImplementedError()
    

    ### predicates (T/F queries) ###
    
    def __eq__(self, other):
        """Returns True if this ArrayList contains the same elements (in order) as
        other. If other is not an ArrayList, returns False."""
        same = False
        if isinstance(other, ArrayList):
            for i in range(0, len(self.data)-1):
                if self.data[i] == other.data[i]:
                    same = True
                else:
                    return false
            return same
       # raise NotImplementedError()

    def __contains__(self, value):
        """Implements `val in self`. Returns true if value is found in this list."""
        found=False
        for i in range(0, len(self.data)-1):
            if self.data[i]==value:
                found = True
        return found
        #raise NotImplementedError()


    ### queries ###
    
    def __len__(self):
        """Implements `len(self)`"""
        count=0
        for x in range(0, len(self.data)):
            count+=1
        return count
    
    def min(self):
        """Returns the minimum value in this list."""
        min=self.data[0]
        for x in range(0, len(self.data)-1):
            if min > self.data[x]:
                min=self.data[x]
        return min
    
    def max(self):
        """Returns the maximum value in this list."""
        # YOUR CODE HERE
        max=self.data[0]
        for x in range(0, len(self.data)-1):
            if max < self.data[x]:
                max=self.data[x]
        return max
        #raise NotImplementedError()
    
    def index(self, value, i=0, j=None):
        """Returns the index of the first instance of value encountered in
        this list between index i (inclusive) and j (exclusive). If j is not
        specified, search through the end of the list for value. If value
        is not in the list, raise a ValueError."""
        # YOUR CODE 
        ValueFound=0
        if j==None:
            j=len(self.data)
            start = self._normalize_idx(i)
            end = self._normalize_idx(j)

            for x in range(start, end):
                if self.data[x]==value:
                    ValueFound+=1
                    return x
            if ValueFound==0:
                raise ValueError
        if j!=None:
            start = self._normalize_idx(i)
            end = self._normalize_idx(j)

            for x in range(start, end):
                if self.data[x]==value:
                    ValueFound+=1
                    return x
            if ValueFound==0:
                raise ValueError

    def count(self, value):
        """Returns the number of times value appears in this list."""
        # YOUR CODE HERE
        count=0
        for x in range(0, len(self.data)):
            if self.data[x]==value:
                count +=1
        return count
        #raise NotImplementedError()

    
    ### bulk operations ###

    def __add__(self, other):
        """Implements `self + other_array_list`. Returns a new ArrayList
        instance that contains the values in this list followed by those 
        of other."""
        newarray = ArrayList ()
        for i in range(0, len(self.data)):
            newarray.append(self.data[i])
        #newarray.data[i]=self.data[i]
        #newarray.data.append(None)
        #print(newarray.data[i], self.data[i])
        for i in range(0, len(other.data)):
            newarray.append(other.data[i])
        #newarray.data.append(None)
        #newarray.data[len(self.data)-1]=other.data[i]
        #print(newarray.data[i], self.data[i])
        return newarray
        
    def clear(self):
        self.data = ConstrainedList() # don't change this!
        
    def copy(self):
        """Returns a new ArrayList instance (with a separate data store), that
        contains the same values as this list."""
        newarray = ArrayList()
        for i in range(0, len(self.data)):
            newarray.append(self.data[i])
        return newarray

    def extend(self, other):
        """Adds all elements, in order, from other --- an Iterable --- to this list."""
        # YOUR CODE HERE
        for i in other:
            self.append(i)
        #self.data.append(None)
        #self.data[len(self.data)-1]=other.data[i]
        #print(other.data[i], self.data[i])
        return self
        #raise NotImplementedError()

            
    ### iteration ###
    
    def __iter__(self):
        """Supports iteration (via `iter(self)`)"""
        #code
        for i in range(0, len(self.data)):
            yield self.data[i]
        #raise NotImplementedError()


# In[5]:


# (6 points) test subscript-based access

from unittest import TestCase
import random

tc = TestCase()
lst = ArrayList()
data = [1, 2, 3, 4]
lst.data = ConstrainedList(data)

for i in range(len(data)):
    tc.assertEqual(lst[i], data[i])
    
with tc.assertRaises(IndexError):
    x = lst[100]

with tc.assertRaises(IndexError):
    lst[100] = 0

with tc.assertRaises(IndexError):
    del lst[100]

lst[1] = data[1] = 20
del data[0]
del lst[0]

for i in range(len(data)):
    tc.assertEqual(lst[i], data[i])

data = [random.randint(1, 100) for _ in range(100)]
lst.data = ConstrainedList(data)
for i in range(len(data)):
    lst[i] = data[i] = random.randint(101, 200)
for i in range(50):
    to_del = random.randrange(len(data))
    del lst[to_del]
    del data[to_del]

for i in range(len(data)):
    tc.assertEqual(lst[i], data[i])
    
for i in range(0, -len(data), -1):
    tc.assertEqual(lst[i], data[i])


# In[6]:


# (4 points) test stringification

from unittest import TestCase
tc = TestCase()

lst = ArrayList()
tc.assertIsInstance(lst.data, ConstrainedList)
tc.assertEqual('[]', str(lst))
tc.assertEqual('[]', repr(lst))

lst.data = ConstrainedList([1])
tc.assertEqual('[1]', str(lst))
tc.assertEqual('[1]', repr(lst))

lst.data = ConstrainedList([10, 20, 30, 40, 50])
tc.assertEqual('[10, 20, 30, 40, 50]', str(lst))
tc.assertEqual('[10, 20, 30, 40, 50]', repr(lst))


# In[207]:


# (8 points) test single-element manipulation

from unittest import TestCase
import random

tc = TestCase()
lst = ArrayList()
data = []

for _ in range(100):
    to_add = random.randrange(1000)
    data.append(to_add)
    lst.append(to_add)

tc.assertIsInstance(lst.data, ConstrainedList)
tc.assertEqual(data, lst.data._as_list())

for _ in range(100):
    to_ins = random.randrange(1000)
    ins_idx = random.randrange(len(data)+1)
    data.insert(ins_idx, to_ins)
    lst.insert(ins_idx, to_ins)

tc.assertEqual(data, lst.data._as_list())

for _ in range(100):
    pop_idx = random.randrange(len(data))
    tc.assertEqual(data.pop(pop_idx), lst.pop(pop_idx))
    
tc.assertEqual(data, lst.data._as_list())

for _ in range(25):
    to_rem = data[random.randrange(len(data))]
    data.remove(to_rem)
    lst.remove(to_rem)
    
tc.assertEqual(data, lst.data._as_list())

with tc.assertRaises(ValueError):
    lst.remove(9999)


# In[208]:


# (4 points) test predicates

from unittest import TestCase
tc = TestCase()
lst = ArrayList()
lst2 = ArrayList()

lst.data = ConstrainedList([])
lst2.data = ConstrainedList([1, 2, 3])
tc.assertNotEqual(lst, lst2)

lst.data = ConstrainedList([1, 2, 3])
tc.assertEqual(lst, lst2)

lst.data = ConstrainedList([])
tc.assertFalse(1 in lst)
tc.assertFalse(None in lst)

lst.data = ConstrainedList(range(100))
tc.assertFalse(100 in lst)
tc.assertTrue(50 in lst)


# In[209]:


# (10 points) test queries

from unittest import TestCase
tc = TestCase()
lst = ArrayList()

tc.assertEqual(0, len(lst))
tc.assertEqual(0, lst.count(1))
with tc.assertRaises(ValueError):
    lst.index(1)

import random
data = [random.randrange(1000) for _ in range(100)]
lst.data = ConstrainedList(data)

tc.assertEqual(100, len(lst))
tc.assertEqual(min(data), lst.min())
tc.assertEqual(max(data), lst.max())
for x in data:    
    tc.assertEqual(data.index(x), lst.index(x))
    tc.assertEqual(data.count(x), lst.count(x))

with tc.assertRaises(ValueError):
    lst.index(1000)
    
lst.data = ConstrainedList([1, 2, 1, 2, 1, 1, 1, 2, 1])
tc.assertEqual(1, lst.index(2))
tc.assertEqual(1, lst.index(2, 1))
tc.assertEqual(3, lst.index(2, 2))
tc.assertEqual(7, lst.index(2, 4))
tc.assertEqual(7, lst.index(2, 4, -1))
with tc.assertRaises(ValueError):
    lst.index(2, 4, -2)


# In[210]:


# (6 points) test bulk operations

from unittest import TestCase
tc = TestCase()
lst = ArrayList()
lst2 = ArrayList()
lst3 = lst+lst2

tc.assertIsInstance(lst3, ArrayList)
tc.assertEqual([], lst3.data._as_list())

import random
data  = [random.randrange(1000) for _ in range(50)]
data2 = [random.randrange(1000) for _ in range(50)]
lst.data = ConstrainedList(data)
lst2.data = ConstrainedList(data2)
lst3 = lst + lst2
tc.assertEqual(100, len(lst3))
tc.assertEqual(data + data2, lst3.data._as_list())

lst.clear()
tc.assertEqual([], lst.data._as_list())

lst.data = ConstrainedList([random.randrange(1000) for _ in range(50)])
lst2 = lst.copy()
tc.assertIsNot(lst, lst2)
tc.assertIsNot(lst.data, lst2.data)
tc.assertEqual(lst.data._as_list(), lst2.data._as_list())

lst.clear()
lst.extend(range(10))
lst.extend(range(10,0,-1))
lst.extend(data.copy())
tc.assertEqual(70, len(lst))
tc.assertEqual(list(range(10))+list(range(10,0,-1))+data, lst.data._as_list())


# In[194]:


# (2 points) test iteration

from unittest import TestCase
tc = TestCase()
lst = ArrayList()

import random
data = [random.randrange(1000) for _ in range(100)]
lst.data = ConstrainedList(data)
tc.assertEqual(data, [x for x in lst])

it1 = iter(lst)
it2 = iter(lst)
for x in data:
    tc.assertEqual(next(it1), x)
    tc.assertEqual(next(it2), x)

