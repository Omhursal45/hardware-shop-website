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

class SearchTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Search Cat")
        Product.objects.create(category=self.category, name="Hammer", image="products/hammer.jpg")
        Product.objects.create(category=self.category, name="Nails", image="products/nails.jpg")
        Product.objects.create(category=self.category, name="Screwdriver", image="products/screwdriver.jpg")

    def test_products_view_search(self):
        response = self.client.get('/products/', {'q': 'hammer'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(len(products), 1)
        self.assertIn('Hammer', products[0].name)

    def test_autocomplete_endpoint(self):
        response = self.client.get('/autocomplete/', {'q': 'nail'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        names = [item['name'] for item in data]
        self.assertIn('Nails', names)

    def test_base_js_on_product_detail(self):
        drill = Product.objects.create(category=self.category, name="Drill", image="products/drill.jpg")
        resp = self.client.get(f'/products/{drill.slug}/')
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode('utf-8')
        self.assertIn('js/base.js', html)
        self.assertIn('id="search-input"', html)
        