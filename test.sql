SELECT 
    bp.price,
    bp.name
FROM 
    bangazonapi_product AS bp
WHERE bp.price >= 1000.00
ORDER BY bp.price ASC;


