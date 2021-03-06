from pythondsa.src.exceptions import Empty
from pythondsa.src.lists import _DoublyLinkedBase


class ArrayQueue:
    """Queue implementation using a Python list as underlying storage."""

    DEFAULT_CAPACITY = 10  # moderate capacity for new queues

    def __init__(self):
        """Creates an empty queue."""
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        """Returns the number of elements in the queue."""
        return self._size

    def _resize(self, cap):
        """Resizes the list to capacity >= len(self)."""
        old = self._data                  # keep track of existing list
        self._data = [None] * cap
        walk = self._front

        for k in range(self._size):
            self._data[k] = old[walk]     # shift indices
            walk = (1 + walk) % len(old)  # old size used for modulus
        self._front = 0

    def is_empty(self):
        """Returns True if the queue is empty"""
        return self._size == 0

    def first(self):
        """
        Returns the lement at the front of the queue, without removing it.

        Raises Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty('The queue is empty')
        return self._data[self._front]

    def enqueue(self, e):
        """Add an element to the back of the queue."""
        if self._size == len(self._data):
            self._resize(2 * len(self._data))  # double the array size

        last_in_line = (self._front + self._size) % len(self._data)
        self._data[last_in_line] = e
        self._size += 1

    def dequeue(self):
        """
        Removes and returns the element in front of the queue.

        Raises Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty('The queue is empty')

        result = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1

        return result


class LinkedQueue:
    """FIFO Queue implementation using a singly linked list for storage."""

    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""
        __slots__ = '_element', '_next'  # streamline memory usage

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        """Create an empty queue."""
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        """Return the number of elements in queue."""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return (but do not remove) the element at the front of the queue."""
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._head._element

    def dequeue(self):
        """Remove and return the first element of the queue (i.e., FIFO).

        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():
            self._tail = None
        return answer

    def enqueue(self, e):
        """Add an element to the back of the queue."""
        newest = self._Node(e, None)
        if self.is_empty():
            self._head = newest
        else:
            self._tail._next = newest
        self._tail = newest
        self._size += 1


