import sys
import boto3
import pandas as pd
from sqlalchemy import create_engine
from botocore.config import Config

csvFile=sys.argv[1]
dbIdentifier=sys.argv[2]
mysqlUser=sys.argv[3]
mysqlPass=sys.argv[4]

my_config = Config(
    region_name = 'us-east-1'
)

def csv_to_mysql(csv_path, table_name, mysql_user, mysql_password, mysql_host, mysql_port, mysql_database="mydb"):
        # read CSV file into pandas DataFrame
        df = pd.read_csv(csv_path)

        # create database connection using sqlalchemy
        engine = create_engine(f"mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}")
        # write DataFrame to MySQL database
        df.to_sql(table_name, engine, if_exists='replace', index=False)

def get_rds_endpoint(db_identifier):
        rds_client = boto3.client('rds',config=my_config)
        response = rds_client.describe_db_instances(DBInstanceIdentifier=db_identifier)
        if len(response['DBInstances']) == 0:
          return None
        db_instance = response['DBInstances'][0]
        endpoint = db_instance['Endpoint']['Address']
        return endpoint



endpoint = get_rds_endpoint(dbIdentifier)
csv_to_mysql(csvFile,"drivers",mysqlUser,mysqlPass,endpoint,3306,"mydb")

