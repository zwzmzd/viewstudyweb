import web
import pymysql

urls = (
        '/', 'index',
        '/login', 'login',
        '/foods', 'foods',
        '/carts', 'carts',
        '/orders', 'orders',
        '/admin/orders', 'admin_orders',
       )

class index:
    def GET(self):
        return "Hello, world!"

class login:
    def POST(self):
        data = web.input()
        username = data.username
        password = data.password
        print username
        print password
        return username + password

class foods:
    def GET(self):
        access_token = web.input().access_token
        return None

class carts:
    def POST(self):
        data = web.input()
        access_token = data.access_token
        return None

    def PATCH(self):
        data = web.input()
        access_token = data.access_token
        return None

class orders:
    def POST(self):
        data = web.input()
        access_token = data.access_token
        cart_id = data.cart_id
        return None

class admin_orders:
    def GET(self):
        data = web.input()
        access_token = data.access_token
        return None
        


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
