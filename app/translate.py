import requests
from flask import current_app
from flask_babel import _


def translate(text, source_language, dest_language):
    if (
        "MS_TRANSLATOR_KEY" not in current_app.config
        or not current_app.config["MS_TRANSLATOR_KEY"]
    ):
        return _("Error: the translation service is not configured.")
    auth = {
        "Ocp-Apim-Subscription-Key": current_app.config["MS_TRANSLATOR_KEY"],
        "Ocp-Apim-Subscription-Region": "global",
    }
    app_request = requests.post(
        "https://api.cognitive.microsofttranslator.com"
        "/translate?api-version=3.0&from={0}&to={1}".format(
            source_language, dest_language
        ),
        headers=auth,
        json=[{"Text": text}],
    )
    current_app.logger.info(app_request.text)
    if app_request.status_code != 200:
        return _("Error: the translation service failed.")
    return app_request.json()[0]["translations"][0]["text"]
