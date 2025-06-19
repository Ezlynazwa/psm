from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from store.models import Product, ProductVariation, Order, OrderItem
from store.forms import CheckoutForm, PaymentForm


class ProductModelTests(TestCase):
    def test_get_skin_conditions_list_no_conditions(self):
        """Should return empty list if no skin_condition set"""
        product = Product.objects.create(name="Test", skin_condition=None, quantity=1)
        self.assertEqual(product.get_skin_conditions_list(), [])

    def test_get_skin_conditions_list_parses_correctly(self):
        """Should split comma-separated skin_condition and trim whitespace"""
        product = Product.objects.create(
            name="Test",
            skin_condition="dry, oily , combination",
            quantity=1
        )
        expected = ['dry', 'oily', 'combination']
        self.assertEqual(product.get_skin_conditions_list(), expected)

    def test_is_in_stock_when_quantity_positive(self):
        """is_in_stock should be True if quantity > 0"""
        product = Product.objects.create(name="Test", quantity=5)
        self.assertTrue(product.is_in_stock)

    def test_is_in_stock_when_quantity_zero(self):
        """is_in_stock should be False if quantity == 0"""
        product = Product.objects.create(name="Test", quantity=0)
        self.assertFalse(product.is_in_stock)


class ProductVariationModelTests(TestCase):
    def test_imageURL_with_image(self):
        """Should return image URL when image is set"""
        variation = ProductVariation.objects.create(
            product=Product.objects.create(name="P", quantity=1),
            quantity=1,
        )
        # TODO: attach a test image file to variation.image and check variation.imageURL
        self.assertTrue(hasattr(variation, 'imageURL'))

    def test_imageURL_without_image(self):
        """Should return empty string when no image"""
        variation = ProductVariation.objects.create(
            product=Product.objects.create(name="P", quantity=1),
            quantity=1,
        )
        self.assertEqual(variation.imageURL, "")


class OrderModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Prod", price=10, quantity=10)
        self.order = Order.objects.create(user=None, complete=False)

    def test_shipping_false_for_all_digital(self):
        """shipping should be False when all items are digital"""
        # TODO: create digital ProductVariation and OrderItem
        pass

    def test_shipping_true_if_any_physical(self):
        """shipping should be True if at least one non-digital item exists"""
        pass

    def test_get_cart_total_and_items(self):
        """get_cart_total and get_cart_items should return proper sums"""
        # TODO: add OrderItems and assert sums
        pass


class OrderItemModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="P", price=20, quantity=10)

    def test_get_total_with_product(self):
        item = OrderItem.objects.create(
            product=self.product,
            quantity=3,
            order=Order.objects.create(user=None, complete=False)
        )
        self.assertEqual(item.get_total, 60)

    def test_get_total_without_product(self):
        item = OrderItem.objects.create(
            product=None,
            quantity=3,
            order=Order.objects.create(user=None, complete=False)
        )
        self.assertEqual(item.get_total, 0)


class CheckoutFormTests(TestCase):
    def test_form_without_new_address(self):
        data = { 'add_new_address': False }
        form = CheckoutForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_with_new_address_missing_fields(self):
        data = { 'add_new_address': True, 'address': '', 'city': '', 'state': '', 'zipcode': '' }
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('address', form.errors)
        self.assertIn('city', form.errors)


class PaymentFormTests(TestCase):
    def test_payment_form_valid(self):
        # TODO: construct valid form data, including file if needed
        form = PaymentForm(data={})
        self.assertFalse(form.is_valid())  # adjust based on required fields


class StoreViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.product = Product.objects.create(name="Test", price=5, quantity=5)

    def test_view_product_get(self):
        response = self.client.get(reverse('store:view_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('product', response.context)

    # TODO: add tests for add to cart POST, remove_from_cart, increase_quantity, decrease_quantity, track_order
