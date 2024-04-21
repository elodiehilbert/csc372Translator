xNum1 = int(input("Give me an integer: "))
xNum2 = int(input("Give me another integer: "))


if xNum1 > xNum2:
	print("Max =", xNum1)
	
else:
	print("Max =", xNum2)
	


print("Sum =", xNum1 + xNum2)

if xNum1 > xNum2:
	print("Difference=", xNum1 - xNum2)
	
else:
	print("Difference=", xNum2 - xNum1)
	


print("Product =", xNum1 * xNum2)

if xNum1 > xNum2:
	xMin = int(xNum2)
	
else:
	xMin = int(xNum1)
	


xVal = 1
while xVal <= xMin - 1:
	if (xNum1 % xVal == 0) and (xNum2 % xVal == 0):
		xGCD = int(xVal)
		
	
	xVal+= 1


print("GCD =", xGCD)

print("LCM =", xNum1 / xGCD * xNum2)
