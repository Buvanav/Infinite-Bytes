from faker import Faker
import pandas as pd
import random
import os

fake = Faker('en_IN')
os.makedirs('demo_data', exist_ok=True)

print("🚀 Finbridge: Generating 400+ rows...")

# 400 TRANSACTIONS (20 workers × 20 txns)
merchants = ['Swiggy', 'Zomato', 'Ola', 'Uber', 'Amazon', 'Flipkart']
types = ['credit', 'debit', 'loan_emi', 'wallet_topup']
data = []
for wid in range(1, 21):
    for _ in range(20):
        data.append({
            'txn_id': fake.uuid4()[:8],
            'worker_id': f'W{wid:03d}',
            'date': fake.date_between(start_date='-6m', end_date='today'),
            'amount': round(random.uniform(50, 3000), 2) * random.choice([1, -1]),
            'type': random.choice(types),
            'merchant': random.choice(merchants),
            'channel': random.choice(['UPI', 'Card', 'NEFT'])
        })
pd.DataFrame(data).to_csv('demo_data/transactions.csv', index=False)
print("✅ Transactions: 400 rows")

# 20 KYC
data = []
cities = ['Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Hyderabad']
for i in range(1, 21):
    data.append({
        'worker_id': f'W{i:03d}',
        'name': fake.name(),
        'dob': fake.date_of_birth(minimum_age=20, maximum_age=45),
        'city': random.choice(cities),
        'kyc_status': random.choice(['FULL_KYC', 'MIN_KYC', 'PENDING']),
        'pan_masked': fake.bban()[:2].upper() + '***' + fake.bban()[-5:].upper(),
        'aadhaar_masked': f'XXXX-XXXX-{fake.random_number(digits=4)}'
    })
pd.DataFrame(data).to_csv('demo_data/kyc_demo.csv', index=False)
print("✅ KYC: 20 workers")

# 120 INCOME (20 workers × 6 months)
data = []
months = pd.date_range('2025-06-01', periods=6, freq='MS').strftime('%Y-%m')
for wid in range(1, 21):
    base = random.uniform(12000, 45000)
    for month in months:
        data.append({
            'worker_id': f'W{wid:03d}',
            'month': month,
            'income': max(5000, round(base + random.uniform(-6000, 6000), 2))
        })
pd.DataFrame(data).to_csv('demo_data/income_history.csv', index=False)
print("✅ Income: 120 rows")

# 20 INSURANCE
data = []
for i in range(1, 21):
    has_ins = random.random() > 0.7
    data.append({
        'worker_id': f'W{i:03d}',
        'has_health_insurance': int(has_ins),
        'premium_per_month': round(random.uniform(400, 1200), 0) if has_ins else 0,
        'insurer': random.choice(['Finbridge Secure', 'GigCare', 'None']),
        'coverage_amount': random.randint(300000, 800000) if has_ins else 0
    })
pd.DataFrame(data).to_csv('demo_data/insurance.csv', index=False)
print("✅ Insurance: 20 workers")
print("🎉 TOTAL: 560 ROWS READY!")