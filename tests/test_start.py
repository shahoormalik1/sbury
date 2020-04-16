import pandas
import unittest
from solution_start import get_latest_transaction_date
from solution_start import derive_basket_items, generate_purchase_counts


class TestStart(unittest.TestCase):

    def test_get_latest_transaction_date_returns_most_recent_date(self):
        transactions_df = pandas.concat(
            [
                pandas.read_json(
                    "{\"customer_id\": \"C6\", \"basket\": [{\"product_id\": \"P53\", \"price\": 476}, {\"product_id\": \"P42\", \"price\": 1937}, {\"product_id\": \"P43\", \"price\": 1019}], \"date_of_purchase\": \"2018-12-03 17:52:00\"}"),
                pandas.read_json(
                    "{\"customer_id\": \"C125\", \"basket\": [{\"product_id\": \"P28\", \"price\": 1752}], \"date_of_purchase\": \"2019-01-27 08:23:00\"}"),
                pandas.read_json(
                    "{\"customer_id\": \"C76\", \"basket\": [{\"product_id\": \"P39\", \"price\": 1033}], \"date_of_purchase\": \"2019-02-27 13:55:00\"}")
            ]
        )

        result = get_latest_transaction_date(transactions_df)

        self.assertEqual(result.date_of_purchase[0], "2019-02-27 13:55:00")

    def test_derive_basket_items(self):
        test_transactions = pandas.read_json('./test_transactions.json', lines=True)

        basket_items = derive_basket_items(test_transactions)

        customer_to_count = 'C135'

        count_customer = basket_items[basket_items['customer_id'] == customer_to_count].shape[0]

        count_rows = basket_items.shape[0]

        self.assertEqual(count_rows, 11)
        self.assertEqual(count_customer, 3)

    def test_generate_purchase_counts(self):
        test_t = pandas.read_json('./test_transactions.json', lines=True)
        test_c = pandas.read_csv('./test_customers.csv', header=0)
        test_p = pandas.read_csv('./test_products.csv', header=0)

        basket_items = derive_basket_items(test_t)

        purchase_counts = generate_purchase_counts(basket_items, test_p, test_c)

        row_count = purchase_counts.shape[0]
        c122_count = purchase_counts[purchase_counts['customer_id'] == 'C122']['purchase_count'].values[0]
        c104_count = purchase_counts[purchase_counts['customer_id'] == 'C104']['purchase_count'].values[0]

        self.assertEqual(row_count, 5)
        self.assertEqual(c122_count, 2)
        self.assertEqual(c104_count, 1)


if __name__ == '__main__':
    unittest.main()