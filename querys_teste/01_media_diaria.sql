-- para cada subsistema, calcule a carga média(MWmed)
-- considerando todo o período carregado na tabela


SELECT 
        nom_subsistema AS subsistema,
        round(avg(val_cargaenergiamwmed), 2) AS mediaDeCarga
FROM carga_consolidada

GROUP BY nom_subsistema
