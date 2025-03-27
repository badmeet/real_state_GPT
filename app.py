import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
import re
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key="AIzaSyBKLaHxz2Ln3CcVS6hl998HD6GReIwTDxE")

# Load and preprocess data
def load_data():
    try:
        df = pd.read_csv('real_estate_data_omr_randomized.csv')
        
        # Convert price to numeric (lakhs)
        def convert_price(price):
            try:
                if isinstance(price, str):
                    price = price.lower()
                    if 'cr' in price or 'crore' in price:
                        value = float(re.search(r'([\d.]+)', price).group(1))
                        return value * 100  # Convert crore to lakhs
                    else:
                        return float(re.search(r'([\d.]+)', price).group(1))
                return float(price)
            except:
                return np.nan

        # Convert size to numeric (sq. ft.)
        def convert_size(size):
            try:
                if isinstance(size, str):
                    return float(re.search(r'([\d.]+)', size).group(1))
                return float(size)
            except:
                return np.nan

        # Extract number of bedrooms
        def extract_bedrooms(bhk):
            try:
                if isinstance(bhk, str):
                    return int(re.search(r'(\d+)', bhk).group(1))
                return int(bhk)
            except:
                return np.nan

        # Apply conversions
        df['Price'] = df['Price'].apply(convert_price)
        df['Size'] = df['Size'].apply(convert_size)
        df['Bedrooms'] = df['BHK'].apply(extract_bedrooms)
        
        # Calculate price per square foot
        df['Price_Per_SqFt'] = df['Price'] * 100000 / df['Size']  # Convert lakhs to rupees
        
        # Drop rows with missing values
        df = df.dropna()
        
        return df
    except Exception as e:
        app.logger.error(f"Error loading data: {str(e)}")
        return None

# Load data at startup
df = load_data()
if df is None:
    raise Exception("Failed to load and preprocess data")

# Create amenities score
def calculate_amenities_score(amenities):
    amenities_list = amenities.split(', ')
    return len(amenities_list)

df['Amenities_Score'] = df['Amenities'].apply(calculate_amenities_score)

# Normalize numerical features
scaler = MinMaxScaler()
numerical_features = ['Price', 'Size', 'Price_Per_SqFt', 'Amenities_Score']
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Function to get response from Gemini
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        app.logger.error(f"Error getting Gemini response: {str(e)}")
        return None

# Function to find best apartment based on user preferences
def find_best_apartment(user_preferences):
    prompt = f"""
    You are a friendly and knowledgeable real estate assistant. Your goal is to **understand the user's preferences** and recommend the best apartment in a warm, humble, and convincing way.

    **User Preferences:** {user_preferences}

    **Dataset of Available Apartments:**
    {df.to_string()}

    🔹 **Response Format (Make it clear and engaging)**
    
    🏡 **Best Apartment for You**  
    Hi there! Based on what you're looking for, I found an apartment that I think you'll absolutely love! 😊  

    - **🏢 Name:** [Best match]  
    - **📍 Location:** [City/Area]  
    - **📏 Size:** [sq. ft.]  
    - **💰 Price:** [₹X Lakhs]  
    - **✨ Amenities:** [Relevant features]  

    **🌟 Why is this a great choice for you?**  
    - This apartment fits your requirements **perfectly** because [reason based on budget, size, amenities, location].  
    - It offers **great value for money** compared to similar options.  
    - You'll love [mention any standout feature like a scenic view, clubhouse, or easy access to transport].  

    🔹 **Other Good Options You Might Like:**  
    If you're open to exploring, here are **two other apartments** that also match your needs:  

    **🏠 Option 2:** [Second best match] – **[Size, Price, Amenities]**  
    - **Why?** [Short reason why it's a good choice]  

    **🏠 Option 3:** [Third best match] – **[Size, Price, Amenities]**  
    - **Why?** [Short reason why it's a good choice]  

    😊 Let me know what you think! I'm happy to refine the search if you have any other preferences!  
    """
    return get_gemini_response(prompt)

@app.route('/')
def index():
    # Get personalized recommendations
    recommendations = get_personalized_recommendations(df)
    return render_template('index.html', recommendations=recommendations)

@app.route('/market')
def market():
    return render_template('market.html')

