"""This module contains the routes for processing PDF files."""

from flask import request
from flask_restx import Namespace, Resource, reqparse, fields
from pydantic import ValidationError
from server.models.request import ProcessRequestModel

process_ns = Namespace("Process", path="/process", description="PDF Processing Routes")

# Define Swagger model for metadata JSON (visual only)
process_model = process_ns.model(
    "ProcessRequest",
    {
        "user_id": fields.String(required=True, description="User ID"),
        "description": fields.String(description="Optional description"),
        "tags": fields.List(fields.String, description="Tags list"),
    },
)

# Define request parser for Swagger file upload + metadata
parser = reqparse.RequestParser()
parser.add_argument(
    "data", type=str, required=True, location="form", help="JSON metadata"
)
parser.add_argument(
    "file",
    type="FileStorage",
    required=True,
    location="files",
    help="PDF file to upload",
)


@process_ns.route("/")
class ProcessPDF(Resource):
    """Process PDF endpoint."""

    @process_ns.doc("process_pdf")
    @process_ns.expect(parser)
    def post(self):
        """Process uploaded PDF with metadata"""

        try:
            data_raw = request.form.get("data")
            if not data_raw:
                return {"error": "Missing 'data' JSON"}, 400

            data = ProcessRequestModel.model_validate_json(data_raw)

            if "file" not in request.files:
                return {"error": "Missing file upload"}, 400

            file = request.files["file"]
            if not file.filename.endswith(".pdf"):
                return {"error": "Invalid file type. Only PDF allowed."}, 400

            return {
                "message": "File processed successfully",
                "user_id": data.user_id,
            }, 200

        except ValidationError as ve:
            return {"error": "Validation Error", "details": ve.errors()}, 422

        except IOError as e:
            return {"error": "Unexpected error", "details": str(e)}, 500
