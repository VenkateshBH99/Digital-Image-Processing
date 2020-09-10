from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from copy import deepcopy
from scipy import ndimage
import random

class A(object):
	def __init__(self,img,k):
		self.stack=[]
		self.img=img
		self.height,self.width=self.img.shape
		self.img_label=np.full_like(self.img,0)
		self.k=k
		self.threshold=10

	def start(self):
		for i in range(self.k):
			x=random.randint(0,self.height-1)
			y=random.randint(0,self.width-1)
			while self.img_label[x,y]!=0:
				x=random.randint(0,self.height-1)
				y=random.randint(0,self.width-1)
			self.img_label[x,y]=i+1
			self.stack.append((x,y))
			# c=0
		while len(self.stack)!=0:
			x,y=self.stack.pop(0)
			self.grow(x,y)
		
	def neighbour(self,x1,y1):
		neighbour=[]
		for i in (-1,0,1):
			for j in (-1,0,1):
				if i==0 and j==0:
					continue
				x=x1+i
				y=y1+j
				if self.in_region(x,y):
					neighbour.append((x,y))
		return neighbour

	def in_region(self,x,y):
		return True if 0<=x<self.height and 0<=y<self.width else False


	def grow(self,x1,y1):
		curr_label=self.img_label[x1,y1]
		for x,y in self.neighbour(x1,y1):
			# print(x,y)
			if self.img_label[x,y]==0:
				if abs(self.img[x,y]-self.img[x1,y1])<=self.threshold:
					self.img_label[x,y]=curr_label
					self.stack.append((x,y))
			
	def result(self):
		temp={}
		val=0
		count=0
		clus={}
		val1=int(255/self.k)
		for i in range(self.k-1):
			temp[i+1]=val
			val=val+val1
			clus[i+1]=0
		temp[self.k]=255
		clus[self.k]=0
		for i in range(self.height):
			for j in range(self.width):
				if self.img_label[i,j]==0:
					# print(i,j)
					count+=1
				else:
					self.img[i,j]=temp[self.img_label[i,j]]
					clus[self.img_label[i,j]]+=1
		print(count)
		print(clus)
		print(self.img.shape)
		cv2.imwrite('seg.png',self.img)
		# cv2.imshow('Result',self.img)
		# cv2.waitkey(0)






Image = cv2.imread('image.jpg')
r, g, b = Image[:,:,0], Image[:,:,1], Image[:,:,2]
gray_img = 0.2989 * r + 0.5870 * g + 0.1140 * b
cv2.imwrite('GracyImage.PNG', gray_img)
SRG=A(gray_img,5)
SRG.start()
SRG.result()