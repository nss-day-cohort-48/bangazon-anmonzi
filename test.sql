SELECT 
    bp.price,
    bp.name
FROM 
    bangazonapi_product AS bp
WHERE bp.price >= 1000.00
ORDER BY bp.price ASC;


SELECT 
bp.price,
bp.name,
bp.description,
bp.id
FROM 
bangazonapi_product AS bp
WHERE bp.price <= 999.00
ORDER BY bp.price DESC;


SELECT 
    bo.id AS order_id,
    user.first_name || ' ' || user.last_name AS full_name,
    bp.merchant_name AS payment_type,
    SUM(product.price) AS total_price
FROM 
    bangazonapi_order AS bo
JOIN
    bangazonapi_customer AS bc
    ON bo.customer_id = bc.id
JOIN 
    auth_user AS user
    ON bc.user_id = user.id
JOIN 
    bangazonapi_payment AS bp
    ON bo.payment_type_id = bp.id
JOIN 
    bangazonapi_orderproduct AS bop
    ON bo.id = bop.order_id
JOIN 
    bangazonapi_product AS product
    ON bop.product_id = product.id
WHERE bo.payment_type_id IS NOT NULL
GROUP BY bo.id;



SELECT
    bo.id AS order_id,
    user.first_name || ' ' || user.last_name AS full_name,
    sum(bp.price) AS order_total,
    count(bop.id) AS num_items
FROM 
    bangazonapi_order AS bo
JOIN 
    bangazonapi_customer AS bc 
    ON bc.id = bo.customer_id
JOIN 
    auth_user AS user 
    ON user.id = bc.user_id
JOIN bangazonapi_orderproduct AS bop 
    ON bop.order_id = bo.id
JOIN bangazonapi_product AS bp 
    ON bop.product_id = bp.id
WHERE bo.payment_type_id IS NULL
GROUP BY order_id;