import urllib.request
import urllib.parse


def getinfo(game, goods_id, cookie):
    request = urllib.request.Request('https://buff.163.com/api/market/goods/sell_order?game=%s&goods_id=%s' % (game, goods_id))
    request.add_header('cookie', cookie)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53')
    get = urllib.request.urlopen(request)
    return get.read().decode('utf-8')


# def getnum(game, goods_name, cookie):
#     urlparse = urllib.parse.quote(goods_name)
#     request = urllib.request.Request("https://buff.163.com/api/market/goods?game=%s&page_num=1&search=%s" % (game, urlparse))
#     request.add_header('cookie', cookie)
#     request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53')
#     get = urllib.request.urlopen(request)
#     return get.read().decode('utf-8')


def getinfo_igxe(game, goods_id):
    request = urllib.request.Request('https://www.igxe.cn/product/trade/730/%s?sort_rule=1' % goods_id)
    # request.add_header('cookie', cookie)
    # request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53')
    get = urllib.request.urlopen(request)
    return get.read().decode('utf-8')

def getinfo_max(game, goods_id):
    request = urllib.request.Request('https://api.xiaoheihe.cn/mall/trade/spu/info?spu_id=%s' % goods_id)
    # request.add_header('cookie', cookie)
    # request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53')
    get = urllib.request.urlopen(request)
    return get.read().decode('utf-8')