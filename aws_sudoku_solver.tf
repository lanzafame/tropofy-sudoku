provider "aws" {
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
    region = "${var.region}"
}

resource "aws_instance" "sudoku_solver" {
    ami = "ami-28cff44b"
    instance_type = "t2.micro"
    tags {
        Name = "polymathian-tropofy"
    }
    vpc_security_group_ids = ["${aws_security_group.tropofy_port.id}"]
    provisioner "remote-exec" {
        inline = [
            "sudo yum -y update",
            "sudo yum -y install docker",
            "sudo service docker start",
            "sudo docker run -d -p 80:9123 lanzafame/tropofy-sudoku:latest"
        ]
    connection {
        type = "ssh"
        user = "ec2-user"
        private_key = "${file(var.private_key)}"
        timeout = "2m"
        agent = false
    }
    }
    key_name = "${aws_key_pair.tropofy_ssh_access.key_name}"
}

resource "aws_iam_user" "user" {
    name = "tropofy_user"
    path = "/"
}

resource "aws_iam_user_ssh_key" "user" {
    username = "${aws_iam_user.user.name}"
    encoding = "PEM"
    public_key = "${var.public_key}"
}

resource "aws_key_pair" "tropofy_ssh_access" {
    key_name = "tropofy_ssh_key"
    public_key = "${var.public_key}"
}

resource "aws_security_group" "tropofy_port" {
    name = "tropofy_port"
    description = "Allow all inbound traffic to port 22(ssh) and 9123(app)"

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags {
        Name = "tropofy_port"
    }
}

output "ip" {
    value = "${aws_instance.sudoku_solver.public_ip}"
}
