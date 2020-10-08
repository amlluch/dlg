import json

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

numbers_to_add = list(range(10000001))


@app.route('/total', methods=['GET'])
def total() -> str:

    # prioritize query string as url can be cached
    try:
        list_of_numbers = json.loads(request.args.get("list"))
    except TypeError:
        if not request.data:
            return make_response('Invalid input. No input data.', 400)
        list_of_numbers = request.get_json(force=True)

    if type(list_of_numbers) is not list:
        return make_response('Invalid input. It must be a list', 400)
    if not len(list_of_numbers):
        return make_response('Invalid input. Empty list.', 400)
    if not set(list_of_numbers).issubset(numbers_to_add):
        return make_response('Some value(s) in the list out of range', 416)

    return jsonify({"total": sum(list_of_numbers)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
