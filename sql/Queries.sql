--peak hour demand
SELECT
    hour,
    AVG(energy_sold_kwh) AS avg_demand
FROM charging_sessions
WHERE hour BETWEEN 7 AND 9
   OR hour BETWEEN 17 AND 21
GROUP BY hour
ORDER BY hour;

--Daily demand trend
SELECT
    DATE(datetime) AS day,
    SUM(energy_sold_kwh) AS total_energy_sold
FROM charging_sessions
GROUP BY day
ORDER BY day;

--Revenue Comparison

SELECT
    SUM(static_revenue) AS total_static_revenue,
    SUM(dynamic_revenue) AS total_dynamic_revenue
FROM static_pricing
JOIN dynamic_pricing
ON static_pricing.session_id = dynamic_pricing.session_id;

-- profit uplift
SELECT
    SUM(dynamic_profit) - SUM(static_profit) AS profit_difference
FROM static_pricing
JOIN dynamic_pricing
ON static_pricing.session_id = dynamic_pricing.session_id;


--hourly charging behaviour
SELECT
    hour,
    AVG(charging_sessions) AS avg_sessions,
    AVG(energy_sold_kwh) AS avg_energy
FROM charging_sessions
GROUP BY hour
ORDER BY hour;