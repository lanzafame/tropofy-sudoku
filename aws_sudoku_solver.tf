provider "aws" {
    access_key = ""
    secret_key = ""
    region = "ap-southeast-2"
}

resource "aws_instance" "sudoku_solver" {
    ami = "ami-0d729a60"
    instance_type = "t2.micro"
}
