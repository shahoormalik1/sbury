import argparse
import glob
import pandas.io.parsers
from datetime import date


def read_csv(csv_location: str):
    return pandas.read_csv(csv_location, header=0)


def read_json_folder(json_folder: str):
    transactions_files = glob.glob("{}*/*.json".format(json_folder))

    return pandas.concat(pandas.read_json(tf, lines=True) for tf in transactions_files)


def derive_basket_items(transactions_df):
    basket_df = pandas.DataFrame({})

    for index, row in transactions_df.iterrows():

        basket_items = row['basket']

        for basket_item in basket_items:
            basket_item['customer_id'] = row['customer_id']

            basket_df = basket_df.append(basket_item, ignore_index=True)


    return basket_df


def generate_purchase_counts(basket_df, products_df, customers_df):
    all_data = pandas.merge(basket_df, products_df, how='left', on='product_id').\
                        merge(customers_df, how='left', on='customer_id')

    group_by = ['customer_id', 'loyalty_score', 'product_id', 'product_category']

    purchase_counts = all_data.groupby(group_by).size().reset_index().rename(columns={0: 'purchase_count'})

    return purchase_counts


def run_transformations(customers_location: str, products_location: str,
                        transactions_location: str, output_location: str):
    customers_df = read_csv(customers_location)
    products_df = read_csv(products_location)
    transactions_df = read_json_folder(transactions_location)

    return customers_df, products_df, transactions_df


def get_latest_transaction_date(transactions):
    latest_purchase = transactions.date_of_purchase.max()
    latest_transaction = transactions[transactions.date_of_purchase == latest_purchase]
    return latest_transaction


def to_canonical_date_str(date_to_transform):
    return date_to_transform.strftime('%Y-%m-%d')


def output_file(output_df, output_path):

    d = to_canonical_date_str(date.today())
    output_df.to_csv(output_path + f'purchase_counts_{d}.csv', index=False)

    print('complete')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='DataTest')
    parser.add_argument('--customers_location', required=False, default="./input_data/starter/customers.csv")
    parser.add_argument('--products_location', required=False, default="./input_data/starter/products.csv")
    parser.add_argument('--transactions_location', required=False, default="./input_data/starter/transactions/")
    parser.add_argument('--output_location', required=False, default="./output_data/outputs/")
    args = vars(parser.parse_args())

    customers, products, transactions = run_transformations(args['customers_location'], args['products_location'],
                        args['transactions_location'], args['output_location'])

    basket_df = derive_basket_items(transactions)

    purchase_counts = generate_purchase_counts(basket_df, products, customers)

    output_file(purchase_counts, args['output_location'])


