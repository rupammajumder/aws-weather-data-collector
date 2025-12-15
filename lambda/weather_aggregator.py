import boto3
import json
import pandas as pd
import os
from datetime import datetime, timedelta
s3 = boto3.client('s3')
bucket_name = 'demobucketfordemoproject01'  
prefix = 'dailyreport/'  
output_prefix = 'aggregated-weather-reports/weekly_report/'
def lambda_handler(event, context):
   # Calculate the date range (last 4 day)
   now = datetime.utcnow()
   lastfourrday = now - timedelta(days=4)
   # List all objects in the S3 folder
   response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
   json_data = []
   for obj in response.get('Contents', []):
       key = obj['Key']
       last_modified = obj['LastModified']
       # Filter files modified in the last four days
       if last_modified.replace(tzinfo=None) >= lastfourrday:
           file_obj = s3.get_object(Bucket=bucket_name, Key=key)
           body = file_obj['Body'].read()
           try:
               data = json.loads(body)
               # Assume each file contains a list or dict of records
               if isinstance(data, list):
                   json_data.extend(data)
               else:
                   json_data.append(data)
           except Exception as e:
               print(f"Error reading JSON from {key}: {e}")
   # Convert to DataFrame and write to CSV
   if json_data:
       df = pd.DataFrame(json_data)
       csv_path = "/tmp/combined_data.csv"
       df.to_csv(csv_path, index=False)  # No index column in output
       # Upload to S3
       output_key = f"{output_prefix}combined_data_{now.strftime('%Y%m%d%H%M%S')}.csv"
       s3.upload_file(csv_path, bucket_name, output_key)
       return {
           'statusCode': 200,
           'body': f"CSV file uploaded to {output_key}"
       }
   else:
       return {
           'statusCode': 204,
           'body': "No JSON data found in the last 24 hours."
       }