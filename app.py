from flask import Flask, render_template
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import datetime
import os

app = Flask(__name__)

def load_certificate(file_path):
    try:
        with open(file_path, 'rb') as f:
            return x509.load_pem_x509_certificate(f.read(), default_backend())
    except FileNotFoundError:
        return None

def format_name(name):
    return ', '.join(['{}={}'.format(attr.oid._name, attr.value) for attr in name])

def format_expiry_date(expiry_date):
    return expiry_date.strftime('%d-%m-%Y %H:%M:%S')

@app.route('/')
def index():
    tls_cert_path = os.environ.get('TLS_CERT_PATH')
    ca_cert_path = os.environ.get('CA_CERT_PATH')

    tls_cert = load_certificate(tls_cert_path)
    ca_cert = load_certificate(ca_cert_path)
    
    if not tls_cert or not ca_cert:
        return "Certificate file(s) not found. Please check the file paths.", 404

    current_time = datetime.datetime.utcnow()
    tls_cert_valid = tls_cert.not_valid_before <= current_time <= tls_cert.not_valid_after
    tls_signed_by_ca = tls_cert.issuer == ca_cert.subject
    tls_cert_expiry = format_expiry_date(tls_cert.not_valid_after)
    ca_cert_expiry = format_expiry_date(ca_cert.not_valid_after)

    return render_template('index.html', tls_cert=tls_cert, ca_cert=ca_cert,
                           tls_cert_valid=tls_cert_valid, tls_signed_by_ca=tls_signed_by_ca,
                           tls_cert_expiry=tls_cert_expiry, ca_cert_expiry=ca_cert_expiry,
                           formatted_tls_subject=format_name(tls_cert.subject),
                           formatted_tls_issuer=format_name(tls_cert.issuer),
                           formatted_ca_subject=format_name(ca_cert.subject),
                           formatted_ca_issuer=format_name(ca_cert.issuer))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')