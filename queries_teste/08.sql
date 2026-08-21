/*

=> ENA
    na_bruta_regiao_percentualmlt — 
    energia natural afluente total (toda a água que passa pelos rios), 
    como % da média de longo termo (MLT)

    ena_armazenavel_regiao_percentualmlt — 
    só a parcela que pode ser armazenada nos reservatórios 
    (desconta a "fio d'água", que passa direto pelas usinas sem represar)

    Pra correlacionar com nível de reservatório, 
    ena_armazenavel_regiao_percentualmlt é a escolha certa —
    é literalmente a água que vira ENA armazenável, ou seja, a que 
    fisicamente pode elevar o EAR. 
    A "bruta" mistura água que nunca chega a encher reservatório, então dilui a correlação
-----------------------------------------------------------------------------------------------
=> EAR
ear_verif_subsistema_percentual — 
já normalizado como % da capacidade máxima daquele subsistema

Isso é importante porque ear_verif_subsistema_mwmes e ear_max_subsistema 
têm escalas totalmente diferentes entre subsistemas 
(Sudeste é muito maior que Sul, por exemplo) — 
comparar os percentuais é o que permite colocar os 4 subsistemas no mesmo 
gráfico sem um dominar visualmente o outro.

------------------------------------------------------------------------------------------
Comparação final:

ena_armazenavel_regiao_percentualmlt  (ENA armazenável, % da MLT)
        vs
ear_verif_subsistema_percentual        (EAR, % da capacidade máxima)
*/

SELECT
    t1.id_subsistema,
    ena_armazenavel_regiao_percentualmlt,
    ear_verif_subsistema_percentual

FROM ear_consolidado AS t1
LEFT JOIN ena_consolidado AS t2
ON t1.id_subsistema = t2.id_subsistema
AND t1.ear_data = t2.ena_data