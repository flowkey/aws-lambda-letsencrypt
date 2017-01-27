# aws-lambda-letsencrypt

AWS Lambda (Python) function for Letsencrypt

## Get Started

### Build bundled zip

Before configuring your Lambda function, the bundled zip file is needed. You can create bundled zip file by (1) runnning package.sh inside EC2 instance, or (2) using Docker container to execute package.sh

#### Running package.sh inside EC2 instance

The package.sh collects necessary components and zip them. The bundled zip file will be uploaded to specified S3 bucket, so you need specify appropriate instance role to write S3 bucket or run `aws configure` to set up manually.

Then, just execute following:

```
$ export BUCKET_NAME=YOUR-BUCKET # specify bucket to save output
$ curl -L https://raw.githubusercontent.com/kento1218/aws-lambda-letsencrypt/master/package.sh | bash
```

#### Using Docker

You need to create Docker image by following:

```
docker build -t aws-lambda-letsencrypt-build .
```

You can run the image by `docker run` or ECS. By docker:

```
docker run -e AWS_ACCESS_KEY_ID='YOUR-ACCESS-KEY-FOR-S3' -e AWS_SECRET_ACCESS_KEY='YOUR-ACCESS-SECRET-FOR-S3' -e BUCKET_NAME='YOUR-BUCKET' aws-lambda-letsencrypt-build:latest
```

### Setup Lambda function

You can setup your Lambda function by specifying the bundled zip. As aws-lambda-letsencrypt uses following environment variables, you need to add them on Lambda configuration.

* EMAIL - Your email
* DOMAINS - space-separated domain list
* DISTRIBUTION_ID - CloudFront distribution to update
* TEST_MODE - specify '1' if you want to run `certbot --staging`

## Special Thanks

Following article and tool are really helpful to run certbot in Lambda.

https://vittegleo.com/blog/letsencrypt-lambda-function/
https://github.com/dlapiduz/certbot-s3front
