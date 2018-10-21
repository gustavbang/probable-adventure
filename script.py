script = """
var a = 1
var b = 2
var c = 3
print a
print b
print c

"""

tmp = script.strip().split("\n")

variables = {}

tmp_var = tmp[0].split(" ")

#fylder dicvt med variablerne
variables[tmp_var[1]] = tmp_var[3]

print(variables)

#-------------------------------
#Denne er mere dynamisk
for t in tmp:

    tmp_var = t.split(" ")

    if tmp_var[0] == "var":
        variables[tmp_var[1]] = float(tmp_var[3])
    else:
        #Skriver printede statements ud
        print(variables[tmp_var[1]])

print(variables)