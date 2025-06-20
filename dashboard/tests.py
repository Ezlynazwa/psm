from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from users.models import CustomerProfile, Employee
from store.models import Product, Order, OrderItem
from dashboard.views import get_report_context, export_report

User = get_user_model()

class ReportContextTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # create staff user
        self.user = User.objects.create_user(username='staff', password='pass')
        self.user.is_staff = True
        self.user.save()
        # create staff Employee with required date_hired
        Employee.objects.create(
            user=self.user,
            name='Staff',
            date_hired=timezone.now()
        )
        # create customer user and profile (avoid duplicate via get_or_create)
        cust_user = User.objects.create_user(username='cust', password='pass')
        CustomerProfile.objects.get_or_create(user=cust_user)
        # product for order
        self.product = Product.objects.create(
            name='Test', brand='Brand', size='50ml', price=Decimal('10.00'), quantity=5
        )
        # order within last 7 days
        self.order = Order.objects.create(user=cust_user, complete=True, total=Decimal('10.00'))
        self.order.date_ordered = timezone.now() - timedelta(days=1)
        self.order.save(update_fields=['date_ordered'])
        # order item
        OrderItem.objects.create(order=self.order, product=self.product, quantity=1)

    def get_request(self):
        request = self.factory.get('/')
        request.user = self.user
        return request

    def test_get_report_context_keys(self):
        context = get_report_context(self.get_request())
        expected_keys = {
            'total_revenue', 'total_orders', 'aov', 'revenue_growth',
            'customer_count', 'new_customers', 'returning_customers',
            'top_products', 'category_performance', 'sales_over_time',
            'orders_table', 'products_sold', 'customer_spending',
            'date_range', 'start_date'
        }
        self.assertTrue(expected_keys.issubset(context.keys()))

    def test_get_report_context_values(self):
        context = get_report_context(self.get_request())
        self.assertEqual(context['total_revenue'], Decimal('10.00'))
        self.assertEqual(context['total_orders'], 1)
        self.assertAlmostEqual(context['aov'], Decimal('10.00'))
        self.assertEqual(context['customer_count'], 1)

class ExportReportTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # create staff user
        self.user = User.objects.create_user(username='staff', password='pass')
        self.user.is_staff = True
        self.user.save()

    def get_request(self):
        request = self.factory.get('/')
        request.user = self.user
        return request

    def test_export_report_csv(self):
        response = export_report(self.get_request(), 'csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode()
        self.assertIn('Metric,Value', content)
        self.assertIn('Total Revenue', content)

    def test_export_report_pdf(self):
        response = export_report(self.get_request(), 'pdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="sales_report.pdf"', response['Content-Disposition'])
