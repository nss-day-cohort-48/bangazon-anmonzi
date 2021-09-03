import json
from rest_framework import status
from bangazonapi.models import Order, Customer
from rest_framework.test import APITestCase


class OrderTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "address": "100 Infinity Way", "phone_number": "555-1212", "first_name": "Steve", "last_name": "Brownlee"}
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a product category
        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        # Create a product
        url = "/products"
        data = { "name": "Kite", "price": 14.99, "quantity": 60, "description": "It flies high", "category_id": 1, "location": "Pittsburgh" }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a payment type
        url = "/paymenttypes"
        data = {"merchant_name": "Visa", "account_number": "000000000000", "expiration_date": "2020-01-01", "create_date": "2019-11-11"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.payment_type_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_add_product_to_order(self):
        """
        Ensure we can add a product to an order.
        """
        # Add product to order
        url = "/cart"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was added
        url = "/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["size"], 1)
        self.assertEqual(len(json_response["lineitems"]), 1)


    def test_remove_product_from_order(self):
        """
        Ensure we can remove a product from an order.
        """
        # Add product
        self.test_add_product_to_order()

        # Remove product from cart
        url = "/cart/1"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was removed
        url = "/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["size"], 0)
        self.assertEqual(len(json_response["lineitems"]), 0)

    # TODO: Complete order by adding payment type
    def test_update_order_with_payment(self):
        """
        Ensure we can update an order with payment information to complete
        """
        # Seed database with an order
        order = Order()
        # order.customer =
        order.created_date = "2018-04-12"
        order.save()

        # Define new properties for order
        data = {
            "customer_id": 1,
            "created_date": "2019-04-12",
            "payment_type_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/orders/{order.id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify payment was added
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f"/orders/{order.id}", None, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["customer_id"], 1)
        self.assertEqual(json_response["created_date"], "2019-04-12")
        self.assertEqual(json_response["payment_type_id"], 1)
        

    # TODO: New line item is not added to closed order