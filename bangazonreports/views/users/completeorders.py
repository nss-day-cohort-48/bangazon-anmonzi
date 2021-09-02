"""Module for generating most expensive products report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def complete_orders(request):
    """Function to build an HTML report of most expensive products"""
    if request.method == 'GET':
        # Connect to database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # SQL Query
            db_cursor.execute("""
            SELECT 
                bo.id AS order_id,
                user.first_name || ' ' || user.last_name AS full_name,
                bp.merchant_name AS payment_type,
                SUM(product.price) AS total_price,
                count(bop.id) AS num_items
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
            """)

            dataset = db_cursor.fetchall()

            complete_orders = {}

            for row in dataset:
                oid = row["order_id"]

                complete_orders[oid] = {}
                complete_orders[oid]["order_id"] = oid
                complete_orders[oid]["full_name"] = row["full_name"]
                complete_orders[oid]["payment_type"] = row["payment_type"]
                complete_orders[oid]["total_price"] = row["total_price"]
                complete_orders[oid]["num_items"] = row["num_items"]

        list_of_complete_orders = complete_orders.values()

        template = 'users/list_of_complete_orders.html'
        context = {
            'complete_orders': list_of_complete_orders
        }

        return render(request, template, context)