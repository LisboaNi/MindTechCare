from django.test import TestCase
from validations.validators import validate_cnpj, encrypt_password

class ValidationTests(TestCase):

    def test_valid_cnpj(self):
        valid_cnpj = '33.779.971/0001-30'
        invalid_cnpj = '12.345.678/0001-00'  
        self.assertTrue(validate_cnpj(valid_cnpj))
        self.assertFalse(validate_cnpj(invalid_cnpj))
        
    def test_encrypt_password(self):
        password = 'my_secret_password'
        encrypted_password = encrypt_password(password)
        self.assertNotEqual(password, encrypted_password)  
