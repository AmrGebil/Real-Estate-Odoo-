import json
from odoo import http
from odoo.http import request

class PropertyApis(http.Controller):

    @http.route('/api/addproperty', methods=['POST'], type='http', auth='none', csrf=False)
    def property(self):
        # Ensure only POST requests handle property creation
        if request.httprequest.method != 'POST':
            return request.make_json_response(
                {"error": "Only POST method is allowed for this endpoint."}, status=405
            )

        try:
            # Decode request body
            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)

            # Validate input (add your field-specific validation here)
            if not vals.get('name'):  # Example validation for 'name' field
                return request.make_json_response(
                    {"error": "Missing required field: 'name'."}, status=400
                )

            # Create property record
            rec = request.env['property'].sudo().create(vals)

            # Successful creation response
            return request.make_json_response(
                {
                    "message": f"Property created successfully with ID {rec.id}",
                    "id": rec.id
                },
                status=201
            )

        except json.JSONDecodeError:
            return request.make_json_response(
                {"error": "Invalid JSON format."}, status=400
            )
        except Exception as e:
            # General error handling
            return request.make_json_response(
                {"error": f"An error occurred: {str(e)}"}, status=500
            )


