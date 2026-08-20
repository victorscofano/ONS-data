-- para cada subsistema, identifique a data de maior carga registrada.

SELECT 
        nom_subsistema AS subsistema,
        din_instante AS data,
        round(max(val_cargaenergiamwmed), 2) AS maximo_carga

FROM carga_consolidada

GROUP BY nom_subsistema
ORDER BY maximo_carga DESC
