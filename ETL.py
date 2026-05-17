import pandas as pd
import sqlalchemy as sa

oltp_engine = sa.create_engine()
dw_engine = sa.create_engine()

def run_etl_pipeline():
    print("=== Starting Movie Rental ETL Process ===")

    print("\n1. Extracting data from OLTP...")
    df_customer_raw = pd.read_sql("SELECT * FROM customer", oltp_engine)
    df_rental_raw = pd.read_sql("SELECT * FROM rental", oltp_engine)
    df_payment_raw = pd.read_sql("SELECT * FROM payment", oltp_engine)
    df_film_raw = pd.read_sql("SELECT * FROM film", oltp_engine)
    df_store_raw = pd.read_sql("SELECT * FROM store", oltp_engine)

    print("\n2. Transforming data...")
    
    df_dim_customer = df_customer_raw.copy()
    df_dim_customer['full_name'] = df_dim_customer['first_name'] + " " + df_dim_customer['last_name']
    df_dim_customer = df_dim_customer[['customer_id', 'first_name', 'last_name', 'full_name', 'email']]
    
    df_rental_raw['return_date'] = df_rental_raw['return_date'].fillna(pd.Timestamp('1970-01-01'))
    
    df_rental_clean = df_rental_raw[df_rental_raw['return_date'] >= df_rental_raw['rental_date']]
    
    df_rental_clean['rental_duration_days'] = (df_rental_clean['return_date'] - df_rental_clean['rental_date']).dt.days

    print("\n3. Loading data into Data Warehouse...")
    
    df_dim_customer.to_sql(name='Dim_Customer', con=dw_engine, if_exists='append', index=False)
    print("- Loaded Dim_Customer successfully.")

    df_film_columns = df_film_raw[['film_id', 'title', 'description', 'release_year', 'rental_rate']]
    df_film_columns.to_sql(name='Dim_Film', con=dw_engine, if_exists='append', index=False)
    print("- Loaded Dim_Film successfully.")

    df_store_columns = df_store_raw[['store_id']]
    df_store_columns.to_sql(name='Dim_Store', con=dw_engine, if_exists='append', index=False)
    print("- Loaded Dim_Store successfully.")

    df_fact_merged = pd.merge(df_rental_clean, df_payment_raw, on='rental_id', how='inner')
    
    df_fact_final = pd.DataFrame()
    df_fact_final['customer_key'] = df_fact_merged['customer_id_x']
    df_fact_final['film_key'] = df_fact_merged['customer_id_y']
    df_fact_final['payment_amount'] = df_fact_merged['amount']
    df_fact_final['rental_duration_days'] = df_fact_merged['rental_duration_days']
    df_fact_final['rental_count'] = 1
    
    df_fact_final.to_sql(name='Fact_Rental_Payment', con=dw_engine, if_exists='append', index=False)
    print("- Loaded Fact_Rental_Payment successfully.")

    print("\n=== ETL Process Completed Successfully! ===")

if __name__ == "__main__":
    run_etl_pipeline()