# flask-cert-details

Small utility to demonstrate the validity / rotation of certificates. Particularly helpful for demonstrating HashiCorp Vault's PKI Secrets Engine in Kubernetes clusters.

*Note that this will not show details on the certificate chain used in the process of securing in-transit communication with the application.*

## usage

Set the following environment variables:

* TLS_CERT_PATH - Filesystem path to certificate file
* CA_CERT_PATH - Filesystem path to issuing CA file

Run the application:

```bash
$ python3 app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

## output

Access using a browser either via FQDN, or via the URL presented the CLI (depending on how you're running it):

![screenshot of flask-cert-details displaying certificate and CA information](./images/output.png)

## kubernetes

When using in Kubernetes, it's useful to mount the Secret containing the managed certificates as a volume on a deployment:

When something like the Vault Secrets Operator rotates the certificate, the next request to this app will show the details.

```yaml
...
    spec:
      volumes:
        - name: short-lived-cert
          secret:
            secretName: short-lived-cert
            defaultMode: 420
          ...
          volumeMounts:
            - name: short-lived-cert
              readOnly: true
              mountPath: /opt/certificate/
          ...
          env:
            - name: TLS_CERT_PATH
              value: /opt/certificate/tls.crt
            - name: CA_CERT_PATH
              value: /opt/certificate/issuing_ca
...

```