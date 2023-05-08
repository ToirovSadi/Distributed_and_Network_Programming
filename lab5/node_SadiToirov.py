from argparse import ArgumentParser
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

M = 5
PORT = 1234
RING = [2, 7, 11, 17, 22, 27]

class Node:
    def get_successor(self, id):
        for node in self.ring:
            if node >= id:
                return node
        return self.ring[0]
    
    def __init__(self, node_id):
        """Initializes the node properties and constructs the finger table according to the Chord formula"""
        self.ring = sorted(RING)
        self.finger_table = []
        self.node_id = node_id
        self.succ = self.get_successor(node_id+1)
        self.data = {}
        for i in range(M):
            nxt = (node_id + 2 ** i) % (2 ** M)
            successor = self.get_successor(nxt)
            self.finger_table.append((nxt, successor))

        self.finger_table.sort()
        print(f"Node created! Finger table = {self.finger_table}")

    def closest_preceding_node(self, id):
        """Returns node_id of the closest preceeding node (from n.finger_table) for a given id"""
        if id < self.node_id:
            id += 2 ** M - 1
        
        for i in range(M-1, -1, -1):
            x = self.finger_table[i][1]
            
            if x < self.node_id:
                x += 2 ** M - 1
            if self.node_id < x <= id:
                return self.finger_table[i][1]
        
        return self.node_id

    def find_successor(self, id):
        """Recursive function returning the identifier of the node responsible for a given id"""
        if id == self.node_id:
            return self.node_id

        l = self.node_id
        m = id
        r = self.succ
        if r < l: # make them in same scale
            r += 2 ** M - 1
        if m < l: # make them in same scale
            m += 2 ** M - 1

        if l < m <= r:
            return self.succ
        
        succ_id = self.closest_preceding_node(id)
        if succ_id == self.node_id:
            succ_id = self.succ
            
        print(f'Forwarding the request (key={id}) to node {succ_id}')
        with ServerProxy(f'http://node_{succ_id}:{PORT}') as node:
            return node.find_successor(id)
    
    def put(self, key, value):
        """Stores the given key-value pair in the node responsible for it"""
        print(f"put({key}, {value})")
        succ_id = self.find_successor(key)
        if self.node_id == succ_id:
            return self.store_item(key, value)
        else:
            with ServerProxy(f'http://node_{succ_id}:{PORT}') as node:
                return node.store_item(key, value)

    def get(self, key):
        """Gets the value for a given key from the node responsible for it"""
        print(f"get({key})")
        succ_id = self.find_successor(key)
        if self.node_id == succ_id:
            return self.retrieve_item(key)
        else:        
            with ServerProxy(f'http://node_{succ_id}:{PORT}') as node:
                return node.retrieve_item(key)

    def store_item(self, key, value):
        """Stores a key-value pair into the data store of this node"""
        self.data[key] = value
        return True

    def retrieve_item(self, key):
        """Retrieves a value for a given key from the data store of this node"""
        if key in self.data:
            return self.data[key]
        return -1


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('node_id', help='id of the node', type=int)
    args = parser.parse_args()

    n = Node(args.node_id)
    with SimpleXMLRPCServer(('0.0.0.0', PORT), logRequests=False) as s:
        s.register_instance(n)
        s.serve_forever()
