# figure out here, what hash of (x*y) ends in 0
import hashlib


"""
pseudo code


"""

# def hash_test(string):
# 	return hashlib.sha256(string)
y=0
x=5
output = 'abcd5'
while output[-1] != '0' :
	output = hashlib.sha256(str(x*y).encode()).hexdigest()
	y+=1

#.hexdigest(), .encode() ??

print(y-1, output)
print(hashlib.sha256(str(x*y).encode()).hexdigest())

print(hashlib.sha256(str(x*(y-1)).encode()).hexdigest())
st = 'hi2233jkjkjk'
print(st, st.encode())



# Find a number p that when hashed with the previous block’s solution a hash with 4 leading 0s is produced.
output = '1111'
while output[:4] != '0000' :
	output = hashlib.sha256(str(self.prev_block  * y).encode()).hexdigest()
	