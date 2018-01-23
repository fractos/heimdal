# Heimdal

[![Docker Pulls](https://img.shields.io/docker/pulls/fractos/heimdal.svg?style=for-the-badge)](https://hub.docker.com/r/fractos/heimdal/)

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

All non-matching traffic will receive a 403 Forbidden response immediately, without consulting the target.

## Installation and Running

Heimdal needs to be installed behind a load balancer appliance or other proxy that adds an `X-Forwarded-For` header.

You can pass a rules file for Heimdal to use with a Docker volume command, mapping a file into the container as `/etc/heimdal/rules.json`.

| Environment Variable | Description                                                               | Mandatory |
|----------------------|---------------------------------------------------------------------------|-----------|
| `LISTENER_PORT`      | Heimdal's listening port for requests                                     | Yes       |
| `TARGET_HOST`        | Proxy target hostname                                                     | Yes       |
| `TARGET_PORT`        | Proxy target port                                                         | Yes       |
| `RULES_FILE`         | Location of the rules file to use - defaults to `/etc/heimdal/rules.json` | No        |

```
sudo docker run -d --rm \
    --env LISTENER_PORT='<listener port>' \
    --env TARGET_HOST='<target host>' \
    --env TARGET_PORT='<target port>' \
    -v <absolute path to rules file>:/etc/heimdal/rules.json \
    heimdal
```

**Note**

Input for -v needs to be an absolute path.

## Etymology

Heimdal uses the `quickproxy` library which in turn uses the Tornado web server.