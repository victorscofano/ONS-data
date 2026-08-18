-- para cada subsistema, identifique a data de maior carga registrada.

SELECT 
        nom_subsistema AS subsistema,
        din_instante AS data,
        round(max(val_cargaenergiamwmed), 2) AS maximoCarga

FROM carga_consolidada

GROUP BY nom_subsistema
ORDER BY maximoCarga DESC
