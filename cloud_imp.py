class hashpointer:
	def __init__(self,v=None):
		self.hash=v
		self.next=None



class blockchain:
	def __init__(self):
		self.merkleroot=filesplit()
		self.merkletree=[]
	
	#merkle tree formation

	def merkle(self,hashList):

    			if len(hashList) == 1:
        			return hashList[0]
    	newHashList = []
    
    	for i in range(0, len(hashList)-1, 2):
        	newHashList.append(hash2(self,hashList[i], hashList[i+1]))
    	if len(hashList) % 2 == 1: # odd, hash last item twice, if last element left
    	    newHashList.append(hash2(self,hashList[-1], hashList[-1]))
    	return merkle(newHashList)

	def hash2(self,first,second):

    	# Reverse inputs before and after hashing due to big-endian / little-endian nonsense
    		firstreverse = first.decode('hex')[::-1]
    		secondreverse = second.decode('hex')[::-1]
    	h = hashlib.sha256(hashlib.sha256(firstreverse+secondreverse).digest()).digest()
    	self.merkletree.insert(0,h[::-1].encode('hex'))
    	return h[::-1].encode('hex')

    #file splitting	
#change the input file 
    	def filesplit():
    		splitLen = 50       # 20 lines per file
			outputBase = 'output' # output.1.txt, output.2.txt, etc.

			inputfile=input("enter file name : ")

			file = open(inputfile, 'r')

			inputlist=[]
			outputlist=[]

			input=True
				while input:
					input=file.read(200)
					if input:
					inputlist.append(input)

			at = 1
			for lines in range(0, len(inputlist), splitLen):
    		# First, get the list slice
    			outputData = inputlist[lines:lines+splitLen]
    			output = open(outputBase + str(at) + '.txt', 'w')
    			outputlist.append(''.join(outputData))
    			output.write(''.join(outputData))
    			output.close()

    		# Increment the counter
    			at += 1

    	#contains hash values of the divided files	
    		txhashes2=[]

			for files in outputlist:
				hash_object=hashlib.sha256(files)
				txhashes2.append(hash_object.hexdigest())
			self.merkleroot=merkle(self,txhashes2)
