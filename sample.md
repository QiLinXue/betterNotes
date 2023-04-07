# ESC190 Lecture Notes Part 3: Advanced Data Structures and Algorithms

See all lecture notes [here](../).

## L22: Stacks and Queues

### Stack ADT

@@DEF
A **stack** is a collection of elements with the operations `push` and `pop`

*   `push` inserts the elements into the collection
*   `pop` removes the most *recently added element* that's not yet removed and returns it
@@

Intuitively, we can think of this as a stack of blocks. We can only add blocks to the top of this stack and remove it from the top. This is known as LIFO (last in first out). If we start with an empty list `[ ]` then run the following commands, we have:

1.  `push(1)`
2.  `push(50)`
3.  `pop()` (returns 50)
4.  `push(100)`
5.  `pop()` (returns 100)
6.  `pop()` (returns 1)

Note: Note that our "stack of blocks" analogy is an analogy of how we could implement a stack. It is a very natural way of implementing it, since if we put new items at the top of the stack, then popping them from the top automatically fulfills the requirement of removing the most recently added element.  
  
However, we could have implemented a stack differently, since a stack is an ADT, and ADTs don't tell us the implementation details.

### Queue ADT

@@DEF
A **queue** is a collection of elements with the operations `enqueue` and `dequeue`

*   `enqueue` inserts the elements into the collection
*   `dequeue` removes the *earliest added element that's not yet removed and returns it*
@@

The anlogy for queues is a physical queue (i.e. a line of people). If we have a queue of people waiting to get into the Praxis lecture, the first person in the queue is the first person to get in (and therefore leave the queue). This is known as FIFO (first in first out). An example starting with an empty list:

1.  `enqueue(1)`
2.  `enqueue(50)`
3.  `dequeue()` (returns 1)

### Implementation of Stack

We can use a python list to act as a stack very naturally,

    class Stack:
        def __init__(self):
            self.data = []
        
        def push(self, item):
            self.data.append(item)
        
        def pop(self):
            return self.data.pop()

This is because the Python `pop()` already acts like the stack `pop()` operation. It removes the last element of the list and returns it. While the above works perfectly fine, for the sake of learning, we will implement a stack without using these default methods (which allows us to extend concepts to other ADT implementations). We have,

    class Stack:
        def __init__(self):
            self.data = []
        
        def push(self, item):
            self.data.append(item)
        
        def pop(self):
            # return self.data.pop()
            ret_val = self.data[-1]
            del self.data[-1]
            return ret_val
    
    if __name__ == '__main__':
        s = Stack()
        s.push(1)
        s.push(50)
        print(s.pop())
        s.push(100)
        print(s.pop())
        print(s.pop())

which will output `50, 100, 1` as we predicted earlier.

### Implementation of Queue

I claim that this is trivial to do if we have the previous section. Why is this the case?  
  
The reason is that the only difference between a stack and a queue is whether we choose to remove the most recent element or the earliest element. This means making a small change in the index is sufficient (i.e. `-1` to `0`)

    class Queue:
        def __init__(self):
            self.data = []
        
        def enqueue(self, item):
            self.data.append(item)
        
        def dequeue(self):
            ret_val = self.data[0]
            del self.data[0]
            return ret_val
    
    if __name__ == '__main__':
        s = Queue()
        s.enqueue(1)
        s.enqueue(50)
        print(s.dequeue())
        s.enqueue(100)
        print(s.dequeue())
        print(s.dequeue())

which prints out `1 50 100` as expected.

### Complexity

This seems boring for such a simple data structure, but it is actually very exciting! First, note that the time complexity of `push` and `enqueue` is the same as the time complexity of appending to a list. This is \\(\\mathcal{O}(1)\\) but it's not obvious why this is the case!

*   If we were to implement this in C via an array, we can allocate extra memory such that writing to the array is \\(\\mathcal{O}(1)\\). However, if we add enough elements to the array, then we run out of space and need to re-allocate memory, making the worst case scenario \\(\\mathcal{O}(n)\\).
*   However in practice, this worst case scenario above isn't actually that bad. If every time we run out of memory, we double the allocated space, then there's only so many times we need to reallocate space (since exponents grow very fast). Note that this is a very common strategy people use.