class CircularQueue:
    """Queue implementation using circularly linked list for storage."""

    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""

        __slots__ = '_element', '_next'  # streamline memory usage

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        """Create an empty queue."""
        self._tail = None
        self._size = 0

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return (but do not remove) the element at the front of the queue.

        Raise Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty('Queue is empty')
        head = self._tail._next
        return head._element

    def dequeue(self):
        """Remove and return the first element of the queue (i.e. FIFO).

        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty('Queue is empty')
        oldhead = self._tail._next
        if self._size == 1:
            self._tail = None
        else:
            self._tail._next = oldhead._next
        self._size -= 1
        return oldhead._element

    def enqueue(self, e):
        """Add an element to the back of the queue."""
        newest = self._Node(e, None)
        if self.is_empty():
            newest._next = newest
        else:
            newest._next = self._tail._next  # new node points to head
            self._tail._next = newest        # old tail points to new node
        self._tail = newest
        self._size += 1

    def rotate(self):
        """Rotate front element to the back of the queue."""
        if self._size > 0:
            self._tail = self._tail._next


class ArrayDeque:
    """Double-ended queue implementation based on an array."""

    DEFAULT_CAPACITY = 10

    def __init__(self, maxlen=None):
        """Create an empty deque."""
        self._size = 0
        self._front = 0
        self._maxlen = maxlen
        if not self._maxlen or self._maxlen >= ArrayDeque.DEFAULT_CAPACITY:
            self._data = [None] * ArrayDeque.DEFAULT_CAPACITY
        else:
            self._data = [None] * self._maxlen

    def __getitem__(self, i):
        """Return a reference to the element at index i.

        Raise IndexError if the requested index is not in range.
        """
        if isinstance(i, slice):
            raise NotImplementedError('Deque does not currently support slicing.')
        elif isinstance(i, int):
            if i < self._size * -1 or i > self._size - 1:
                raise IndexError('Deque index out of range.')
            if i < 0:  # Handle negative indices
                index = (self._front + self._size + i) % len(self._data)
            else:
                index = (self._front + i) % len(self._data)
            return self._data[index]
        else:
            raise TypeError('Invalid argument type.')

    def __setitem__(self, i, v):
        if isinstance(i, slice):
            raise NotImplementedError('Deque does not currently support slicing.')
        elif isinstance(i, int):
            if i < self._size * -1 or i > self._size - 1:
                raise IndexError('Deque index out of range.')
            if i < 0:  # Handle negative indices
                index = (self._front + self._size + i) % len(self._data)
            else:
                index = (self._front + i) % len(self._data)
            self._data[index] = v
        else:
            raise TypeError('Invalid argument type.')

    def __len__(self):
        """Return the number of elements in the deque."""
        return self._size

    def _resize(self, cap):
        """Resizes the deque to capacity >= len(self)."""
        old = self._data  # save existing data
        self._data = [None] * cap
        walk = self._front

        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0

    def add_first(self, e):
        """Add an element to the front of the deque."""
        if self._size == len(self._data):
            self._resize(2 * len(self._data))

        self._front = (self._front - 1) % len(self._data)
        self._data[self._front] = e
        self._size += 1

    def add_last(self, e):
        """Add an element to the back of the deque."""
        if self._size == len(self._data):
            self._resize(2 * len(self._data))  # double array size

        last_in_line = (self._front + self._size) % len(self._data)
        self._data[last_in_line] = e
        self._size += 1

    def clear(self):
        """Remove all elements from the deque leaving it with length 0."""
        self._size = 0
        self._front = 0
        if not self._maxlen or self._maxlen >= ArrayDeque.DEFAULT_CAPACITY:
            self._data = [None] * ArrayDeque.DEFAULT_CAPACITY
        else:
            self._data = [None] * self._maxlen

    def count(self, value):
        """Return the number of matches for value in deque."""
        value_count = 0
        for i in range(self._size):
            if self._data[(self._front + i) % len(self._data)] == value:
                value_count += 1
        return value_count

    def remove(self, value):
        """Remove the first occurrence of value.

        Raise a ValueError if value not found.
        """
        found = False
        for i in range(self._size):
            current = (self._front + i) % len(self._data)
            if self._data[current] == value:
                found = True
                break
        if not found:
            raise ValueError('value not found in deque.')
        if i > self._size // 2:
            for i in range(i, self._size - 1, 1):
                current = (self._front + i) % len(self._data)
                next = (current + 1) % len(self._data)
                self._data[current] = self._data[next]
                last = (self._front + self._size - 1) % len(self._data)
                self._data[last] = None
        else:
            for i in range(i, 0, -1):
                current = (self._front + i) % len(self._data)
                prev = (current - 1) % len(self._data)
                self._data[current] = self._data[prev]
                self._data[self._front] = None
                self._front += 1
                self._size -= 1

    def rotate(self, n=1):
        """Rotate the deque n steps to the right. If n is negative, rotate to the left."""
        if n >= 0:
            for step in range(n):
                self.add_first(self.delete_last())
        else:
            for step in range(abs(n)):
                self.add_last(self.delete_first())

    def delete_first(self):
        """Delete an element from the front of the deque.

        Raise Empty exception if the deque is empty."""
        if self.is_empty():
            raise Empty('The deque is empty.')

        result = self._data[self._front]  # Save result to return later
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1

        return result

    def delete_last(self):
        """Delete an element from the back of the deque.

        Raise Empty exception if the deque is empty."""
        if self.is_empty():
            raise Empty('The deque is empty.')

        last_in_line = (self._front + self._size - 1) % len(self._data)
        result = self._data[last_in_line]
        self._data[last_in_line] = None
        self._size -= 1

        return result

    def first(self):
        """Return a reference to the element at the front of the deque.

        Raise Empty exception if the deque is empty."""
        if self.is_empty():
            raise Empty('The deque is empty.')
        return self._data[self._front]

    def last(self):
        """Return a reference to the element at the back of the deque.

        Raise Empty exception if the deque is empty."""
        if self.is_empty():
            raise Empty('The deque is empty')
        last_in_line = (self._front + self._size - 1) % len(self._data)
        return self._data[last_in_line]

    def is_empty(self):
        """Return True if the deque does not contain any elements."""
        return self._size == 0

    def is_full(self):
        """Return True if the deque has an assigned maxlen and is full."""
        return len(self._data) == self._maxlen


class LinkedDeque(_DoublyLinkedBase):
    """Double-ended queue implementation based on a doubly linked list."""

    def first(self):
        """Return (but do not remove) the element at the front of the deque."""
        if self.is_empty():
            raise Empty('Deque is empty')
        return self._header._next._element  # the item after the header sentinel

    def last(self):
        """Return (but do not remove) the element at the back of the deque."""
        if self.is_empty():
            raise Empty('Deque is empty')
        return self._trailer._prev._element  # the item before the trailer sentinel

    def insert_first(self, e):
        """Add an element to the front of the deque."""
        self._insert_between(e, self._header, self._header._next)

    def insert_last(self, e):
        """Add an element to the back of the deque."""
        self._insert_between(e, self._trailer._prev, self._trailer)

    def delete_first(self):
        """Remove and return the element from the front of the deque.

        Raise Empty exception if the deque is empty."""
        if self.is_empty():
            raise Empty('Deque is empty')
        return self._delete_node(self._header._next)

    def delete_last(self):
        """Remove and return the element from the back of the deque.

        Raise Empty exception if the deque is empty."""
        if self.is_empty():
            raise Empty('Deque is empty')
        return self._delete_node(self._trailer._prev)
