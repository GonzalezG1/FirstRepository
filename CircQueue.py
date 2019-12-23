
# coding: utf-8

# # Circular, Array-backed Queue

# ## Overview
# 
# For this assignment you will implement a circular, array-backed queue data structure.
# 
# In the following class, which you are to complete, the backing array will be created and populated with `None`s in the `__init__` method, and the `head` and `tail` indexes set to sentinel values (you shouldn't need to modify `__init__`). Enqueueing and Dequeueing items will take place at the tail and head, with `tail` and `head` tracking the position of the most recently enqueued item and that of the next item to dequeue, respectively. To simplify testing, your implementation should make sure that when dequeuing an item its slot in the array is reset to `None`, and when the queue is emptied its `head` and `tail` attributes should be set to `-1`.
# 
# Because of the fixed size backing array, the `enqueue` operation is defined to raise a `RuntimeError` when the queue is full — the same exception should be raised when `dequeue` is called on an empty queue.
# 
# Finally, the `resize` method will allow the array underlying the queue to be increased in size. It is up to you how to implement this (you can either leave the elements in their current positions, though this may require "unwrapping" elements, or you can simply move all elements towards the front of the array). You may assume that `resize` will only be called with a value greater than the current length of the underlying array.

# In[1]:


class Queue:
    def __init__(self, limit=10):
        self.data = [None] * limit
        self.head = -1
        self.tail = -1

    # YOUR CODE HERE
    #raise NotImplementedError()

    def enqueue(self, val):
        # YOUR CODE HERE
        if self.head - self.tail == 1:
            raise RuntimeError

        if len(self.data) - 1 == self.tail and self.head == 0:
            raise RuntimeError

        if self.head == -1 and self.tail == -1:
            self.data[0] = val
            self.head = 0
            self.tail = 0
        else:
            if len(self.data) - 1 == self.tail and self.head != 0:
                self.tail = -1
            self.data[self.tail + 1] = val
            self.tail = self.tail + 1

    def dequeue(self):
        # YOUR CODE HERE
        if self.head == self.tail:
            temp = self.head
            self.head = -1
            self.tail = -1
            return self.data[temp]

        if self.head == -1 and self.tail == -1:
            raise RuntimeError
        if self.head != len(self.data):
            ret = self.data[self.head]
            self.data[self.head] = None
            self.head = self.head + 1
        else:
            # resetting head
            self.head = 0
            ret = self.data[self.head]
            self.data[self.head] = None
            self.head = self.head + 1
        return ret
    
    def resize(self, newsize):
        assert(len(self.data) < newsize)
        # YOUR CODE HERE
              
        newdata = [None] * newsize
        head = self.head
        current = self.data[head]
        count = 0
        while current != None:
            newdata[count] = current
            count += 1
            if count != 0 and head == self.tail:
                break
            if head != len(self.data) - 1:
                head = head + 1
                current = self.data[head]
            else:
                head = 0
                current = self.data[head]
        self.data = newdata
        self.head = 0
        self.tail = count - 1
    
    def empty(self):
        # YOUR CODE HERE
        if self.head == -1 and self.tail == -1:
            return True
        return False
    
    def __bool__(self):
        return not self.empty()
    
    def __str__(self):
        if not(self):
            return ''
        return ', '.join(str(x) for x in self)
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        # YOUR CODE HERE
        head = self.head
        current = self.data[head]
        count = 0
        while current != None:
            yield current
            count += 1
            if count != 0 and head == self.tail:
                break
            if head != len(self.data) - 1:
                head = head + 1
                current = self.data[head]
            else:
                head = 0
                current = self.data[head]


# In[2]:


# (5 points)

from unittest import TestCase
tc = TestCase()

q = Queue(5)
tc.assertEqual(q.data, [None] * 5)

for i in range(5):
    q.enqueue(i)
    
with tc.assertRaises(RuntimeError):
    q.enqueue(5)

for i in range(5):
    tc.assertEqual(q.dequeue(), i)
    
tc.assertTrue(q.empty())


# In[3]:


# (5 points)

from unittest import TestCase
tc = TestCase()

q = Queue(10)

for i in range(6):
    q.enqueue(i)
    
tc.assertEqual(q.data.count(None), 4)

for i in range(5):
    q.dequeue()
    
tc.assertFalse(q.empty())
tc.assertEqual(q.data.count(None), 9)
tc.assertEqual(q.head, q.tail)
tc.assertEqual(q.head, 5)

for i in range(9):
    q.enqueue(i)

with tc.assertRaises(RuntimeError):
    q.enqueue(10)

for x, y in zip(q, [5] + list(range(9))):
    tc.assertEqual(x, y)
    
tc.assertEqual(q.dequeue(), 5)
for i in range(9):
    tc.assertEqual(q.dequeue(), i)

tc.assertTrue(q.empty())


# In[4]:


# (5 points)

from unittest import TestCase
tc = TestCase()

q = Queue(5)
for i in range(5):
    q.enqueue(i)
for i in range(4):
    q.dequeue()
for i in range(5, 9):
    q.enqueue(i)
    
with tc.assertRaises(RuntimeError):
    q.enqueue(10)

q.resize(10)

for x, y in zip(q, range(4, 9)):
    tc.assertEqual(x, y)
    
for i in range(9, 14):
    q.enqueue(i)

for i in range(4, 14):
    tc.assertEqual(q.dequeue(), i)
    
tc.assertTrue(q.empty())
tc.assertEqual(q.head, -1)

