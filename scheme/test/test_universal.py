import pandas as pd
import unittest
import os

from scheme import Universal
from datasets import *


class TestNBNNScheme(unittest.TestCase):
    def test_insertion(self):
        """Test that insertion changes the fingerprinted data set"""
        # todo: the algorithm fails for <2 attributes
        data = pd.DataFrame({'Id': [i for i in range(6)],
                             'Attr1': ['blue', 'red', 'blue', 'blue', 'yellow', 'red'],
                             'Attr2': ['yes', 'no', 'no', 'no', 'yes', 'yes']})
        scheme = NBNNScheme(gamma=1, secret_key=7, fingerprint_bit_length=8, k=3, number_of_recipients=3, xi=2)
        fingerprinted_data = scheme.insertion(data, 0)
        self.assertFalse(data.equals(fingerprinted_data))

    def test_detection(self):
        data = 'german_credit_full'  # fails for small (150 rows, 11 columns) datasets
        scheme = NBNNScheme(gamma=1, secret_key=7, fingerprint_bit_length=8, k=3, number_of_recipients=3, xi=2)
        fingerprinted_data = scheme.insertion(data, 0)

        suspect_id = scheme.detection(fingerprinted_data)
        print(suspect_id)
        self.assertEqual(0, suspect_id)

    def test_fingerprint_len(self):
        """Test the lentgth of the fingerpprint"""
        bit_len = 32
        base_scheme = NBNNScheme(fingerprint_bit_length=bit_len)
        fingerprint = base_scheme.create_fingerprint(0)
        self.assertEqual(len(fingerprint), bit_len)


class TestBNNScheme(unittest.TestCase):
    def test_insertion(self):
        data = pd.DataFrame({'Id': [i for i in range(6)],
                             'Attr1': ['blue', 'red', 'blue', 'blue', 'yellow', 'red'],
                             'Attr2': ['yes', 'no', 'no', 'no', 'yes', 'yes']})
        scheme = BNNScheme(gamma=1, secret_key=7, fingerprint_bit_length=8, k=3, number_of_recipients=3, xi=2)
        fingerprinted_data = scheme.insertion(data, 0)
        print(fingerprinted_data)
        self.assertFalse(data.equals(fingerprinted_data))

    def test_detection_medium_dataset(self):
        data = 'german_credit_full'  # fails for small (150 rows, 11 columns) datasets
        scheme = BNNScheme(gamma=1, secret_key=7, fingerprint_bit_length=8, k=3, number_of_recipients=3, xi=2)
        fingerprinted_data = scheme.insertion(data, 0)

        suspect_id = scheme.detection(fingerprinted_data)
        print(suspect_id)
        self.assertEqual(0, suspect_id)

    def test_detection_very_small_dataset(self):
        data = 'german_credit_sample'  # fails for small (150 rows, 11 columns) datasets
        scheme = BNNScheme(gamma=1, secret_key=7, fingerprint_bit_length=8, k=3, number_of_recipients=3, xi=2)
        fingerprinted_data = scheme.insertion(data, 0)

        suspect_id = scheme.detection(fingerprinted_data)
        print(suspect_id)
        self.assertEqual(0, suspect_id)

    def test_detection_small_dataset(self):
        data = 'german_credit_medium_sample'
        scheme = BNNScheme(gamma=1, secret_key=7, fingerprint_bit_length=8, k=3, number_of_recipients=3, xi=2)
        fingerprinted_data = scheme.insertion(data, 0)

        suspect_id = scheme.detection(fingerprinted_data)
        print(suspect_id)
        self.assertEqual(0, suspect_id)

    def test_detection_adult_data(self):
        data = 'adult_full'
        scheme = BNNScheme(gamma=5, secret_key=7, fingerprint_bit_length=16, k=3, number_of_recipients=3, xi=2)
        fingerprinted_data = scheme.insertion(data, 0)

        suspect_id = scheme.detection(fingerprinted_data)
        print(suspect_id)
        self.assertEqual(0, suspect_id)

    def test_detection_breast_cancer(self):
        data = 'breast_cancer_full'
        scheme = BNNScheme(gamma=2, secret_key=7, fingerprint_bit_length=8, k=3, number_of_recipients=3, xi=2)
        fingerprinted_data = scheme.insertion(data, 0)

        suspect_id = scheme.detection(fingerprinted_data)
        print(suspect_id)
        self.assertEqual(0, suspect_id)

    def test_detection_mushrooms(self):
        data = 'mushrooms_full'
        scheme = BNNScheme(gamma=2, secret_key=7, fingerprint_bit_length=8, k=3, number_of_recipients=3, xi=2)
        fingerprinted_data = scheme.insertion(data, 0)

        suspect_id = scheme.detection(fingerprinted_data)
        print(suspect_id)
        self.assertEqual(0, suspect_id)

    def test_detection_nursery(self):
        data = 'nursery_full'
        scheme = BNNScheme(gamma=2, secret_key=7, fingerprint_bit_length=16, k=3, number_of_recipients=3, xi=2)
        fingerprinted_data = scheme.insertion(data, 0)

        suspect_id = scheme.detection(fingerprinted_data)
        print(suspect_id)
        self.assertEqual(0, suspect_id)


