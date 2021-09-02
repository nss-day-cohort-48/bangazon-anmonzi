"""Module for generating most expensive products report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def incomplete_orders(request):
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
            """)

            dataset = db_cursor.fetchall()

            incomplete_orders = {}

            for row in dataset:
                oid = row["order_id"]

                incomplete_orders[oid] = {}
                incomplete_orders[oid]["order_id"] = oid
                incomplete_orders[oid]["full_name"] = row["full_name"]
                incomplete_orders[oid]["order_total"] = row["order_total"]
                incomplete_orders[oid]["num_items"] = row["num_items"]

        list_of_incomplete_orders = incomplete_orders.values()

        template = 'users/list_of_incomplete_orders.html'
        context = {
            'incomplete_orders': list_of_incomplete_orders
        }

        return render(request, template, context)