from django.test import TestCase
from .models import Product, Category, Review


class ReviewModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Cat")
        self.product = Product.objects.create(
            category=self.category,
            name="Sample",
            image="products/sample.jpg",
        )

    def test_review_creation_and_average(self):

        self.assertEqual(self.product.average_rating, 0)
        Review.objects.create(product=self.product, rating=4)
        Review.objects.create(product=self.product, rating=2)
        self.product.refresh_from_db()
        self.assertAlmostEqual(self.product.average_rating, 3.0)
