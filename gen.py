import pandas as pd
import google.generativeai as genai

# 🔹 Configure Gemini API
genai.configure(api_key="AIzaSyBKLaHxz2Ln3CcVS6hl998HD6GReIwTDxE")  # Replace with your actual API key

# 🔹 Load Real Estate Data from CSV
df = pd.read_csv(r"./real_estate_data_omr_randomized.csv")  # Replace with actual path
print("✅ Data Loaded Successfully!\n")

# 🔹 Function to Get Response from Gemini
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

# 🔹 Find Best Apartment Based on User Preferences
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
    - You’ll love [mention any standout feature like a scenic view, clubhouse, or easy access to transport].  

    🔹 **Other Good Options You Might Like:**  
    If you're open to exploring, here are **two other apartments** that also match your needs:  

    **🏠 Option 2:** [Second best match] – **[Size, Price, Amenities]**  
    - **Why?** [Short reason why it’s a good choice]  

    **🏠 Option 3:** [Third best match] – **[Size, Price, Amenities]**  
    - **Why?** [Short reason why it’s a good choice]  

    😊 Let me know what you think! I'm happy to refine the search if you have any other preferences!  
    """
    return get_gemini_response(prompt)

# 🔹 Main Function with User Input
if __name__ == "__main__":
    print("🔹 Tell me what you're looking for in an apartment (e.g., budget, size, amenities, location, etc.)")
    user_preferences = input("\n🔹 Enter your requirements: ")

    print("\n🔹 Finding the Best Apartment for You... Please wait! 🏡")
    best_apartment = find_best_apartment(user_preferences)
    print("\n🏢 **Here's My Recommendation:**\n")
    print(best_apartment)