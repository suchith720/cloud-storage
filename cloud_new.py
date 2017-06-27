import hashlib
import datetime
#class hash pointer

class hashpointer:
	def __init__(self,v=None):
		self.hash=v
		self.next=None

	def isnull(self):
		if self.hash==None and self.next==None:
			return(True)
		return(False)

	def __str__(self):
		if self.hash=='':
			return('')

		return(str(self.hash))

#class blockheader


class blockheader:
	def __init__(self,uId=None,fID=None):
		self.block_no=None
		self.merkleroot=None
		self.userID=uId
		self.timestamp=str(datetime.datetime.utcnow())
		self.fileID=fID
		self.file_no=None
		self.prev_pointer=hashpointer()
		self.merkletree=[]
		self.dataList=[]

	def compact_header(self):
		block_list=[]
		if self.userID==None:
			return(block_list)

		block_list.append(str(self.block_no))
		block_list.append(self.userID)
		block_list.append(self.fileID)
		block_list.append(self.timestamp)
		block_list.append(self.merkleroot)
		block_list.append(str(self.prev_pointer))
		block_list.append(str(self.file_no))
		return(block_list)

	def calc_hash(self):
		final_list=self.compact_header()
		print(final_list)
		final_str=''.join(final_list)
		value=hashlib.sha256(hashlib.sha256(final_str).digest()).digest()
		return(value.encode('hex'))

	def __str__(self):
		return(str(self.compact_header()))


#class block

class block:
	def __init__(self,uId=None,fID=None):
		self.block_head=blockheader(uId,fID)
		

	def isempty(self):
		if self.block_head.userID==None:
			return(True)
		else:
			return(False)

	def calc_pointer(self):
		value=self.block_head.calc_hash()
		block_pointer=hashpointer(value)
		block_pointer.next=self
		return(block_pointer)

	def insert(self,uID,fID):
		if self.isempty():
			self.block_head.userID=uID
			self.block_head.fileID=fID
			self.block_head.merkleroot=self.filesplit()
			# merkletree,dataList,file_no
			self.block_head.block_no=0
			return
		
		newblock=block(uID,fID)
		newblock.block_head.merkleroot=self.filesplit()

		(self.block_head,newblock.block_head)=(newblock.block_head,self.block_head)
		(self.block_head.prev_pointer,newblock.block_head.prev_pointer)=(newblock.calc_pointer(),self.block_head.prev_pointer)
		return

	



	def merkle(self,hashList):
		if len(hashList)==1:
			return(hashList[0])

		newhashList=[]

		for i in range(0,len(hashList)-1,2):
			newhashList.append(self.hash2(hashList[i],hashList[i+1]))
		if len(hashList)%2==1:
			newhashList.append(self.hash2(hashList[-1],hashList[-1]))
		return(self.merkle(newhashList))

	def hash2(self,first,second):
		firstreverse=first.decode('hex')[::-1]
		secondreverse=second.decode('hex')[::-1]
		value=hashlib.sha256(hashlib.sha256(firstreverse+secondreverse).digest()).digest()
		self.block_head.merkletree.insert(0,value[::-1].encode('hex'))
		return value[::-1].encode('hex')

	def filesplit(self):
		txhash2=[]
		#size of splitting a file
		splitline=20
		outputBase='output'

		#inputfile=input("enter file name : ")
		#inputfile=inputfile[:-1]
		file=open('input.txt','r')

		inputlist=[]

		input1=True

		while input1:
			input1=file.read(200)
			if input1 :
				inputlist.append(input1)

		at=1

		for lines in range(0,len(inputlist),splitline):
			outputData=inputlist[lines:lines+splitline]
			output=open(outputBase+str(at),'w')
			self.block_head.dataList.append(''.join(outputData))
			output.write(''.join(outputData))
			output.close()
			at+=1

		self.block_head.file_no=at-1

		for files in  self.block_head.dataList:
			#big endian - little endian problem
			hash_object=hashlib.sha256(files)
			txhash2.append(hash_object.hexdigest())

		return(self.merkle(txhash2))

	def __str__(self):
		selflist=[]

		if self.block_head.userID==None:
			return(str(selflist))

		temp=self
		selflist.append(temp.block_head.compact_header())

		while not self.block_head.prev_pointer.isnull():
			temp=temp.block_head.prev_pointer.next
			selflist.append(temp.block_head.compact_header())

		return(str(selflist))








