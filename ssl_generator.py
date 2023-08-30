from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
import datetime
import ipaddress

# Gather user input
common_name = input("Enter Common Name (e.g., prtg01.HoSehBoh.sg): ")
organization = input("Enter Organization Name: ")
organizational_unit = input("Enter Organizational Unit: ")
country = input("Enter Country (2-letter code, e.g., SG): ")
state = input("Enter State or Province: ")
locality = input("Enter Locality: ")
alt_dns_names = input("Enter DNS Names (comma-separated): ").split(',')
alt_ip_addresses = input("Enter IP Addresses (comma-separated): ").split(',')

parsed_ip_addresses = []
for ip in alt_ip_addresses:
    try:
        parsed_ip = ipaddress.ip_address(ip.strip())  # Parse IP address
        parsed_ip_addresses.append(parsed_ip)
    except ValueError:
        print(f"Invalid IP address: {ip.strip()}. Skipping.")

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, country),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
    x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, organizational_unit),
    x509.NameAttribute(NameOID.COMMON_NAME, common_name),
])

subject_alt_names = [
    x509.DNSName(name.strip()) for name in alt_dns_names
] + [
    x509.IPAddress(ip) for ip in parsed_ip_addresses
]

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(private_key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)).add_extension(
    x509.KeyUsage(
        digital_signature=True,
        content_commitment=True,
        key_encipherment=True,
        data_encipherment=True,
        key_agreement=True,
        key_cert_sign=False,
        crl_sign=False,
        encipher_only=False,
        decipher_only=False,
    ),
    critical=False,
).add_extension(
    x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),
    critical=False,
).add_extension(
    x509.SubjectAlternativeName(subject_alt_names),
    critical=False,
).sign(private_key, hashes.SHA256(), default_backend())

with open("server.key", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ))

with open("server.crt", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))
