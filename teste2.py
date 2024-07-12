#x

from random import randint
x=randint(1,3)

print("Escolhe uma opção: \n- Pedra\n- Papel \n- Tesoura")

#y

y = (input())

if y=="Pedra":
    y=1
elif y=="Papel":
    y=2
elif y=="Tesoura":
    y=3

#output

if x==1 and y==1:
    print("Empate!\nEscolheste pedra e o computador também!")
elif x==2 and y==2:
    print("Empate!\nEscolheste papel e o computador também!")
elif x==3 and y==3:
    print("Empate!\nEscolheste tesoura e o computador também!")
elif x==1 and y==3:
    print("Perdeste!\nEscolheste tesoura e o computador escolheu papel!")
elif x==2 and y==1:
    print("Perdeste!\nEscolheste pedra e o computador escolheu papel!")
elif x==3 and y==2:
    print("Perdeste!\nEscolheste papel e o computador escolheu tesoura!")
elif x==1 and y==2:
    print("Ganhaste!\nEscolheste papel e o computador escolheu tesoura!")
elif x==2 and y==3:
    print("Ganhaste!\nEscolheste tesoura e o computador escolheu papel!")
elif x==3 and y==1:
    print("Ganhaste!\nEscolheste pedra e o computador escolheu tesoura!")
else:
    print("Erro! Não escolheste nenhuma das opções!")
































































































































































