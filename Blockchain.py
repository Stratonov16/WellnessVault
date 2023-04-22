import hashlib
import json
from time import time
from urllib.parse import urlparse
from zkp import verify
import requests
import pickle

class Blockchain(object):

    blockchain_list = []

    def __init__(self, user):
        self.chain = []
        self.current_transactions = []
        self.user = user

        # using set so that single user never exists twice
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

        # load blockchains from database
        Blockchain.load_blockchains()

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        print("block created: {}".format(block))

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        Blockchain.save_blockchains()
        return block

    def new_transaction(self, user, doctor, report, tup):
        # Adds a new transaction to the list of transactions

        # tup: y, s, t1, t2, t3

        if (not verify(tup)):
            return False

        """
        Creates a new transaction to go into the next mined Block
        :param user: <str> Address of the user
        :param report: <int> report
        :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'user': report[0],
            'doctor': report[1],
            'Medical Report': report[2],
            'Pulse Rate': report[3],
            'Blood Pressure': report[4],
            'Temperature': report[5],
            'Blood Sugar': report[6],
            'Weight': report[7],
            'Prescription': report[8],
            'Created at': report[9]
        })

        print("Transaction added by user: {}".format(user))

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    """
    A Proof of Work algorithm (PoW) is how new Blocks are created or mined on the blockchain.
    The goal of PoW is to discover a number which solves a problem.
    The number must be difficult to find but easy to verify
    """

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        if (guess_hash[:4] == "0000"):
            print("Validated: p = {}, p' = {}".format(last_proof, proof))
            return True
        return False

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # we’ll make the rule that the longest valid chain is authoritative.

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http:// {node} /chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    @staticmethod
    def create_new_blockchain(user):
        """
        param user: <string> username
        return Blockchain object
        """

        new_blockchain = Blockchain(user)
        Blockchain.blockchain_list.append(new_blockchain)
        Blockchain.save_blockchains()

        return new_blockchain

    @staticmethod
    def save_blockchains():
        """
        return <list> list of Blockchain objects
        using pickle to store list of blockchain
        """

        with open('database', 'wb') as file:
            pickle.dump(Blockchain.blockchain_list, file)

    @staticmethod
    def load_blockchains():
        Blockchain.blockchain_list = []

        with open('database', 'rb') as file:
            Blockchain.blockchain_list = pickle.load(file)
        
        print(Blockchain.blockchain_list)

    @staticmethod
    def get_blockchain(user):

        for blockchain in Blockchain.blockchain_list:
            if blockchain.user == user:
                return blockchain

        return Blockchain.create_new_blockchain(user)
