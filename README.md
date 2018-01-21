# study-group
All resources to be used for XSHELl study group

# requirement

* python 2.7
* OpenCV 2.4

# install

## install isaax agent.

```
$ wget https://isaaxartifacts.blob.core.windows.net/agent/v0.5.6/isaax-agent_v0.5.6_linux_armv7.tar.gz
$ sudo tar xvzf isaax-agent_v0.5.6_linux_armv7.tar.gz -C /opt/
```

## register a device

1. Create an [isaax](https://isaax.io) account
2. Create a project
3. Generate a project token and copy one
4. Login to Raspberry Pi and run `sudo /opt/isaax-agent install <project token>`
