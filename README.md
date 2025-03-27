# Real Estate GPT - AI-Powered Property Search

A modern web application that leverages Google's Gemini AI to provide intelligent property recommendations and market analysis in the OMR (Old Mahabalipuram Road) region of Chennai.

## 🌟 Features

### AI-Powered Property Search
- Natural language property search using Google's Gemini AI
- Intelligent property recommendations based on user preferences
- Location detection from user queries
- Budget and BHK requirement extraction
- Amenities-based filtering

### Property Comparison
- Visual comparison of properties using interactive graphs
- Price comparison across different locations
- Size and amenities comparison
- Price per square foot analysis

### Market Analysis
- Detailed market trends and insights
- Location-wise price analysis
- Property type distribution
- Investment returns analysis

### User Interface
- Modern, responsive design
- Interactive chat interface
- Traditional search filters
- Dynamic property cards
- Real-time sorting and filtering

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **AI**: Google Gemini AI
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Styling**: Custom CSS with modern design principles

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Gemini AI API key

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/real-estate-gpt.git
cd real-estate-gpt
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Gemini AI API key:
   - Get your API key from Google AI Studio
   - Add it to the `app.py` file or set it as an environment variable

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📊 Data

The application uses a dataset of real estate properties in the OMR region, including:
- Property prices
- Location details
- BHK configurations
- Area measurements
- Available amenities

## 💡 Usage

### AI Chat Interface
1. Type your property requirements in natural language
2. Include details like:
   - Preferred location (e.g., "OMR", "Sholinganallur")
   - Budget (e.g., "under 60 lakhs")
   - BHK requirement (e.g., "2BHK")
   - Desired amenities (e.g., "with gym and swimming pool")

### Traditional Search
1. Use the filter section to specify:
   - Location
   - Property type (BHK)
   - Price range
   - Area range
2. Click "Search Properties" to view results

### Property Comparison
1. Add "compare" to your query to see multiple options
2. View comparison graphs for:
   - Price comparison
   - Size comparison
   - Price per square foot
   - Amenities count

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for providing the AI capabilities
- The real estate dataset contributors
- All contributors to this project

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

Made with ❤️ by [Meet Modi, Keshav Sharma, Aditya Yadav/Team Bengan] 
