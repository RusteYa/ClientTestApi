import aiohttp


class Client:
    host = None
    session = None
    params = None

    def __init__(self, host, session):
        self.host = host
        self.session = session
        self.params = {}

    @staticmethod
    def create(host='http://testapi.ru'):
        session = aiohttp.ClientSession()
        return Client(host, session)

    async def authorize(self, username, password):
        params = {'username': username, 'password': password}
        async with await self.session.get(self.host + '/auth', params=params) as resp:
            data = await Client.validation_responce(resp)
            self.params.update({'token': data['token']})
            return data

    async def get_user(self, username):
        async with self.session.get(self.host + '/get-user/' + username, params=self.params) as resp:
            return await Client.validation_responce(resp)

    async def update_user(self, user_id, data):
        async with self.session.post(self.host + '/user/' + str(user_id) + '/update', params=self.params,
                                     data=data) as resp:
            return await Client.validation_responce(resp)

    @staticmethod
    async def validation_responce(resp):
        if resp.status == 200:
            data = await resp.json()
            if data['status'] == 'OK':
                return data
            elif data['status'] == 'Not found':
                raise Exception('User not found')
            elif data['status'] == 'Error':
                raise Exception('Server returned error')
            else:
                raise Exception('Not correct returned data')
        else:
            raise Exception('Unable to connect server. Response status %s' % resp.status)
