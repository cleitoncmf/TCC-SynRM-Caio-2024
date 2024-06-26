# Simulações

## Arquivos para simulação

Se tiver a intenção de testar o script, a pasta contém o arquivo FEM requerido, os dados da corrente em formato CSV e o script para levantar dados gerais da máquina.
(Obs: A tensão induzida é apenas resistiva e não deve ser considerada, o mesmo para a potência)

## Curvas de magnetização da máquina

Essa pasta contém a curva *BxH* do Aço M-36 (Curva B-H M-36.csv) e as curvas de fluxo de eixo direto e em quadratura na bobina *A* em função da corrente *Ia*.
Caso queira replicar a medição dos fluxos dq, comente os modificadores de circuito dentro do loop e coloque a corrente desejada acima do loop (No exemplo abaixo, o motor irá girar com a corrente de 8A na bobina A somente).


```
#Se for coletar dados para corrente continua, especificar as correntes abaixo
#Para funcionar, comente os modificadores de corrente dentro do for loop
femm.mi_modifycircprop("BobinaEstatorA",1,8)
femm.mi_modifycircprop("BobinaEstatorB",1,0)
femm.mi_modifycircprop("BobinaEstatorC",1,0)

#Repetição para girar o rotor e computar os resultados
for angulo in range(0,366-delta_angulo,delta_angulo):
    #'Setando' os valores de corrente de acordo com o CSV de referencia, as variáveis dos circuitos são interpretadas em strings
    #femm.mi_modifycircprop("BobinaEstatorA",1,
                           buscar_valor(nome_tabela_ref,4,str(angulo),1))
    #femm.mi_modifycircprop("BobinaEstatorB",1,
                           buscar_valor(nome_tabela_ref,4,str(angulo),2))
    #femm.mi_modifycircprop("BobinaEstatorC",1,
                           buscar_valor(nome_tabela_ref,4,str(angulo),3)) 
                           
```

## Levantamento das Indutâncias da Máquina

Essa pasta possui as curvas de fluxo concatenado na Bobina A para corrente de 5A na Bobina A.
Também tem as curvas de indutância de 0.5A até 128A, ao passo de uma corrente o dobro da anterior.
Além disso, tem os daods de Ld e Lq em função da corrente *Ia* assim como a diferença entre eles e a razão de saliência.

## Levantamento de Torques

Nesta pasta está as curvas de torque extraídas do FEMM (Curvas_de_Torque_M-36).
Dividindo essas curvas por suas respectivas médias foi obtido as curvas de torque oscilante (Curvas_de_Torque_ripple_M-36).
Há as curvas de torque médio teórico, calculadas utilzando os valores de indutância da pasta **Levantamento das Indutâncias da Máquina**.
E para as cuvas do torque médio simulado, foi efetuada a média das curvas de torque para múltiplos valores de corrente e combinados em um csv.

## Levantamento dos vetores de campo magnético espaciais

Essa pasta contém medições de campo no entreferro da máquina.
Há curvas de fluxo e intensidade de campo para múltiplas correntes.
Isso foi feito diretamente no FEMM, **ainda** não há script para essa metodologia.  
Também há um arquivo com a medição do campo no entreferro para múltiplas correntes, medições em um único ponto do entreferro. 

## Outros

Esta pasta contém alguns dados extras, como as curvas do M-36  para corrente na BObina *Ia* e também para corrente trifásica.
Também há alguns GIF's que ilustram o comportamento do rotor.

## Tensão Induzida

A curva de tensão induzida foi feita manualmente. Devido à metodologia do estudo, não foi possível utilizar a tensão induzida que o próprio FEMM fornece.
Foram pegos os dados de fluxo concatenado e derivados de forma discretizada, ou seja, \frac{E[k]-E[k-1]}{$\delta$ t}. 