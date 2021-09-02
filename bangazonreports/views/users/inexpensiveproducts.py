"""Module for generating most expensive products report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def inexpensive_products(request):
    """Function to build an HTML report of most expensive products"""
    if request.method == 'GET':
        # Connect to database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # SQL Query
            db_cursor.execute("""
            SELECT 
                bp.price,
                bp.name,
                bp.description,
                bp.id
            FROM 
                bangazonapi_product AS bp
            WHERE bp.price <= 999.00
            ORDER BY bp.price DESC;
            """)

            dataset = db_cursor.fetchall()

            inexpensive_products = {}

            for row in dataset:
                pid = row["id"]

                inexpensive_products[pid] = {}
                inexpensive_products[pid]["id"] = pid
                inexpensive_products[pid]["name"] = row["name"]
                inexpensive_products[pid]["price"] = row["price"]
                inexpensive_products[pid]["description"] = row["description"]

        list_of_inexpensive_products = inexpensive_products.values()

        template = 'users/list_of_inexpensive_products.html'
        context = {
            'inexpensive_products': list_of_inexpensive_products
        }

        return render(request, template, context)