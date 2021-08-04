import random

import pytest
import numpy as np
from jina import Document, DocumentArray

from ..catboost_ranker import CatboostRanker

NUM_DOCS = 50
NUM_MATCHES = 5


@pytest.fixture
def ranker():
    return CatboostRanker(
        query_features=['brand', 'price'],
        match_features=['brand', 'price'],
        label='relevance',
    )


@pytest.fixture
def ranker_with_weight():
    return CatboostRanker(
        query_features=['brand', 'price'],
        match_features=['brand', 'price'],
        label='relevance',
        weight='weight',
    )


@pytest.fixture
def relevances():
    return np.random.uniform(0, 1, [1, NUM_DOCS]).flatten()


@pytest.fixture
def documents_to_train_stub_model(relevances):
    """features: color, brand, price. Label relevance"""
    # initial stub model, relevance purely dependent on brand, not price.
    # brand relevance 5 > 4 > 3 > 2 > 1.
    da = DocumentArray()
    for relevance in relevances:
        if 0.8 <= relevance <= 1:
            brand = 5
        elif 0.6 <= relevance < 0.8:
            brand = 4
        elif 0.4 <= relevance < 0.6:
            brand = 3
        elif 0.2 <= relevance < 0.4:
            brand = 2
        else:
            brand = 1
        doc = Document(
            tags={
                'brand': brand,
                'price': random.randint(50, 200),
                'weight': random.uniform(0, 1),
            }
        )
        for _ in range(NUM_MATCHES):
            # each match has an extra relevance field indicates score.
            doc.matches.append(
                Document(
                    tags={
                        'brand': brand,
                        'price': random.randint(50, 200),
                        'relevance': float(relevance),
                    }
                )
            )
        da.append(doc)
    return da


@pytest.fixture
def documents_to_train_price_sensitive_model(relevances):
    """features: color, brand, price. Label relevance"""
    # price sensitive, relevance based on pure price, cheaper relevance higher.
    da = DocumentArray()
    for relevance in relevances:
        if 8 <= relevance <= 10:
            price = random.randint(30, 50)
        elif 6 <= relevance < 8:
            price = random.randint(50, 70)
        elif 4 <= relevance < 6:
            price = random.randint(70, 90)
        elif 2 <= relevance < 4:
            price = random.randint(90, 110)
        else:
            price = random.randint(110, 130)
        doc = Document(
            tags={
                'brand': random.randint(1, 5),
                'price': price,
                'relevance': relevance,
            }
        )
        for _ in range(NUM_MATCHES):
            # each match has an extra relevance field indicates score.
            doc.matches.append(
                Document(
                    tags={
                        'brand': random.randint(1, 5),
                        'price': price,
                        'relevance': float(relevance),
                    }
                )
            )
        da.append(doc)
    return da


@pytest.fixture
def documents_without_label(relevances):
    """features: color, brand, price. Label relevance"""
    # price sensitive, relevance based on pure price, cheaper relevance higher.
    da = DocumentArray()
    for relevance in relevances:
        if 8 <= relevance <= 10:
            price = random.randint(30, 50)
        elif 6 <= relevance < 8:
            price = random.randint(50, 70)
        elif 4 <= relevance < 6:
            price = random.randint(70, 90)
        elif 2 <= relevance < 4:
            price = random.randint(90, 110)
        else:
            price = random.randint(110, 130)
        doc = Document(
            tags={
                'brand': random.randint(1, 5),
                'price': price,
            }
        )
        for _ in range(NUM_MATCHES):
            # each match has an extra relevance field indicates score.
            doc.matches.append(
                Document(
                    tags={
                        'brand': random.randint(1, 5),
                        'price': price,
                    }
                )
            )
        da.append(doc)
    return da
