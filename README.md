
# ⚡ Cat Detector 🐱
[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![Tests](https://github.com/kfrawee/serverless-image-recognition/workflows/Unit-Tests/badge.svg)


> This project demonstrates how to add observability to a fully serverless application using the aws-lambda-powertools python library. This article on the wescale blog allows to understand how to use this library.

## Overview
This project exposes an API to upload an image to an S3 bucket. The AWS Rekognition service then analyzes this image to produce labels that will be stored in a DynamoDB table.
The user can then query the database to find out if a cat has been detected on the uploaded image.

**It is an improved version of the project [image-recognition-api](https://github.com/kfrawee/image-recognition-api) by**
- Applying code best practice.
- Applying better project structure.
- Applying better logging and error handling.

<br>
<p align="center">
<img src="./images/01_architecture_overview.png" title="Architecture diagram" alt="Architecture diagram" width=100%/>
<b>Architecture diagram</b>
</p>

## Authors

- [@ddrugeon](https://www.github.com/ddrugeon)


## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```

## Documentation

[Documentation](https://linktodocumentation)


## License

[MIT](https://choosealicense.com/licenses/mit/)


# Serverless Framework Python HTTP API on AWS

This template demonstrates how to make a simple HTTP API with Python running on AWS Lambda and API Gateway using the Serverless Framework.

This template does not include any kind of persistence (database). For more advanced examples, check out the [serverless/examples repository](https://github.com/serverless/examples/)  which includes DynamoDB, Mongo, Fauna and other examples.

## Usage

### Deployment

```
$ serverless deploy
```

After deploying, you should see output similar to:

```bash
Deploying aws-python-http-api-project to stage dev (us-east-1)

✔ Service deployed to stack aws-python-http-api-project-dev (140s)

endpoint: GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/
functions:
  hello: aws-python-http-api-project-dev-hello (2.3 kB)
```

_Note_: In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).

### Invocation

After successful deployment, you can call the created application via HTTP:

```bash
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/
```

Which should result in response similar to the following (removed `input` content for brevity):

```json
{
  "message": "Go Serverless v3.0! Your function executed successfully!",
  "input": {
    ...
  }
}
```

### Local development

You can invoke your function locally by using the following command:

```bash
serverless invoke local --function hello
```

Which should result in response similar to the following:

```
{
  "statusCode": 200,
  "body": "{\n  \"message\": \"Go Serverless v3.0! Your function executed successfully!\",\n  \"input\": \"\"\n}"
}
```

Alternatively, it is also possible to emulate API Gateway and Lambda locally by using `serverless-offline` plugin. In order to do that, execute the following command:

```bash
serverless plugin install -n serverless-offline
```

It will add the `serverless-offline` plugin to `devDependencies` in `package.json` file as well as will add it to `plugins` in `serverless.yml`.

After installation, you can start local emulation with:

```
serverless offline
```

To learn more about the capabilities of `serverless-offline`, please refer to its [GitHub repository](https://github.com/dherault/serverless-offline).

### Bundling dependencies

In case you would like to include 3rd party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).
