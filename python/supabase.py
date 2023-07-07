import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client
from faker import Faker
from datetime import datetime


def add_entries_to_readings_table(supabase, readings_count):
    fake = Faker()
    foreign_key_list = []
    main_list = []
    now = datetime.utcnow()

    for i in range(readings_count):
        value = {'date_time': now, 'temperature': fake.random_int(15, 20), 'gas': fake.random_int(40, 169),
                 'humidity': fake.random_int(40, 80), 'pressure': fake.random_int(800, 1200)}
        main_list.append(value)

    data = supabase.table('Vendor').insert(main_list).execute()
    data_json = json.loads(data.json())
    data_entries = data_json['data']

    for i in range(len(data_entries)):
        foreign_key_list.append(int(data_entries[i]['vendor_id']))

    return foreign_key_list

def main():
    vendor_count = 10
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    fk_list = add_entries_to_vendor_table(supabase, vendor_count)
    for i in range(len(fk_list)):
        add_entries_to_product_table(supabase, fk_list[i])


main()
