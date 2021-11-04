import logging
import os
from flask import Flask, request, redirect, url_for

from flask import render_template, Response

logging.info("Starting application")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


@app.route('/', methods=['GET'])
def index():
    cas_login_url = os.environ['CAS_SERVER_URL']
    service_verification_url = os.environ['SERVICE_VERIFICATION_URL']

    login_url = f"{cas_login_url}/login?service={service_verification_url}"
    return render_template('index.html', title='CAS client demo',
                           login_url=login_url)


@app.route('/verify', methods=['GET'])
def verify_ticket():

    cas_server_url = os.environ['CAS_SERVER_URL']
    ticket = request.args.get("ticket")
    service = os.environ['SERVICE_VERIFICATION_URL']
    verification_url = f"{cas_server_url}/serviceValidate?" \
                       f"ticket={ticket}&service={service}"

    return render_template('validation.html',
                           title='CAS client validation',
                           ticket=ticket,
                           verification_url=verification_url)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
