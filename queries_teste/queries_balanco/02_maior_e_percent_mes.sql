
/*
    Para cada subsistema, identifique o mês com a maior participação
    percentual da geração eólica sobre o total gerado e o mês com menor.
*/

SELECT
        nom_subsistema,
        mes,
        percentEolicaMes
FROM (
    SELECT
            row_number() OVER (
            PARTITION BY nom_subsistema ORDER BY percentEolicaMes DESC) AS topoPercentMaior,
            row_number() OVER (
            PARTITION BY nom_subsistema ORDER BY percentEolicaMes) AS topoPercentMenor,
            nom_subsistema,
            mes,
            percentEolicaMes
    FROM (

        SELECT
                nom_subsistema,
                mes,
                round((totalEolicaMes * 100.0 / NULLIF(totalGeradoMes, 0)), 2) AS percentEolicaMes
        FROM (
        
            SELECT
                    nom_subsistema,
                    strftime('%Y-%m', din_instante) AS mes,
                    sum(val_gereolica) AS totalEolicaMes,
                    sum(totalGerado) AS totalGeradoMes
            FROM (
                SELECT
                        nom_subsistema,
                        din_instante,
                        val_gereolica,
                        val_gerhidraulica + val_gereolica + val_gersolar + val_gertermica AS totalGerado
                FROM balanco_consolidado
                WHERE val_gerhidraulica IS NOT NULL
                AND val_gereolica IS NOT NULL
                AND val_gersolar IS NOT NULL
                AND val_gertermica IS NOT NULL
            )
            GROUP BY nom_subsistema, mes
        )
    )
)

WHERE topoPercentMaior = 1
OR topoPercentMenor = 1

/*
    a lógica é começar pelo mais interno e ir subindo de camada/nível,
    atentando ao que eu quero exportar para a camada mais acima

*/