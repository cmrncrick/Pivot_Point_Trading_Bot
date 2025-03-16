from datetime import time

QUERY = """
SELECT 
    MAX(High) AS Max_High,
    MIN(Low) AS Min_Low,
    (SELECT Close FROM ES_15m ORDER BY Datetime DESC LIMIT 1) AS Recent_Close
FROM 
    ES_15m
WHERE 
    Datetime >= datetime('now', '-4 days');
"""

TICKER = "ES=F"

INTERVAL_15M = "15m"

LOOKBACK_PERIOD = 4

MARKET_OPEN = time(8, 30)

MARKET_CLOSE = time(15, 00)
