"""Module for generating most expensive products report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def expensive_products(request):
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
            WHERE bp.price >= 1000.00
            ORDER BY bp.price ASC;
            """)

            dataset = db_cursor.fetchall()

            expensive_products = {}

            for row in dataset:
                pid = row["id"]

                expensive_products[pid] = {}
                expensive_products[pid]["id"] = pid
                expensive_products[pid]["name"] = row["name"]
                expensive_products[pid]["price"] = row["price"]
                expensive_products[pid]["description"] = row["description"]

        list_of_expensive_products = expensive_products.values()

        template = 'users/list_of_expensive_products.html'
        context = {
            'expensive_products': list_of_expensive_products
        }

        return render(request, template, context)