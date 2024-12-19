from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Product
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterViewTest(APITestCase):

    def test_register_user(self):
        # Data to create a new user
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        
        # Send POST request to register
        response = self.client.post('/product/register/', data, format='json')

        # Assert that the status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User registered successfully!')


class LoginViewTest(APITestCase):

    def setUp(self):
        # Create a user for login test
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
    
    def test_login_user(self):
        # Data to log in
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }

        # Send POST request to login
        response = self.client.post('/product/login/', data, format='json')

        # Assert successful login
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])




class ProductViewTest(APITestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')

        # Create a product for testing
        self.product = Product.objects.create(name='Test Product', price=100)

    # def test_get_products(self):
    #     response = self.client.get('/product/operations/', format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)

    # def test_create_product(self):
    #     data = {'name': 'New Product', 'price': 150}
    #     response = self.client.post('/product/operations/', data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['name'], 'New Product')

    # def test_update_product(self):
    #     data = {'name': 'Updated Product', 'price': 200}
    #     response = self.client.put(f'/product/operations/{self.product.id}/', data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name'], 'Updated Product')

    # def test_delete_product(self):
    #     response = self.client.delete(f'/product/operations/{self.product.id}/', format='json')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     # Check that the product is deleted
    #     response = self.client.get(f'/product/operations/{self.product.id}/', format='json')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




class LogoutViewTest(APITestCase):

    def setUp(self):
        # Create a user for the test
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

        # Generate JWT tokens for the user
        self.tokens = self.get_tokens_for_user(self.user)
        self.headers = {
            'Authorization': f'Bearer {self.tokens["access"]}'
        }

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    # def test_logout_user(self):
    #     # Send POST request to log out
    #     response = self.client.post('/product/logout/', {}, **self.headers)

    #     # Assert that the status code is 200 OK (Successful logout response)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], 'Successfully logged out.')

    def test_logout_without_authentication(self):
        # Send POST request without the Authorization header
        response = self.client.post('/product/logout/', {}, format='json')

        # Assert that the status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
