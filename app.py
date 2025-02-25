from flask import Flask, render_template, request
from insights import generate_customer_insights
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        df = pd.read_csv(file)

        # Generate insights
        insights_df = generate_customer_insights(df)

        # ✅ Debugging: Print the type of insights_df
        print("Type of insights_df:", type(insights_df))

        # Ensure it's a DataFrame
        if not isinstance(insights_df, pd.DataFrame):
            return f"Error: insights_df is not a DataFrame, instead got {type(insights_df)}", 500

        # Convert DataFrame to HTML
        insights_html = insights_df.to_html(classes="table table-bordered")

        # Generate up to 6 graphs
        graph_urls = []
        for column in df.select_dtypes(include=['number']).columns[:6]:
            plt.figure(figsize=(5, 3))
            sns.histplot(df[column], kde=True, color="blue")
            plt.title(f'Distribution of {column}')

            # Save graph to memory buffer
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            graph_urls.append(base64.b64encode(img.getvalue()).decode())

        return render_template('index.html', insights=insights_html, graph_urls=graph_urls)

if __name__ == '__main__':
    app.run(debug=True)