@app.route('/market/omr-demand')
def omr_demand():
    # Read and process the real estate data
    df = pd.read_csv('real_estate_data_omr_randomized.csv')
    
    # Process price data (convert to numeric)
    def convert_price(price):
        try:
            if isinstance(price, str):
                price = price.lower()
                if 'cr' in price or 'crore' in price:
                    value = float(re.search(r'([\d.]+)', price).group(1))
                    return value * 100  # Convert crore to lakhs
                else:
                    return float(re.search(r'([\d.]+)', price).group(1))
            return float(price)
        except:
            return np.nan

    df['Price'] = df['Price'].apply(convert_price)
    
    # Group data by Location and BHK
    df['BHK'] = df['BHK'].astype(str)  # Ensure BHK is string for grouping
    
    # Calculate average prices by location and BHK
    grouped_data = df.groupby(['Location', 'BHK'])['Price'].mean().reset_index()
    
    # Pivot data for easier processing in template
    pivot_data = grouped_data.pivot(index='Location', columns='BHK', values='Price').reset_index()
    pivot_data = pivot_data.fillna(0)  # Fill NaN with 0
    
    # Convert to list of dictionaries for JSON serialization
    data = []
    for _, row in pivot_data.iterrows():
        data_point = {
            'Location': row['Location'],
            'Price': row['Price'] if 'Price' in row else 0,
            '2 BHK': row['2 BHK'] if '2 BHK' in row else 0,
            '3 BHK': row['3 BHK'] if '3 BHK' in row else 0,
            '4 BHK': row['4 BHK'] if '4 BHK' in row else 0
        }
        data.append(data_point)
    
    # Calculate overall statistics
    stats = {
        'avg_price': df['Price'].mean(),
        'price_range': {
            'min': df['Price'].min(),
            'max': df['Price'].max()
        },
        'yoy_growth': 10.2,  # Example value, replace with actual calculation
        'quarterly_growth': 8.5  # Example value, replace with actual calculation
    }
    
    # Get personalized recommendations
    recommendations = get_personalized_recommendations(df)
    
    return render_template('market/omr_demand.html', 
                         data=data, 
                         stats=stats,
                         recommendations=recommendations)

@app.route('/market/property-types')
def property_types():
    return render_template('market/property_types.html')

@app.route('/market/investment-returns')
def investment_returns():
    return render_template('market/investment_returns.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/properties', methods=['GET'])
def get_properties():
    location = request.args.get('location', '')
    bhk = request.args.get('bhk', '')
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', float('inf')))
    min_area = float(request.args.get('min_area', 0))
    max_area = float(request.args.get('max_area', float('inf')))
    sort_by = request.args.get('sort_by', 'relevance')
    
    # Filter properties
    filtered_df = df.copy()
    
    if location:
        filtered_df = filtered_df[filtered_df['Location'] == location]
    if bhk:
        filtered_df = filtered_df[filtered_df['BHK'] == f"{bhk} BHK"]
    
    # Convert rupees to lakhs for comparison
    min_price_lakhs = min_price / 100000
    max_price_lakhs = max_price / 100000 if max_price != float('inf') else float('inf')
    
    filtered_df = filtered_df[
        (filtered_df['Price'] >= min_price_lakhs) &
        (filtered_df['Price'] <= max_price_lakhs) &
        (filtered_df['Size'] >= min_area) &
        (filtered_df['Size'] <= max_area)
    ]
    
    # Sort properties
    if sort_by == 'price_low':
        filtered_df = filtered_df.sort_values('Price')
    elif sort_by == 'price_high':
        filtered_df = filtered_df.sort_values('Price', ascending=False)
    elif sort_by == 'area':
        filtered_df = filtered_df.sort_values('Size', ascending=False)
    elif sort_by == 'value':
        filtered_df = filtered_df.sort_values('Price_Per_SqFt')
    
    # Convert to list of dictionaries
    properties = filtered_df.to_dict('records')
    
    # Format the response
    for prop in properties:
        prop['Price'] = f"{prop['Price']:.2f} Lakhs"
        prop['Size'] = f"{prop['Size']:.0f} sq. ft."
        prop['Price_Per_SqFt'] = f"₹{prop['Price_Per_SqFt']:.2f}"
    
    return jsonify({
        'total': len(properties),
        'properties': properties
    })

