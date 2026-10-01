from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Create Flask application
app = Flask(__name__)

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not configured in the .env file."
    )

# Create Gemini client
client = genai.Client(api_key=api_key)


def calculate_budget(budget, category):
    """Create a simple budget allocation."""

    if category.lower() == "shopping":
        allocation = {
            "Main Product": budget * 0.60,
            "Accessories": budget * 0.15,
            "Delivery": budget * 0.05,
            "Emergency": budget * 0.10,
            "Savings": budget * 0.10
        }

    elif category.lower() == "event":
        allocation = {
            "Food": budget * 0.40,
            "Decoration": budget * 0.20,
            "Venue": budget * 0.15,
            "Entertainment": budget * 0.10,
            "Emergency": budget * 0.15
        }

    elif category.lower() == "home decor":
        allocation = {
            "Furniture": budget * 0.40,
            "Decoration": budget * 0.25,
            "Lighting": budget * 0.10,
            "Accessories": budget * 0.10,
            "Emergency": budget * 0.15
        }

    else:
        allocation = {
            "Main Requirement": budget * 0.60,
            "Additional Items": budget * 0.15,
            "Emergency": budget * 0.15,
            "Savings": budget * 0.10
        }

    return {
        key: round(value, 2)
        for key, value in allocation.items()
    }


def get_ai_recommendation(budget, category, requirement, preference):
    """Ask Gemini for a personalized recommendation."""

    prompt = f"""
You are PocketSmart AI, a smart budget and recommendation assistant.

User information:
Total Budget: Rs. {budget}
Category: {category}
Requirement: {requirement}
Preference: {preference}

Give a practical recommendation that stays within the user's budget.

Include:
1. Recommended Plan
2. Estimated Spending
3. Money Saving Tips
4. Final Advice

Keep the response clear and suitable for a student project.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    try:
        budget = float(data.get("budget", 0))
    except (TypeError, ValueError):
        budget = 0

    category = data.get("category", "").strip()
    requirement = data.get("requirement", "").strip()
    preference = data.get("preference", "").strip()

    if budget <= 0:
        return jsonify({
            "error": "Please enter a valid budget."
        }), 400

    if not category or not requirement:
        return jsonify({
            "error": "Please fill in the required fields."
        }), 400

    # Calculate budget allocation
    allocation = calculate_budget(
        budget,
        category
    )

    # Get AI recommendation
    try:
        ai_recommendation = get_ai_recommendation(
            budget,
            category,
            requirement,
            preference
        )

    except Exception as e:
        print("Gemini Error:", e)

        ai_recommendation = (
            "AI recommendation could not be generated. "
            "Please check your API key and internet connection."
        )

    return jsonify({
        "budget": budget,
        "allocation": allocation,
        "ai_recommendation": ai_recommendation
    })


if __name__ == "__main__":
    app.run(debug=True)