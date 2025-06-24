import example
from unittest.mock import MagicMock, patch


def test_add_numbers():
    assert example.add_numbers(10, 5) == 15
    assert example.add_numbers(15, 15) == 30
    assert example.add_numbers(10, 10) == 20


def test_is_even():
    assert example.is_even(2) is True
    assert example.is_even(5) is False
    assert example.is_even(10) is True


@patch('example.requests.get')
def test_fetch_data(mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = 'it\'s json object'

    mock_requests_get.return_value = mock_response

    assert 'it\'s json object' == example.fetch_data('https://www.example.com')


def test_process_mock_object():
    test_object_1 = MagicMock()
    test_object_1.value = 10

    test_object_2 = MagicMock()
    test_object_2.value = -10

    assert 20 == example.process_mock_object(test_object_1)
    assert None is example.process_mock_object(test_object_2)


def test_run_data_pipeline():
    data_processor = MagicMock()
    ready_data = MagicMock()

    data_processor.process_data.return_value.analyze_data.return_value = ready_data
    example.run_data_pipeline(data_processor)

    data_processor.process_data.assert_called_once()
    data_processor.process_data.return_value.analyze_data.assert_called_once()

    ready_data.save_result.assert_called_once()


def test_divide_numbers_normal_case():
    assert 5 == example.divide_numbers(10, 2)
    assert 0 == example.divide_numbers(0, 10)
    assert 10 == example.divide_numbers(20, 2)


@patch('builtins.print')
def test_divide_numbers_zero_division(mock_print):
    assert None is example.divide_numbers(10, 0)
    mock_print.assert_any_call("Error: Cannot divide by zero!")


@patch('builtins.print')
def test_divide_numbers_type_error(mock_print):
    assert None is example.divide_numbers(10, '1')
    mock_print.assert_any_call("Error: Unsupported operand type(s) for division!")


@patch('requests.get')
def test_check_even_odd(mock_request_get):
    test_request_1 = MagicMock()
    test_request_1.status_code = 200
    test_request_1.json.return_value = {'results': [{'value': 10}]}

    test_request_2 = MagicMock()
    test_request_2.status_code = 200
    test_request_2.json.return_value = {'results': [{'value': 1}]}

    test_request_3 = MagicMock()
    test_request_3.status_code = 200
    test_request_3.json.return_value = {'results': [{'value': 18}]}

    test_url = 'https://www.example.com'
    test_numbers = [10, 1, 18]

    mock_request_get.side_effect = [test_request_1, test_request_2, test_request_3]

    assert ["Even", "Odd", "Even"] == example.check_even_odd(test_numbers, test_url)


def test_process_data_method():
    test_input = [1, 2, 3]
    test_object = example.DataProcessor()
    assert [2, 4, 6] == test_object.process_data(test_input)


@patch('example.DataProcessor.process_data', return_value=[2, 4, 6])
def test_analyze_data_method(mock_process_data):
    test_input = [1, 2, 3]
    test_object = example.DataProcessor()
    assert 12 == test_object.analyze_data(test_input)
