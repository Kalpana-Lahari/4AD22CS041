from flask import Flask, jsonify
from collections import deque
import time
import random

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
numbers_store = {
    'p': deque(),
    'T': deque(),
    'e': deque(),
    'r': deque()
}

# Helper: mock fetch numbers based on qualified id.
def fetch_numbers(number_id):
    # Simulate network delay (within 500 ms)
    delay = random.uniform(0.05, 0.4)
    time.sleep(delay)

    # Simulated numbers for each type
    if number_id == 'p':  # prime numbers
        # Some first prime numbers
        numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    elif number_id == 'T':  # Fibonacci numbers
        numbers = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    elif number_id == 'e':  # even numbers
        numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    elif number_id == 'r':  # random numbers
        numbers = [random.randint(1, 100) for _ in range(10)]
    else:
        # Invalid ID, return None to simulate failure
        return None

    # Randomly select a number of numbers up to 10, simulating partial responses
    count = random.randint(1, WINDOW_SIZE)
    return numbers[:count]


def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


@app.route('/numbers/<string:number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in numbers_store:
        return jsonify({"error": "Invalid number ID"}), 400

    current_store = numbers_store[number_id]
    before_store = list(current_store)

    fetched_numbers = fetch_numbers(number_id)
    if fetched_numbers is None:
        return jsonify({
            "before": before_store,
            "after": before_store,
            "average": calculate_average(before_store),
            "error": "Failed to fetch numbers from third-party server"
        }), 500

    # Store unique numbers, maintain window size (oldest replaced by newest)
    for number in fetched_numbers:
        if number not in current_store:
            if len(current_store) >= WINDOW_SIZE:
                current_store.popleft()
            current_store.append(number)

    after_store = list(current_store)
    average = calculate_average(after_store)

    return jsonify({
        "before": before_store,
        "after": after_store,
        "average": average
    })


if __name__ == '__main__':
    # Run Flask app at http://127.0.0.1:5000 by default
    app.run(host='0.0.0.0', port=5000)