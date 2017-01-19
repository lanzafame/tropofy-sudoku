# Tropofy Sudoku Solver

## Deployment Instructions

Define (AWS Access key and Secret key)[https://console.aws.amazon.com/iam/home?#security_credential] in a Terraform variable file (keys.tfvars) like this:
```
access_key = "youraccesskey"
secret_key = "yoursecretkey"
```

Run terraform plan:
```
$ terraform plan -var-file="path/to/your/tfvars/file"
```
