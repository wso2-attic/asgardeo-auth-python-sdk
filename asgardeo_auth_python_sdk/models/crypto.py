from jose import jwt


def get_supported_signature_algorithms():
    return ["RS256", "RS512", "RS384", "PS256"]


def validate_jwt(id_token, jwks, client_id, issuer):
    return jwt.decode(id_token,
                      jwks,
                      audience=client_id,
                      algorithms=get_supported_signature_algorithms(),
                      issuer=[issuer],
                      options={"verify_at_hash": False})
