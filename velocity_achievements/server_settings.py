# Django settings for velocity_achievements project in production.

ADMINS = (
    "christophe.biocca@gmail.com",
)

MANAGERS = ADMINS

EMAIL_BACKEND = 'email_services.backends.PostmarkEmailBackend'
EMAIL_SERVICES_CLIENT_KEY = 'd59ce74a-7d74-412f-bd4d-f7035804ebbf'
