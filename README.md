# Heimdal

Heimdal is a Layer 7 web application firewall that selectively proxies traffic onto a target host based on CIDR matches for IP addresses and the HTTP methods allowed for that match.

It uses the `X-Forwarded-For` HTTP header to determine the remote IP address of a connection.

For example, in AWS an Elastic Load Balancer might add two entries to an `X-Forwarded-For` header:

```
X-Forwarded-For: 37.59.40.223, 172.140.17.1
```

Where the first dotted IP address is the actual remote IP of the request and the second is the load balancer appliance itself.

## Rule configuration

The rules are encoded in a basic JSON format:

```
{
  "rules": [
    {
      "effect": "ALLOW",
      "methods": [
        "GET", "HEAD", "OPTIONS"
      ],
      "source": [
        "0.0.0.0/0"
      ]
    },
    {
      "effect": "ALLOW",
      "methods": [
        "PUT", "POST", "PATCH"
      ],
      "source": [
        "46.102.195.175/32",
        "62.254.125.126/32"
      ]
    }
  ]
}
```

This allows GET, HEAD, OPTIONS requests from anywhere, but only allows PUT, POST, PATCH operations from two distinct IP addresses.

## Installation and Running

Heimdal needs to be installed behind a load balancer appliance or other proxy that adds an `X-Forwarded-For` header.

```
sudo docker run -d --rm \
    --env AWS_ACCESS_KEY_ID='<access key id>' \
    --env AWS_SECRET_ACCESS_KEY='<secret access key>' \
    --env RULES_S3_URI='<s3 uri for rules file>' \
    --env HOST='<target host>' \
    --env PORT='<listening / target port>' \
    heimdal
```
