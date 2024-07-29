from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    def setUp(self):
        """Set up test client, admin user, and regular user."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_fieldsets(self):
        """Test that the fieldsets are correct"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertContains(res, 'Personal Info')
        self.assertContains(res, 'Permissions')
        self.assertContains(res, 'Important dates')

    def test_user_add_fieldsets(self):
        """Test that the add fieldsets are correct"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertContains(res, 'email')
        self.assertContains(res, 'password1')
        self.assertContains(res, 'password2')
        self.assertNotContains(res, 'Username')  # Ensure username field is not present