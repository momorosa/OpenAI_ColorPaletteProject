import os
import json
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
print(f"OpenAI API Key: {openai_api_key}")

# Set the OpenAI API key
openai.api_key = openai_api_key

app = Flask(__name__, template_folder="templates", static_url_path="", static_folder="static")

def get_colors(msg):
    print(f"Generating colors for: {msg}")
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    Your should generate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 colors.

    Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]

    Q: Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B"]

    Desired Format: a JSON array of hexadecimal color codes

    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """
    try:
        response = openai.ChatCompletion.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo",
            max_tokens=200,
        )
        colors = json.loads(response.choices[0].message['content'])
        print(f"Generated colors: {colors}")
        return colors
    except Exception as e:
        print(f"Error generating colors: {e}")
        raise

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    try:
        query = request.form.get("query")
        print(f"Received query: {query}")
        colors = get_colors(query)
        return jsonify({"colors": colors})
    except Exception as e:
        print(f"Error in prompt_to_palette: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
