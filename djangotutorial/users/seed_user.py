import random

def generate_mock_users(count):
    names = ["Алиса", "Віктор", "Алекс", "Єва", "Микола"]
    roles = ["Admin", "User"]

    users = []
    for i in range(count):
        user = {
            "id": 1000 + i,
            "name": random.choice(names),
            "role": random.choice(roles),
            "score": random.randint(50, 100)
        }
        users.append(user)
    return users


random.seed(12345)

sampled_users = generate_mock_users(3)
print(sampled_users)
