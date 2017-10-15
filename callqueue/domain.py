class ValidationError(Exception):
    """Body/Request parameters are invalid"""


def parse_call(params):
    try:
        return {'call_id': params['uuid'],
                'conversation_id': params['conversation_uuid'],
                'to': params['to'],
                'from': params['from']}
    except KeyError as e:
        fmt = 'Missing key %r'
        raise ValidationError(fmt % e.args[0])