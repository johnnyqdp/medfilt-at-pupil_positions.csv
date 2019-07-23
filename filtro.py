#github.com/johnnyqdp

import csv
import fileinput
import os
from numpy import genfromtxt
from scipy import signal
import fileinput
from shutil import copyfile

########## VARIÁVEIS: ##########

#TAMANHO DO FILTRO (tem que ser ímpar): /// ENGLISH: Median filter window size (needs to be odd)
size=15

#DELETAR TODOS OS VALORES IGUAIS A 0? (acho melhor deixar em False) /// ENGLISH: Delete all values == 0?
deletezero = False

#Modificar a separação de casas decimais do arquivo final de . para ,?
#(Isso é útil pra abrir o arquivo no excel) /// ENGLISH: English speaking users just change it to False
excel = True


#Esse código pega um arquivo pupil_positions.csv e gera esse arquivo de saida:
#diameter_3d_filtrado.csv - arquivo com a coluna diameter3d, com o filtro de mediana aplicado nos valores
#######################################################################################################

#Removendo as colunas indesejadas do arquivo pupil_capture, para deixar apenas a diameter_3d
de = 0
ate = 13
with open("pupil_positions.csv", "r") as fp_in, open("deletarIssoAqui.csv", "w") as fp_out:
    reader = csv.reader(fp_in, delimiter=",")
    writer = csv.writer(fp_out, delimiter=",")
    for row in reader:
        del row[de:ate]
        writer.writerow(row)
de = 1
ate = 21
with open("deletarIssoAqui.csv", "r") as fp_in, open("deletarIssoAquiTambem.csv", "w") as fp_out:
    reader = csv.reader(fp_in, delimiter=",")
    writer = csv.writer(fp_out, delimiter=",")
    for row in reader:
        del row[de:ate]
        writer.writerow(row)

#Removendo todos os valores 0.0
if deletezero:
    with fileinput.FileInput("deletarIssoAquiTambem.csv", inplace=True) as file:
        for line in file:
            print(line.replace('0.0', '\n'), end='')

#Removendo todos os \n
with open('deletarIssoAquiTambem.csv') as infile, open('diameter_3d.csv', 'w') as outfile:
    for line in infile:
        if not line.strip(): continue  
        outfile.write(line)  

#Agora... aplicar o filtro de mediana:
entrada = genfromtxt("diameter_3d.csv", delimiter='\n')
saida = signal.medfilt(entrada, kernel_size=size)

#Gerar Resultado (apenas imprimindo o array "saida"):
l = list(saida)
file = open("diameter_3d_filtrado.csv", "w+")
wr = csv.writer(file, delimiter='\n')
wr.writerow(l)
file.close()

#Deletando as besteiras:
os.remove("deletarIssoAqui.csv")
os.remove("deletarIssoAquiTambem.csv")
os.remove("diameter_3d.csv")

#AGORA, AS CASAS DECIMAIS DE AMBOS OS ARQUIVOS GERADOS SERÃO MODIFICADAS DE . PARA ,
#PARA O EXCEL RECONHECER AUTOMATICAMENTE
if excel:
    with fileinput.FileInput("diameter_3d_filtrado.csv", inplace=True) as file:
        for line in file:
            print(line.replace('.', ','), end='')

#Aí sim :D
print('Processo Finalizado!')