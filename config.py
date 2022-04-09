from os import getenv

transifex_api_url = getenv("TRANSIFEX_API_URL", "https://rest.api.transifex.com")
transifex_project_slug = getenv("TRANSIFEX_PROJECT_SLUG", "norg")
transifex_organisation_slug = getenv("TRANSIFEX_ORGANISATION_SLUG", "norg")
transifex_token = getenv(
    "TRANSIFEX_TOKEN", "1/35c27de88008a12687af9654d720e71618809d5e"
)
