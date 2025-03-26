from app import app


def test_cart():
    with app.test_client() as client:
        client.post("/cart/add/1")
        client.post("/cart/add/1")
        client.post("/cart/add/3")

        cart_response = client.get("/cart")
        assert cart_response.status_code == 200
        assert "apple" in cart_response.text
        assert "banana" in cart_response.text
        assert (
            "130" in cart_response.text
        )  # Price for 2 apples (50 * 2) + one banana (30)


def test_valid_promocode():
    with app.test_client() as client:
        client.post("/cart/add/1")
        client.post("/cart/add/1")
        client.post("/cart/add/3")

        base_price = client.get("/cart")
        assert "130" in base_price.text

        promo_price = client.post(
            "/cart/promocode", data={"code": "SALE20"}, follow_redirects=True
        )
        assert "104" in promo_price.text


def test_invalid_promocode():
    with app.test_client() as client:
        client.post("/cart/add/1")
        client.post("/cart/add/1")
        client.post("/cart/add/3")

        base_price = client.get("/cart")
        assert "130" in base_price.text

        promo_price = client.post(
            "/cart/promocode", data={"code": "WRONG"}, follow_redirects=True
        )
        assert "130" in promo_price.text
