-- Para cada subsistema, compare a carga média em dias úteis
-- contra a carga média em fins de semana

SELECT
        nom_subsistema AS subsistema,
        round(avg(CASE 
                WHEN strftime('%w', din_instante) BETWEEN '1' AND '5' THEN val_cargaenergiamwmed
             END
        ), 2) AS dia_util,
        round(avg(CASE 
                WHEN strftime('%w', din_instante) IN ('0', '6') THEN val_cargaenergiamwmed
             END
        ), 2) AS fim_de_semana

FROM carga_consolidada

GROUP BY nom_subsistema
