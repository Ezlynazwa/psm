from django.core.management.base import BaseCommand
import numpy as np
from recommendation.engine import initialize_services, EvaluationPipeline
from recommendation.engine import EpsilonGreedyRecommender

class Command(BaseCommand):
    help = 'Grid search over blend weights and exploration epsilon'

    def handle(self, *args, **options):
        pipeline = EvaluationPipeline()
        train_df, test_df = pipeline.train_test_split()

        best = {'score': -1}
        weights = np.linspace(0, 1, 5)
        epsilons = [0.0, 0.05, 0.1, 0.2]

        for wc in weights:
            for wr in weights:
                wp = 1 - wc - wr
                if wp < 0:
                    continue
                for eps in epsilons:
                    hybrid, skl, _ = initialize_services()
                    hybrid.w_content = wc
                    hybrid.w_rule = wr
                    hybrid.w_popular = wp
                    explorer = EpsilonGreedyRecommender(hybrid, epsilon=eps)

                    p = pipeline.precision_at_k(explorer, test_df, k=5)
                    r = pipeline.recall_at_k(explorer, test_df, test_size, k=5)
                    metric = (p + r) / 2

                    if metric > best['score']:
                        best.update({'wc': wc, 'wr': wr, 'wp': wp, 'eps': eps, 'score': metric})

        self.stdout.write(self.style.SUCCESS(
            f"Best config -> content: {best['wc']:.2f}, rule: {best['wr']:.2f}, popular: {best['wp']:.2f}, eps: {best['eps']:.2f} (metric={best['score']:.4f})"
        ))
