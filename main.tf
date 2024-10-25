provider "aws" {
  region = "us-west-2"  # Change this to your desired region
}

# VPC Creation
resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "streamlit-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id
  tags = {
    Name = "streamlit-igw"
  }
}

# Public Subnet
resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-2a"
  map_public_ip_on_launch = true

  tags = {
    Name = "streamlit-subnet"
  }
}

# Security Group for EC2 instance
resource "aws_security_group" "streamlit_sg" {
  vpc_id = aws_vpc.main_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "streamlit-sg"
  }
}

# EC2 Instance to run Streamlit app
resource "aws_instance" "streamlit_instance" {
  ami           = "ami-07c5ecd8498c59db5"  # Use an Amazon Linux or Ubuntu AMI suitable for your region
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.streamlit_sg.id]

  # Use a key pair for SSH access
  key_name = "key"

  # User data to install software and run the app
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install python3 -y
              pip3 install streamlit xgboost pandas numpy
              
              # Add your app code here
              echo "
              import streamlit as st
              st.title('Heart Attack Predictor')
              " > app.py
              
              # Run Streamlit app on port 80
              nohup streamlit run app.py --server.port 80 &
              EOF

  tags = {
    Name = "streamlit-server"
  }
}

# Output EC2 public IP
output "instance_ip" {
  value = aws_instance.streamlit_instance.public_ip
}