@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    # Calculate market statistics
    avg_price = df['Price'].mean()
    avg_price_per_sqft = (df['Price'] * 100000 / df['Size']).mean()
    total_properties = len(df)
    
    # Location-wise analysis
    location_stats = {}
    for location in df['Location'].unique():
        location_df = df[df['Location'] == location]
        location_stats[location] = {
            'avg_price': location_df['Price'].mean(),
            'avg_price_per_sqft': (location_df['Price'] * 100000 / location_df['Size']).mean(),
            'total_properties': len(location_df),
            'min_price': location_df['Price'].min(),
            'max_price': location_df['Price'].max()
        }
    
    # BHK-wise analysis
    bhk_stats = {}
    for bhk in df['Bedrooms'].unique():
        bhk_df = df[df['Bedrooms'] == bhk]
        bhk_stats[f"{bhk}BHK"] = {
            'avg_price': bhk_df['Price'].mean(),
            'avg_price_per_sqft': (bhk_df['Price'] * 100000 / bhk_df['Size']).mean(),
            'total_properties': len(bhk_df)
        }
    
    return jsonify({
        'market_overview': {
            'average_price': f"{avg_price:.2f} Lakhs",
            'average_price_per_sqft': f"₹{avg_price_per_sqft:.2f}",
            'total_properties': total_properties
        },
        'location_stats': location_stats,
        'bhk_stats': bhk_stats
    })

@app.route('/api/recommend', methods=['POST'])
def recommend_properties():
    data = request.json
    budget = float(data.get('budget', 0))
    preferred_location = data.get('location', '')
    preferred_bhk = int(data.get('bhk', 2))
    preferred_amenities = data.get('amenities', [])
    
    # Convert budget from rupees to lakhs
    budget_lakhs = budget / 100000
    
    # Filter by budget and BHK
    filtered_df = df[
        (df['Price'] <= budget_lakhs * 1.1) &  # Allow 10% above budget
        (df['Bedrooms'] == preferred_bhk)
    ]
    
    if preferred_location:
        filtered_df = filtered_df[filtered_df['Location'] == preferred_location]
    
    if len(filtered_df) == 0:
        return jsonify({
            'recommendations': [],
            'total': 0,
            'message': 'No properties found matching your criteria'
        })
    
    # Calculate similarity scores based on amenities
    if preferred_amenities:
        def amenities_match_score(amenities_str):
            property_amenities = set(amenities_str.split(', '))
            preferred = set(preferred_amenities)
            return len(property_amenities.intersection(preferred)) / len(preferred)
        
        filtered_df['amenities_score'] = filtered_df['Amenities'].apply(amenities_match_score)
        filtered_df = filtered_df.sort_values(['amenities_score', 'Price_Per_SqFt'], ascending=[False, True])
    
    # Get top 10 recommendations
    recommendations = filtered_df.head(10).to_dict('records')
    
    # Format the response
    for prop in recommendations:
        prop['Price'] = f"{prop['Price']:.2f} Lakhs"
        prop['Size'] = f"{prop['Size']:.0f} sq. ft."
        prop['Price_Per_SqFt'] = f"₹{prop['Price_Per_SqFt']:.2f}"
        if 'amenities_score' in prop:
            prop['match_score'] = f"{prop['amenities_score'] * 100:.0f}%"
            del prop['amenities_score']
    
    return jsonify({
        'recommendations': recommendations,
        'total': len(recommendations)
    })

@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = sorted(df['Location'].unique().tolist())
    return jsonify(locations)

@app.route('/api/amenities', methods=['GET'])
def get_amenities():
    # Get unique amenities from all properties
    all_amenities = set()
    for amenities in df['Amenities']:
        all_amenities.update(amenities.split(', '))
    return jsonify(sorted(list(all_amenities)))

