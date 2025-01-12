# Create a build stage to copy the files from S3 using credentials
FROM alpine:latest as layer-copy

ARG AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION:-""} 
ARG AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-""} 
ARG AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-""} 
ARG AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN:-""} 
ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} 
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} 
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} 
ENV AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN} 

# Add Layers
RUN apk add aws-cli curl unzip
RUN mkdir -p /opt

RUN curl $(aws lambda get-layer-version-by-arn --arn arn:aws:lambda:ap-northeast-1:133490724326:layer:AWS-Parameters-and-Secrets-Lambda-Extension:12 --query 'Content.Location' --output text) --output layer.zip
RUN unzip layer.zip -d /opt
RUN rm layer.zip

# Start second stage from blank image to squash all previous history, including credentials.
FROM scratch As layers
WORKDIR /opt
COPY --from=layer-copy /opt .

# Function code 
FROM public.ecr.aws/lambda/python:3.11
WORKDIR /opt
COPY --from=layers /opt .
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ${LAMBDA_TASK_ROOT}/
