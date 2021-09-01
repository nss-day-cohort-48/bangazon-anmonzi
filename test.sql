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