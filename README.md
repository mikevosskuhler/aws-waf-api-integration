# AWS WAF API Gateway integration
Protect your Api endpoints using AWS WAF. 
This repository contains a basic example on how to make you Api endpoints only available for one or a select group of IPs. 

# Getting started
After following these instructions you will have:
- A WAF ACL
- A IP ruleset
- An example API endpoint that fetches weather data. 

## Prerequisites
You need the following tools to get this project deployed:
- [git](https://git-scm.com/downloads)
- [AWS CLI](https://aws.amazon.com/cli/)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

If you configure the AWS CLI with a key and secret, you don't have to add any configurations to the AWS SAM CLI. 

## Clone the repo
`git clone https://github.com/mikevosskuhler/aws-waf-api-integration.git`

## Modify the template to match your use case
To whitelist access to the endpoint from your home address modify the following syntax in the cloudformation template.yaml in the waf-acl directory:
```
  homeip:
    Type: 'AWS::WAFv2::IPSet'
    Properties:
      Description: home ip Addres
      Name: home
      Scope: REGIONAL
      IPAddressVersion: IPV4
      Addresses:
        - 1.2.1.1/32
```

1.2.1.1 has to be replaced with your ip address or you can opt to use a larger CIDR block.

## Deploy the cloudformation template
From the waf-acl directory use the following command:
`aws cloudformation create-stack --stack-name home-waf --template-body file://template.yaml`

## Deploy the lambda backed api endpoint
From the sam-weather-api directory use the folling command:
`sam deploy -g .`
And give the SAM CLI the parameters you want to use for your deployment

## Adding your openweather api key
Use the following command to add your openweather api key to your ssm parameter store
`aws ssm put-parameter --name weatherkey --type SecureString --value "<your api key here>"`

## using the WAF ACL for other endpoints
You can now use this ACL for any endpoint you create by using the same syntax being used in the weather api SAM template:
```
  MyWebACLAssociation:
    Type: "AWS::WAFv2::WebACLAssociation"
    Properties:
      ResourceArn: !Sub 'arn:aws:apigateway:${AWS::Region}::/restapis/${ApiGatewayApi}/stages/prod'
      WebACLArn: !ImportValue wafarn
```You can replace ApiGatewayApi with the name of any other api endpoints created in the template you want to protect. 
