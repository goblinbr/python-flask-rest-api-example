from itsdangerous import URLSafeSerializer


__serializer = URLSafeSerializer('mysupersecretkey')


def generate_new_token(data):
    global __serializer
    return __serializer.dumps(data)
