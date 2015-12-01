import web
import pymysql

def getDB():
    db = web.database(dbn='mysql', user='root', pw='toor', db='goodview')
    return db

urls = (
        '/', 'index',
        '/giverating', 'giverating',
        '/getrating', 'getrating',
        '/rate', 'rate',
        '/addlist', 'addlist',
       )

render = web.template.render('templates/', base='layout')

class giverating:
    def GET(self):
        data = web.input()
        item = data.item
        rate = data.rate
        ratetype = data.ratetype
        db = getDB()
        db.insert('rating', item=int(item), rate=int(rate), ratetype=int(ratetype))
        raise web.accepted()

class getrating:
    def GET(self):
        data = web.input()
        item = data.item
        db = getDB()
        db.insert('rating', item=int(item), rate=int(rate), ratetype=int(ratetype))
        raise web.accepted()

class rate:
    def GET(self):
        data = web.input()
        itemkey = data.item

        db = getDB()
        result = list(db.select('item', {'imgpath': itemkey}, where='imgpath=$imgpath'))
        if len(result) == 0:
            raise web.notfound()
            
        result = result[0]
        abspath = u'http://7xoro6.com1.z0.glb.clouddn.com/%s' % result['imgpath']

        return render.imageandform(result)

class addlist:
    def GET(self):
        return
        with open('bigben.txt', 'r') as fp:
            firstline = fp.readline()
            name = firstline.strip()

            db = getDB()
            cid = db.insert('category', categoryname=name)
            
            for line in fp:
                imgpath = line.strip().split()[0]
                db.insert('item', imgpath=imgpath.strip(), category=cid)



class index:
        
    def GET(self):
        return ''

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
        


app = web.application(urls, globals())
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
