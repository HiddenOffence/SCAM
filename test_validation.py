
"""Tests for quiz answer validation."""

import unittest
from app import app


class QuizValidationTests(unittest.TestCase):
    """Check that the quiz accepts only valid answers."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_valid_answer(self):
        response = self.client.post(
            "/quiz/1/question/0",
            data={"answer": "1"}
        )
        self.assertEqual(response.status_code, 302)

    def test_text_answer(self):
        response = self.client.post(
            "/quiz/1/question/0",
            data={"answer": "abc"}
        )
        self.assertEqual(response.status_code, 400)

    def test_nonexistent_answer(self):
        response = self.client.post(
            "/quiz/1/question/0",
            data={"answer": "999999"}
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_answer(self):
        response = self.client.post(
            "/quiz/1/question/0",
            data={}
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