@app.route('/api/property/<int:id>', methods=['GET'])
def get_property_details(id):
    if id < 0 or id >= len(df):
        return jsonify({'error': 'Property not found'}), 404
    
    property_data = df.iloc[id].to_dict()
    
    # Format the response
    property_data['Price'] = f"{property_data['Price']:.2f} Lakhs"
    property_data['Size'] = f"{property_data['Size']:.0f} sq. ft."
    property_data['Price_Per_SqFt'] = f"₹{property_data['Price_Per_SqFt'] * 100000:.2f}"
    
    # Get similar properties
    similar_properties = find_similar_properties(id)
    
    return jsonify({
        'property': property_data,
        'similar_properties': similar_properties
    })

def find_similar_properties(property_id):
    target_property = df.iloc[property_id]
    
    # Create feature matrix for similarity calculation
    features = ['Price', 'Size', 'Price_Per_SqFt', 'Amenities_Score', 'Bedrooms']
    feature_matrix = df[features].values
    
    # Calculate similarity scores
    property_features = feature_matrix[property_id].reshape(1, -1)
    similarity_scores = cosine_similarity(property_features, feature_matrix)
    
    # Get indices of most similar properties (excluding the target property)
    similar_indices = similarity_scores[0].argsort()[::-1][1:6]
    
    # Get similar properties data
    similar_properties = df.iloc[similar_indices].to_dict('records')
    
    # Format the response
    for prop in similar_properties:
        prop['Price'] = f"{prop['Price']:.2f} Lakhs"
        prop['Size'] = f"{prop['Size']:.0f} sq. ft."
        prop['Price_Per_SqFt'] = f"₹{prop['Price_Per_SqFt'] * 100000:.2f}"
    
    return similar_properties

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({
                'response': "I'm not sure what kind of property you're looking for. Could you please specify your requirements?",
                'properties': []
            })

        # Get response from Gemini
        response = find_best_apartment(message)
        
        if response is None:
            return jsonify({
                'response': "I apologize, but I encountered an error while processing your request. Please try again.",
                'properties': []
            }), 500

        # Initialize response object
        api_response = {
            'response': response,
            'properties': []  # We'll keep this empty as the Gemini response includes property details
        }
        
        return jsonify(api_response)
        
    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': "I apologize, but I encountered an error while processing your request. Please try again.",
            'properties': []
        }), 500

def get_personalized_recommendations(df):
    # Calculate average prices by location
    location_avg_prices = df.groupby('Location')['Price'].mean().reset_index()
    
    # Find premium and affordable locations
    premium_locations = location_avg_prices.nlargest(2, 'Price')['Location'].tolist()
    affordable_locations = location_avg_prices.nsmallest(2, 'Price')['Location'].tolist()
    
    recommendations = {
        'premium': [],
        'mid_range': [],
        'affordable': []
    }
    
    # Premium recommendations
    premium_props = df[df['Location'].isin(premium_locations)].nlargest(2, 'Price')
    for _, prop in premium_props.iterrows():
        recommendations['premium'].append({
            'location': prop['Location'],
            'price': prop['Price'],
            'bhk': prop['BHK'],
            'size': prop['Size'],
            'amenities': prop['Amenities'].split(', '),
            'highlights': [
                'Premium location',
                'High-end amenities',
                'Excellent connectivity'
            ]
        })
    
    # Mid-range recommendations
    mid_price = df['Price'].median()
    mid_range_props = df[
        (df['Price'] > mid_price * 0.8) & 
        (df['Price'] < mid_price * 1.2)
    ].sample(2)
    for _, prop in mid_range_props.iterrows():
        recommendations['mid_range'].append({
            'location': prop['Location'],
            'price': prop['Price'],
            'bhk': prop['BHK'],
            'size': prop['Size'],
            'amenities': prop['Amenities'].split(', '),
            'highlights': [
                'Great value for money',
                'Good connectivity',
                'Essential amenities'
            ]
        })
    
    # Affordable recommendations
    affordable_props = df[df['Location'].isin(affordable_locations)].nsmallest(2, 'Price')
    for _, prop in affordable_props.iterrows():
        recommendations['affordable'].append({
            'location': prop['Location'],
            'price': prop['Price'],
            'bhk': prop['BHK'],
            'size': prop['Size'],
            'amenities': prop['Amenities'].split(', '),
            'highlights': [
                'Budget-friendly',
                'Growing location',
                'Good investment potential'
            ]
        })
    
    return recommendations

if __name__ == '__main__':
    app.run(debug=True) 