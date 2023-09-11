# import unittest
# from unittest.mock import patch
#
# from fastapi.testclient import TestClient
#
# from main import app
#
#
# class TestIntegration(unittest.TestCase):
#
#     def setUp(self):
#         self.client = TestClient(app)
#
#     @patch('application.auth.get_current_user')
#     def test_chat_endpoint(self, mock_get_current_user):
#         mock_user = {"id": 1, "username": "test_user"}
#         mock_get_current_user.return_value = mock_user
#         response = self.client.post(
#             "/chat/",
#             json={"message_text": "Hello, test!"},
#             headers={"Authorization": "Bearer mock_token"}
#         )
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("ai_message", response.json())
#         ai_message = response.json()["ai_message"]
#         self.assertIsInstance(ai_message, str)
#         self.assertTrue(ai_message)
#
#     @patch('application.database.get_db')
#     def test_get_user_messages(self,mock_get_db):
#         user_id = 1
#
#         mock_db = mock_get_db.return_value
#         mock_user = mock_db.query.return_value.filter.return_value.first.return_value
#         mock_user.username = "test_username"
#
#         response = self.client.get(f"/chat/{user_id}")
#
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertIn("user", data)
#         self.assertIn("message_history", data)
#
#         self.assertEqual(data["user"], "test_username")
#         self.assertIsInstance(data["message_history"], str)
#         self.assertTrue(data["message_history"])
