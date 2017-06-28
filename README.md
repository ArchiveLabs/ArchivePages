# ArchivePages

This is a proof of concept on how to make webpages that are hosted on Archive.org more accessible.

There is a reverse proxy using Nginx with the xaccel feature.

A simple python script dynamically looks up the item path and passes this to the reverse proxy.

## Provisioning/Deployment

```
ansible-playbook provision/main.yml -i "123.123.123.123," -u username --ssh-extra-args='-o ForwardAgent=yes'
```


## Disclaimer

This is not an official Archive.org project. It is merely a proof of concept.

## Author

Richard Caceres (richard@archive.org)

## License

AGPL-3
