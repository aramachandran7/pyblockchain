import hashlib
from hashlib import sha256
import json
from time import time
from uiud import uiud4
from textwrap import dedent

from flask import Flask 


# really, really simple blockchain framework. LOL

class Blockchain(object):
	def __init__(self):
		self.chain = []
		self.current_transactions = []

		self.new_block(previous_hash=1, proof=100)

	# creates a new block, adds to the chain
	def new_block(self, proof, previous_hash=None):
		
		block = {
			'index':len(self.chain)+1,
			'timestamp':time(),
			'transactions':self.current_transactions,
			'proof':proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]) # calc the hash for the last value in the chain=previous block. 
		}


		self.current_transactions = [] # why reset current transactions? 

		self.chain.append(block)

		return block


	# adds a new transaction to the list of transactions
	def new_transaction(self, sender, recipient, amount):
		self.current_transactions.append({
			'sender': sender,
			'recipient': recipient,
			'amount': amount,
			})

		return self.last_block['index'] + 1


	# this is our hash function, hashes a block
	@staticmethod
	def hash(block):
		# execute sha256 on this mofo, return string
		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()	



	# def proof_of_work(self, last_proof):
	# 	p=0
 #        while self.valid_proof(last_proof, p) is False:
 #        	p +=1
	# 	return p

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
	
	# while sha256(f'{last_proof}{p}'.encode()).hexdigest()[:4] != '0000' :
    # 	p+=1
    """
    Simple Proof of Work Algorithm:
     - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
     - p is the previous proof, and p' is the new proof
    :param last_proof: <int>
    :return: <int>
    """
    




	@staticmethod
	def valid_proof(last_proof, proof):
		"""
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:4] == '0000' 




	@property
	def last_block(self):
		return self.chain[-1]




app = Flask(__main__) # creating a flask server to act as a single node in our blockchain


node_identifier = str(uiud4()).replace('-', '') # creating a random string of chars for the identifier

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
	last_block = blockchain.last_block()
	proof = blockchain.proof_of_work(last_block)


	#reward the miner for mining. 
	blockchain.new_transaction(
		'sender':0, 
		'recipient':node_identifier, 
		'amount':1
			)

	# create (forge) a new block

	previous_hash = blockchain.hash(last_block)
	block = blockchain.new_block(proof, previous_hash)

	response = {
		'message':'new block forged',
		'index':block['index'],
		'transactions':block['transactions'], 
		'proof':block['proof'],
		'previous_hash': block['previous_hash']
	}

	return jsonify(response), 200



@app.route('/transactions/new', methods=['POST'])
def new_transaction():

	values=request.get_json() # getting the value for the request. 

	required = ['sender', 'recipient', 'amount']

	# check if the values of a string are the values in a dictionary line up with the values in a 
	if not all(k in values for k in required):
		return 'Missing Values', 400

	#ths is the index for the new transaction, as new_transaction returns an index. 
	index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

	response = {'message': f'transaction will be added to block {index}'}

	return jsonify(response), 201



@app.route('/chain', methods=['GET'])
def full_chain():
	response = {
		'chain':blockchain.chain, 
		'length':len(blockchain.chain)

	}
	return jsonify(response), 200


if __name__ == __main__ :
	app.run(host='0.0.0.0', port=5000)