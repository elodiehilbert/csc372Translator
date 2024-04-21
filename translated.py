xNum = int(5)
print(xNum + 5)
print(xNum - 2)
print(xNum * 3)
print(xNum / 5)
print(12 % 5)
print(1 or 0)
print(1 and 1)
print(1 < 5 and not 1)
print(5 > 3)
print(3 >= 3)

bVal = bool(1 or 0)
print(bVal)

sThing = "Hello"
print(sThing)

if 5 > 3:
	print(5)
	


if 5 < 4:
	print("No")
	
else:
	print("yesy")
	


xJ = int(0)
while xJ < 3:
	xI = int(0)
	while xI < 3:
		print(xJ + xI)
		xI += 1
	
	xJ += 1


sInput = input("Say Something: ")
print(sInput)

def fMultiply(xa, xb):
	return xa * xb
	


print(fMultiply(5, 3))

def fAdd(xa):
	def lmiSineBuF(xb):
		return xa + xb
	return lmiSineBuF


def fAddFiveNums(xa):
	def LWIIlRHJrY(xb):
		def wYyijgVFex(xc):
			def IRmqaNtBCo(xd):
				def YUscfyaKWU(xe):
					return xa + xb + xc + xd +xe
				return YUscfyaKWU
			return IRmqaNtBCo
		return wYyijgVFex
	return LWIIlRHJrY


fAddThree= fAdd(3)

print(fAddThree(20))
print(fAdd(10)(20))

