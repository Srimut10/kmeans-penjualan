import requests
import json
from datetime import datetime

SUPABASE_URL = "https://xaudrzfhhssvliozsxbo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhhdWRyemZoaHNzdmxpb3pzeGJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk3NTU0OTQsImV4cCI6MjA5NTMzMTQ5NH0.vyeu-_zq9Ue9SpRHfqMR491508T6a1e54LFjpcoQdik"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

class HistoryManager:
    def save_analysis(self, username, analysis_data):
        try:
            payload = {
                "username": username,
                "timestamp": datetime.now().isoformat(),
                "filename": analysis_data.get('filename'),
                "n_clusters": analysis_data.get('n_clusters'),
                "silhouette_score": analysis_data.get('silhouette_score'),
                "features": json.dumps(analysis_data.get('features', [])),
                "total_data": analysis_data.get('total_data'),
                "total_sales": analysis_data.get('total_sales'),
                "result_file": analysis_data.get('result_file'),
                "product_col": analysis_data.get('product_col'),
                "sales_col": analysis_data.get('sales_col')
            }
            res = requests.post(
                f"{SUPABASE_URL}/rest/v1/history",
                headers=HEADERS,
                json=payload
            )
            if res.status_code in [200, 201]:
                data = res.json()
                return data[0]['id'] if data else None
            return None
        except Exception as e:
            print(f"Error save_analysis: {e}")
            return None

    def get_history(self, username):
        try:
            res = requests.get(
                f"{SUPABASE_URL}/rest/v1/history",
                headers=HEADERS,
                params={
                    "username": f"eq.{username}",
                    "order": "id.desc",
                    "select": "*"
                }
            )
            data = res.json()
            # Parse features dari JSON string
            for row in data:
                if isinstance(row.get('features'), str):
                    try:
                        row['features'] = json.loads(row['features'])
                    except:
                        row['features'] = []
            return data
        except Exception as e:
            print(f"Error get_history: {e}")
            return []

    def delete_history(self, username, history_id):
        try:
            res = requests.delete(
                f"{SUPABASE_URL}/rest/v1/history",
                headers=HEADERS,
                params={"id": f"eq.{history_id}", "username": f"eq.{username}"}
            )
            return res.status_code in [200, 204]
        except:
            return False

    def clear_history(self, username):
        try:
            res = requests.delete(
                f"{SUPABASE_URL}/rest/v1/history",
                headers=HEADERS,
                params={"username": f"eq.{username}"}
            )
            return res.status_code in [200, 204]
        except:
            return False
