Odin
====

Use LDA[1] to get the topics from redmine[2] system.

# Using environment variables for configuration

```shell
docker run -e REDMINE_URL=your_redmine_url -e REDMINE_USERNAME=username -e REDMINE_PASSWORD=password -p 8888:8888 -d --name odin odin
```

# Get the jupyter notebook url

```shell
docker logs odin
```

[1]https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation
[2]http://www.redmine.org
