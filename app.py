from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()

    scrapedText = ''

    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')

            for p in paragraphs:
                scrapedText += p.get_text() + '\n\n'
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
        scrapedText +='---------------------'

    return jsonify({'scrapedText': scrapedText})

@app.route('/tools', methods=['POST'])
def generate_summary():
    data = request.get_json()
    prompt = data.get('query')

    prompt_ctx = """
        Context: Use the fund data below to answer the questions
    
    Fund Name                      | Fund Manager            | Inception Date | NAV   | AUM (in millions) | Fund Objective                                                           | Benchmark Index   | Top Holdings                         | Sector Allocation      | Performance (1Y, 3Y, 5Y) | Risk Measures (Std. Dev, Beta, Sharpe Ratio) | Fees (Management Fee, Expense Ratio)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. Alpha Growth Fund           | John Smith              | 01-02-2005      | 120.50| 1500              | Long-term capital appreciation through investments in growth stocks      | S&P 500           | Apple, Microsoft, Amazon             | Technology: 40%        | 15%, 12%, 10%            | 18%, 1.1, 0.75                         | 0.8%, 1.10%
2. Beta Income Fund            | Jane Doe                | 10-05-2010      | 75.20 | 800               | Generate income through investments in dividend-paying stocks             | MSCI World        | Coca-Cola, Procter & Gamble, Pfizer  | Consumer Staples: 35%  | 5%, 4%, 3%               | 12%, 0.9, 0.45                         | 0.7%, 0.90%
3. Gamma International Fund     | Alan Turing             | 15-09-2014      | 98.00 | 1200              | Long-term growth through investments in international companies          | MSCI EAFE         | Nestle, Toyota, Unilever             | Industrials: 30%       | 10%, 8%, 7%              | 16%, 1.0, 0.65                         | 0.9%, 1.20%
4. Delta Small Cap Value Fund   | Grace Hopper            | 08-12-2016      | 45.30 | 500               | Capital appreciation through investments in undervalued small-cap stocks | Russell 2000      | Acme Inc, Beta Corp, Charlie Co.     | Health Care: 25%       | 20%, 17%, 15%            | 22%, 1.3, 0.90                         | 1.0%, 1.30%
5. Epsilon Technology Fund      | Ada Lovelace            | 03-04-2013      | 150.10| 1000              | Long-term growth through investments in technology companies             | NASDAQ 100        | Nvidia, Adobe, Salesforce            | Information Tech: 60%  | 25%, 20%, 18%            | 25%, 1.5, 1.00                         | 1.1%, 1.40%
6. Zeta Balanced Fund           | Charles Babbage         | 29-07-2008      | 110.00| 900               | Balanced growth and income through a mix of stocks and bonds             | 60% S&P 500, 40% Agg Bond| Apple, Microsoft, US Treasury Bonds  | Technology: 20%        | 10%, 8%, 6%              | 14%, 0.8, 0.55                         | 0.7%, 0.95%
7. Eta Real Estate Fund         | Hedy Lamarr             | 17-11-2011      | 85.40 | 750               | Income and capital appreciation through investments in real estate       | FTSE NAREIT      | Simon Property, AvalonBay, Equity Res | Real Estate
    """

    prompt = prompt_ctx+"Question:"+prompt
    print (prompt)

    try:
        print ('Calling API')
        response = openai.Completion.create(
                                                model="text-davinci-003",
                                                max_tokens=500,
                                                temperature=1,
                                                prompt = prompt,
                                                top_p=1)

        print (response.choices[0].text)
    except Exception as e:
        print (e)
        return jsonify({'summary': str(e)}), 500

    return jsonify({'summary': response.choices[0].text})

if __name__ == '__main__':
    app.run(debug=True)
