-- Calcule a carga média mensal por subsistema para todo o período possível

SELECT 
        nom_subsistema,
        strftime('%Y-%m', din_instante) AS mes,
        round(avg(val_cargaenergiamwmed), 2) AS mediaMensal
FROM carga_consolidada
GROUP BY mes, nom_subsistema
ORDER BY nom_subsistema ASC, din_instante ASC;
