import json
from odoo import http
from odoo.http import request
from urllib.parse import parse_qs

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

    @http.route('/api/addpropertyusing query', methods=['POST'], type='http', auth='none', csrf=False)
    def property_creation_using_query(self):
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
            comluns = ', '.join(vals.keys())
            values = ','.join(['%s'] * len(vals))
            cr = request.env.cr
            query = f"""INSERT INTO property ({comluns}) VALUES ({values}) RETURNING id, name, postcode, bedroom, expected_price  """

            cr.execute(query, tuple(vals.values()))
            rec = cr.fetchone()
            # Successful creation response
            return request.make_json_response(
                {
                    "message": f"Property created successfully with ID {rec[0]}",
                    "id": rec[0],
                    "name": rec[1],
                    "postcode": rec[2],
                    "bedroom": rec[3],
                    "expected_price":rec[4]
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

    @http.route('/api/updateproperty/<int:property_id>', methods=['PUT'], type='http', auth='none', csrf=False)
    def property_update(self, property_id):
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

    @http.route('/api/property/<int:property_id>', methods=['GET'], type='http', auth='none', csrf=False)
    def retrun_one_property(self, property_id):
        try:
            property = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property:
                return request.make_json_response(
                    {"message": "Property doesn`t found"}, status=400
                )

            return request.make_json_response(
                {
                    "message": "Property list",
                    "id": property.id,
                    "name": property.name,
                    "postcode": property.postcode,
                    "expected_price": property.expected_price,
                    "selling_price": property.selling_price,
                    "bedroom": property.bedroom,
                    "garden_orientation": property.garden_orientation,
                    "state": property.state,
                },
                status=200
            )
        except Exception as e:
            return request.make_json_response(
                {"error": f"An error occurred: {str(e)}"}, status=500
            )

    @http.route('/api/properties_list', methods=['GET'], type='http', auth='none', csrf=False)
    def retrun_properties_list(self):
        try:
            parms = parse_qs(request.httprequest.query_string.decode('utf-8'))
            domain = []
            if parms.get('sate') :
                domain += [('state', '=', parms.get('sate')[0])]
            properties = request.env['property'].sudo().search(domain)
            if not property:
                return request.make_json_response(
                    {"message": "Property doesn`t found"}, status=400
                )

            return request.make_json_response(
               [{ "message": "Properties list",
                    "id": property.id,
                    "name": property.name,
                    "postcode": property.postcode,
                    "expected_price": property.expected_price,
                    "selling_price": property.selling_price,
                    "bedroom": property.bedroom,
                    "garden_orientation": property.garden_orientation,
                    "state": property.state,
                } for property in properties],
                status=200
            )
        except Exception as e:
            return request.make_json_response(
                {"error": f"An error occurred: {str(e)}"}, status=500
            )







