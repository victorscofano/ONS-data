WITH
janela_cmo AS (
    SELECT
        t1.*,
        LEAD(t1.din_instante) OVER (
            PARTITION BY t1.id_subsistema ORDER BY t1.din_instante
        ) AS fim_semana
    FROM cmo_consolidado AS t1
),
ear_semanal AS (
    SELECT
        t1.id_subsistema,
        t1.din_instante,
        round(avg(t2.ear_verif_subsistema_percentual), 2) AS ear_media_semana
    FROM janela_cmo AS t1
    LEFT JOIN ear_consolidado AS t2
        ON t2.id_subsistema = t1.id_subsistema
        AND t2.ear_data >= t1.din_instante
        AND (t1.fim_semana IS NULL OR t2.ear_data < t1.fim_semana)
    GROUP BY t1.id_subsistema, t1.din_instante
),
ena_semanal AS (
    SELECT
        t1.id_subsistema,
        t1.din_instante,
        round(avg(t2.ena_armazenavel_regiao_percentualmlt), 2) AS ena_media_semana
    FROM janela_cmo AS t1
    LEFT JOIN ena_consolidado AS t2
        ON t2.id_subsistema = t1.id_subsistema
        AND t2.ena_data >= t1.din_instante
        AND (t1.fim_semana IS NULL OR t2.ena_data < t1.fim_semana)
    GROUP BY t1.id_subsistema, t1.din_instante
),
intercambio_sinalizado AS (
    SELECT
        t1.din_instante,
        CASE WHEN t1.val_intercambiomwmed >= 0 THEN t1.nom_subsistema_origem ELSE t1.nom_subsistema_destino END AS nom_subsistema,
        abs(t1.val_intercambiomwmed) AS saldo
    FROM intercambio_consolidado AS t1
    UNION ALL
    SELECT
        t1.din_instante,
        CASE WHEN t1.val_intercambiomwmed >= 0 THEN t1.nom_subsistema_destino ELSE t1.nom_subsistema_origem END AS nom_subsistema,
        -abs(t1.val_intercambiomwmed) AS saldo
    FROM intercambio_consolidado AS t1
),
intercambio_semanal AS (
    SELECT
        t2.id_subsistema,
        t2.din_instante,
        round(sum(t1.saldo), 2) AS saldo_intercambio_semana
    FROM intercambio_sinalizado AS t1
    JOIN janela_cmo AS t2
        ON t2.nom_subsistema = t1.nom_subsistema
        AND t1.din_instante >= t2.din_instante
        AND (t2.fim_semana IS NULL OR t1.din_instante < t2.fim_semana)
    GROUP BY t2.id_subsistema, t2.din_instante
)
SELECT
    t1.id_subsistema,
    t1.nom_subsistema,
    t1.din_instante,
    t1.val_cmomediasemanal,
    t1.val_cmoleve,
    t1.val_cmomedia,
    t1.val_cmopesada,
    t2.ear_media_semana,
    t3.ena_media_semana,
    t4.saldo_intercambio_semana
FROM janela_cmo AS t1
LEFT JOIN ear_semanal AS t2
    ON t2.id_subsistema = t1.id_subsistema AND t2.din_instante = t1.din_instante
LEFT JOIN ena_semanal AS t3
    ON t3.id_subsistema = t1.id_subsistema AND t3.din_instante = t1.din_instante
LEFT JOIN intercambio_semanal AS t4
    ON t4.id_subsistema = t1.id_subsistema AND t4.din_instante = t1.din_instante
ORDER BY t1.id_subsistema, t1.din_instante;