from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
import datetime

# Generate a private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Create a self-signed certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
])
cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(private_key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"example.com")]),
    critical=False,
).sign(private_key, hashes.SHA256())

# Save private key and certificate to files
with open("server.key", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ))

with open("server.crt", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))