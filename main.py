# -*-coding:utf-8-*-
import web
import hashlib
import random
from web import form
import urllib
import setting

web.config.debug = setting.debug

def getDB():
    db = web.database(dbn='mysql', 
                      host=setting.DB['host'],
                      port=int(setting.DB['port']),
                      user=setting.DB['user'], 
                      pw=setting.DB['password'],
                      db=setting.DB['name'])
    return db


def login_required(func):
    def __func(self, *args, **kwargs):
        if session.get('userid') is None:
            raise web.seeother('/?url=%s' % urllib.quote(web.ctx.fullpath)) 
        kwargs['userid'] = session.get('userid')
        return func(self, *args, **kwargs)
    return __func


urls = (
        '/', 'index',
        '/new', 'new',
        '/giverating', 'giverating',
        '/rate', 'rate',
        '/addlist', 'addlist',
        '/dump/(.*)', 'dump',
        '/todo/(.*)', 'todo',
       )

class todo:
    @login_required
    def GET(self, category, userid):
        db = getDB()
        r = list(db.query('''
SELECT *
FROM item
WHERE category = $category
AND id NOT
IN (
 
SELECT item.id
FROM  `rating` ,  `item`
WHERE rating.usertoken = $usertoken
AND item.id = rating.item
)
ORDER BY imgpath''',
            vars={'usertoken': session.usertoken, 'category': int(category)}))
        return render.todo(r)


class dump:
    '''获得标定数据'''
    def GET(self, usertoken):
        buf = []

        db = getDB()
        r = list(db.query('''
SELECT item.imgpath, rating.rate
FROM  `rating` ,  `item`
WHERE rating.usertoken = $usertoken
AND item.id = rating.item
ORDER BY item.imgpath''', 
            vars={'usertoken': usertoken}))

        for case in r:
            buf.append(case['imgpath'])
            buf.append('-1' if case['rate'] < 3 else '1')

        return u'\n'.join(buf)


class giverating:
    @login_required
    def POST(self, userid):
        data = web.input()
        item = data.item
        rate = data.rate
        ratetype = data.ratetype

        db = getDB()

        r = list(db.select('item', {'imgpath': item}, where='imgpath=$imgpath'))
        if len(r) == 0:
            raise web.notfound()

        # 尝试更新老的标记
        affected = db.update('rating', 
                  vars=dict(item=r[0]['id'], ratetype=int(ratetype), usertoken=session.usertoken), 
                  where='usertoken=$usertoken and item=$item and ratetype=$ratetype', 
                  rate=int(rate))
        if affected == 0:
            db.insert('rating', item=r[0]['id'], rate=int(rate), ratetype=int(ratetype), usertoken=session.usertoken)
        raise web.accepted()


class rate:
    @login_required
    def GET(self, userid):
        data = web.input()
        itemkey = data.item

        db = getDB()
        result = list(db.select('item', {'imgpath': itemkey}, where='imgpath=$imgpath'))
        if len(result) == 0:
            raise web.notfound()
        result = None if len(result) == 0 else result[0]

        old_rating = list(db.select('rating', 
                  dict(item=result['id'], ratetype=setting.ratetype, usertoken=session.usertoken), 
                  where='usertoken=$usertoken and item=$item and ratetype=$ratetype'))
        old_rating = None if len(old_rating) == 0 else old_rating[0]


        a = list(db.query('select * from item where imgpath=(select min(imgpath) from item where imgpath >$imgpath and category=$category)', vars={'imgpath': result['imgpath'], 'category':result['category']}))
        b = list(db.query('select * from item where imgpath=(select max(imgpath) from item where imgpath <$imgpath and category=$category)', vars={'imgpath': result['imgpath'], 'category':result['category']}))
        pre = None if len(b) == 0 else b[0]
        next = None if len(a) == 0 else a[0]


        if old_rating is None:
            rating_form = form.Form(
                form.Radio('rate', ['1', '2', '3', '4', '5']),
            )
        else:
            # 如果之前已经标定了
            rating_form = form.Form(
                form.Radio('rate', ['1', '2', '3', '4', '5'], value=str(old_rating.rate)),
            )
        return render.imageandform(result, rating_form, pre, next)


class addlist:
    def GET(self):
        raise web.forbidden()
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
        session.pop('userid', None)
        return render.index()

    def POST(self):
        data = web.input()
        token = data.get('token')
        if token == setting.entry_token:
            # 新用户
            session['granted'] = True
            raise web.seeother('/new')
        else:
            db = getDB()
            r = list(db.select('webuser', {'usertoken': token}, where='usertoken=$usertoken'))
            if len(r) == 0:
                raise web.forbidden()
            else:
                # 老用户登录
                session['userid'] = r[0]['id']
                session['usertoken'] = r[0]['usertoken']
                session['username'] = r[0]['username']

                prev_url = data.get('url')
                if prev_url: # 用户从其它页面跳转而来
                    raise web.seeother(prev_url)
                else:
                    last = list(db.query('select max(imgpath) from item where id in (select item from rating where usertoken=$usertoken)', {'usertoken': r[0]['usertoken']}))
                    lastimg = last[0]['max(imgpath)'] if len(last) > 0 else None
                    return render.welcome(r[0]['username'], r[0]['usertoken'], lastimg)

class new:
    def GET(self):
        if session.get('granted') is None or session.get('userid') is not None:
            raise web.forbidden()
        return render.new()

    def POST(self):
        if session.get('granted') is None or session.get('userid') is not None:
            raise web.forbidden()

        username = web.input().username
        usertoken = hashlib.sha224(str(random.getrandbits(128))).hexdigest()[:8]
        db = getDB()
        uid = db.insert('webuser', username=username, usertoken=usertoken)

        session['userid'] = uid
        session['usertoken'] = usertoken
        session['username'] = username

        session.pop('granted', None)
        return render.welcome(username, usertoken, None)

        
        
app = web.application(urls, globals())
if web.config.get('_session') is None:
    db = getDB()
    session = web.session.Session(app, web.session.DBStore(db, 'sessions'), {'count': 0})
    web.config._session = session
else:
    session = web.config._session
render = web.template.render('templates/', base='layout', globals={'context': session})

if __name__ == "__main__":
    app.run()
