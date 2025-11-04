from rest_framework.test import APITestCase


class AuthNotesFlowTests(APITestCase):
    def test_register_login_create_list(self):
        # Register
        resp = self.client.post("/api/auth/register/", {"username": "u1", "password": "password123"})
        self.assertEqual(resp.status_code, 201)

        # Login
        resp = self.client.post("/api/auth/login/", {"username": "u1", "password": "password123"})
        self.assertEqual(resp.status_code, 200)

        # Create note
        resp = self.client.post("/api/notes/", {"title": "T1", "content": "C1"})
        self.assertEqual(resp.status_code, 201)
        note_id = resp.data["id"]

        # List notes
        resp = self.client.get("/api/notes/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(any(n["id"] == note_id for n in resp.data["results"] if isinstance(resp.data, dict) and "results" in resp.data) or any(n["id"] == note_id for n in resp.data if isinstance(resp.data, list)))

        # Archive
        resp = self.client.post(f"/api/notes/{note_id}/archive/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data["is_archived"])

        # Unarchive
        resp = self.client.post(f"/api/notes/{note_id}/unarchive/")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.data["is_archived"])
