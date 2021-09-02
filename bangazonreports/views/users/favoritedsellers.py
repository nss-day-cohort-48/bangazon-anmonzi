"""Module for generating most expensive products report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Favorite
from bangazonreports.views import Connection


def favorited_sellers_by_customer_list(request):
    """Function to build an HTML report of most expensive products"""
    if request.method == 'GET':
        # Connect to database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # SQL Query
            db_cursor.execute("""
            SELECT
                bf.customer_id,
                bf.seller_id,
                u.id user_id,
                user.first_name || ' ' || user.last_name AS customer_name,
                u.first_name || ' ' || u.last_name AS seller_name
            FROM bangazonapi_favorite AS bf
            JOIN 
                bangazonapi_customer AS bc
                ON bf.customer_id = bc.id
            JOIN
                auth_user AS user
                ON bc.user_id = user.id
            JOIN 
                bangazonapi_customer AS bcc
                ON bf.seller_id = bcc.id
            JOIN
                auth_user AS u
                ON bcc.user_id = u.id;
            """)

            dataset = db_cursor.fetchall()

            favorites_by_user = {}

            for row in dataset:
                favorite = Favorite()
                favorite.customer_id = row["customer_id"]
                favorite.seller_id = row["seller_id"]

                uid = row["user_id"]

                if uid in favorites_by_user:
                    favorites_by_user[uid]['favorites'].append(favorite)

                else:
                    favorites_by_user[uid] = {}
                    favorites_by_user[uid]["id"] = uid
                    favorites_by_user[uid]["full_name"] = row["customer_name"]
                    favorites_by_user[uid]["favorites"] = [favorite]

        list_of_favorites_by_user = favorites_by_user.values()

        template = 'users/list_of_favorites_by_user.html'
        context = {
            'favorites_by_user': list_of_favorites_by_user
        }

        return render(request, template, context)

