# def remove_endpoints(endpoints):
#     hidden_paths = [
#         "auth/jwt/verify",
#         "auth/users/activation",
#         "auth/users/resend_activation",
#         "auth/users/reset_email",
#         "auth/users/reset_email_confirm",
#         "auth/users/reset_password",
#         "auth/users/reset_password_confirm",
#         "auth/users/set_email",
#         "auth/users/set_password",
#     ]

#     return [
#         (path, path_regex, method, callback)
#         for path, path_regex, method, callback in endpoints
#         if not any(hidden_path in path for hidden_path in hidden_paths)
#     ]
