import pytest

from callqueue.domain import parse_call, ValidationError


def test_valid_call_when_request_is_valid():
    valid_request = {'uuid': 'some_id', 
                     'conversation_uuid': 'another_id', 
                     'from': '1234', 
                     'to': '2345'}

    call = parse_call(valid_request)

    assert call['call_id'] == valid_request['uuid']
    assert call['conversation_id'] == valid_request['conversation_uuid']
    assert call['from'] == valid_request['from']
    assert call['to'] == valid_request['to']


def test_validation_error_when_request_is_missing_key():
    valid_request = {'conversation_uuid': 'another_id', 
                     'from': '1234', 
                     'to': '2345'}

    with pytest.raises(ValidationError):
        parse_call(valid_request)
