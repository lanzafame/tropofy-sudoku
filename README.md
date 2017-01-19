# Tropofy Sudoku Solver

## Setup Instructions

To build this project, you will need to install both [Rocker](https://github.com/grammarly/rocker) and [Docker](https://docker.com).

To deploy this project, you will need to install [Terraform](https://www.terrafrom.io) and have an [AWS account](https://aws.amazon.com).

## Build Instructions

The `Rockerfile` has two significant advantages over regular `Dockerfiles`. Firstly, it is able to contain two `FROM` statements, allowing for a simpler build/run image setup. Secondly, it allows for the easy sharing of intermediary data, via the `EXPORT` and `IMPORT` statements.

To build the project, run the following:

```
$ rocker build .
```

Note: `Rockerfiles` allow you to specify the `--tag` in the file.

This command will output a Docker image, like the following:

```
$ docker images
REPOSITORY                 TAG                 IMAGE ID            CREATED             SIZE
lanzafame/tropofy-sudoku   latest              38d9b5ec52a2        12 hours ago        462.6 MB
```

Note: Due to some issues getting Python C extensions to work on Alpine (see: `musl` vs `glibc`) the image is still far to big, but is half of the straight `wheezy` based image.

Once the image is built, push it to [Docker Hub](https://hub.docker.com) or a private Docker registry, if you have one available. During the deployment of the EC2 Instance, Terraform will pull the image from Docker Hub and run the container.

## Deployment Instructions

Define [AWS Access key and Secret key](https://console.aws.amazon.com/iam/home?#security_credential) in a Terraform variable file (keys.tfvars) like this:
```
access_key = "youraccesskey"
secret_key = "yoursecretkey"
public_key = "yourpublickey"
```

Run terraform plan:
```
$ terraform plan -var-file="path/to/your/tfvars/file -out plan.file"
```

If `plan` returns no errors, run `apply`:
```
$ terrafrom apply plan.file
```

Terraform will spin up a security group in the AWS VPC, create a key pair using your public SSH key, create a IAM user for the SSH key, it will then spin up an EC2 instance with the SSH key associated with it.

Note: to convert your key pair to AWS PEM encoding, just `cp id_rsa id_rsa.pem` and then `sudo chmod 400 id_rsa.pem`.

Terraform also provisions the EC2 instance via SSH remote exec. It installs docker, starts the docker service and then pulls/runs the docker image upload to http://hub.docker.com/r/lanzafame/tropofy-sudoku.

Once Terraform has finished building the infrastructure it will spit out the public IP address of the EC2 instance, which will present you with a Tropofy login page when accessed from a browser.

When you are finished using the deployed app, run `terraform destroy` to delete all the infrastructure that it deployed:

```
$ terraform destroy -var-file="path/to/your/tfvars/file"
```

