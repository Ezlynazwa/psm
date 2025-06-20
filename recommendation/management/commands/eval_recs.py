from django.core.management.base import BaseCommand
from recommendation.engine import initialize_services, EvaluationPipeline

class Command(BaseCommand):
    help = 'Compute Precision@K and Recall@K for current recommender'

    def add_arguments(self, parser):
        parser.add_argument('--k', type=int, default=5, help='Number of recommendations (K)')
        parser.add_argument('--test_size', type=float, default=0.2, help='Fraction of data for testing')

    def handle(self, *args, **options):
        k = options['k']
        test_size = options['test_size']

        # Initialize services and get explorer
        services = initialize_services()
        explorer = services['explorer']

        # Prepare evaluation pipeline and split data
        pipeline = EvaluationPipeline()
        train_df, test_df = pipeline.train_test_split(test_size=test_size)

        # Compute metrics
        p_at_k = pipeline.precision_at_k(explorer, test_df, k)
        r_at_k = pipeline.recall_at_k(explorer, test_df, k)

        # Output results
        self.stdout.write(self.style.SUCCESS(
            f"Precision@{k}: {p_at_k:.4f}\nRecall@{k}: {r_at_k:.4f}"
        ))
