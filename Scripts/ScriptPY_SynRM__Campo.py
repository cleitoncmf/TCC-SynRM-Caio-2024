#Script para girar o rotor da máquina, ler o fluxo concatenado pelas bobinas e salvar os resultados em um arquivo .csv
#Biblioteca necessária pyFEMM, baixe no cmd com 'pip install pyfemm'
import csv
import femm
import math

nome_do_arquivo = 'Protótipo de rotor de relutância_4polos_M-36_realinhado.fem'
nome_tabela_ref = "Corrente_8A_delta25.csv"

#vetor de correntes para ir para o cabeçalho do csv de saida
currents = [x for x in range(0, 66,2)]

#Para o calculo de multiplas correntes, o csv base será multiplicado por n fatores
#Por exemplo, o primeiro fator será zero, então a saída será zero
#Já o segundo fator 0.25 que vezes 8 corresponde a uma corrente de 2A
#Terceiro fator 0.5 o que corresponde a 4A, assim por diante
fatores = [x/8 for x in range(0, 66,2)]

femm.openfemm()
femm.opendocument(nome_do_arquivo)

def buscar_valor(csv_file, coluna_busca, valor_busca, coluna_retorno):
    with open(csv_file, 'r') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        
        # Itera sobre as linhas do arquivo CSV
        for linha in leitor_csv:
            # Verifica se o valor de coluna_busca corresponde ao valor buscado
            if linha[coluna_busca] == valor_busca:
                # Retorna o valor associado à coluna_retorno
                return linha[coluna_retorno]
    
    # Se o valor não for encontrado, retorna None
    return None

#Cria ou abre o arquivo onde serão gravados os valores dos fluxos concatenados
f = 'Campos_Entreferro_M-36.csv'
cabecalho = ["Posicao"]

#Cabeçalho do arquivo, para multiplas correntes, no caso de querer as indutâncias

for current in currents:
    cabecalho.append(f"Campo_Corrente_{current}A")

# Abre o arquivo CSV no modo de escrita
with open(f, 'w', newline='') as arquivo_csv:
    # Cria um objeto escritor CSV
    escritor_csv = csv.writer(arquivo_csv)
    
    # Escreve o cabeçalho no arquivo CSV
    escritor_csv.writerow(cabecalho)
    print(f'O arquivo CSV "{f}" foi criado com sucesso.\n')

#Intervalo entre os ângulos e contador de iterações do loop
delta_angulo = 5
cont=0
count=0

resultado = []
femm.mi_modifycircprop("BobinaEstatorA",1,0)
femm.mi_modifycircprop("BobinaEstatorB",1,0)
femm.mi_modifycircprop("BobinaEstatorC",1,0)

#Repetição para girar o rotor e computar os resultados
#Essa configuração irá calcular apenas a posição de 45°
for angulo in range(45,96-delta_angulo,delta_angulo):
    resultado.append(angulo)
    for n in fatores:
        print(f"Analisando corrente {currents[count]}...\n")
        count+=1

        #'Setando' os valores de corrente de acordo com o CSV e depois multiplicando pelo fator n
        femm.mi_modifycircprop("BobinaEstatorA",1,str(n*float(buscar_valor(nome_tabela_ref,4,str(angulo),1))))
        femm.mi_modifycircprop("BobinaEstatorB",1,str(n*float(buscar_valor(nome_tabela_ref,4,str(angulo),2))))
        femm.mi_modifycircprop("BobinaEstatorC",1,str(n*float(buscar_valor(nome_tabela_ref,4,str(angulo),3)))) 

        #O contorno do rotor, assim como os materiais estão no grupo 5
        femm.mi_selectgroup(5)

        #Roda a analise de resultados
        femm.mi_analyze()

        #Mostra o resultado da simulacao
        femm.mi_loadsolution()

        #Mostra a densidade de fluxo
        #Se habilitou a apresentação da solução e quiser mostar a densidade de fluxo
        #Fica muito mais lento
        #femm.mo_showdensityplot(0,0,0.8,0.006,"bmag")
       
        #Salva o print do resultado (posição inicial)
        #Se quiser salvar um print de cada imagem, descomente
        #Fica mais lento
        #femm.mo_savebitmap(f'figuras\Campo_{current}A_posicao_{angulo}_graus_M-36.bmp')
        
        #Computa as variáveis das bobinas do Estator
        Corrente_estatorA,Tensao_estatorA,Fluxo_Concatenado_estatorA = femm.mo_getcircuitproperties("BobinaEstatorA")
        Corrente_estatorB,Tensao_estatorB,Fluxo_Concatenado_estatorB = femm.mo_getcircuitproperties("BobinaEstatorB")
        Corrente_estatorC,Tensao_estatorC,Fluxo_Concatenado_estatorC = femm.mo_getcircuitproperties("BobinaEstatorC")
        
        #Computa o campo no ponto (0,9.98), há uma componente x e y
        Bx, By = femm.mo_getb('0','9.98')
        
        #Grava os resultados de interesse, módulo de B
        resultado.append(math.sqrt(Bx**2+By**2))
        print(f'Corrente bobina A:{Corrente_estatorA}\nCorrente bobina B:{Corrente_estatorB}\nCorrente bobina C:{Corrente_estatorC}\nCampo:',math.sqrt(Bx**2+By**2),'\n') 


    with open(f,'a', newline='') as arquivo_csv:
        # Cria um objeto escritor CSV
        escritor_csv = csv.writer(arquivo_csv)

        # Escreve o cabeçalho no arquivo CSV
        escritor_csv.writerow(resultado)

    #Gira o rotor ao redor do ponto (0,0)
    #se quiser girar a corrente E o rotor, descomente abaixo
    #femm.mi_selectgroup(5)
    #femm.mi_moverotate(0,0,-delta_angulo)
    resultado=[]
    print(f"Iteração {cont} de {round(90/delta_angulo)}.\n")
    cont+=1
    count=0

#Alinhar o Rotor
femm.mi_moverotate(0,0,-(360-angulo))
femm.messagebox('Processo de Simulação Concluído')
print("Concluído")