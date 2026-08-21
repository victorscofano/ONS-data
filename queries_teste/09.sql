/*

valores positivos: exporta energia para o outro
valores negativos: importa energia do outro

Quais subsistemas mais "exportam" e mais "importam" 
energia via intercâmbio, 
e como isso mudou entre 2023-2025.

*/


SELECT
        strftime('%Y', date(din_instante)) AS ano,
        CASE
            WHEN val_intercambiomwmed >= 0 THEN nom_subsistema_origem
            ELSE nom_subsistema_destino
        END AS exportador,
        CASE
            WHEN val_intercambiomwmed >= 0 THEN nom_subsistema_destino
            ELSE nom_subsistema_origem
        END AS importador,
        round(sum(abs(val_intercambiomwmed)), 2) AS valor
FROM intercambio_consolidado
GROUP BY ano, exportador, importador
ORDER BY ano, valor DESC;