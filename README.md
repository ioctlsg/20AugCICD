# Self-signed certificates for SSL(https)

Creating a self-signed SSL certificate involves generating your own certificate without involving a trusted Certificate Authority (CA). While self-signed certificates are not recommended for production environments due to the lack of trust, they can be useful for testing and local development purposes. Here's a basic guide on how to create a self-signed SSL certificate:

**Note:** The steps provided below are for educational purposes and should not be used for securing production websites.

1. **Open a Terminal or Command Prompt:**
   Open a terminal or command prompt on your server or computer and change director to your SSL folder where you unzip the files(https://github.com/ioctlsg/Self-Signed-Cert-OpenSSL/blob/main/openssl-1.0.2j-fips-x86_64.zip)

   ![alt text](https://github.com/ioctlsg/Self-Signed-Cert-OpenSSL/blob/main/Capture.PNG)
 ![alt text](https://github.com/ioctlsg/Self-Signed-Cert-OpenSSL/blob/main/Command_Prompt.png)

2. **Generate a Configuration file for SSL:**
   This Configuation text file (e.g prtgcert.txt) would hold the paramenter of your ssl infomation. This file is senstive 
   
```bash
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no
[req_distinguished_name]
C = SG
ST = Singapore
L = Singapore
O = HoSehBoh Pte Ltd
OU = IT
CN = prtg01.HoSehBoh.sg
[v3_req]
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = this.that.sg
IP.1 = 192.168.10.10
```

![alt text](https://github.com/ioctlsg/Self-Signed-Cert-OpenSSL/blob/main/HoSehBo.png)

3. **Generate a Key Pair:**
   Use the following command to generate a key pair. This key(prtg01.key) will be used to sign your certificate(prtg01.crt):
   
   ```bash
   openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout prtg01.key -out prtg01.crt -config prtgcret.txt -extensions v3_req
   ```

4. **Install the Key to your service:**
   Depending on your web server or application, you will need to install the generated private key and self-signed certificate. This typically involves specifying the paths to these files in your server's configuration. Some have tools for installation e.g. prtg

5. **Install the Certificate to your computer on windows:**

Flow the windows left to right. 
 ![alt text](https://github.com/ioctlsg/Self-Signed-Cert-OpenSSL/blob/main/import%201.png)
 ![alt text](https://github.com/ioctlsg/Self-Signed-Cert-OpenSSL/blob/main/import%202.png)
 ![alt text](https://github.com/ioctlsg/Self-Signed-Cert-OpenSSL/blob/main/import%203.png)
 ![alt text](https://github.com/ioctlsg/Self-Signed-Cert-OpenSSL/blob/main/import%204.png)

6. **Testing:**
   Access your website using the HTTPS protocol (e.g., `https://yourwebserverip`) to verify that the self-signed certificate is working. You might encounter browser warnings since the certificate isn't trusted by default.

  ![alt text](https://github.com/ioctlsg/Self-Signed-Cert-OpenSSL/blob/main/03_prtg-certificate-importer.webp)

## Why self-signed is a bad idea ?

Self-signed certificates for SSL (Secure Sockets Layer) have a number of disadvantages compared to certificates signed by trusted Certificate Authorities (CAs). Here are some of the key disadvantages:

1. **Lack of Trust:** The main issue with self-signed certificates is that they are not issued by a trusted third party. When a user's browser encounters a self-signed certificate, it will display a warning message to the user indicating that the certificate is not trusted. This can create a poor user experience and discourage users from interacting with your website.

2. **Security Risks:** Self-signed certificates do not undergo the same level of validation and verification that certificates from reputable CAs do. This means that there's a higher risk of fraudulent or malicious certificates being used, which can put users at risk of man-in-the-middle attacks or other security breaches.

3. **Manual Distribution:** In order to use a self-signed certificate, you need to manually distribute the certificate to all the devices and browsers that will interact with your website. This can be cumbersome and error-prone, especially if you need to update the certificate periodically.

4. **Revocation Challenges:** If a self-signed certificate needs to be revoked due to compromise or other security reasons, there is no established mechanism for revocation. With CA-signed certificates, revocation lists and mechanisms are in place to promptly revoke compromised certificates.

5. **Interoperability Issues:** Some applications and services might not accept or work properly with self-signed certificates due to their lack of trust. This can result in compatibility issues that affect the functionality of your website or application.

6. **Browser Warnings:** Browsers display warnings when users encounter a self-signed certificate. These warnings can confuse and scare users, making them less likely to continue using your website or application.

7. **SEO Impact:** Google has indicated that using HTTPS (which requires a valid SSL certificate) is a ranking factor for search results. However, self-signed certificates are not recognized as secure by search engines, potentially affecting your website's search engine ranking.

8. **Limited Validation:** CA-signed certificates typically go through a validation process to verify the identity of the certificate holder. This validation process is not present with self-signed certificates, meaning that users cannot be sure of the authenticity of the website they're interacting with.

9. **Browser and OS Changes:** Over time, browsers and operating systems may tighten their security policies and handling of self-signed certificates, potentially leading to more severe warnings or even complete blockage of access to websites using self-signed certificates.

In summary, while self-signed certificates can be useful for certain specific purposes like internal testing, they are generally not recommended for production websites or applications due to the lack of trust, potential security risks, and poor user experience they can create. It's recommended to obtain SSL certificates from trusted Certificate Authorities to ensure the security and trustworthiness of your online services.

Python script - work in progress. 
