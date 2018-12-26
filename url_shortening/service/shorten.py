import hashlib

from url_shortening.model.models import TinyUrl


BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class HashShorten:
    def base62_encode(self, num, alphabet=BASE62):
        if num == 0:
            return alphabet[0]

        arr = []
        base = len(alphabet)
        while num:
            num, rem = divmod(num, base)
            arr.append(alphabet[rem])
        arr.reverse()

        return ''.join(arr)

    def shorten_encode(self, origin_url, retry=0):
        if retry:
            origin_url = origin_url + str(retry)

        m = hashlib.md5()
        m.update(origin_url.encode())
        hexstr = m.hexdigest()
        n = int(hexstr, 16)
        return self.base62_encode(n)[:6]

    def shorten_url(self, origin_url, custom_key):
        write_db = False
        if custom_key:
            rec = TinyUrl.model(custom_key).query.filter(TinyUrl.model(custom_key).key == custom_key).first()
            if rec and rec.origin_url != origin_url:
                return None, write_db

            if not rec:
                write_db = True

            return custom_key, write_db

        retry = 0
        while True:
            key = self.shorten_encode(origin_url, retry)
            rec = TinyUrl.model(key).query.filter(TinyUrl.model(key).key == key).first()
            if not rec:
                write_db = True
                break

            if rec.origin_url == origin_url:
                break

            retry += 1

        return key, write_db


class PoolShorten:
    def shorten_url(self, origin_url, custom_key):
        pass


def get_origin_url(key):
    return TinyUrl.model(key).query.filter(TinyUrl.model(key).key == key).first()
