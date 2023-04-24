from Blockchain import Blockchain
from uuid import uuid4

# load blockchains from database
Blockchain.load_blockchains()

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

def mine(user):
    blockchain = Blockchain.viewUser(user)
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.proof_of_work(last_proof)
    new_block = blockchain.new_block(proof)

    response = {
        'message': "New Block is Made",
        'index': new_block['index'],
        'transactions': new_block['transactions'],
        'proof': new_block['proof'],
        'previous_hash': new_block['previous_hash'],
    }

    return response


def create_transaction(user, doctor, report, tup):
    blockchain = Blockchain.viewUser(user)

    index = blockchain.new_transaction(user, doctor, report, tup)
    message = f'Transaction will be added to Block {index}'

    response = {'message': message}
    return response


def full_chain(user):
    blockchain = Blockchain.viewUser(user)
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return response


def register_nodes(user, nodes):
    # Retrieve the blockchain object associated with the given user
    blockchain = Blockchain.viewUser(user)

    # If nodes is None or empty, return an error message
    if not nodes:
        return {'message': 'Error: Please supply a valid list of nodes'}

    # Register each node in the given list with the blockchain
    for node in nodes:
        blockchain.register_node(node)

    # Return a success message with the total number of nodes in the blockchain network
    return {'message': 'New nodes have been added', 'total_nodes': list(blockchain.nodes)}


def consensus(user):
    # Retrieve the blockchain object associated with the given user
    blockchain = Blockchain.viewUser(user)

    # Check if the current node's copy of the blockchain is authoritative
    replaced = blockchain.longest_chain()

    # If the blockchain was replaced, return a success message with the updated chain
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    # If the blockchain is authoritative, return a success message with the current chain
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    # Always return the response dictionary
    return response

def isValid(user):
    blockchain = Blockchain.viewUser(user)
    return blockchain.valid_chain(blockchain.chain)

def viewUser(user):
    return Blockchain.viewUser(user)

def viewUser_list():
    return Blockchain.blockchain_list

