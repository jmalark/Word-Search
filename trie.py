####
#trie.py
#HW8
#####

class TrieNode:
    """Represents a single node of a trie data structure"""
    def __init__(self):
        """Creates a node with no children, that is not the end of a word"""
        self.word = False
        self.children = {}

    def setChild(self, symbol, node):
        """Sets (or adds) a child associated with the given symbol"""
        self.children[symbol] = node
    
    def getChild(self, symbol):
        """Returns the child associated with the symbol (or None if there is no such child)"""
        return self.children.get(symbol, None)

    def isWord(self):
        """Returns true if this node represents the end of a word that was added to the trie"""
        return self.word

    def setWord(self, word):
        """Sets whether this node corresponds to the end of a word or not."""
        self.word = word

class Trie:
    """The interface to a trie class, for storing and efficiently searching a collection of strings (or sequences more generally)"""
    def __init__(self):
        """Creates an empty trie"""
        self.root = TrieNode()
    
    def add(self, item):
        """Adds the given string to the trie"""
        node = self.root
        
        for c in item:
            child = node.getChild(c)
            if child == None:
                #If the node doesn't have a corresponding child, we
                #need to make one
                child = TrieNode()
                node.setChild(c, child)
            node = child
        
        node.setWord(True)

    def search(self, item):
        """Returns true if the item is in the trie, False otherwise"""
        node = self.root

        for c in item:
            node = node.getChild(c)
            if node == None:
                return False

        return node.isWord()

    def isPrefix(self, item):
        """Returns true if the item is a prefix or a word in the Trie, False otherwise"""

        #basically the exact code from search, except it doesn't call isWord, it returns true whenever it makes it that far
        node = self.root

        for c in item:
            node = node.getChild(c)
            if node == None:
                return False

        return True
