WITH customer_metrics AS (
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        COALESCE(SUM(o.total_amount), 0) AS total_order_spend,
        COUNT(o.order_id) AS order_count,
        MIN(o.order_date) AS first_purchase_date
    FROM customers AS c
    LEFT JOIN orders AS o
        ON o.customer_id = c.customer_id
    GROUP BY
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email
),
ranked_customers AS (
    SELECT
        customer_metrics.*,
        NTILE(3) OVER (
            ORDER BY total_order_spend DESC, customer_id
        ) AS spend_tier
    FROM customer_metrics
)
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    total_order_spend,
    order_count,
    first_purchase_date,
    CASE spend_tier
        WHEN 1 THEN 'High'
        WHEN 2 THEN 'Medium'
        ELSE 'Low'
    END AS value_tier
FROM ranked_customers
ORDER BY total_order_spend DESC, customer_id;