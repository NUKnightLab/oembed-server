#Knight Lab oEmbed Server
A system to take oembed requests for KnightLab's embeddable tools.

###Useful Documentation
Coming soon...

#### Deployment

Use the git-deploy subcommand script to deploy to `stg` and `prd`. Be sure
`git-deploy` is on your PATH and you are setup to ssh into the appropriate
servers.

You will need the folling include in your local `.git/config` for this repository:

```
[include]
    path = ../conf/deploy.conf
```

This adds endpoints and configurations to enable the `git-deploy` commands

Example:

`git deploy stg --migrate` merges master into stg and deploys code to the stg
application and work servers, executes database migrations, and restarts
the cityhallmonitor application service.

