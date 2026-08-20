-- Para cada subsistema, calcule o percentual médio de participação
-- de cada fonte de geração de energia sobre o total gerado

/*
    QUERY 1: PERCENTUAL MÉDIO DIÁRIO DE PARTICIPAÇÃO DE CADA FONTE

    QUERY 2: PERCENTUAL TOTAL (OU PARTICIPAÇÃO TOTAL) NO PERÍODO
    é matematicamente equivalente a uma média ponderada das razoes diárias,
    usando o totalGerado de cada dia como peso
*/
SELECT
        nom_subsistema AS subsistema,
        round(avg(val_gerhidraulica * 100.0 / NULLIF(totalGerado, 0)), 2) AS percent_hidraulica,
        round(avg(val_gertermica * 100.0 / NULLIF(totalGerado, 0)), 2) AS percent_terminca,
        round(avg(val_gereolica * 100.0 / NULLIF(totalGerado, 0)), 2) AS percent_eolica,
        round(avg(val_gersolar * 100.0 / NULLIF(totalGerado, 0)), 2) AS percent_solar
FROM (
    SELECT
            nom_subsistema,
            val_gerhidraulica,
            val_gertermica,
            val_gereolica,
            val_gersolar,
            val_gerhidraulica + val_gertermica + val_gereolica + val_gersolar AS totalGerado
    FROM balanco_consolidado
    WHERE val_gerhidraulica
    AND val_gertermica
    AND val_gereolica
    AND val_gersolar
)
GROUP BY subsistema
ORDER BY subsistema;

-- SELECT
--     nom_subsistema,
--     round(sum(val_gerhidraulica) * 100.0 / sum(totalGerado), 2) AS "participHidraulica(%)",
--     round(sum(val_gertermica) * 100.0 / sum(totalGerado), 2) AS "participTermica(%)",
--     round(sum(val_gereolica) * 100.0 / sum(totalGerado), 2) AS "participEolica(%)",
--     round(sum(val_gersolar) * 100.0 / sum(totalGerado), 2) AS "participSolar(%)"
-- FROM (
--     SELECT
--         nom_subsistema,
--         val_gerhidraulica,
--         val_gertermica,
--         val_gereolica,
--         val_gersolar,
--         val_gerhidraulica + val_gertermica + val_gereolica + val_gersolar AS totalGerado
--     FROM balanco_consolidado
--     WHERE val_gerhidraulica IS NOT NULL
--       AND val_gertermica   IS NOT NULL
--       AND val_gereolica    IS NOT NULL
--       AND val_gersolar     IS NOT NULL
-- )
-- GROUP BY nom_subsistema
-- ORDER BY nom_subsistema;