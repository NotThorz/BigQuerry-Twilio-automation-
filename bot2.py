# Import the necessary libraries
# Import the BigQuery and logging libraries from the google.cloud package
# Import the Credentials class from the google.oauth2.service_account package to authenticate and authorize the application to access the BigQuery API
# Import the Client class from the twilio.rest package to initialize the Twilio API client
from google.cloud import bigquery
import logging
from google.oauth2.service_account import Credentials
from twilio.rest import Client
import time


def send_twilio_message(total_revenue, ecommerce_purchases, phone_number):
    """
    Sends a WhatsApp message using the Twilio API client.
    """
    # Initialize the Twilio API client
    # Replace YOUR_API_KEY and YOUR_API_SECRET with my API key and secret
    # Use the Client() function to create a Twilio client object, passing in the API key and secret as arguments
    # Use a try-except block to catch any exceptions that may occur when initializing the client
    try:
        # change with the SID and secret
        twilio_client = Client(
            'YOUR_API_KEY', 'YOUR_API_SECRET')  # replace this
    except Exception as e:
        logging.error("Error initializing Twilio client: {}".format(e))

    try:
        body = 'Your total revenue of today is {} , and the total purchases are {}'.format(
            total_revenue, ecommerce_purchases)
        # chaneg the twilio whatsApp number with yours
        from_ = 'whatsapp:+TWILIO_WHATSAPP_NUMBER'  # replace this
        to = 'whatsapp:+{}'.format(phone_number)
        twilio_client.messages.create(to=to, from_=from_, body=body)
    except Exception as e:
        logging.error("Error sending WhatsApp message: {}".format(e))


def get_bigquery_data(phone_number, paths_and_ids, table_mapping, result):
    """
    Retrieves data from the BigQuery API using the specified client object.
    Returns the total revenue and number of ecommerce purchases.
    """
    # Authenticate and authorize my application to access the BigQuery API
    # Replace path_to_key_file with the path to my private key file
    # Replace YOUR_PROJECT_ID with the ID of my Google Cloud project
    # Use the Credentials.from_service_account_file() function to read the service account key from the specified file
    # Use the bigquery.Client() function to create a BigQuery client object, passing in the project ID and credentials as arguments
    # Use a try-except block to catch any exceptions that may occur when authenticating and authorizing the application
    try:
        creds = Credentials.from_service_account_file(paths_and_ids[result])
        client = bigquery.Client(project=result, credentials=creds)
    except Exception as e:
        logging.error(
            "Error authenticating and authorizing BigQuery client: {}".format(e))

    try:

        # Use the .format() method to insert the current client's table name into the SELECT query
        query = 'SELECT SUM(ecommerce.purchase_revenue) as total_revenue, COUNT(event_name) as ecommerce_purchases FROM `{}`where event_name = "purchase" '.format(
            table_mapping[phone_number])
        query_job = client.query(query)
        results = query_job.result()
        if results:
            total_revenue = results[0]['total_revenue']
            ecommerce_purchases = results[0]['ecommerce_purchases']
        else:
            total_revenue = 0
            ecommerce_purchases = 0
        return total_revenue, ecommerce_purchases
        # for row in query_job:
        #   total_revenue = row['total_revenue']
        #  ecommerce_purchases = row['ecommerce_purchases']
        # return total_revenue, ecommerce_purchases
    except Exception as e:
        logging.error("Error retrieving data from BigQuery: {}".format(e))
        return 0, 0


def main():
    """
    The main function of the script.
    Loops over each client in the table_mapping dictionary and retrieves data from BigQuery for each client.
    Sends a WhatsApp message to each client using the Twilio API.
    """

    # Set up logging to capture any errors that occur
    # Use the logging.basicConfig() function to set the format and level of the log messages
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.ERROR)

    # Create a dictionary that maps client phone numbers to table names
    # The dictionary maps phone numbers to table names in the BigQuery dataset
    # Each key is a phone number in string format, and each value is the name of a table in the dataset
    table_mapping = {
        '+1234567890': 'simoahava-com.analytics_206575074.events_intraday_',
        # change these with real numbers of client
        '+0987654321': 'snappy-storm-356014.analytics_319624014.events_intraday_',
        '11111111111': 'intraday_table_3'
    }

    paths_and_ids = {
        # replace the path with the path to the JSON should be something like this C:/user/pc/key.json .
        'simoahava-com': r'path_to_key_file',
        'snappy-storm-356014': r'path_to_key_file',
        'myofer---prod': r'path_to_key_file'
    }
    print("Script is running ..\n")
    # Loop over each client and their phone numbers
    # Use the .keys() method to get a list of phone numbers from the table_mapping dictionary
    for phone_number in table_mapping.keys():
        result = table_mapping[phone_number].split('.')[0]
        # Retrieve the data for the current client based on his phone number
        total_revenue, ecommerce_purchases = get_bigquery_data(phone_number, paths_and_ids,
                                                               table_mapping, result)
        # Send the message using Twilio
        send_twilio_message(total_revenue, ecommerce_purchases,
                            phone_number)
    # time.sleep(84600)


# Call the main function when the script is running
if __name__ == "__main__":
    main()
