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



	def proof_of_work(self, last_proof):
		"""
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        p = 0
        # while sha256(f'{last_proof}{p}'.encode()).hexdigest()[:4] != '0000' :
        # 	p+=1
        while self.valid_proof(last_proof, p) is False :
        	p +=1

        return p




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
        return guess_hash[:4] = '0000' 




	@property
	def last_block(self):
		return self.chain[-1]




app = Flask(__main__)

node_identifier = str(uiud4()).replace('-', '')

blockchain = Blockchain()



def mine():
	return "We'll mine a new block "


def new_transaction():
	return "We'll do a new transaction"

def full_chain():
	response = {
		
	}