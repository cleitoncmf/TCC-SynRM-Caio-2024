#Script para girar o rotor da máquina, ler o fluxo concatenado pelas bobinas e salvar os resultados em um arquivo .csv
#Biblioteca necessária pyFEMM, baixe no cmd com 'pip install pyfemm'
import csv
import femm

nome_do_arquivo = 'Protótipo de rotor de relutância_4polos_M-36.fem'
nome_tabela_ref = "Corrente_8A_delta25.csv"

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

#Cria ou abre o arquivo onde serão gavados os valores dos fluxos concatenados
f = 'Dados_M-36_Trifásico.csv'
cabecalho = ["Posicao","Fluxo_Concatenado_estatorA","Fluxo_Concatenado_estatorB","Fluxo_Concatenado_estatorC","Tensao_A","Tensao_B","Tensao_C","Indutancia_A","Indutancia_B","Indutancia_C","R_A","R_B","R_C","Potencia_A","Potencia_B","Potencia_C"]

# Abre o arquivo CSV no modo de escrita
with open(f, 'w', newline='') as arquivo_csv:
    # Cria um objeto escritor CSV
    escritor_csv = csv.writer(arquivo_csv)
    
    # Escreve o cabeçalho no arquivo CSV
    escritor_csv.writerow(cabecalho)
    print(f'O arquivo CSV "{f}" foi criado com sucesso.\n')

#Intervalo entre os ângulos e contador de iterações do loop
#delta_angulo = int(input("Intervalo dos angulos: "))
delta_angulo = 5
cont=0

#Setando valores iniciais de corrente para calcular indutancias proprias
#Para funcionar, transforme as bobinas que estão em zero em comentarios no loop.
femm.mi_modifycircprop("BobinaEstatorA",1,0)
femm.mi_modifycircprop("BobinaEstatorB",1,0)
femm.mi_modifycircprop("BobinaEstatorC",1,0)

#Repetição para girar o rotor e computar os resultados
for angulo in range(0,366-delta_angulo,delta_angulo):
    #'Setando' os valores de corrente de acordo com o CSV, as variáveis dos circuitos são interpretadas em strings
    femm.mi_modifycircprop("BobinaEstatorA",1,buscar_valor(nome_tabela_ref,4,str(angulo),1))
    femm.mi_modifycircprop("BobinaEstatorB",1,buscar_valor(nome_tabela_ref,4,str(angulo),2))
    femm.mi_modifycircprop("BobinaEstatorC",1,buscar_valor(nome_tabela_ref,4,str(angulo),3)) 

    #O contorno do rotor, assim como os materiais estão no grupo 5
    femm.mi_selectgroup(5)

    #Roda a analise de resultados
    femm.mi_analyze()

    #Mostra o resultado da simulacao
    femm.mi_loadsolution()
    #Mostra a densidade de fluxo
    #Se habilitou a apresentação da solução e quiser mostar a densidade de fluxo
    #Fica muito mais lento
    femm.mo_showdensityplot(0,0,1.6,10**-8,"bmag")
    #Salva o print do resultado (posição inicial)
    #Se quiser salvar um print de cada imagem, descomente
    #Fica mais lento
    nome_da_figura = ".figs\posicao_",angulo,"_graus.emf"
    femm.mo_savebitmap(f'figuras\posicao_{angulo}_graus.bmp')
    #Computa as variáveis das bobinas do Estator
    Corrente_estatorA,Tensao_estatorA,Fluxo_Concatenado_estatorA = femm.mo_getcircuitproperties("BobinaEstatorA")
    Corrente_estatorB,Tensao_estatorB,Fluxo_Concatenado_estatorB = femm.mo_getcircuitproperties("BobinaEstatorB")
    Corrente_estatorC,Tensao_estatorC,Fluxo_Concatenado_estatorC = femm.mo_getcircuitproperties("BobinaEstatorC")

    #Grava os resultados de interesse na lista resultado
    resultado = [angulo,Fluxo_Concatenado_estatorA,Fluxo_Concatenado_estatorB,Fluxo_Concatenado_estatorC,Tensao_estatorA,Tensao_estatorB,Tensao_estatorC,Fluxo_Concatenado_estatorA/Corrente_estatorA,Fluxo_Concatenado_estatorB/Corrente_estatorB,Fluxo_Concatenado_estatorC/Corrente_estatorC,Tensao_estatorA/Corrente_estatorA,Tensao_estatorB/Corrente_estatorB,Tensao_estatorC/Corrente_estatorC,Tensao_estatorA*Corrente_estatorA,Tensao_estatorB*Corrente_estatorB,Tensao_estatorC*Corrente_estatorC]
    with open(f,'a', newline='') as arquivo_csv:
        #Cria um objeto escritor CSV
        escritor_csv = csv.writer(arquivo_csv)
    
        #Escreve o cabeçalho no arquivo CSV
        escritor_csv.writerow(resultado)
    #Gira o rotor ao redor do ponto (0,0)
    femm.mi_selectgroup(5)
    femm.mi_moverotate(0,0,-delta_angulo)
    
    cont+=1
    print(f"Iteração {cont} de {round(360/delta_angulo)}.")
    print("Corrente A: ",Corrente_estatorA,"\nCorrente B: ",Corrente_estatorB,"\nCorrente C: ",Corrente_estatorC,"\n")

#Alinhar o Rotor
femm.mi_selectgroup(5)
femm.mi_moverotate(0,0,-delta_angulo)
print("Concluído")
