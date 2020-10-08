import unittest

import flask_testing

from app import app


class TestDlg(flask_testing.TestCase):

    def setUp(self) -> None:
        ...

    def tearDown(self) -> None:
        ...

    def create_app(self) -> app:
        return app

    def test_list_in_range_in_query_string(self) -> None:
        list_of_numbers = str([1, 2, 3])
        with app.test_client() as c:
            resp = c.get(f'/total?list={list_of_numbers}')
        self.assertEqual(resp.status_code, 200)
        json_data = resp.get_json()
        self.assertEqual(json_data["total"], 6)

    def test_empty_list(self) -> None:
        empty_list = str([])
        with app.test_client() as c:
            resp_querystring = c.get(f'/total?list={empty_list}')
            resp_body_param = c.get('/total', data=empty_list)
        self.assertEqual(resp_querystring.status_code, 400)
        self.assertEqual(resp_querystring.data, b'Invalid input. Empty list.')
        self.assertEqual(resp_body_param.status_code, 400)
        self.assertEqual(resp_body_param.data, b'Invalid input. Empty list.')

    def test_big_list(self) -> None:
        big_list = str(list(range(10000001)))
        with app.test_client() as c:
            resp_querystring = c.get(f'/total?list={big_list}')
            resp_body_param = c.get('/total', data=big_list)
        self.assertEqual(resp_querystring.status_code, 200)
        self.assertEqual(resp_body_param.status_code, 200)

    def test_big_list_out_of_range(self) -> None:
        big_list = str(list(range(10000002)))
        with app.test_client() as c:
            resp_querystring = c.get(f'/total?list={big_list}')
            resp_body_param = c.get('/total', data=big_list)
        self.assertEqual(resp_querystring.status_code, 416)
        self.assertEqual(resp_body_param.status_code, 416)

    def test_list_out_range(self) -> None:
        all_integers = str([0, -1, 2])
        with app.test_client() as c:
            resp_querystring = c.get(f'/total?list={all_integers}')
            resp_body_param = c.get('/total', data=all_integers)
        self.assertEqual(resp_querystring.status_code, 416)
        self.assertEqual(resp_body_param.status_code, 416)

    def test_list_in_range_in_parameter(self) -> None:
        list_of_numbers = str([1, 2, 3, 4])
        with app.test_client() as c:
            resp = c.get('/total', data=list_of_numbers)
        self.assertEqual(resp.status_code, 200)
        json_data = resp.get_json()
        self.assertEqual(json_data["total"], 10)

    def test_different_list_in_parameter_and_querystring(self) -> None:
        fixtures = (
            ("[1, 2, 3]", "[1, 2, 3, 4]", 200, 6),
            ("[1, 2, 3, 4]", "[1, 2, 3]", 200, 10),
            ("[1, 2, -3, 4]", "[1, 2, 3]", 416, None),
            ("[1, 2, 3, 4]", "[1, -2, 3]", 200, 10),
        )
        for parameters in fixtures:
            with app.test_client() as c:
                resp = c.get(f'/total?list={parameters[0]}', data=parameters[1])
            self.assertEqual(resp.status_code, parameters[2])
            if parameters[2] == 200:
                json_data = resp.get_json()
                self.assertEqual(json_data["total"], parameters[3])

    def test_no_data(self) -> None:
        with app.test_client() as c:
            resp = c.get('/total')
        self.assertEqual(resp.status_code, 400)


if __name__ == "__main__":
    unittest.main()
