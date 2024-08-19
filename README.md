# cc
Code Challenge


# Table of Contents
- [Problem Description and Solution](#problem-description-and-solution)
- [How to Run the Project](#how-to-run-the-project)

# Problem and Solution

## Problem:

Finance team needs a solution that tracks dollar price in Mexican Pesos for the current month, since the first day of the month until the fixed date given.

## Requirements:

Access via API, and output like this:

```json
    {
        "2024-06-01": "17.50",
        ...,
        "2024-06-12": "18.78"
    }
```

### Techstack

- Terraform o CloudFormation
- AWS
- Python
- SIE API
- Github

## Solution:

### Techstack:

- Cloudformation
- AWS Lambda
- AWS Gateway
- AWS S3
- Python
- SIE API Serie SF63528
- Github

The usage of AWS Lambda is for executing the code, S3 will store the binary/script, and Gateway is for execute that function via GET.

I will be add some more complexity for store sensible data or variables, like AWS secrets manager, but as the project evolves.

# How to Run the Project

Get your API token from SIE and place it in the ```Scrapper/.env```
```
    API_TOKEN=...
```

Clone the project and make build_lambda.sh executable

```bash
    chmod +x build_lambda.sh
```

Then execute lambda to build the project

```bash
    ./build_lambda.sh
```

Now you can place it into S3 or uploadit manual to lambda. (Working on cloudformation)