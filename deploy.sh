#!/bin/sh

ssh -o StrictHostKeyChecking=no ec2-user@${{ secrets.EC2_PUBLIC_IP_ADDRESS }} << 'ENDSSH'
  cd /home/ec2-user/app
  export $(cat .env | xargs)
  docker login -u ${{ secrets.DOCKER_HUB_USERNAME }} -p ${{ secrets.DOCKER_HUB_TOKEN }}
  docker pull qwer342/python:latest
  docker pull qwer342/nginx:latest
  docker-compose -f docker-compose.prod.yml up -d
ENDSSH
