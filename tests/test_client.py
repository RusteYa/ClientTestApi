import pytest


class Tests:
    @pytest.mark.asyncio
    async def test_successful_authorize(self, client):
        data = await client.authorize(username='test', password='12345')

        assert data['status'] == 'OK'
        assert data['token'] is not None

    @pytest.mark.asyncio
    async def test_successful_get_user(self, client):
        data = await client.get_user('test')

        assert data['id'] is not None

    @pytest.mark.asyncio
    async def test_successful_update_user(self, client):
        test_data = {
            "active": "1",
            "blocked": True,
            "name": "Petr Petrovich",
            "permissions": [
                {
                    "id": 1,
                    "permission": "comment"
                },
            ]
        }
        user_id = 23
        data = await client.update_user(user_id, test_data)

        assert data['status'] == 'OK'
