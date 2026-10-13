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


if __name__ == "__main__":
    unittest.main()
