import boto3
import os
import sys
import time

def create_payments_table():
    aws_region = os.getenv("AWS_REGION", "ap-southeast-1")
    ddb_endpoint = os.getenv("DDB_ENDPOINT", "http://localhost:8000")
    table_name = os.getenv("DYNAMODB_PAYMENTS_TABLE", "lea-payments-local")
    
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=aws_region,
        endpoint_url=ddb_endpoint,
        aws_access_key_id='dummy',
        aws_secret_access_key='dummy'
    )
    
    try:
        existing_table = dynamodb.Table(table_name)
        existing_table.load()
        print(f"Table {table_name} already exists")
        return
    except:
        pass
    
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'payment_intent_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'payment_intent_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'quote_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'stripe_session_id',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user_id-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'user_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'quote_id-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'quote_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'stripe_session_id-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'stripe_session_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            BillingMode='PAY_PER_REQUEST',
            StreamSpecification={
                'StreamEnabled': True,
                'StreamViewType': 'NEW_AND_OLD_IMAGES'
            }
        )
        
        print(f"Creating table {table_name}...")
        table.wait_until_exists()
        print(f"Table {table_name} created successfully!")
        
        print("Table description:")
        print(f"  - Table name: {table.table_name}")
        print(f"  - Table status: {table.table_status}")
        print(f"  - Item count: {table.item_count}")
        
    except Exception as e:
        print(f"Error creating table: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_payments_table()

