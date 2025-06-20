from django.test import TestCase
from decimal import Decimal
from django.contrib.auth import get_user_model

from store.models import Product, ProductVariation, Order, OrderItem

User = get_user_model()

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='TestProduct',
            brand='TestBrand',
            size='50ml',
            price=Decimal('20.00'),
            quantity=5
        )

    def test_str(self):
        self.assertEqual(str(self.product), 'TestBrand - TestProduct')

    def test_get_skin_conditions_list(self):
        self.product.skin_condition = 'acne, redness'
        self.product.save()
        self.assertListEqual(
            self.product.get_skin_conditions_list(),
            ['acne', 'redness']
        )

    def test_is_in_stock(self):
        self.assertTrue(self.product.is_in_stock)
        self.product.quantity = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock)

class ProductVariationModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='PVTest',
            brand='BrandX',
            size='10ml',
            price=Decimal('5.00'),
            quantity=0
        )
        self.variation = ProductVariation.objects.create(
            product=self.product,
            variation_code='V1',
            quantity=3
        )

    def test_str(self):
        self.assertEqual(
            str(self.variation),
            f'{self.product.name} ({self.variation.variation_code})'
        )

    def test_imageURL_no_image(self):
        self.assertEqual(self.variation.imageURL, '')

class SignalTest(TestCase):
    def test_product_quantity_updates_on_variation_save(self):
        p = Product.objects.create(
            name='SigProd', brand='Sig', size='1ml',
            price=Decimal('1.00'), quantity=0
        )
        v1 = ProductVariation.objects.create(
            product=p, variation_code='A', quantity=2
        )
        v2 = ProductVariation.objects.create(
            product=p, variation_code='B', quantity=3
        )
        p.refresh_from_db()
        self.assertEqual(p.quantity, 5)

        v1.quantity = 4
        v1.save()
        p.refresh_from_db()
        self.assertEqual(p.quantity, 7)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.order = Order.objects.create(user=self.user, complete=False)
        self.product = Product.objects.create(
            name='OPTest', brand='OB', size='5ml',
            price=Decimal('2.50'), quantity=10
        )
        self.variation = ProductVariation.objects.create(
            product=self.product, variation_code='X', quantity=10
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            variation=self.variation,
            quantity=2
        )

    def test_shipping_property(self):
        self.assertTrue(self.order.shipping)
        self.product.digital = True
        self.product.save()
        self.assertFalse(self.order.shipping)

    def test_cart_totals(self):
        self.assertEqual(self.order.get_cart_total, Decimal('5.00'))
        self.assertEqual(self.order.get_cart_items, 2)

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='OIT', brand='OB', size='1ml',
            price=Decimal('3.00'), quantity=1
        )
        self.item = OrderItem.objects.create(
            product=self.product, quantity=2
        )

    def test_get_total(self):
        self.assertEqual(self.item.get_total, Decimal('6.00'))
        self.item.product = None
        self.item.save()
        self.assertEqual(self.item.get_total, 0)
