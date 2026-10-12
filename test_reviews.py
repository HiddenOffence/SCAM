
"""Security test for the student review form."""

from app import app


def test_review_without_csrf():
    """Verify that a review without a CSRF token is rejected."""

    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post(
            "/reviews",
            data={
                "name": "Test Student",
                "rating": "5",
                "comment": "This is a test review.",
            },
        )

        assert response.status_code == 200
        assert b"CSRF" in response.data

    print("PASS: Review without CSRF token was rejected.")


if __name__ == "__main__":
    test_review_without_csrf()
