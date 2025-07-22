"""Health API"""

from flask_restx import Namespace, Resource

health_ns = Namespace("Health", path="/health", description="Health Check Endpoints")


@health_ns.route("/")
class HealthCheck(Resource):
    """Health check endpoint."""

    def get(self):
        """Health check route"""
        return {"status": "ok", "message": "Server is healthy"}
