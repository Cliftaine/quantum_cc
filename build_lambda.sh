#!/bin/bash

# Create the directory scrapper_lambda
mkdir scrapper_lambda/

# Copy Python libraries to scrapper_lambda
cp -r Scrapper/python_libs/* scrapper_lambda/

# Copy the Lambda function to scrapper_lambda
cp Scrapper/lambda_function.py scrapper_lambda/

# Copy the .env to scrapper_lambda
cp Scrapper/.env scrapper_lambda/

# Navigate to the scrapper_lambda directory
cd scrapper_lambda

# Create a ZIP file with the contents of the directory
zip -r scrapper_lambda.zip .

# Go back to the previous directory
cd ..

# Copy the ZIP file to the main directory
cp scrapper_lambda/scrapper_lambda.zip scrapper_lambda.zip

# Remove the scrapper_lambda directory
rm -r scrapper_lambda
