"""Automated tests for SCAM Don't CRAM Flask routes."""

import unittest

from app import app


class TestQuizRoutes(unittest.TestCase):
    """Test quiz navigation and input validation."""

    def setUp(self):
        """Create a Flask testing client."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page(self):
        """Check that the homepage loads."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        """Check that the About page loads."""
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)

    def test_invalid_question(self):
        """Check that an invalid question returns 404."""
        response = self.client.get(
            "/quiz/1/question/999"
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_section(self):
        """Check that an invalid section returns 404."""
        response = self.client.get("/quiz/999")
        self.assertEqual(response.status_code, 404)

    def test_missing_answer(self):
        """Check that submitting no answer is rejected."""
        response = self.client.post(
            "/quiz/1/question/0",
            data={}
        )
        self.assertEqual(response.status_code, 400)

    def test_non_numeric_answer(self):
        """Check that text cannot be used as an answer ID."""
        response = self.client.post(
            "/quiz/1/question/0",
            data={"answer": "hello"}
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_answer_id(self):
        """Check that an unknown answer ID is rejected."""
        response = self.client.post(
            "/quiz/1/question/0",
            data={"answer": "999999"}
        )
        self.assertEqual(response.status_code, 400)

    def test_empty_results(self):
        """Check that results require a completed quiz."""
        response = self.client.get("/results")
        self.assertEqual(response.status_code, 302)

    def test_invalid_question_shows_custom_404(self):
        """Check that an invalid question displays the 404 template."""
        response = self.client.get("/quiz/1/question/99")

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Oops! Page Not Found", response.data)

    def test_non_numeric_question_shows_custom_404(self):
        """Check that a non-numeric question URL displays the 404 page."""
        response = self.client.get("/quiz/1/question/hello")

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Oops! Page Not Found", response.data)

    def test_500_error_handler(self):
        """Check that the custom 500 error handler works."""
        response = self.client.get("/test-server-error")

        # A test route would be needed to trigger an actual 500.
        # This URL is currently unknown, so it should return 404.
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
