import asyncio

from api.client import Client


async def main():
    c = Client.create('http://testapi.ru')

    await c.authorize(username='test', password='12345')
    data = await c.get_user(username='test')
    del data['status']
    del data['created_at']
    data.update(name='Petr Petrovich',
                blocked=False,
                permissions=[
                    {
                        "id": 1,
                        "permission": "comment"
                    },
                ])

    await c.update_user(data['id'], data)
    await c.session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