In Python, lists are implemented [internally](https://wiki.python.org/moin/TimeComplexity) as an array, so the above analysis applies as well.  
  
Retrieving elements in an array by index and deleting the last element of an array are both \\(\\mathcal{O}(1)\\) so the time complexity of `pop` is \\(\\mathcal{O}(1)\\)  
  
However, `dequeue` is \\(\\mathcal{O}(n)\\). This is because once the item at index 0 is removed, the item that used to be at index 1 needs to be at index 0. In order for this to happen, the rest of the elements need to be shifted to the left, so a total of 10 operations are done.

### Improving Queues

Our naive implementation of a queue is very inefficient. Intuitively, a simple task such as removing the leftmost element can be done in constant time, so how can we fix this?  
  
We can use linked lists!

![...](diagrams/linked_list_queue.png.jpg)

Refer to the above diagram. The basic idea is that if we remove the first element, instead of shifting everything to the left, we can just change the `HEAD` pointer of the linked list to direct to the second element, which takes \\(\\mathcal{O}(1)\\) time. We can implement this as follows:

    import linkedlist
    
    class LLQueue:
        def __ini__(self):
            self.data = linkedlist.LinkedList()
        
        def enqueue(self):
            self.data.append(item)
            
        def dequeue(self):
            ret_value = self.data.head.value
            self.data.head = self.data.head.next

where `linkedlist` is the code we wrote in Lecture 21. Note that there is one problem. In order to append, we had to traverse the entire linked list, so the time complexity for `enqueue` is now \\(\\mathcal{O}(n)\\). We can fix this by modifying the linked list implementation to keep track of the tail of the linked list, so that appending is \\(\\mathcal{O}(1)\\). That is,

    class LinkedList:
        def __init__(self):
            self.head = None
            self.tail = None

Note that we now have to edit our existing functions so that it updates the tail pointer as well when we append and insert. See (and visualize) the changes that were made [here!](https://github.com/QiLinXue/esc190-notes/commit/3fe8daba4b99358152a34e187fcba656932ccba6) The updated linked list file is

    class LinkedList:
        def __init__(self):
            self.head = None
            self.tail = None
        
        def get_i(self, i):
            # return the value at index i
            cur = self.head
            for j in range(i):
                cur = cur.next
            return cur.value
    
        def append(self, value):
            '''Add a new node with the value value to the end of the list'''
            # Create a new node
            new_node = Node(value)
            
            if self.head == None:
                self.head = new_node
                self.tail = new_node
    
            self.tail.next = new_node
            self.tail = new_node
        
        def insert(self, value, i):
            '''Insert a node with the value value at index i'''
            new_node = Node(value)
    
            if i == 0:
                new_node.next = self.head
                self.head = new_node
            
            else:
                cur = self.head
                for j in range(i-1):
                    cur = cur.next
                new_node.next = cur.next
                cur.next = new_node
            
            if new_node.next == None:
                self.tail = new_node
    
        def __str__(self):
            cur = self.head
            s = ""
            if(cur == None):
                return "Empty list :("
            
            while cur != None:
                print(cur)
                s += str(cur) + " -> "
                cur = cur.next
            return s[:-4] # remove last arrow
    

Note that the lecture had a minor typo. In the lecture, `self.tail` was initially set to `None` but it was never initialized, so running something like `self.tail.next = new_node` would lead to an error.  
  
This is one very practical case where linked lists come in handy. The native implementation of queues in Python is via `collections.deque` which does it via doubly linked list, similar to what we constructed above.

## L23: Midterm Question (PyInteger)

In this lecture, we review the midterm: specifically question 5 where we are asked to implement the ADT `pyinteger` which allows us to represent arbitrarily large integers and perform the two basic operations,

*   `plusplus(n1)` adds `1` to the `pyinteger n1`
*   `add(n1, n2)` adds the `pyinteger n2` to the `pyinteger n1`

We first set up our header file, `pyinteger.h`:

    #if !defined(PYINTEGER_H)
    #define PYINTEGER_H
    
    typedef struct pyinteger{
        int *digits;
        int size;
        int capacity;
    } pyinteger;
    
    void plusplus(void *pyint);
    void add(pyinteger *pyint1, pyinteger *pyint2);
    
    #endif

where `pyinteger` is a struct that contains the following fields:

*   `digits` is a pointer to an array of integers that stores the digits of the integer
*   `size` is the number of digits in the integer
*   `capacity` is the maximum number of digits that can be stored in the array

Here, we are representing an integer via an array where each element in this array is a digit from 0-9. For example, the integer 1234 would be represented as `[1, 2, 3, 4]`. We use a similar approach to the one we used in Lecture 21 to update the `capacity.` Every time the capacity is reached and we need to add another digit, we double the capacity of the array.

### Creating the Struct

Now we work in `pyinteger.c` and we wish to implement the ADT. But first, we can create an optional function that allows us to create a `pyinteger` struct which initially stores `int n`. What are some natural tasks that we must do?

*   How can we determine the initial `capacity`? In other words, how do we make sure we initially allocated enough space for our array?
*   How can we put the digits into the array `*digits`? To do this, we need to find a good way of extracting the digits from the initial integer.

To determine the initial capacity, we need to determine the number of digits `int n` has.

@@THM
I claim that the formula for the number of digits of \\(n\\) is given by \\\[\\text{num of digits} = \\text{floor}(\\log\_{10}(n)) + 1.\\\]
@@

@@PROOF
_Proof:_ A \\(k\\)-digit number can be written as \\\[n = a\_{k-1}10^{k-1} + a\_{k-2}10^{k-2} + \\cdots + a\_110^1 + a\_.\\\] where the leading coefficient \\(a\_{k-1} \\neq 0\\). To double-check this, note that \\(15 = 1 \\times 10^1 + 5\\) so the leading power is \\(k-1\\). Note that: \\\[10^{k-1} \\le n < 10^k.\\\] It is important that the right inequality is strict! This is because \\(10^k\\) has \\(k+1\\) digits while \\(n\\) only has \\(k\\) digits. For those who want more rigour, note that each \\(a\_i\\) is smaller or equal to \\(9\\) so we can bound \\(n \\le \\sum\_{i=0}^{k-1} 9 \\cdot 10^{i}\\).  
@@


Since the logarithm is a monotonically increasing function, we have \\\[\\log\_{10}(10^{k-1}) \\le \\log\_{10}(n) < \\log\_{10}(10^k)\\\] or equivalently, \\\[k-1 \\le \\log\_{10}(n) < k.\\\] Therefore, \\(\\text{floor}(\\log\_{10}(n))=k-1\\) so \\\[k = \\text{floor}(\\log\_{10}(n)) + 1\\\] as expected.  
  
**However:** If \\(n=0\\) then we get something that is undefined, so we have to treat this case separately.

Obviously, you are not expected to prove this on the midterm, but I provided the proof here for those who are interested and for the rigour. It's a handy fact to know though, so you don't need to be stressed about weird edge cases! The process of extracting the digits from the integer is a bit tricky, but it's something that we've done before! To get the last digit, we can compute \\\[n \\% 10.\\\] To get the second to last digit, we can shift all the digits by diving the number by \\(10\\) and ignoring the decimal part. Then we can repeatedly apply this same algorithm until we have no more digits left. Therefore, we should start from the end of the array and work our way backwards. Here is the code:

    void create_integer(pyinteger **pyint, int n){
        // Allocate memory for the pyinteger struct
        *pyint = (pyinteger*)malloc(sizeof(pyinteger));
    
        // Proven in a theorem
        if (n == 0){
            (*pyint)->capacity = 1;
        }
        else{
            (*pyint)->capacity = (int)(log10(n)) + 1;
        }
    
        // Currently the number of digits is the same as the capacity
        (*pyint)->num_digits = (*pyint)->capacity;
    
        // Allocate memory for the digits
        (*pyint)->digits = (int*)malloc(sizeof(int) * (*pyint)->capacity);
    
        // Fill the digits
        for (int loc = (*pyint)->num_digits - 1; loc >= 0; loc--){
            (*pyint)->digits[loc] = n % 10;
            n /= 10;
        }
    }

### Implementing PlusPlus

Now we need to implement the function `plusplus`. This function should add `1` to the integer. Why might this be a tricky task? Well, the naive approach is to just add `1` to the units digit, but if the units digit is \\(9\\), then something weird might happen. Let's break it up into two cases, and work with the easier case first (this is a good idea in a test situation, since you know there will definitely be partial marks)

*   Case 1: The units digit is not 9. We simply get the value at index `pyint->num_digits - 1` and check if it's a 9. If not, then we increment it by 1!
*   Case 2: We draw analogy from long addition. We change the 9 into a 0, then carry over to the previous digit. If that digit is not 9, we add 1. If it is 9, we change it into a 0 and continue.

we can implement it (with a small hiccup we'll discuss in a bit) as follows:

    void plusplus(pyinteger *pyint){
        int loc;
        for (loc = pyint->num_digits - 1; loc >= 0; loc--){
            if (pyint->digits[loc] == 9){
                pyint->digits[loc] = 0;
            } else {
                pyint->digits[loc]++;
                break;
            }
        }
    }

Note that at this stage, there is one more hiccup. If everything is 9, then the size of the number can increase! This specific case is a bit annoying, but just doing everything up to this point will give you 8/10 points. _If you can't fully figure how to solve a question, solving it partially can still land you a lot of points!_  
  
So how do we fix this? To deal with this case, we ask the following natural questions:

*   How can we even detect if we need to do this case?
*   How do we decide if we need to re-allocate memory?
*   How do I shift the digits? (This is actually a bit misleading, as we'll see in a bit)

To detect if we even need to consider this case, there are many ways to do so. One way is to check the value of `loc` after the for loop finishes. If the for loop exits via the break statement, we should have `loc >= 0.` If it doesn't exit via the break statement, that means the first digit was also a 9, so `loc == 0.`  
  
How can we check if we need to re-allocate memory? At this point, we know that the number of digits has increased by 1, so we can update `num_digits.` Now we can check if the number of digits is greater than the capacity. If it is, then we need to re-allocate memory. We can do this by doubling the capacity.  
  
Finally, we need to be able to shift all the digits over. At least, this was my first thought when I saw the problem. However, if we work through a simple example (or think about it), at this point, every single digit should be 0! Therefore, all we need to do here is set the first digit to 1. Easy!

    void plusplus(pyinteger *pyint){
        int loc;
        for (loc = pyint->num_digits - 1; loc >= 0; loc--){
            if (pyint->digits[loc] == 9){
                pyint->digits[loc] = 0;
            } else {
                pyint->digits[loc]++;
                break;
            }
        }
    
        if(loc == -1){
            pyint->num_digits++;
            if(pyint->num_digits > pyint->capacity){
                pyint->capacity *= 2;
                // Reallocate memory for the digits
                pyint->digits = (int*)realloc(pyint->digits, sizeof(int) * pyint->capacity);
            }
            
            // First digit is 1
            pyint->digits[0] = 1;
    
            // Last digit is 0
            pyint->digits[pyint->num_digits - 1] = 0;
        }
    }

### Implementing Add

Now we need to implement adding. First, why might this be a hard task? It's because the digits are not aligned in a "nice" manner. When we learn long addition in elementary school, we align the rightmost digit (ones digit) of the two numbers. But the way we implemented it here, we align the leftmost digit.  
  
Note: we did not get to finish this in class, but here are some ideas for solutions

*   Partial Solution: You can call `plusplus()` multiple times. This is very easy to implement, since all you have to figure out is how to implement a for loop that adds 1 to `n1` a total of `n2` times.  
      
    One way to do this is to create a helper function to compare two pyintegers. Then we can create a temporary `pyinteger` and initialize it to 0. We then increment both this temporary pyinteger and `n1` until the temporary pyinteger is equal to `n2`.  
      
    This is not optimal, since the time complexity is \\(\\mathcal{O}(n\\log n)\\) while the optimal complexity is \\(\\mathcal{O}(\\log n)\\). Because we care about time complexity in this course, you will not receive full marks, but it's possible to receive 8/10 points.
*   Another way to solve this is to get rid of the annoying problem. Modify the `pyintegers` such that the units digit align. This can be done by shifting the digits over and filling everything before the leading digit with 0s. Then we can apply the standard long addition algorithm we learned in elementary school. Just remember to shift the digits back after we're done!
*   Another way uses the same idea as above, but instead of shifting the digits, we can reformulate the standard "long addition" algorithm with indices, to make it easier to implement with code. Then all we have to do is write the algorithm with the C language!

Note: This section will get updated depending on the direction of Friday's class.

## L25: Heaps and Priority Queue

  
A **priority queue** is a queue where the first element dequered is the one with the highest priority.

*   `Insert(S,x)` adds a new element with priority `x` to priority queue `S`
*   `min(S)` returns the element with the smallest value from the priority queue
*   `extract_min(S)` removes and returns the element with the smallest value from the priority queue

This has many uses. It can simulate real-world systems queues organized by priority (i.e. patients in a hospital or files requested from a server). Alternatively, it can be used in searching algorithms (i.e. in games) such as A\* (A Star).

### Slow Method 1

The naive implementation is to store everything in an (unsorted) array. Every time that we wish to extract the minimum, we have to search through the entire array to find the minimum. See the below code,

    class PriorityQueueSlow:
        def __init__(self):
            self.data = []
            self.size = 0
        
    
        def insert(self, value):
            self.data.append(value)
            self.size += 1
        
        def extract_min(self):
            if self.size == 0:
                return None
    
            cur_min = self.data[0]
            cur_min_loc = 0
            for i in range(1, self.size):
                if self.data[i] < cur_min:
                    cur_min = self.data[i]
                    cur_min_loc = i
    
            del self.data[cur_min_loc]
            self.size -= 1
            return cur_min

What is the time complexity? Inserting is effectively O(1) as discussed last time, and extracting the minimum is O(n), since we need to search through the entire array.

### Slow Method 2

One idea is to keep the data sorted, so we don't need to look for the minimum. This is not enough though: we want to ensure we are deleting the last element of the array (which takes constant time), not the first one (which takes linear time, due to the need to shift all the elements over). Therefore, we need to keep `self.data` sorted in non-increasing order. We have,

    class PriorityQueueSlow2:
        def __init__(self):
            self.data = []
            self.size = 0
        
        def insert(self, value):
            i = 0
            while i < self.size:
                if value > self.data[i]:
                    break
                i += 1
    
            # i is the index before which we can insert value
            self.data.insert(i, value)
            self.size += 1
        
        def extract_min(self):
            if self.size == 0:
                return None
            self.size -= 1
            return self.data.pop() # O(1)

Here, linear search is being done to find the index to insert the new element, so while `extract_min()` now takes constant time, inserting takes linear time. Someone bright might claim that we can use binary search to find the index to insert the new element, but this does not solve the problem. This is because inserting also takes linear time, as everything needs to be shifted.  
  
That's a bit of a bummer! It seems like no matter how we structure things, we cannot escape the \\(\\mathcal{O}(n)\\) complexity of inserting/removing an element. This introduces the concept of heaps.

### Heaps

We can implement a more efficient algorithm using heaps. But to understand heaps, we first need to introduce **trees.**

A **tree** is a collection of nodes, where each node has two children, except the **leaves** (nodes at the bottom with no children), and every leaf is as far left as possible on the last level.

Usually, we deal with binary trees (meaning each node has at most 2 children). For example, the below is a **complete** binary tree (a tree where all nodes except leaves have two children and each leaf is as far left as possible).

![](assets/complete_tree.jpg)

For heaps (specifically a min-heap), we desire a **heap order property** which means that each node is smaller than its children. A heap is a complete graph and when we add a new element, we first add it to the leftmost position in the bottom row.  
  
In order to satisfy the heap order property, we _percolate_ the node upwards, exchanging it with the parent if it is smaller than the parent. For example, if we add 14 to a heap (boxed), we can swap it with the parent until the heap order property is satisfied, as shown below.

![](assets/up-heap.jpg)

One way to implement a heap is to use a linked list where each node has a `left_child` and `right_child` and while this is more intuitive, it is often faster to implement it via an array and use mathematics to perform index gymnastics. Note that this only works because a heap is a complete binary tree. We store the first tree in this section as \\\[ \[\\\_, a, b,c,d,e,f,g,h,i,j,k,l,m,\\dots\] \\\]\\ where the first index is left blank for convenience, which will be made clear in just a bit. Given a node at index \\(i\\) we can get the parent and the children via the following formulas: \\\[\\text{parent}(i) = i/2\\\] \\\[\\text{left}(i) = 2i\\\] \\\[\\text{right}(i) = 2i+1\\\] Why does this work? First note that the index of the leftmost element of each row is given by \\(2^0,2^1,2^2,\\dots\\) since the binary tree is complete. So `a` has index 1, `b` has index 2, `d` has index 4, and `h` has index 8. These nice numbers are only possible since we are neglecting index 0, which is empty in our array.

_Proof:_ We first prove that \\(\\text{left}(i)=2i\\). As we have already mentioned, the leftmost element of each row has index \\(2^0,2^1,2^2,\\dots\\). Therefore, if \\(i=2^{k}\\), then it is clear that its left child is just the leftmost element of the next row, so for this case, we verify \\(\\text{left}(i)=2i\\). Now we prove via induction that \\(\\text{left}(i)=2i\\) for all \\(i\\).  
  
Assume that this is true for some \\(2^k \\le i < 2^{k+1} - 1\\). Then, the left child of \\(i+1\\) is located \\(2\\) to the right of the left child of \\(i\\). That is, \\\[\\text{left}(i+1) \\overset{\\#}{=} \\text{left}(i) + 2 = 2i+2 = 2(i+1)\\\] where the equality given by \\(\\#\\) is true via induction. We've already shown this is true for the base case \\(i=2^k\\) so we're done.  
  
Note that this automatically implies that the formula \\(\\text{right}(i) = 2i+1\\) is also true, since the right element has index 1 more than the left element. Note tha with the exception of \\(i=1\\), if \\(i\\) is even, then it is the left child of its parent, and if \\(i\\) is odd, then it is the right child of its parent. Thus, it remains to show that \\(\\text{parent}(i) = 2i\\). This is easy if we consider the inverse of the above formula.  
  
If \\(i\\) is even, then its parent is \\(\\text{left}^{-1}(i) = i/2\\). If \\(i\\) is odd, then its parent is \\\[\\text{right}^{-1}(i) = (i-1)/2 = i/2\\\] if we treat \\(i/2\\) as an operation that rounds down to the nearest integer (i.e. `i//2` in Python).

## L26: Implementing Heaps and Dynamic Programming

### Insert

How do we insert an element into a heap? We have the pseudocode

    Insert(x):
        k=n+1
        pq[k] = x
        while k > 1 and pq[k/2] > pq[k]
            swap(pq[k], pq[k/2])
            k = k / 2
    

To think of this, treat `k` as current node, and treat `k/2` as parent node (by the formulas given in the previous lecture). Then the rest is just applying the _percolation_ described earlier.

### Extracting the Minimum

Getting the minimum element is very easy. It's the first element! (i.e. at index 1.) However, how can we remove it and still maintain a binary tree where the heap-order property is satisfied?  
  
To do so, we apply a clever trick. First, replace the first element with the last element (but remember to save it first!) The heap-order property is not satisfied, but we can _percolate_ this element down until the heap-order property is satisfied. Note that there is a subtle difference:

*   When percolating up, only one comparison needs to be made. We need to compare it with the left child and the right child. If it's bigger than either one, then we swap it with the one it's bigger than.
*   It is possible for the current node we're percolating down to be bigger than both children. In that case, we should swap it with the smaller child, since the smaller child can be a parent of the larger one.

The pseudocode is given by,

    extract_min():
        min = pq[1]
        swap(pq[1], pq[n])
        n = n - 1
        k = n
        while(2*k <= n):
            j = 2*k
            if j < n and pq[j] > pq[j+1]:
                j = j + 1
            if pq[k] <= pq[j]:
                break
            swap(pq[k], pq[j])
            k = j
        return min
    

In the above code, the `j < n and pq[j] > pq[j+1]` condition ensures that the current node has two children and if it does, selects the index of the smaller one. One example of how this works is shown below, where we have already replaced the smallest element with the last element, which in this case is 32. ![](assets/down-heap.jpg) The python implementation can be found [here.](https://www.cs.toronto.edu/~guerzhoy/190/labs/heaps.py)

### Time Complexity

We define the **height** \\(h\\) of a tree to be the longest path from a node to a leaf. Note that from a geometric series, we can bound the number of elements in a tree of height \\(h\\) by \\\[n \\le 2^0 + 2^1 + \\cdots + 2^{h} = 2^{h+1} - 1\\\] For a complete tree with height \\(h\\) the number of nodes must be greater than the maximum number of nodes for a tree with height \\(h-1\\), which gives \\\[n > 2^0 + 2^1 + \\cdots + 2^{h-1} = 2^{h} - 1\\\] For \\(h \\ge 1\\) we have \\\[h-1 \\le \\log\_2(2^h-1) \\le \\log\_2 n \\le \\log\_2(2^{h+1}-1) < h+1\\\] where the middle inequality is due to the above inequalities we derived, and applying the fact that logarithms are monotonic. The inequalities at the two ends are due to the fact that \\\[2^{h}/2 \\le 2^{h} - 1\\\] and \\\[2^{h+1} -1 < 2^{h+1}.\\\] Therefore, we have $\\log(n) \\sim h$ and thus since both inserting and extracting the minimum needing at most \\(h\\) swaps, the time complexity is \\\[\\mathcal{O}(h) = \\mathcal{O}(\\log(n)).\\\]

### Dynamic Programming

Dynamic programming is not a very well-defined term, but it encompasses a set of techniques for problem solving. Specifically, it breaks up a problem into sub-tasks and uses the results from those sub-tasks to solve the original problem. We start off with a simple question:

Compute the \\(n^\\text{th}\\) Fibonacci number.

The naieve ESC180 implementation is via:

    def fib(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return fib(n-1) + fib(n-2)
    

While this works, it is extremely inefficient because it calculates the same values over and over again. This is because the function calls itself twice with the same argument in the recursive case. As a result, the time complexity of this implementation is exponential, which means it grows very quickly with increasing values of n.  
  
To fix this problem, we use a technique called **memoization** (which is _not_ a typo, but you can think of "memorization" as an analogy). This involves maintaining a table of values that were already computed so that we don't have to recompute them. We then have:

    def fib(n, mem = {}):
        if n in mem:
            return mem[n]
        if n == 0:
            return 0
        if n == 1:
            return 1
        mem[n] = fib(n-1, mem) + fib(n-2, mem)
        return mem[n]
    

Therefore, if we have already computed something, we don't have to go through an entire series of recursive calls! The time complexity of this implementation is now linear, because we only have to do \\(3n\\) recursive calls. Note that this analysis assumes addition is constant in time, which is true for doubles, but may not be true for other data types (since fibonacci integers can increase exponentially)  
  
We can also solve the same problem **without** recursion by having a list that gets updated as we go along. Specifically, we have

    def fib_iter(int n):
        fib_list = [0] * n
        fib_list[0:2] = [0, 1]
        for i in range(2, n + 1):
            fib_list[i] = fib_list[i-1] + fib_list[i-2]
        return fib_list[n]
    

**Follow-up question:** the size of this array is linear in `n.` Can you do this task in constant space (i.e. the size of the array does not depend on `m`?)

In general, for dynamic programming:

1.  Divide a complex problem into a number of simpler overlapping problem.
2.  Defined a relationship between solutions to more complex problems and solutions to simpler problems. This is known as a Bellman Equation.
This is an important step. For the Fibonacci example, we had \\\[ F\_i = \\begin{cases} 0&i=0 \\\\ 1 & i=1 \\\\ F\_{i-1} + F\_{i-2} & i \\ge 2 \\end{cases}\\\]3.  Store solutions to each subproblem, solving each subproblem once (i.e. using `fib_list` to store solutions)
4.  Use stored solutions to solve the original problem.

Now, suppose we had a harder problem.

**Problem:** There are a row of `n` houses, each house can be painted with one of the three colors: red, blue or green. The cost of painting each house with a certain color is different. You have to paint all the houses such that no two adjacent houses have the same color.  
  
The cost of painting each house with a certain color is represented by a `nx3` cost matrix. For example, `costs[0][0]` is the cost of painting house 0 with color red; `costs[1][2]` is the cost of painting house 1 with color green, and so on... Find the minimum cost to paint all houses.

Note that the above wording was stolen from a LeetCode _medium_ problem, but encodes the same information as the problem in the lecture. (Generally, coding interviews will contain questions at this level, so it is good practice to do medium-level Leetcode problems fast if you are trying to get software engineering PEY positions at top companies.)  
  
The subproblem we are trying to solve is the minimum cost to paint the \\(i^\\text{th}\\) house. We can define the following relationship: \\\[ \\begin{align} R(i) &= cost(i,red) + min(G(i-1), B(i-1)) \\\\ G(i) &= cost(i,green) + min(R(i-1), B(i-1)) \\\\ B(i) &= cost(i,blue) + min(R(i-1), G(i-1)) \\\\ Cost(i) &= min(R(i), G(i), B(i)) \\end{align} \\\] Here, \\(R(i),G(i),B(i)\\) are the optimal cost if the \\(i^\\text{th}\\) house was painted red, green, or blue respectively. Note that these equations also reflect that no two adjacent houses can be painted the same colour.  
  
From here, the python implementation is straightforward. See [here](https://www.cs.toronto.edu/~guerzhoy/190/lec/W10/houses.py) for details.

## L27: Project Overview

This lecture only talked about the project.

## L28: Coin Change Problem

### Setup + Strategy

Consider coin denominations of `[1, 4, 5]` and a target of `8`. What is the smallest number of coins that can be used to make the target? Can you generalize this to an efficient algorithm?

For the above example, it is clear that the answer is `2` (just take 2 coins of value `4`). But how can we write an algorithm to do this in general? Note that this problem doesn't actually come up in everyday life, as the standard set of denominations `5, 10, 25, 100` is set up in such a way we can always use a greedy algorithm (i.e. when finding the coins, we take the largest coin possible at each step). But it is clear from our simple example that a greedy algorithm will not work.  
  
Instead, we take a dynamic programming approach. Let us define \\\[OPT(i) := \\text{smallest number of coins to make } i.\\\] with the base case of \\\[OPT(0) = 0\\\] and to make life easier, we can also define \\\[OPT(\\text{negative number}) = \\infty\\\] to illustrate that we can't make negative numbers with coins. We can then construct the Bellman equation \\\[OPT(i) = \\min\_{d \\in \\text{denoms}} \\left\\{OPT(i-d) + 1\\right\\}.\\\] Where does this equation come from? We can think of several cases. In each case, we select a coin of value \\(d\\) (which gives our \\(+1\\)), and then we are left with \\(i-d\\) to make, which takes an optimal number of \\(OPT(i-d)\\) coins to make. If we take the minimum of all these cases, we get the optimal solution.  
  
In the simple example above, we have \\\[OPT(8) = 1 + \\min \\left\\{OPT(7) , OPT(4) , OPT(3)\\right\\}\\\]

### Implementation

To implement it in Python, we can set up the function

    import numpy as np
    def make_change(denom, target):
        OPT = np.inf * np.ones(target + 1)
        OPT[0] = 0
        # to be continued
    

This sets up the array: \\\[OPT = \[\\underbrace{0}\_{\\text{#coins to make 0}},\\underbrace{\\infty}\_{\\text{#coins to make 1}},\\dots,\\underbrace{\\infty}\_{\\text{#coins to make target}}\]\\\] where we have initialized all entries to infinity at the very start (where \\(\\infty\\) means that it's impossible to make a coin of that value). This is helpful, especially in using the `numpy` package in Python because `np.inf` obeys the following properties:  
  

*   You can add/subtract numbers from infinity (`np.inf + 1` returns `np.inf`)
*   You can compare infinity to numbres (`np.inf < 5` returns `False`)

Therefore, we can very naturally use `np.inf` and incorporate it into our Bellman equation. Also notice that we have set up our array in such a way that we can have the correspondence \\\[OPT(i) = \\verb#OPT\[i\]#\\\] where the LHS is a function and the RHS is the array. We can now finish the function

    import numpy as np
        def make_change(denom, target):
            OPT = np.inf * np.ones(target + 1)
            OPT[0] = 0
            
            for amount in range(1, target + 1):
    
                # check all denominations
                for d in denom:
    
                    # can we use this denomination?
                    if amount - d >= 0:
    
                        # is this the best way to make this amount?
                        if OPT[amount - d] + 1 < OPT[amount]:
    
                            # update the optimal solution
                            OPT[amount] = OPT[amount-d] + 1
            
            return OPT[target]

Let's break this down. Remember that in order to compute \\(OPT(\\text{target})\\) we need to know what \\(OPT(\\text{target}-1)\\) is, which in order to compute that, we need to know what \\(OPT(\\text{target}-2)\\) is, and so forth, all the way to \\(OPT(1)\\). One way to achieve this is via recursion, but as we've seen in the Fibonacci problem case, using recursion is dangerous because there are a lot of duplicates. Therefore, we will use a **bottom-up** approach.  
  
Let's first compute \\(OPT(1)\\) (which requires the value of \\(OPT(0)\\) to do so). It'll be either \\(OPT(0) + 1 = 1\\) if there exists a coin with denominations \\(1\\) or it'll be \\(\\infty\\) if all coins have a denomination greater than \\(1\\).  
  
Then we can compute \\(OPT(2)\\) which relies on the value of \\(OPT(0)\\) and \\(OPT(1)\\). In general, \\(OPT(n)\\) will rely on the value of \\\[OPT(0), OPT(1), \\dots, OPT(n-1).\\\] To compute it, we use the following steps:

1.  Go through each of the possible denominations \\(d\\). This corresponds to `for d in denom`
2.  Check if we can use this denomination to make the amount we are considering. This corresponds to checking `amount - d >= 0`
3.  If possible, then after using this denomination, we still need to make a total value of `amount - d`. But this is given by `OPT[amount - d]` which we already made optimal (since it comes before). The total number of coins we use if we choose this denomination is thus `1 + OPT[amount - d]`. If this number is smaller than the current optimal number, then we update our optimal number. This corresponds to the last if statement.

### Concrete Example

**Note:** This section is a bit repetitive as I have included very specific steps to help you understand the algorithm if you are still confused. If you are comfortable with the algorithm, you can skip this section.  
  
Let us run the code on our example from before. Let us define

    denom = [1, 4, 5]; target = 8

Then `OPT` is initialized to \\\[\\verb#OPT# = \[0,\\infty,\\infty,\\infty,\\infty,\\infty,\\infty,\\infty,\\infty\]\\\] Now we loop through the amounts. Let `amount = 1`. We will now loop through all the denominations. We have:

*   \\(\\text{amount} - 1 = 0\\) so we move on to the next if statement. We have \\(\\verb#OPT#\[\\text{amount} - 1\] + 1 = 1\\) which is smaller than \\(\\infty\\) so we update the array: `OPT[1] = 1`.
*   \\(\\text{amount} - 4 = -3\\) which is smaller than zero, so we can't use this denomination and thus we move on.
*   \\(\\text{amount} - 5 = -4\\) which is smaller than zero, so we can't use this denomination and thus we move on.

Our `OPT` is now \\\[\\verb#OPT# = \[0,1,\\infty,\\infty,\\infty,\\infty,\\infty,\\infty,\\infty\]\\\] Now we loop through the amounts. Let `amount = 2`. We will now loop through all the denominations. We have:

*   \\(\\text{amount} - 1 = 1\\) so we move on to the next if statement. We have \\(\\verb#OPT#\[\\text{amount} - 1\] + 1 = 2\\) which is smaller than \\(\\infty\\) so we update the array: `OPT[2] = 2`.
*   \\(\\text{amount} - 4 = -2\\) which is smaller than zero, so we can't use this denomination and thus we move on.
*   \\(\\text{amount} - 5 = -3\\) which is smaller than zero, so we can't use this denomination and thus we move on.

Our `OPT` is now \\\[\\verb#OPT# = \[0,1,2,\\infty,\\infty,\\infty,\\infty,\\infty,\\infty\]\\\] Let `amount = 3` We will now loop through all the denominations. We have:

*   \\(\\text{amount} - 1 = 2\\) so we move on to the next if statement. We have \\(\\verb#OPT#\[\\text{amount} - 1\] + 1 = 3\\) which is smaller than \\(\\infty\\) so we update the array: `OPT[3] = 3`.
*   \\(\\text{amount} - 4 = -1\\) which is smaller than zero, so we can't use this denomination and thus we move on.
*   \\(\\text{amount} - 5 = -2\\) which is smaller than zero, so we can't use this denomination and thus we move on.

Our `OPT` is now \\\[\\verb#OPT# = \[0,1,2,3,\\infty,\\infty,\\infty,\\infty,\\infty\]\\\] Let `amount = 4`. We will now loop through all the denominations. We have:

*   \\(\\text{amount} - 1 = 3\\) so we move on to the next if statement. We have \\(\\verb#OPT#\[\\text{amount} - 1\] + 1 = 4\\) which is smaller than \\(\\infty\\) so we update the array: `OPT[4] = 4`.
*   \\(\\text{amount} - 4 = 0\\) so we move on to the next if statement. We have \\(\\verb#OPT#\[\\text{amount} - 4\] + 1 = 1\\) which is smaller than \\(\\verb#OPT\[4\]#=4\\) so we update the array: `OPT[4] = 1`.
*   \\(\\text{amount} - 5 = -1\\) which is smaller than zero, so we can't use this denomination and thus we move on.

Our `OPT` is now \\\[\\verb#OPT# = \[0,1,2,3,1,\\infty,\\infty,\\infty,\\infty\]\\\] Let `amount = 5`. We will now loop through all the denominations. We have:

*   \\(\\text{amount} - 1 = 4\\) so we move on to the next if statement. We have \\(\\verb#OPT#\[\\text{amount} - 1\] + 1 = 2\\) which is smaller than \\(\\infty\\) so we update the array: `OPT[5] = 2`.
*   \\(\\text{amount} - 4 = 1\\) so we move on to the next if statement. We have \\(\\verb#OPT#\[\\text{amount} - 4\] + 1 = 2\\) which is equal to \\(\\verb#OPT\[5\]#=2\\), so we don't update the array.
*   \\(\\text{amount} - 5 = 0\\) so we move on to the next if statement. We have \\(\\verb#OPT#\[\\text{amount} - 5\] + 1 = 1\\) which is smaller than \\(\\verb#OPT\[5\]#=2\\) so we update the array: `OPT[5] = 1`.

Our `OPT` is now \\\[\\verb#OPT# = \[0,1,2,3,1,1,\\infty,\\infty,\\infty\]\\\] Continuing this process for the remaining amounts, we obtain the final `OPT` array: \\\[\\verb#OPT# = \[0,1,2,3,1,1,2,2,2\]\\\] Thus, our function returns `OPT[target] = OPT[8] = 2`, which is the minimum number of coins needed to make the target amount of 8 using the given denominations.

### Retrieving the Solution

So what if we know what the optimal number is? It doesn't help us unless we can retrieve th actual combination of coins in order for this to happen. Let us define \\\[OPT\\\_soln(i) := \\text{a best solution to make i\\}\\\] Note that this is not well-defined. There could be several best solutions, but we only need to pick 1. The idea here is that every time we update `OPT[amount]` we want to also update `OPT_soln[amount]` so that we can retrieve the solution later. If we write `OPT_soln` as a dictionary, we can initialize it via

    OPT_soln = {}
    OPT_soln[0] = []
    

Then whenever we update `OPT[amount] = OPT[amount - d] + 1` where we are using `d` as a valid denomination, we can update our dictionary

    OPT_soln[amount] = OPT_soln[amount - d] + [d]

The above code appends two lists together. This gets overwritten every time `OPT[amount]` gets updated, but this is a good thing since `OPT[amount]` gets updated only when we find a better solution, so `OPT_soln[amount]` becomes a shorter list. Our final code is as follows:

    import numpy as np
        def make_change(denom, target):
            OPT = np.inf * np.ones(target + 1)
            OPT[0] = 0
    
            OPT_soln = {}
            OPT_soln[0] = []
            
            for amount in range(1, target + 1):
    
                # check all denominations
                for d in denom:
    
                    # can we use this denomination?
                    if amount - d >= 0:
    
                        # is this the best way to make this amount?
                        if OPT[amount - d] + 1 < OPT[amount]:
    
                            # update the optimal solution
                            OPT[amount] = OPT[amount-d] + 1
                            OPT_soln[amount] = OPT_soln[amount-d] + [d]
            
            return OPT_soln[target]

After running this code on our example, we get the following `OPT_soln`

{0: \[\],
1: \[1\],
2: \[1, 1\],
3: \[1, 1, 1\],
4: \[4\],
5: \[5\],
6: \[5, 1\],
7: \[5, 1, 1\],
8: \[4, 4\]}

One problem with this algorithm is that sometimes there is no solution. In our example, we are guaranteed a solution since a coin with value \\(1\\) exists. If this didn't exist, then there's no way we can make something of value \\(1\\). To fix this, all we need to do is replace the return statement with

    return OPT_soln.get(target, None)

where it tries to get the value with key `target` but if it doesn't exist (i.e. there's no solution) it returns `None.`

### Recursive Solution

We can write a recursive solution (which isn't efficient at all) but it's quick to write! We have

    def make_change(denom, target):
        if target == 0
            return 0
        if target < 0
            return None
        min_coins = np.inf
        for d in denom:
            cur_min = make_change(denom, target - d) + 1
            if cur_min < min_coins:
                min_coins = cur_min
        return min_coins

The structure actually isn't too much different. For the most part, we've swapped from square brackets to round brackets. Instead of getting a value at an index, we are calling a function instead. Hoever, this is very inefficient.  
  
Suppose we have three denominations. Then to compute \\(OPT(t)\\) we need to compute three functions \\(OPT(t-1),OPT(t-4),OPT(t-5)\\). For each of these three functions, I need to compute three more functions. We have the following tree.

                          (t)
                        /  |  \\
                      /    |    \\
                    /      |      \\
                 (t-1)   (t-4)    (t-5)
                / | \\    / | \\    / | \\

At each level \\(k\\), we call at most \\(3^k\\) functions, where the maximum number of \\(k\\) is `target`. Therefore, the total number of calls we make is bounded by \\\[3^0+3^1+3^2+\\cdots + 3^t = \\frac{3^{t+1}-1}{3-1} = \\mathcal{O}(3^t).\\\] In general, the time complexity, without memoization, is \\\[\\mathcal{O}(d^t)\\\] where \\(d\\) is the number of denominations and \\(t\\) is the target amount. If we use _memoization_ we can save a lot of time. We have the code

    def make_change_recursive(denom, target, memo={}):
        if target in memo:
            # already computed, don't need to re-compute
            return memo[target]
    
        if target == 0:
            memo[0] = 0
            return 0
    
        if target < 0:
            memo[target] = np.inf
            return np.inf
    
        min_coins = np.inf
        for d in denom:
            cur_min = make_change_recursive(denom, target - d, memo) + 1
            if cur_min < min_coins:
                min_coins = cur_min
        
        memo[target] = min_coins
    
        return min_coins

The main idea is that we stop recursive calls whenever we've already computed the value, which we're storing in the dictionary `memo`. How can we get the actual solution here? We do a similar thing as before, where **every time we update the optimal number, we also update a dictionary that keeps track of the solution that corresponds to this optimal number (i.e. optimal path)**. This is a common trick in dynamic programming problems that will be used over and over again.

    def make_change_recursive(denom, target, memo={}, solns={}):
        if target in memo:
            return memo[target], solns[target]
    
        if target == 0:
            memo[0] = 0
            solns[0] = []
            return 0, []
    
        if target < 0:
            memo[target] = np.inf
            solns[target] = None
            return np.inf, None
    
        min_coins = np.inf
        optimal_soln = None
        for d in denom:
            cur_min, cur_soln = make_change_recursive(denom, target - d, memo, solns)
            if cur_min < min_coins:
                min_coins = cur_min + 1
                optimal_soln = cur_soln + [d]
    
        memo[target] = min_coins
        solns[target] = optimal_soln
    
        return min_coins, optimal_soln

The time complexity analysis is left to the next class.

### Complexity Analysis for Memoization Solution

The time complexity is \\(\\mathcal{O}(d\*t)\\) where \\(d\\) is the number of denominations and \\(t\\) is the target amount. We can compute this by determining how many times we call the recursive function \\(\\verb#make\_change\_recursive()#\\). For each target, we recursively call the function \\(d\\) times (this is where the for loop is). The maximum number of targets is \\(t+1\\) (this is only an upper bound because sometimes we don't need to call the function for a target). Therefore, the total number of calls is \\(d\*(t+1))\\).  
  
It remains to verify that the other operations are constant time. Clearly, the base case is constant time since it involves only comparing numbers and changing the value of an array at a particular index. The only other part that might not be constant time is the line

    optimal_soln = cur_soln + [d]

because it involves creating a new list. This line is lazy writing and could be solved by pre-allocating enough space for the list so we don't need to create a new list every time, so we can make this part constant time as well. Since all other operations are in constant time, the time complexity is equal to the number of calls, which is \\(\\mathcal{O}(d\*t)\\).

### Memoization vs Iterative

In many cases, both memoization and iterative (bottom-up) dynamic programming can be used to solve a problem. However, sometimes memoization might be slightly more efficient. This is because in memoization, we take a top-down approach. This means we don't need to compute the optimal values for every number below our target. We only make recursive calls to the numbers that we actually need.  
  
We lose this ability when we take a bottom-up approach with the iterative method as we need to compute the optimal values for every number below our target. Therefore, if there are few denominations that are very spread out and we have a large target, it's going to take much longer for an iterative solution to compute the optimal solution, since it will be computing so many unnecessary values.

## L29: Graphs

We've already seen graphs twice: we've seen both heaps and linked lists. In general,

  
A **graph** \\(G=(V,E)\\) consists of a set of vertices (nodes) \\(V\\) and a set of edges \\(E\\).

For example, the following is a graph,

![](diagrams/graph.jpg)

where \\\[ \\begin{align\*} G &= (V,E) \\\\ V &= \\{v\_1, v\_2, v\_3, v\_4, v\_5\\} \\\\ E &= \\{e\_1, e\_2, e\_3, e\_4, e\_\\} \\\\ e\_1 &= (v\_1, v\_2) \\\\ e\_2 &= (v\_2, v\_3) \\\\ e\_3 &= (v\_2, v\_4) \\\\ e\_4 &= (v\_3, v\_5) \\end{align\*} \\\] Here, the edges can either be undirected or directed. If no arrows are drawn, we assume the edges are undirected (so we can travel from \\(v\_1\\) to \\(v\_2\\) and from \\(v\_2\\) to \\(v\_1\\)) and we treat \\((v\_1,v\_2)\\) as an unordered pair.  
  
Why might we use graphs?

*   Vertices are cities, edges are direct flights between cities: Want to find the best route between cities

*   Reformulate: Find the shortest distance between two nodes on a graph

*   Vertices are school classes, edges connect classes whose schedules overlap: Want to find scheduling times/locations for classes

*   Reformulate: Find a set of nodes that are completely disconnected from each other (i.e. no two nodes share an edge)

*   Vertices are objects in memory, edges connect objects that refer to each other: Want to know when an object can be freed

*   Reformulate: Find the set of nodes that connect to a certain node

as just a few examples. The reason this is important is that there are already standard algorithms for dealing with these types of problems, so if we can take our problem and reformulate it as a graph problem, we automatically get the solution. Some different types of graphs:

*   **Directed Graphs ("digraphs"):** Edges have directions associated with them

![](diagrams/digraph.jpg)

Here, we write \\(e\_1 = (v\_2,v\_1)\\) where the order matters now. The first element is the predecessor (or source) and the second element is the successor (or target).*   **Weighted graphs:** Each edge has a weight associated to it

![](diagrams/weighted_graph.jpg)

and some terminology:

*   Vertex \\(v\_1\\) is **adjacent** to vertex \\(v\_2\\) if an edge connects them.
*   A **path** is a sequence of vertices that are connected by edges. The length of the path is the number of _edges_ in it
*   A **cycle** is a path that starts and ends at the same vertex
*   A graph with no cycles is called a **acyclic graph**
*   A directed acyclic graph is abbreviated as **DAG**
*   A **simple path** is a path that does not contain any repeated vertices
*   A **simple cycle** is a cycle that does not contain any repeated vertices (except for the first and last vertex)
*   Two vertices are **connected** if there is a path between them
*   A subset of vertices is a **connected component** if every pair of vertices in the subset is connected
*   The **degree** of vertex \\(v\\) is the number of edges that connect to it

In general, I believe the definitions to be pretty straightforward. It maps pretty well to what you would expect it to be.

### Implementation

There are two common ways to implement the graph ADT.  
  

*   We can use a **Adjacency Matrix**, which is a \\(n\\times n\\) matrix where \\(\\verb#M\[i\]\[j\]=1#\\) if there is an edge between vertex \\(i\\) and vertex \\(j\\), and \\(\\verb#M\[i\]\[j\]=0#\\) otherwise.
*   We can use an **Adjacency List**, which is a list of lists where \\(\\verb#L\[i\]#\\) is a list of all the vertices that are adjacent to vertex \\(i\\).

## L30: Graphs (continued)

### Adjacency List

We can implement an adjacency list in Python as follows:

    class Node:
        def __init__(self, data):
            self.data = data
            self.adjacent = []
    
    node1 = Node('TO')
    node2 = Node('Ottawa')
    node3 = Node('Orlando')
    
    node1.adjacent.append(node2)
    node1.adjacent.append(node3)
    node2.adjacent.append(node1)
    node3.adjacent.append(node1)
    

which gives the following graph:  
  
```tex
tikz
\tikzstyle{vertex}=[circle,fill=black!25,minimum size=40pt,inner sep=2pt]
\node[vertex] (G_1) at (0,2) {TO};
\node[vertex] (G_2) at (0.7,1) {Ottawa};
\node[vertex] (G_3) at (-0.7,1) {Orlando};
\draw (G_1) -- (G_2);
\draw (G_1) -- (G_3);
```

For an undirected graph, if there are \\(N\\) edges, then the sum of the lengths of all the adjacency lists is \\(2N\\).

### Adjacency Matrix

We can implement an adjacency matrix in Python by defining the following _symmetric_ matrix (for undirected graphs) with \\(0\\)s on the diagonal: \\\[ A = \\begin{pmatrix} 0 & 1 & 1 \\\\ 1 & 0 & 0 \\\\ 1 & 0 & 0 \\end{pmatrix} \\\] where we have labelled \\(\\verb#TO#\\) as node 1, \\(\\verb#Ottawa#\\) as node 2, and \\(\\verb#Orlando#\\) as node 3. Then the entry \\(A\_{ij}\\) is 1 if there is an edge starting at node \\(i\\) and ending at node \\(j\\). Recall from linear algebra that \\(A\_{ij}\\) refers to the element in the \\(i\\)th row and \\(j\\)th column of the matrix \\(A\\).  
  

### Pagerank

One very notable application of an adjacency matrix is the **PageRank** algorithm, which is the first and most well-known algorithm used by Google to rank web pages. It essentially tries to capture the idea of which pages are the most important by asking the following question: If I start at a random page and follow random links, what is the probability that I will end up at page \\(i\\)?

1.  Normalize the matrix \\(A\\) to be \\\[ A = \\begin{pmatrix} 0 & 1/2 & 1/2 \\\\ 1 & 0 & 0 \\\\ 1 & 0 & 0 \\end{pmatrix} \\\] such that each row sums to 1 (i.e. the total probability of ending up at a site when clicking a link is 1).
2.  Imagine that we start at state \\(v\_0\\)
3.  The (un-ormalized) probability distribution of reaching some site after a single link click is given by \\( A^T v\_0\\). Why is this the case? If the current site is Toronto, then we can write \\\[ v\_0 = \\begin{pmatrix} 1 \\\\ 0 \\\\ 0 \\end{pmatrix} \\\] and the (transpose) adjacency matrix \\(A^T\\) maps this vector to the first row of the matrix, which contains all the sites that Toronto links to.  
      
    In lecture, Professor Guerzhoy wrote \\(Av\_0\\) instead. This gives a different result as the result will be a column that represents the sites that lead to Toronto. For a symmetric adjacency matrix, there is no difference, but in reality, we wouldn't have it to be symmetrical.
4.  Just doing this once is a horrible way of measuring the importance of a site. Someone could cheat the system very easily by creating several sites that all link to the same site. The idea is that if we have a very popular site being linked to by many sites, then many of these sites should also be very popular.  
      
    This idea is reflected by iterating the process of multiplying by \\(A^T\\) several times. Suppose we run it \\(k\\) times, where \\(k\\) is some very large number. Surprisingly, the result should actually converge! We get \\\[ (A^T)^{k} \\vec{v}\_0 \\to \\vec{p} \\\] where \\(\\vec{p}\\) is the probability distribution of reaching any site after \\(k\\) clicks. This result should not change much depending on what the initial state is (barring some edge cases such as islands), but it is typically done by assuming an initial uniform distribution.  
      
    The \\(i^\\text{th}\\) element of \\(\\vec{p}\\) will then be the page rank of the \\(i^\\text{th}\\) site. The intuition is that if we start at a random site and click links, then the probability of ending up at site \\(i\\) is equal to the page rank of site \\(i\\).

Outside of pagerank, this is a very fundamental idea that allows us to see which nodes are connected.

### Graph Implementation using Adjacency Matrix

We can implement a graph in Python as follows. Note that I have fixed a few minor bugs from lecture.

    class Graph:
        def __init__(self, capacity):
            self.capacity = capacity # The maximum number of nodes
            self.cur_num_nodes = 0 # The current number of nodes
            self.nodes = [] # The list of nodes
            self.indices = {} # A dictionary mapping node names to indices
            self.adj_array = [] # The adjacency array
    
            # Initialize the adjacency array
            for i in range(self.capacity):
                self.adj_array.append([None] * self.capacity)
    
        def expand(self):
            '''
            Expand the graph by doubling the capacity.
            '''
            adj_array_new = []
            self.capacity *= 2
            
            # Create a new adjacency array
            for i in range(self.capacity):
                adj_array_new.append([None] * self.capacity)
    
            # Copy the old adjacency array into the new one
            for i in range(self.cur_num_nodes):
                for j in range(self.cur_num_nodes):
                    adj_array_new[i][j] = self.adj_array[i][j]
    
            self.adj_array = adj_array_new
    
        def register_node(self, name):
            '''
            Register a new node in the graph.
            '''
    
            # If the graph is full, expand it
            if self.capacity == self.cur_num_nodes:
                self.expand()
    
            # Add the node to the graph
            self.nodes.append(name)
    
            # Add the node to the adjacency array
            self.indices[name] = self.cur_num_nodes
    
            # Increment the number of nodes
            self.cur_num_nodes += 1
    
            # Initialize the new row and column
            for i in range(self.cur_num_nodes):
                self.adj_array[i][self.cur_num_nodes-1] = 0
                self.adj_array[self.cur_num_nodes-1][i] = 0
            
        def connect_by_name(self, name1, name2):
            '''
            Connect two nodes in the graph by name.
            '''
    
            # If either node is not in the graph, add it
            if name1 not in self.indices:
                self.register_node(name1)
            if name2 not in self.indices:
                self.register_node(name2)
            
            # Connect the nodes
            self.connect_by_index(self.indices[name1], self.indices[name2])
            
        def connect_by_index(self, index1, index2):
            '''
            Connect two nodes in the graph by index.
            '''
            self.adj_array[index1][index2] = 1