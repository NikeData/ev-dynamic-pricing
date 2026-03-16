DROP TABLE IF EXISTS charging_sessions;
CREATE TABLE charging_sessions (
    session_id SERIAL PRIMARY KEY,
    datetime TIMESTAMP NOT NULL,
    hour INT NOT NULL,
    day_of_week INT NOT NULL,
    is_weekend INT NOT NULL,
    temperature DECIMAL(5,2),
    wholesale_price DECIMAL(6,4) NOT NULL,
	retail_price DECIMAL(6,4) NOT NULL,	
	charging_sessions INT NOT NULL,
	energy_per_session DECIMAL(10,2) NOT NULL,
    energy_sold_kwh DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from charging_sessions;

DROP TABLE IF EXISTS static_pricing;
CREATE TABLE static_pricing (
    session_id INTEGER REFERENCES charging_sessions(session_id), 
    static_markup_percent DECIMAL(5,2) DEFAULT 0.25,
    static_retail_price DECIMAL(6,4),
    static_revenue DECIMAL(12,2),
	static_cost DECIMAL(6,4),
    static_profit DECIMAL(12,2)
);

DROP TABLE IF EXISTS dynamic_pricing;
CREATE TABLE dynamic_pricing (
    session_id INTEGER REFERENCES charging_sessions(session_id), 
    dynamic_price DECIMAL(6,4),
    predicted_energy_sold_kwh DECIMAL(10,2),
    "Adjusted_demand_kwh" DECIMAL(10,2),
    dynamic_revenue DECIMAL(12,2),
    dynamic_profit DECIMAL(12,2)
);

--For powerbi dashboard
CREATE VIEW pricing_comparison AS
SELECT
    c.datetime,
    c.hour,
    c.day_of_week,
    c.temperature,
    c.wholesale_price,
    s.static_retail_price,
    s.static_profit,
	d.predicted_energy_sold_kwh,
	d.Adjusted_demand_kwh,
    d.dynamic_price,
    d.dynamic_profit
FROM charging_sessions c
JOIN static_pricing s
ON c.session_id = s.session_ID
JOIN dynamic_pricing d
ON c.session_id = d.session_id;



