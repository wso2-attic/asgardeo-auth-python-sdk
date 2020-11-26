from jose import jwt
from jose.utils import base64url_decode
from sdk.exception.identityautherror import IdentityAuthError


def get_supported_signature_algorithms():
    return ["RS256", "RS512", "RS384", "PS256"]


def validate_jwt(id_token, jwks, client_id, issuer):
    return jwt.decode(id_token,
                      jwks,
                      audience=client_id,
                      algorithms=get_supported_signature_algorithms(),
                      issuer=[issuer],
                      options={"verify_at_hash": False})


# def validate_jwt(id_token,jwks,client_id,issuer):
#
#     id_token = "eyJ4NXQiOiJNMlF4WkRNME4ySTVaRFZoWmpVM056SXlNR1pqTnpsak1Ua3dZekl6TkROa01tRTBNV1EwWXpObE9ESTVZVGczWkRKa01UQTBOR1F4TVdSaU0yVXdaZyIsImtpZCI6Ik0yUXhaRE0wTjJJNVpEVmhaalUzTnpJeU1HWmpOemxqTVRrd1l6SXpORE5rTW1FME1XUTBZek5sT0RJNVlUZzNaREprTVRBME5HUXhNV1JpTTJVd1pnX1JTMjU2IiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoiVGZqTU1hN1ZUbFdaREVVckVtRnNydyIsImF1ZCI6ImhzRzZzMTVrS2Rfck9KWGdlR0NXb0JrT2FsY2EiLCJjX2hhc2giOiJaS01UOFowYlJCQWZXNkpIQnpSWkhnIiwic3ViIjoia3VnYW4iLCJuYmYiOjE2MDQzOTcwNjIsImF6cCI6ImhzRzZzMTVrS2Rfck9KWGdlR0NXb0JrT2FsY2EiLCJhbXIiOlsiQmFzaWNBdXRoZW50aWNhdG9yIl0sImlzcyI6Imh0dHBzOlwvXC9sb2NhbGhvc3Q6OTQ0M1wvdFwvd3NvMi5jb21cL29hdXRoMlwvdG9rZW4iLCJleHAiOjE2MDQ0MDA2NjIsImlhdCI6MTYwNDM5NzA2Mn0.lvRqE7G03tE1Xx8UHnaTtjTblgPzoaSdohkvs1a-ELcVHc04HoiXLojzwZXR9Ej2r_dODgcs1gv1ePlKbn9dxS4alPj6nu08E2s067GaYUBfL9ntxRN7tnm8CcV2Bfbd0xJWZ4chGOGTLxrCPzl-4Z0jYDfz3eoRVXRnh1_BF6wjHqbiac0W6EyhITyfoxd4RIpdvy0bENyL8k19R8U38EbmXQpz3emkXbpbMxBhPOuAr1oj31Ba0o4oaRcQpgd-nvejpFQqw-CqhM3TJvI-GzQtvsmL-KT3mfe9LEv4tfZ1tNbcLTGXcBGn-m3AoQ7GekTlpnkAOzJOf9IcDDWb_A"
#
#     jwks=[
#         {
#             "kty": "RSA",
#             "e": "AQAB",
#             "use": "sig",
#             "kid": "M2QxZDM0N2I5ZDVhZjU3NzIyMGZjNzljMTkwYzIzNDNkMmE0MWQ0YzNlODI5YTg3ZDJkMTA0NGQxMWRiM2UwZg_RS256",
#             "alg": "RS256",
#             "n": "n2gY7qGmuRa07sLYmoiXy7BQEKzXSTnli5x4cAnyzfLlN9SF7dzxVBb1Zy2EYZggORrDDAWztQ6bfeGWfXyYSGPMTHzKOedudbajscUuH6MtIkxui1VH9jQQydIcMhGAMrWWQBr3PVp3tqzmagplXwEOY8HhLr3SrF4zhfXhqeVnNLKB0GTZDcZI_HMjq7luh0kWaRphvXapiYDUmG8ESTD7_h6f3wVjfS0AftQ_-ZWUXIKLxJl7HASO1Ugp9mGeRDD5MFaBvi2GCV8xaoafBfTJEOOZq0RxIIghkD_0y_k1pv3jmclTIUb_yrgu-3sJ9Xz_m_T_AWgucnu1MgvI6w"
#         }
#     ]
#     client_id='hsG6s15kKd_rOJXgeGCWoBkOalca'
#     issuer = "https://localhost:9443/t/wso2.com/oauth2/token"
#
#     # key = get_jwk(get_kid(id_token), jwks)
#
#     try:
#         jwt.decode(id_token,
#                    jwks,
#                    audience = client_id,
#                    algorithms=get_supported_signature_algorithms(),
#                    issuer=[issuer],
#                    options={"verify_at_hash":False})
#     except Exception as ex:
#        raise Error(ex)
