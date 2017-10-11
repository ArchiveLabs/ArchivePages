# ArchivePages

`<identifier>.pages.archivelab.org`.

This is a proof of concept on how to make webpages that are hosted on Archive.org more accessible.

There is a reverse proxy using Nginx with the xaccel feature.

A simple python script dynamically looks up the item path and passes this to the reverse proxy.

The item must have an `index.thml` file in the root directory.


## Provisioning/Deployment

```
cd provision
ansible-playbook main.yml -i "123.123.123.123," -u username --ssh-extra-args='-o ForwardAgent=yes'
```


## Disclaimer

This is not an official Archive.org project. It is merely a proof of concept.


## Example sites  

http://archiveexperiments.pages.archivelab.org ([item](https://archive.org/details/ArchiveExperiments))  
http://wayback-timemachine.pages.archivelab.org ([item](https://archive.org/details/wayback-timemachine))  
http://freefakebooks.pages.archivelab.org ([item](https://archive.org/details/FreeFakebooks))  
http://iiif-bookreader.pages.archivelab.org ([item](https://archive.org/details/iiif-bookreader))  

## Author

Richard Caceres (richard@archive.org)


## License

AGPL-3
