import json
from odoo import http
from odoo.http import request

class PropertyApis(http.Controller):

    @http.route('/api/addproperty', methods=['POST'], type='http', auth='none', csrf=False)
    def property_creation(self):
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

    @http.route('/api/addproperty/json', methods=['POST'], type='json', auth='none', csrf=False)
    def property_json_creation(self):
        # Ensure only POST requests handle property creation
        if request.httprequest.method != 'POST':
            return   {"error": "Only POST method is allowed for this endpoint."}


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
            return {
                    "message": f"Property created successfully with ID {rec.id}",
                    "id": rec.id
                }

        except json.JSONDecodeError:
            return  {"error": "Invalid JSON format."}

        except Exception as e:
            # General error handling
            return {"error": f"An error occurred: {str(e)}"}

    @http.route('/api/updateproperty/<int:property_id>', methods=['POST'], type='http', auth='none', csrf=False)
    def property_creation(self, property_id):
        try:
            property =request.env['property'].sudo().search([('id', '=', property_id)])
            if not property:
                return request.make_json_response(
                    {"message": "Property doesn`t found"}, status=400
                )

            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)
            property.write(vals)
            return request.make_json_response(
                {
                    "message": "Property has been updated",
                    "id": property.id,
                    "name": property.name
                }
            )
        except Exception as e:
            return request.make_json_response(
                {"error": f"An error occurred: {str(e)}"}, status=500
            )









