import random

from faker import Faker

SEED = 1234


def generate_companies(companies_count):
    fake = Faker()
    fake.seed_instance(SEED)

    ids = list(range(companies_count))
    random.seed(SEED)
    random.shuffle(ids)

    companies = []

    for i in range(companies_count):
        companies.append({
            "id": ids[i],
            "name": fake.company(),
            "phone": fake.phone_number(),
        })

    return companies
