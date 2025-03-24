from aiohttp import web
import time
import json
import base64
import pickle
import time
import aiomysql
from settings import config, messages


async def mysql_init(app):
    mysql_conf = app['config']['mysql']
    while True:
        try:
            mysql_pool = await aiomysql.create_pool(host=mysql_conf['host'],
                                                    port=mysql_conf['port'],
                                                    user=mysql_conf['user'],
                                                    password=mysql_conf['password'],
                                                    db=mysql_conf['db'])
            break
        except:
            time.sleep(5)
    app.on_shutdown.append(mysql_close)
    app['mysql_pool'] = mysql_pool
    return app


async def mysql_close(app):
    app['mysql_pool'].close()
    await app['mysql_pool'].wait_closed()


async def index(request):
    with open("./static/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return web.Response(text=html, content_type="text/html")


async def waf(request):
    return web.Response(text=messages[0], status=403)


def check(string):
    black_list = [b'R', b'i', b'o', b'b', b'V', b'__setstate__']
    white_list = [b'__main__', b'builtins', b'contact', b'time', b'dict', b'reason']
    try:
        s = base64.b64decode(string)
    except:
        return False
    for i in white_list:
        s = s.replace(i, b'')
    for i in black_list:
        if i in s:
            return False
    return True


async def getWishes(request):
    wishes = []
    id = request.query.get("id")
    try:
        pool = request.app['mysql_pool']
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    id = str(int(id))
                    sql = 'select id,wish from wishes where id={id}'.format(
                        id=id)
                except:
                    sql = 'select id,wish from wishes'
                await cur.execute(sql)
                datas = await cur.fetchall()
    except:
        return web.Response(text=messages[1])
    for (id, wish) in datas:
        if check(wish):
            wishes.append(pickle.loads(base64.b64decode(wish)))
    return web.Response(text=json.dumps(wishes), content_type="application/json")


async def addWishes(request):
    data = {}
    if request.query.get("contact") and request.query.get("place") and request.query.get("reason") and request.query.get("date") and request.query.get("id"):
        data["contact"] = request.query.get("contact")
        data["place"] = request.query.get("place")
        data["reason"] = request.query.get("reason")
        data["date"] = request.query.get("date")
        data["timestamp"] = int(time.time()*1000)
        id = request.query.get("id")
        wish = base64.b64encode(pickle.dumps(data))
    else:
        return web.Response(text=messages[3])
    try:
        pool = request.app['mysql_pool']
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = 'insert into wishes(`id`, `wish`) values ({id}, "{wish}")'.format(
                    id=id, wish=wish.decode())
                await cur.execute(sql)
                return web.Response(text=messages[2])
    except:
        return web.Response(text=messages[1])


async def rmWishes(request):
    try:
        pool = request.app['mysql_pool']
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = 'delete from wishes'
                await cur.execute(sql)
                return web.Response(text=messages[2])
    except:
        return web.Response(text=messages[1])


async def hint(request):
    with open(__file__, 'r') as f:
        source = f.read()
    return web.Response(text=source)

if __name__ == '__main__':
    app = web.Application()
    app['config'] = config
    app.router.add_static('/static', path='./static')
    app.add_routes([web.route('*', '/', index),
                    web.route('*', '/waf', waf),
                    web.route('*', '/addWishes', addWishes),
                    web.get('/getWishes', getWishes),
                    web.post('/rmWishes', rmWishes),
                    web.get('/hint', hint)])
    app = mysql_init(app)
    web.run_app(app, port=5000)