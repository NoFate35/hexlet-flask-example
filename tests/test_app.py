from app import app


def test_cart():
    with app.test_client() as client:
        response = client.get('/')
        assert b'Cart is empty' in response.data

        response = client.post(
            '/cart-items',
            data={'item_id': '1', 'item_name': 'One'},
            follow_redirects=True,
        )
        assert b'One: 1' in response.data

        response = client.post(
            '/cart-items',
            data={'item_id': '1', 'item_name': 'One'},
            follow_redirects=True,
        )
        assert b'One: 2' in response.data

        response = client.post(
            '/cart-items',
            data={'item_id': '2', 'item_name': 'Two'},
            follow_redirects=True,
        )
        assert b'One: 2' in response.data
        assert b'Two: 1' in response.data

        response = client.post(
            '/cart-items',
            data={'item_id': '2', 'item_name': 'Two'},
            follow_redirects=True,
        )
        assert b'One: 2' in response.data
        assert b'Two: 2' in response.data

        response = client.post(
            '/cart-items',
            data={'item_id': '2', 'item_name': 'Two'},
            follow_redirects=True,
        )
        assert b'One: 2' in response.data
        assert b'Two: 3' in response.data

        response = client.post(
            '/cart-items/clean',
            data={'item_id': '2', 'item_name': 'Two'},
            follow_redirects=True,
        )
        assert b'Cart is empty' in response.data
        assert b'One:' not in response.data
        assert b'Two:' not in response.data