class TestUniversal(unittest.TestCase):
    def test_insertion_path(self):
        scheme = Universal(gamma=2)
        secret_key = 123
        recipient = 0
        data = '../../datasets/german_credit_sample.csv'
        fingerprinted = scheme.insertion(data, recipient, secret_key)
        # suspect = scheme.detection(fingerprinted, secret_key)
        self.assertIsNotNone(fingerprinted)

    def test_insert_and_save(self):
        scheme = Universal(gamma=2)
        secret_key = 123
        recipient = 0
        data = '../../datasets/german_credit_sample.csv'
        fingerprinted = scheme.insertion(data, recipient, secret_key, save=True)
        # suspect = scheme.detection(fingerprinted, secret_key)
        self.assertIsNotNone(fingerprinted)

    def test_detection_path(self):
        scheme = Universal(gamma=2, fingerprint_bit_length=8)
        secret_key = 123
        recipient = 0
        data = '../../datasets/german_credit_sample.csv'
        fingerprinted = scheme.insertion(data, recipient, secret_key)
        suspect = scheme.detection(fingerprinted, secret_key)
        self.assertEqual(recipient, suspect)

    def test_detection_2(self):
        scheme = Universal(gamma=2)
        secret_key = 123
        recipient = 0
        data = '../../datasets/adult.csv'
        fingerprinted = scheme.insertion(data, recipient, secret_key)
        suspect = scheme.detection(fingerprinted, secret_key)
        self.assertEqual(recipient, suspect)

    def test_insert_and_save_custom(self):
        scheme = Universal(gamma=2)
        secret_key = 123
        recipient = 0
        data = '../../datasets/german_credit_sample.csv'
        outfile = "fingerprinted/gc.csv"
        scheme.insertion(data, recipient, secret_key, write_to=outfile)
        self.assertTrue(os.path.isfile(outfile))
        os.remove(outfile)

    def test_decimal_data(self):
        scheme = Universal(gamma=2)
        secret_key = 123
        recipient = 0
        data = '../../datasets/abalone_data.csv'
        outfile = "fingerprinted/abalone.csv"
        scheme.insertion(data, recipient, secret_key, write_to=outfile)
        self.assertTrue(os.path.isfile(outfile))

    def test_numerical_data(self):
        scheme = Universal(gamma=2)
        secret_key = 123
        recipient = 0
        data = '../../datasets/breast_cancer_wisconsin.csv'
        outfile = "fingerprinted/breast_cancer_wisconsin.csv"
        scheme.insertion(data, recipient, secret_key, write_to=outfile)
        self.assertTrue(os.path.isfile(outfile))

    def test_decimal_detection(self):
        scheme = Universal(gamma=2, fingerprint_bit_length=128)
        secret_key = 123
        recipient = 0
        data = '../../datasets/abalone_data.csv'
        fp_data = scheme.insertion(data, recipient, secret_key)
        suspect = scheme.detection(fp_data, secret_key)
        self.assertEqual(suspect, recipient)

    def test_decimal_detection_2(self):
        scheme = Universal(gamma=2, fingerprint_bit_length=32)
        secret_key = 123
        recipient = 0
        data = '../../datasets/insurance.csv'
        fp_data = scheme.insertion(data, recipient, secret_key)
        suspect = scheme.detection(fp_data, secret_key)
        self.assertEqual(suspect, recipient)

    def test_subset_decimal(self):
        scheme = Universal(gamma=5, fingerprint_bit_length=8)
        secret_key = 123
        recipient = 0
        data = '../../datasets/insurance.csv'
        fp_data = scheme.insertion(data, recipient, secret_key, include=['bmi', 'age', 'charges'])
        suspect = scheme.detection(fp_data, secret_key, include=['bmi', 'age', 'charges'])
        self.assertEqual(suspect, recipient)

    def test_insurance_default(self):
        scheme = Universal(gamma=1)
        secret_key = 123
        recipient = 0
        data = '../../datasets/insurance.csv'
        fp_data = scheme.insertion(data, recipient, secret_key)
        suspect = scheme.detection(fp_data, secret_key)
        self.assertEqual(suspect, recipient)

    def test_insurance(self):
        scheme = Universal(gamma=10, fingerprint_bit_length=16)
        secret_key = 1234
        recipient = 0
        data = '../../datasets/insurance.csv'
        fp_data = scheme.insertion(data, recipient, secret_key, write_to='fingerprinted/insurance.csv')

        suspect = scheme.detection(fp_data, secret_key)
        self.assertEqual(suspect, recipient)

    def test_bank_personal_loan_modelling(self):
        scheme = Universal(gamma=10, fingerprint_bit_length=16)
        secret_key = 1234
        recipient = 0
        data = '../../datasets/Bank_Personal_Loan_Modelling.csv'
        fp_data = scheme.insertion(data, recipient, secret_key)

        suspect = scheme.detection(fp_data, secret_key)
        self.assertEqual(suspect, recipient)
