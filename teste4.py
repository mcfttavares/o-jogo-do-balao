palindrome = True
str = (input())

for i in range(0, len(str)):
     if str[i] != str [len(str)-i-1]:
        palindrome = False
if palindrome == True:
    print("É uma capicua.")
else:
    print("Não é uma capicua.")