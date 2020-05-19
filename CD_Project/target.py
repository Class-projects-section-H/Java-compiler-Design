import re
import sys

if len(sys.argv) != 2:
    print("Correct usage: python3 target.py example.txt\n")
    exit()

def printcode(list_of_lines, message=""):
    print(message.upper())
    for line in list_of_lines:
        print(line.strip())

arithmetic_operations = {'+':'ADD','*':'MUL','-':'SUB','/':'DIV'}
conditional_operations = {'==':'BNE','!=':'BE','<':'BGE','>':'BLE','<=':'BGT','>=':'BLT'} #Not operation
register_values = {}
register_available = ['REG0','REG1','REG2','REG3','REG4','REG5','REG6','REG7']
register_occupied  = []

def get_register():
    if(not len(register_available) == 0): #Checks if registers are available
        register = register_available.pop(0)
        register_occupied.append(register)
    else:                                 #IF no register available then uses the oldest register (LRU)
        register = register_occupied[0]
        register = register_occupied.pop(0)
        register_values.pop(register)
        register_occupied.append(register)
    return register

def check_register(operand): #Checking if operand has been assigned to register
    for key in register_values.keys():
        if(operand == register_values[key]):
            register = key
            register_occupied.remove(register) #If it's present ,it will get added to the end of list 
            register_occupied.append(register)
            return register
    register = get_register()
    print("\tMOV {} {}".format(register,operand))
    register_values[register]=operand
    return register

def arithmetic_operation(line,operation):
    first_operand=unicode(line[2],"utf-8")
    if(first_operand.isnumeric()): #Checking If First operand is a number or variable
        register1 = line[2]
    else:
        register1 = check_register(line[2]) 
    #register1 = check_register(line[2])
    second_operand=unicode(line[4],"utf-8") 
    if(second_operand.isnumeric()):  #Checking If Second operand is a number or variable
        register2 = line[4]
    else:
        register2 = check_register(line[4])
    register3 = get_register() #Register which contains the evaluated expression
    print("\t{} {} {} {}".format(operation,register3,register1,register2))
    
    regex_match= re.findall("^t[0-9]*$",line[0]) #Temporary Variable
    if(len(regex_match)):
        pass
    else:
        print("\tSTR {} {}".format(register3,line[0]))
    #print("before register_values",register_values)
    #To remove Redundancy
    if(line[0] == line[2]): #Checks if variable is the same as first operand
        register_occupied.remove(register1)
        register_available.append(register1)
        register_values.pop(register1)
    
    elif(line[0] == line[4] and not second_operand.isnumeric()): #Checks if variable is the same as second operand
        register_occupied.remove(register2)
        register_available.append(register2)
        register_values.pop(register2)
    #print("after register_values",register_values)
    register_values[register3] = line[0]
    #print("register3",register_values)

    

def conditional_operation(line):
    # register1 = check_register(line[2])
    first_operand=unicode(line[2],"utf-8")
    if(first_operand.isnumeric()):
        register1 = line[2]
    else:
        register1 = check_register(line[2])
    second_operand=unicode(line[4],"utf-8")
    if(second_operand.isnumeric()):
        register2 = line[4]
    else:
        register2 = check_register(line[4])
    print("\tCMP {} {}".format(register1,register2))

condition_used = " "

def eval_statements(line):
    global condition_used
    line = line.split()

    for operator in arithmetic_operations:
        if operator in line and len(line) == 5 :
            arithmetic_operation(line,arithmetic_operations[operator])
            return
    
    for operator in conditional_operations:
        if operator in line and len(line) == 5 :
            condition_used = conditional_operations[operator]
            conditional_operation(line)
            return

    if(len(line) == 1): #labels
        regex_match = re.findall("^[A-Za-z0-9]*:$",line[0])
        if(len(regex_match)):
            print(line[0])
            return
    
    # if 'not' in line and len(line) == 4:
    #     print("\t{} {}".format(condition_used,line[3]))
    #     return 

    #False condition
    if 'if' in line and len(line) == 4:
        print("\t{} {}".format(condition_used,line[3]))
        return 


    if 'goto' in line and len(line) == 2:
        print("\tB {}".format(line[1]))
        return
    
    if '=' in line and len(line) == 3: #Initialising variable
        register1 = check_register(line[2])
        print("\tSTR {} {}".format(register1,line[0]))
        regex_match= re.findall("^t[0-9]*$",line[2]) 
        first_operand=unicode(line[2],"utf-8")
        if(first_operand.isnumeric() or len(regex_match)):
            pass
        else:
            register2 = get_register()
        
        # for register in register_values.keys():
        #     if(register_values[register] == line[0]):
        #         register_values.pop(register)
        #         register_occupied.remove(register)
        #         register_available.append(register)
        #         break
        
        #print("before register_values:",register_values);
        if(not first_operand.isnumeric() and not len(regex_match)): # when d=a
            #print("register2:",register2)
            register_values[register2] = line[0]
            #print("first_operand:",register_values)
        register_values_byte=unicode(register_values[register1],'utf-8')
        if(register_values_byte.isnumeric() or len(regex_match)): # when d=2 or d=t1
            register_occupied.remove(register1)
            register_occupied.append(register1)
            #print("register1:",register1)
            register_values[register1] = line[0]
            #print("first_operand:",register_values)
        return 
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        optimized_code = str(sys.argv[1])

    list_of_lines = []
    opti_code = open(optimized_code, "r")
    for line in opti_code:
        list_of_lines.append(line)
    opti_code.close()

    for line in list_of_lines:
        eval_statements(line)