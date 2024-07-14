provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "byteos" {
  ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 AMI
  instance_type = "t2.micro"

  tags = {
    Name = "ByteOS"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y docker
              service docker start
              usermod -a -G docker ec2-user
              curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              yum install -y git
              curl -sL https://rpm.nodesource.com/setup_14.x | bash -
              yum install -y nodejs
              npm install -g http-server
              git clone https://github.com/LMNxtLab/ByteOS.git
              cd ByteOS
              ./terraform/bootstrap.sh
              EOF

  key_name = "your-key-pair-name"

  vpc_security_group_ids = ["your-security-group-id"]

  associate_public_ip_address = true
}
