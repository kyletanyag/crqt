import numpy as np
import warnings
import math
class topsis:
	a=None #Matrix (m criteria and n alternatives (mxn))
	w=None #Weight matrix
	r=None #Normalisation matrix 
	m=None #Number of rows
	n=None #Number of columns
	aw=[] #worst alternative
	ab=[] #best alternative
	diw=None
	dib=None
	siw=None
	sib=None	
	
	#Return a numpy array with float items
	def floater(self,a):
		ax=[]
		for i in a:
			try:
				ix=[]
				for j in i:
					ix.append(float(j))
			except:
				ix=float(i)
				pass
			ax.append(ix)
		return np.array(ax)

	def __init__(self,a,w,j):
		self.a=np.array(a)
		self.m=len(a)
		self.n=len(a[0])
		self.w=np.transpose(np.array([w]))
		# print(self.a)
		self.j=j

	#Step 2
	def step2(self):
		self.r=self.a
		for j in range(self.n):
			nm=sum(self.a[:,j]**2)**0.5
			self.r[:,j]=self.a[:,j]/nm

	#Step 3
	def step3(self):
		self.t=self.r*self.w
	
	#Step 4
	def step4(self):
		for i in range(self.m):
			if self.j[i]==1:
				self.aw.append(min(self.t[i,:]))
				self.ab.append(max(self.t[i,:]))
			else:
				self.aw.append(max(self.t[i,:]))
				self.ab.append(min(self.t[i,:]))
	#Step 5			
	def step5(self):
		self.diw = np.zeros(self.n)
		self.dib = np.zeros(self.n)
		for i in range(self.n):
			self.diw[i] = sum((self.t[:,i]-self.aw)**2)**0.5
			self.dib[i] = sum((self.t[:,i]-self.ab)**2)**0.5

	#Step 6
	def step6(self):
		# np.seterr(all='ignore')
		self.siw=self.diw/(self.diw+self.dib)
	
	def calc(self):
		self.step2()
		self.step3()
		self.step4()
		self.step5()
		self.step6()
		return self.siw
