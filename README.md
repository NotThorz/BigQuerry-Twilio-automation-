# BigQuerry-Twilio-automation-

This script is designed to retrieve data from a BigQuery database and send a WhatsApp message to a specified phone number using the Twilio API. The script is set up to loop over each client in a table_mapping dictionary and retrieve data from BigQuery for each client. It then sends a WhatsApp message to each client using the Twilio API, reporting on the total revenue and number of ecommerce purchases. The script is set up to handle any errors that may occur, logging any errors that occur during the execution of the script. The script requires the following dependencies to be installed: google.cloud, google.oauth2.service_account, twilio.rest.
