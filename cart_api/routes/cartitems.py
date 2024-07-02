import falcon
from playhouse.shortcuts import model_to_dict
from cart_api.database import DatabaseCartItem


# Exercise 3:
# Using the database model you created in Exercise 1 create a cartitems route
# CartItems should have a responder for POST and GET
# CartItem should have responders for GET DELETE PATCH
# Your API response statuses and bodies should conform to your OpenAPI spec


class CartItems:
    def on_post(self, req, resp):
        obj = req.get_media()
        product = DatabaseCartItem( 
            name = obj['name'],
            price= obj['price'],
            quantity = obj['quantity'],
        )
        product.save()
        resp.media = model_to_dict(product)
        resp.status = falcon.HTTP_201
    def on_get(self, req, resp):
        resp.media = [model_to_dict(item) for item in DatabaseCartItem.select()]
        resp.status = falcon.HTTP_200

class CartItem:
    def on_get(self, req, resp, product_id):
        product = DatabaseCartItem.get(id=product_id)
        resp.media = model_to_dict(product)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, product_id):
        DatabaseCartItem.delete_by_id(product_id)
        resp.status = falcon.HTTP_204
    
    def on_patch(self, req, resp, product_id):
        val = model_to_dict(req.get_media())['quantity']
        new = DatabaseCartItem.update(quantity=val).where(id=product_id)
        new.save()
        resp.status = falcon.HTTP_204
