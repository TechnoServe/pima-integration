import os
import hmac
from flask import request, jsonify

def require_api_key(app):
    API_KEYS = [k.strip() for k in os.environ["API_AUTH_KEY"].split(",") if k.strip()]
    EXEMPT_PATHS = {"/healthz"}

    def _valid(candidate):
        return any(hmac.compare_digest(candidate, k) for k in API_KEYS)

    @app.before_request
    def check_api_key():
        if request.path in EXEMPT_PATHS:
            return
        if _valid(request.headers.get("X-API-Key", "")):
            return
        return jsonify({"error": "Unauthorized"}), 401