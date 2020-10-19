import pytest


class TestRoutes:
    @classmethod
    def setup_class(cls):
        ...

    @classmethod
    def teardown_class(cls):
        ...

    def test_list_in_range_in_query_string(self, test_app) -> None:
        list_of_numbers = str([1, 2, 3])
        with test_app.test_client() as c:
            resp = c.get(f"/total?list={list_of_numbers}")
        assert resp.status_code == 200
        json_data = resp.get_json()
        assert json_data["total"] == 6

    def test_empty_list(self, test_app) -> None:
        empty_list = str([])
        with test_app.test_client() as c:
            resp_querystring = c.get(f"/total?list={empty_list}")
            resp_body_param = c.get("/total", data=empty_list)
        assert resp_querystring.status_code == 400
        assert resp_querystring.data == b"Invalid input. Empty list."
        assert resp_body_param.status_code == 400
        assert resp_body_param.data == b"Invalid input. Empty list."

    @pytest.mark.timeout(100)
    def test_big_list(self, test_app, big_list) -> None:
        with test_app.test_client() as c:
            resp_querystring = c.get(f"/total?list={str(big_list)}")
            resp_body_param = c.get("/total", data=str(big_list))
        assert resp_querystring.status_code == 200
        assert resp_body_param.status_code == 200

    @pytest.mark.timeout(100)
    def test_big_list_out_of_range(self, test_app, big_list) -> None:
        big_list.append(10000002)
        with test_app.test_client() as c:
            resp_querystring = c.get(f"/total?list={str(big_list)}")
            resp_body_param = c.get("/total", data=str(big_list))
        assert resp_querystring.status_code == 416
        assert resp_body_param.status_code == 416

    def test_list_out_range(self, test_app) -> None:
        all_integers = str([0, -1, 2])
        with test_app.test_client() as c:
            resp_querystring = c.get(f"/total?list={all_integers}")
            resp_body_param = c.get("/total", data=all_integers)
        assert resp_querystring.status_code == 416
        assert resp_body_param.status_code == 416

    def test_list_in_range_in_parameter(self, test_app) -> None:
        list_of_numbers = str([1, 2, 3, 4])
        with test_app.test_client() as c:
            resp = c.get("/total", data=list_of_numbers)
        assert resp.status_code == 200
        json_data = resp.get_json()
        assert json_data["total"] == 10

    @pytest.mark.parametrize(
        "query_string, body_param, status_code, message",
        [
            ("[1, 2, 3]", "[1, 2, 3, 4]", 200, 6),
            ("[1, 2, 3, 4]", "[1, 2, 3]", 200, 10),
            ("[1, 2, -3, 4]", "[1, 2, 3]", 416, None),
            ("[1, 2, 3, 4]", "[1, -2, 3]", 200, 10),
        ],
    )
    def test_different_list_in_parameter_and_querystring(
        self, test_app, query_string, body_param, status_code, message
    ) -> None:
        with test_app.test_client() as c:
            resp = c.get(f"/total?list={query_string}", data=body_param)
        assert resp.status_code == status_code
        if status_code == 200:
            json_data = resp.get_json()
            assert json_data["total"] == message

    def test_no_data(self, test_app) -> None:
        with test_app.test_client() as c:
            resp = c.get("/total")
        assert resp.status_code == 400
