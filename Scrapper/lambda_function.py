"""
Technical test for Quantum.

AWS Lambda function that returns a JSON object with historical USD to MXN
exchange rates from a given date to the first day of the month. Data is 
retrieved from an API, processed, and returned as a dictionary with dates 
as keys and formatted rates as values. 

Author:
    Javier Duran Vega

Functions:
    - get_range_dates: Calculates start and end dates for the given range.
    - get_usd: Fetches USD to MXN rates from an API for the specified range.
    - make_json: Converts API response to a dictionary with dates and rates.
    - lambda_handler: AWS Lambda function that returns exchange rate data in JSON.
"""

from typing import Tuple, Dict, Union
import datetime
import os
import json
import requests
from dotenv import load_dotenv

def get_range_dates(
    input_date: str,
    input_format: str = "%d/%m/%Y",
    sie_format: str = "%Y-%m-%d"
) -> Tuple[str, str]:
    """
    Calculate the start and end dates from the input date.

    Args:
        input_date (str): The input date in the specified format.
        input_format (str): The format of the input date.
        sie_format (str): The format for the output dates.

    Returns:
        Tuple[str, str]: A tuple containing the first and last date of the month.
    """
    input_datetime = datetime.datetime.strptime(input_date, input_format)
    end_date = input_datetime.strftime(sie_format)
    first_date = input_datetime.replace(day=1).strftime(sie_format)

    return first_date, end_date

def get_usd(start_date: str, end_date: str) -> Union[str, Tuple[None, str]]:
    """
    Fetch USD data from the API for the given date range.

    Args:
        start_date (str): The start date in the format YYYY-MM-DD.
        end_date (str): The end date in the format YYYY-MM-DD.

    Returns:
        Union[str, Tuple[None, str]]: The response body if successful, 
        or a tuple with None and an error message.
    """
    base_url = os.environ.get("BASE_URL")
    api_token = os.environ.get("API_TOKEN")

    url = f"{base_url}/{start_date}/{end_date}"
    headers = {
        "Bmx-Token": api_token,
        "Accept-Encoding": "gzip"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return None, f"Error: {response.status_code}"

    return response.content.decode('utf-8')

def make_json(body: str) -> Dict[str, str]:
    """
    Convert the API response body into a dictionary with dates as keys.

    Args:
        body (str): The API response body in JSON format.

    Returns:
        Dict[str, str]: A dictionary with dates as keys and formatted USD data as values.
    """
    data = json.loads(body)
    result = {}

    for item in data["bmx"]["series"][0]["datos"]:
        result[item["fecha"]] = f"{float(item['dato']):.2f}"

    return result

def lambda_handler(event: dict, context: object) -> dict: # pylint: disable=unused-argument
    """
    AWS Lambda handler function to process the event and return the result.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (object): The context object containing runtime information.

    Returns:
        dict: The response object with status code and body.
    """
    input_date = (event.get('queryStringParameters', {}).get('inputDate')
                    if 'queryStringParameters' in event
                    else None
                )

    if not input_date:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing query parameter: inputDate')
        }

    load_dotenv()
    start_date, end_date = get_range_dates(input_date)
    usd_data = get_usd(start_date, end_date)

    if isinstance(usd_data, tuple):
        return {
            'statusCode': 500,
            'body': json.dumps(usd_data[1])
        }

    json_res = make_json(usd_data)

    return {
        'statusCode': 200,
        'body': json.dumps(json_res)
    }
