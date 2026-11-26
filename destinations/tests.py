from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from accommodations.models import Accommodation
from community.models import TravelStory
from community.tasks import send_new_story_email
from destinations.models import Destination
from producers.models import Producer
from django.db import IntegrityError, transaction

User = get_user_model()


class RodopiteOtBlizoTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='ivan',
            email='ivan@example.com',
            password='StrongPassword123!',
        )
        self.user2 = User.objects.create_user(
            username='maria',
            email='maria@example.com',
            password='StrongPassword123!',
        )
        self.destination = Destination.objects.create(
            name='Дяволското гърло',
            category='cave',
            difficulty='easy',
            region='Смолян',
            description='Една от най-известните пропастни пещери в Родопите.',
            author=self.user1,
        )

    def test_01_custom_user_created_with_unique_email(self):
        self.assertEqual(self.user1.email, 'ivan@example.com')
        self.assertEqual(User.objects.count(), 2)

    def test_02_user_profile_exists_for_user(self):
        self.assertTrue(hasattr(self.user1, 'profile'))
        self.assertEqual(self.user1.profile.user, self.user1)

    def test_03_duplicate_email_raises_error(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    username='ivan_clone',
                    email='ivan@example.com',
                    password='StrongPassword123!',
                )

    def test_04_destination_short_description_fails_validation(self):
        dest = Destination(
            name='Кратък текст',
            category='peak',
            difficulty='moderate',
            region='Смолян',
            description='Кратко',
            author=self.user1,
        )
        with self.assertRaises(ValidationError):
            dest.full_clean()

    def test_05_destination_str_representation(self):
        self.assertEqual(str(self.destination), 'Дяволското гърло')

    def test_06_accommodation_creation_and_nearby_destinations(self):
        acc = Accommodation.objects.create(
            name='Родопски уют',
            accommodation_type='guest_house',
            region='Триград',
            price_per_night=Decimal('95.00'),
            capacity=10,
            description='Уютна къща за гости близо до пещерата.',
            owner=self.user1,
        )
        acc.nearby_destinations.add(self.destination)
        self.assertEqual(acc.capacity, 10)
        self.assertIn(self.destination, acc.nearby_destinations.all())

    def test_07_producer_creation_and_str(self):
        producer = Producer.objects.create(
            name='Мед от Родопите',
            product_type='honey',
            region='Чепеларе',
            phone='+359888111222',
            description='Натурален горски мед от високопланински райони.',
            owner=self.user1,
        )
        self.assertIn('Чепеларе', str(producer))

    def test_08_story_creation_and_total_likes(self):
        story = TravelStory.objects.create(
            title='Уикенд в Триградското ждрело',
            content='Страхотна разходка сред скали и чист въздух.',
            author=self.user1,
            destination=self.destination,
        )
        story.likes.add(self.user2)
        self.assertEqual(story.total_likes(), 1)

    def test_09_user_favorite_destinations_m2m(self):
        self.user2.profile.favorite_destinations.add(self.destination)
        self.assertIn(self.destination, self.user2.profile.favorite_destinations.all())

    def test_10_api_destinations_public_get(self):
        client = APIClient()
        response = client.get(reverse('api-destinations'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_11_api_destinations_filter_by_region(self):
        client = APIClient()
        response = client.get(reverse('api-destinations'), {'region': 'Смолян'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        no_match = client.get(reverse('api-destinations'), {'region': 'Варна'})
        self.assertEqual(no_match.status_code, 200)
        self.assertEqual(len(no_match.data), 0)

    def test_12_api_destinations_post_requires_authentication(self):
        client = APIClient()
        response = client.post(
            reverse('api-destinations'),
            {
                'name': 'Орлово око',
                'category': 'peak',
                'difficulty': 'hard',
                'region': 'Ягодина',
                'description': 'Панорамна площадка с невероятна гледка.',
            },
            format='json',
        )
        self.assertIn(response.status_code, [401, 403])

    def test_13_api_destinations_post_authenticated_creates_object(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.post(
            reverse('api-destinations'),
            {
                'name': 'Орлово око',
                'category': 'peak',
                'difficulty': 'hard',
                'region': 'Ягодина',
                'description': 'Панорамна площадка с невероятна гледка.',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Destination.objects.count(), 2)

    def test_14_celery_send_new_story_email_task(self):
        result = send_new_story_email(
            'Уикенд в Триградското ждрело',
            'ivan',
            'maria@example.com',
        )
        self.assertTrue(result)

    def test_15_missing_page_returns_404(self):
        response = self.client.get('/nesushtestvuvasht-url-za-test/')
        self.assertEqual(response.status_code, 404)



    def test_16_other_user_cannot_edit_destination(self):
        self.client.force_login(self.user2)

        response = self.client.get(
            reverse('destination-edit', kwargs={'pk': self.destination.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_17_other_user_cannot_delete_destination(self):
        self.client.force_login(self.user2)

        response = self.client.get(
            reverse('destination-delete', kwargs={'pk': self.destination.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_18_owner_can_edit_destination(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse('destination-edit', kwargs={'pk': self.destination.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_19_owner_can_delete_destination(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse('destination-delete', kwargs={'pk': self.destination.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Destination.objects.filter(pk=self.destination.pk).exists()
        )
