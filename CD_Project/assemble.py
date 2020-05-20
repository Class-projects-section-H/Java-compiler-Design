import re

list_register=[] #List of Register assigned
condition=" "
def register(operand,flag_print): #Checks if a register is assigned to a variable ,if not a register is assigned
	used_registers=[]
	for i in list_register:
		used_registers.append(i[0])
	for i in list_register:  #If variable assigned to register, then it is pushed to the end of list 
		if(i[1]==operand):
			list_register.remove(i)
			list_register.append(i)
			return i[0]
	if(len(list_register)==8): #IF All registers are occupied
		reg=list_register[0][0]
		list_register.pop(0) 
		list_register.append([reg,operand]) #LRU
		if(flag_print):
			print("\tMOV r"+str(reg)+" "+str(operand))
		return reg
	else:
		for i in range(8):  #Assigning a register to a variable ,it assigns the lowest unused register
			if(i not in used_registers):
				list_register.append([i,operand])
				if(flag_print):
					print("\tMOV r"+str(i)+" "+str(operand))
				return i
	

def begin(line):
	line=line.split(" ")
	#print(line)
	if(len(line)==3): #Assignment Operation
		if(re.search("^[0-9]+$", line[2]) or line[2]=="true" or line[2]=="false" ): #checking if the right operand is number
			var2=register(line[2],1)
			print("\tSTR r"+str(var2)+" "+str(line[0]))
			for i in list_register:
				if(i[0]==var2):
					i[1]=line[0]
					break
		else:
			var_temp=register(line[2],1)
			var2=register(line[0],0)
			if(re.search("^t[0-9]+", line[2])): #For temporary variable
				for i in list_register:
					if(i[1]==line[0]):
						i[0]=var_temp
				for i in list_register:
					if(i[1]==line[2]):
						list_register.remove(i)
			print("\tSTR r"+str(var_temp)+" "+str(line[0]))
		return

	if(len(line)==5):
		if(line[3] in ["+","-","/","*"]): #Arithmetic Operations
			var_temp=str(register(line[0],0))
			if(re.search("^[0-9]+$", line[2]) ): #To check if operand is numeric
				first_operand=line[2]
			else:
				first_operand="r"+str(register(line[2],1))
			if(re.search("^[0-9]+$", line[4]) ): #To check if operand is numeric
				second_operand=line[4]
			else:
				second_operand="r"+str(register(line[4],1))
			if(line[3]=="+"):
				print("\tADD r"+var_temp+" "+first_operand+" "+second_operand)
			elif(line[3]=="-"):
				print("\tSUB r"+var_temp+" "+first_operand+" "+second_operand)
			elif(line[3]=="/"): 
				print("\tDIV r"+var_temp+" "+first_operand+" "+second_operand)
			else:
				print("\tMUL r"+var_temp+" "+first_operand+" "+second_operand)
		else:  #Conditional Operations
			global condition
			condition=line[3]
			if(re.search("^[0-9]+$", line[2]) ):
				first_operand=line[2]
			else:
				first_operand="r"+str(register(line[2],1))
			if(re.search("^[0-9]+$", line[4]) ):
				second_operand=line[4]
			else:
				second_operand="r"+str(register(line[4],1))
			print("\tCMP "+first_operand+" "+second_operand)
		return

	if(len(line)==4 and "goto" in line): #Branching for false conditions
		#global condition
		if(condition == "=="):
			print("\tBNE "+line[3])
		elif(condition == "!="):
			print("\tBE "+line[3])
		elif(condition == ">="):
			print("\tBLT "+line[3])
		elif(condition == "<="):
			print("\tBGT "+line[3])
		elif(condition == ">"):
			print("\tBLE "+line[3])
		else:
			print("\tBGE "+line[3])
		return

	if(len(line)==2 and "goto" in line): #Branching for true conditions
		print("\tB "+line[1])
		return

	if(len(line)==1): #labels
		print(line[0])
		return


file = open("icg.txt", "r")
for line in file: #Reading the optimized code file
	line = line.rstrip("\n")
	begin(line.strip())
file.close()
 