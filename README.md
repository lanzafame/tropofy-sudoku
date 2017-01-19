# Tropofy Sudoku Solver

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