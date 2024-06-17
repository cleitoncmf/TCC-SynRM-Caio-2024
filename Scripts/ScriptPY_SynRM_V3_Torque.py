#Script para girar o rotor da máquina, ler o fluxo concatenado pelas bobinas e salvar os resultados em um arquivo .csv
#Biblioteca necessária pyFEMM, baixe no cmd com 'pip install pyfemm'
import csv
import femm

nome_do_arquivo = 'Protótipo de rotor de relutância_4polos_M-36_realinhado.fem'
nome_tabela_ref = "Corrente_8A_delta25.csv"
#currents = [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
angs_carga = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45]
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
f = 'Curvas_de_Torque_M-36_8A.csv'
cabecalho = ["Posicao"]

#Cabeçalho do arquivo, para multiplas correntes, no caso de querer as indutâncias
'''
for current in currents:
    cabecalho.append(f"Indutância_Corrente_{current}A")
'''
for carga in angs_carga:
    cabecalho.append(f"Torque_Angulo_{carga}°")

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


resultado = []

#Repetição para girar o rotor e computar os resultados
for angulo in range(0,55-delta_angulo,delta_angulo):
    resultado.append(angulo)
    for carga in angs_carga:
        print(f"Analisando corrente/angulo {carga}...\n")
        #Setando o valor da corrente da lista currents, para análise de multiplas correntes contínuas
        #femm.mi_modifycircprop("BobinaEstatorA",1,current)
        #'Setando' os valores de corrente de acordo com o CSV, as variáveis dos circuitos são interpretadas em strings
        femm.mi_modifycircprop("BobinaEstatorA",1,buscar_valor(nome_tabela_ref,4,str(angulo+carga),1))
        femm.mi_modifycircprop("BobinaEstatorB",1,buscar_valor(nome_tabela_ref,4,str(angulo+carga),2))
        femm.mi_modifycircprop("BobinaEstatorC",1,buscar_valor(nome_tabela_ref,4,str(angulo+carga),3)) 

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
        #femm.mo_savebitmap(f'figuras\Torque_{carga}_posicao_{angulo}_graus_M-36.bmp')
        
        #Computa as variáveis das bobinas do Estator
        #Corrente_estatorA,Tensao_estatorA,Fluxo_Concatenado_estatorA = femm.mo_getcircuitproperties("BobinaEstatorA")
        #Corrente_estatorB,Tensao_estatorB,Fluxo_Concatenado_estatorB = femm.mo_getcircuitproperties("BobinaEstatorB")
        #Corrente_estatorC,Tensao_estatorC,Fluxo_Concatenado_estatorC = femm.mo_getcircuitproperties("BobinaEstatorC")
        
        #Selecionar a área do rotor para calcular o torque
        femm.mo_seteditmode("area")
        femm.mo_groupselectblock(5)
        femm.mo_selectblock(0,0)
        femm.mo_selectblock(9.9,2.7)

        t = femm.mo_blockintegral(22)
        
        #Grava os resultados de interesse na lista resultado e limpa a seleção
        resultado.append(t)
        femm.mo_clearblock()
        

    with open(f,'a', newline='') as arquivo_csv:
        # Cria um objeto escritor CSV
        escritor_csv = csv.writer(arquivo_csv)

        # Escreve o cabeçalho no arquivo CSV
        escritor_csv.writerow(resultado)
    #Gira o rotor ao redor do ponto (0,0)
    femm.mi_selectgroup(5)
    femm.mi_moverotate(0,0,-delta_angulo)
    resultado=[]
    cont+=1
    print(f"Iteração {cont} de {round(50/delta_angulo)}.\n")

#Alinhar o Rotor
femm.mi_selectgroup(5)
femm.mi_moverotate(0,0,-delta_angulo)
femm.messagebox('Processo de Simulação Concluído')
print("Concluído")