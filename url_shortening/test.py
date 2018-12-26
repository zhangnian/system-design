import json

from faker import Faker

from url_shortening.api import app


def main():
    fake = Faker()

    with app.test_client() as client:
        for _ in range(1):
            jdata = {'origin_url': fake.url()}
            r = client.post('/shortening', data=json.dumps(jdata), content_type='application/json')
            if r.status_code == 200:
                resp = json.loads(r.data.decode())
                print(resp)
            else:
                print('api call error')


if __name__ == '__main__':
    main()