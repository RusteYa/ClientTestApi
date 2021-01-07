import asyncio
import json

import pytest
from aioresponses import aioresponses

from api.client import Client


@pytest.fixture(scope='class')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='class')
async def client():
    resp_auth = {
        "status": "OK",
        "token": "dsfd79843r32d1d3dx23d32d"
    }
    resp_get_user = {
        "status": "OK",
        "active": "1",
        "blocked": False,
        "created_at": 1587457590,
        "id": 23,
        "name": "Ivanov Ivan",
        "permissions": [
            {
                "id": 1,
                "permission": "comment"
            },
            {
                "id": 2,
                "permission": "upload photo"
            },
            {
                "id": 3,
                "permission": "add event"
            }
        ]
    }
    resp_upd_user = {
        "status": "OK",
    }

    with aioresponses() as m:
        m.get('http://testapi.ru/auth?password=12345&username=test', status=200, body=json.dumps(resp_auth))
        m.get('http://testapi.ru/get-user/test?token=dsfd79843r32d1d3dx23d32d', status=200,
              body=json.dumps(resp_get_user))
        m.post('http://testapi.ru/user/23/update?token=dsfd79843r32d1d3dx23d32d', status=200,
               body=json.dumps(resp_upd_user))

        client = Client.create()

        yield client
        await client.session.close()
