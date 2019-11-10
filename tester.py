# print('hi')
# some practice programming

class list_transform(object):
	def __init__(self):
		self.initialList = []
		self.scanList = []

	def setup(self, input_list,scan_list):
		self.initialList = input_list
		self.scanList = scan_list

	def return_bool(self):
		return self.initialList







list_test = [5,6,7,8,9,8,3,2,1]
print(list_test)
list_filtered = [i for i in list_test if i != 7]
print(list_filtered)
	