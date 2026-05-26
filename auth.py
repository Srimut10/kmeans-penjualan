import hashlib
import requests
from datetime import datetime

SUPABASE_URL = "https://xaudrzfhhssvliozsxbo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhhdWRyemZoaHNzdmxpb3pzeGJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk3NTU0OTQsImV4cCI6MjA5NTMzMTQ5NH0.vyeu-_zq9Ue9SpRHfqMR491508T6a1e54LFjpcoQdik"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

class AuthManager:
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password):
        try:
            res = requests.get(
                f"{SUPABASE_URL}/rest/v1/users",
                headers=HEADERS,
                params={"username": f"eq.{username}", "select": "username,password,name"}
            )
            data = res.json()
            if data and data[0]['password'] == self.hash_password(password):
                return True, data[0]['name']
            return False, None
        except:
            return False, None

    def register(self, username, password, name):
        try:
            res = requests.get(
                f"{SUPABASE_URL}/rest/v1/users",
                headers=HEADERS,
                params={"username": f"eq.{username}"}
            )
            if res.json():
                return False, "Username sudah digunakan"

            res = requests.post(
                f"{SUPABASE_URL}/rest/v1/users",
                headers=HEADERS,
                json={
                    "username": username,
                    "password": self.hash_password(password),
                    "name": name,
                    "created_at": datetime.now().isoformat()
                }
            )
            if res.status_code in [200, 201]:
                return True, "Registrasi berhasil"
            return False, f"Gagal registrasi: {res.text}"
        except Exception as e:
            return False, f"Error: {e}"

    def change_password(self, username, old_password, new_password):
        try:
            res = requests.get(
                f"{SUPABASE_URL}/rest/v1/users",
                headers=HEADERS,
                params={"username": f"eq.{username}", "select": "password"}
            )
            data = res.json()
            if not data:
                return False, "User tidak ditemukan"
            if data[0]['password'] != self.hash_password(old_password):
                return False, "Password lama salah"

            res = requests.patch(
                f"{SUPABASE_URL}/rest/v1/users",
                headers=HEADERS,
                params={"username": f"eq.{username}"},
                json={"password": self.hash_password(new_password)}
            )
            if res.status_code in [200, 204]:
                return True, "Password berhasil diubah"
            return False, "Gagal mengubah password"
        except Exception as e:
            return False, f"Error: {e}"
