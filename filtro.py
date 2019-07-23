import csv
import fileinput
import os
from numpy import genfromtxt
from scipy import signal
import fileinput
from shutil import copyfile


#Esse código pega um arquivo pupil_positions e gera esse arquivo de saida:
#diameter_3d_filtrado.csv - arquivo só com a coluna diameter3d, com o filtro de mediana aplicado nos valores

#TAMANHO DO FILTRO:
size=14
#DELETAR TODOS OS VALORES 0?
deletezero = True

#######################################################################################################

#ESSA PARTE SERVE PARA PEGAR UM ARQUIVO pupil_positions.csv E GERAR UM ARQUIVO 
#diameter_3d.csv QUE POSSUI APENAS OS VALORES DA COLUNA diameter_3d DO PRIMEIRO ARQUIVO
#Para poder aplicar o filtro de mediana


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

#Remover todos os \n
with open('deletarIssoAquiTambem.csv') as infile, open('diameter_3d.csv', 'w') as outfile:
    for line in infile:
        if not line.strip(): continue  
        outfile.write(line)  

#######################################################################################################

#AGORA ESSA PARTE VAI PEGAR O ARQUIVO diameter_3d.csv GERADO E CRIAR UM ARQUIVO diameter_3d_filtrado.csv 
#COM O FILTRO DE MEDIANA APLICADO!


entrada = genfromtxt("diameter_3d.csv", delimiter='\n')
saida = signal.medfilt(entrada, kernel_size=size)

#Gerar Resultado:
l = list(saida)
file = open("diameter_3d_filtrado.csv", "w+")
wr = csv.writer(file, delimiter='\n')
wr.writerow(l)
file.close()

os.remove("deletarIssoAqui.csv")
os.remove("deletarIssoAquiTambem.csv")
os.remove("diameter_3d.csv")

#AGORA, AS CASAS DECIMAIS DE AMBOS OS ARQUIVOS GERADOS SERÃO MODIFICADAS DE . PARA ,
#PARA O EXCEL RECONHECER AUTOMATICAMENTE
with fileinput.FileInput("diameter_3d_filtrado.csv", inplace=True) as file:
    for line in file:
        print(line.replace('.', ','), end='')


print('Processo Finalizado!')