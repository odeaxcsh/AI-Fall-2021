# first of all some utilities on doubly-linked lists 

# this function takes some parameters that I'll to explain:
# root: this parameter is an instance of Fibonacci_Heap.Node class
# and this pram is not actually the root of a list. it's just an element of the list that will be iterated on and iteration will be done horizontally
# do: what you want to do with the node in the iteration path, the return value matters in this implementation: 
# if return type is None:
#   then nothing unexpected won't happen
# if return type is a node:
#   then cursor will jump to the node
# if return value is str('break'):
#   then iteration stops
# else:
#   every other value is illegal and will raise exceptions
#
# the other parameters will be passed to the do function!
def _iterate_through_linked_list(root, do, *do_args, **do_keys):
    current = root
    while current is not None:
        jump_to = do(current, *do_args, **do_keys)
        current = jump_to if jump_to else current.right
        if current is root or current == 'break':
            break

# easily remoces a node from a linked list and return reminder list
# NOTE: list will be changed!
def _remove_node_from_linked_list(node):
    if node is None:
        return
    elif node is node.right:
        return None
    else:
        node = [node.right, node.left]
        node[0].left = node[1]
        node[1].right = node[0]
        return node[0]

# merge two linked list and returen merged
# NOTE: lists will be changed!
def _merge_linked_lists(first, second):
    if first is None:
        return second
    elif second is None:
        return first
    else:
        first = [first, first.right]
        second = [second, second.right]
        first[0].right = second[1]
        second[0].right = first[1]
        first[1].left = second[0]
        second[1].left = first[0]
        return first[0]

# returns ceil of log(n)ss
def _log2(num):
    log = 1
    while num != 1:
        log += 1
        num //= 2
    return log

class Fibonacci_Heap(object):
    class Locator:
        ''' 
            this class is really unnecessary!
            but I have to implement becuase the other heap classes have one and actually need one
            and our will dijkstra algorithm use it later!
        '''
        DELETED = None
        __slots__ = ['location']
        def __init__(self, location):
            self.location = location
            # the location points to the node in the tree
            # and the node on the tree points to this object to
            # so they can change(update) each other and so this is an adoptable Fibonacci heap
            location.locator = self

    # a Fibonacci heap is a list of heaps that each of them has a list of heaps and so on..!
    # to implement the list of heaps in every level we use a doubly-linked list. why doubly? why not just a linked list?
    # I think we use DLL because the merge operation has a complexity of o(n) in a singly linked list
    # and also in deleting a node (in this case min) we have the same time complexity with SLL and on both of these operations DLL appears in constant time complexity.
    # To implement heaps hierarchy relation (each node has some heaps as children) we design a hierarchy list using 'child' and 'parent'
    class Node: 
        __slots__ = ['right', 'left', 'child', 'parent', 'key', 'value', 'loser', 'degree', 'locator']
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.degree = 0
            self.loser = False
            self.right = self
            self.left = self
            self.child = None
            self.parent = None
            self.locator = None
    
    def __init__(self):
        self._head = None
        self._min = None
        self._size = 0

    def at(self, locator):
        return locator.location

    def empty(self):
        return self._size == 0

    # simply creat a node and push it into the main list
    def add(self, key, value=None):
        new_node = Fibonacci_Heap.Node(key, value)
        self._head = _merge_linked_lists(self._head, new_node)
        if self._min is None or key < self._min.key:
            self._min = new_node
        self._size += 1
        return Fibonacci_Heap.Locator(new_node)
    

    # remove min:
    # first of all we delete the min and append its children to the main list
    # after this, consolidate the heaps with this process:
    # 1. find two nodes with the same degree:
    # 2. append the node with the higher degree to the other node children(make node with higher degree child of the other)
    # 3. repeat 1, 2 till there are no such nodes

    # this operation implemented in a little weird way but it works well and could've been explained if it wasn't late and my English skills weren't frustrating
    def remove_min(self):
        if self.empty():
            raise IndexError('heap is empty')

        min_ = self._min    # take a record of min
        self._min = None    # rmeove min
        min_.locator.location = Fibonacci_Heap.Locator.DELETED  # remove min
        self._head = _remove_node_from_linked_list(min_) # remove min

        def reset(node):
            node.parent = None
            node.loser = False
        _iterate_through_linked_list(min_.child, reset)     # change childrens' parents of min from min to None
                                                            # loser will be explained(probably) later
        self._head = _merge_linked_lists(self._head, min_.child)    # append children of min to the main list

        self._size -= 1

        if self._size < 2:
            self._min = self._head
            return min_.key, min_.value
        
        key, value = min_.key, min_.value
        roots = [None] * (_log2(self._size) + 1)

        # takes a node as e
        # finds the node that has the same degree with e and merges them
        def check_and_merge(node, self, roots):
            jump_to = 'break' if node.right is node else node.right
            self._head = _remove_node_from_linked_list(node)
            node.right = node.left = node
            other = roots[node.degree]
            while other is not None:
                roots[node.degree] = None
                if other.key < node.key:
                         node, other = other, node
                other.parent = node
                node.child = _merge_linked_lists(node.child, other)
                node.degree += 1
                other = roots[node.degree]
            roots[node.degree] = node
            return jump_to

        # do check and merging for all elements of the main list
        _iterate_through_linked_list(self._head, check_and_merge, self, roots)
        for i in range(_log2(self._size) + 1):
            self._head = _merge_linked_lists(self._head, roots[i])

            # find new min:
            if roots[i] is not None:
                if self._min is None or roots[i].key < self._min.key:
                    self._min = roots[i]
        return key, value

    # after decreasing a key if heap properties hold, all is ok and "done!".
    # if the key of the modified node is less than its parent key then we easily cut the node and append it to roots list
    # this operation may make tree very unbalanced so to solve this problem we use a marking technic
    # if a node lost a node in operation we mark it as loser
    # if a loser node loss another node we cut and append it to the roots list
    def decrease(self, locator, new_key):
        current = locator.location
        if current.key < new_key:
            return 
            # raise Exception("new_key value must be smaller than current value({}), but {} is passed".format(locator.location.key, new_key))
        current.key = new_key
        if new_key < self._min.key:
            self._min = current
        if current.parent and current.key < current.parent.key:
            current.loser = True
            while current.parent and current.loser:
                parent = current.parent
                parent.child = _remove_node_from_linked_list(current)
                parent.degree -= 1
                current.parent = None
                current.right = current.left = current
                current.loser = False
                self._head = _merge_linked_lists(self._head, current)
                current = parent
            if current.parent is not None:
                current.loser = True
