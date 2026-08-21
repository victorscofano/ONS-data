
/*
    Para cada subsistema e dia, compare
    a carga registrada em carga_diaria
    com a soma das leituras de carga
    em balanco_consolidado.

    classifique como "divergente" qualquer
    dia que a diferença absoluta
    ultrapasse 5% do valor de carga_diaria


*/

WITH cargaBalancoPorDia AS (
    SELECT
            id_subsistema,
            strftime('%Y-%m-%d', din_instante) AS dia,
            avg(val_carga) AS mediaCargaBalanco
                
    FROM balanco_consolidado
    WHERE id_subsistema != 'SIN'
    GROUP BY id_subsistema, dia
),

tb_join AS (
    SELECT
        t1.dia AS dia,
        t1.id_subsistema,
        mediaCargaBalanco,
        val_cargaenergiamwmed
    FROM cargaBalancoPorDia AS t1

    LEFT JOIN carga_consolidada AS t2
    ON t1.id_subsistema = t2.id_subsistema
    AND t1.dia = t2.din_instante
),

tb_diferencas AS (

    SELECT
            dia,
            id_subsistema,
            abs((mediaCargaBalanco - val_cargaenergiamwmed) *100.0 / val_cargaenergiamwmed) AS difAbsoluta,
            CASE
                WHEN abs((mediaCargaBalanco - val_cargaenergiamwmed) *100.0 / val_cargaenergiamwmed) > 5 THEN 'Divergente'
                ELSE 'Normal'
            END AS classificacao
    FROM tb_join

)


SELECT 
        id_subsistema,
        dia,
        round(difAbsoluta, 13) AS dif_absoluta,
        classificacao

FROM tb_diferencas

WHERE dif_absoluta ISNULL
ORDER BY difAbsoluta DESC
