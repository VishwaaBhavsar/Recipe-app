import streamlit as st
import random
from datetime import datetime, timedelta
import requests
import pandas as pd
from typing import List, Dict, Any
import json
from pathlib import Path

# Set page config for wider layout
st.set_page_config(layout="wide", page_title="Flavour with Fusion", page_icon="🍳")

# Enhanced CSS with custom fonts and improved styling
st.markdown("""
    <style>
    /* Import Google Fonts */
   @import url('https://fonts.googleapis.com/css2?family=Cabin+Sketch:wght@400;700&display=swap&family=Cabin+Sketch:wght@400;700&display=swap&family=Great+Vibes&family=Playfair+Display:wght@400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap');


            
    /* Theme variables with enhanced colors */
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --accent-color: #FFE66D;
        --text-color: #2C3E50;
        --bg-color: rgba(255, 255, 255, 0.97);
        --card-bg: rgba(255, 255, 255, 0.98);
        --border-color: #e9ecef;
    }

    /* Dark theme overrides with enhanced colors */
    [data-theme="dark"] {
        --text-color: #FFFFFF;
        --bg-color: rgba(38, 39, 48, 0.97);
        --card-bg: rgba(30, 30, 30, 0.98);
        --border-color: #4A4A4A;
    }

    /* Logo and Header Container */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem 0;
        margin-bottom: 1rem;
    }

    .logo-title-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    /* Main title styling with logo */
    .main-title-with-logo {
        font-family: 'Playfair Display', serif;
        font-size: 5.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        letter-spacing: -0.5px;
    }

    /* Theme variables with enhanced colors */
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --accent-color: #FFE66D;
        --text-color: #2C3E50;
        --bg-color: rgba(255, 255, 255, 0.97);
        --card-bg: rgba(255, 255, 255, 0.98);
        --border-color: #e9ecef;
    }

    /* Dark theme overrides with enhanced colors */
    [data-theme="dark"] {
        --text-color: #FFFFFF;
        --bg-color: rgba(38, 39, 48, 0.97);
        --card-bg: rgba(30, 30, 30, 0.98);
        --border-color: #4A4A4A;
    }

    /* Global styles */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1543353071-873f17a7a088') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Poppins', sans-serif;
    }

    /* Home button styling */
    .home-button {
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 1000;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        text-decoration: none;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .home-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }

    /* Main container styling */
    .content-container {
        background-color: var(--bg-color);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 2.5rem auto;
        max-width: 1200px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    }

    /* Main title styling */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 5.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2.5rem 0;
        margin-bottom: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        letter-spacing: -0.5px;
    }
    
    /* Subtitle styling with adjusted transparency */
    .subtitle {
        font-family: 'Cinzel', serif;
        font-size: 2.5rem;
        color: var(-text-color);
        text-align: center;
        margin-bottom: 3.5rem;
        font-weight: 500;
        line-height: 1.8;
        opacity: 0.8;
        background-color: rgba(255, 255, 255, 0.7);
        padding: 1rem;
        border-radius: 15px;
        letter-spacing: 0.3px;
    }
    
    /* Recipe Card Styling */
    .recipe-card {
        background: var(--card-bg);
        border-radius: 25px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
        border: 1px solid var(--border-color);
    }

    .recipe-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }

    .recipe-image {
        width: 100%;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        object-fit: cover;
        height: 250px;
        transition: transform 0.3s ease;
    }

    .recipe-image:hover {
        transform: scale(1.02);
    }

    .recipe-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .recipe-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-color);
        margin: 0;
        letter-spacing: -0.5px;
    }

    .recipe-meta {
        display: flex;
        gap: 1.5rem;
        color: var(--text-color);
        opacity: 0.9;
        font-size: 1rem;
        font-family: 'Montserrat', sans-serif;
    }

    .recipe-tag {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Welcome cards styling */
    .welcome-card {
        background-color: rgba(255, 255, 255, 0.6);
        padding: 2rem;
        border-radius: 25px;
        text-align: center;
        margin: 1.5rem;
        transition: all 0.4s ease;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
        position: relative;
        overflow: hidden;
    }

    .welcome-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
    }
    
    .welcome-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }

    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }

    .card-text {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        color: var(--text-color);
        opacity: 0.9;
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        border: none;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.2rem;
        margin-top: 2rem;
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        width: 100%;
    }

    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }

    /* Input field styling */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: var(--bg-color);
        border: 2px solid var(--border-color);
        border-radius: 15px;
        padding: 1rem;
        color: var(--text-color);
        width: 100%;
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.2);
    }

    /* Results container styling */
    .results-container {
        background: var(--card-bg);
        padding: 2.5rem;
        border-radius: 25px;
        margin-top: 2.5rem;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
    }

    /* Meal card styling */
    .meal-card {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-left: 5px solid var(--primary-color);
        transition: all 0.4s ease;
    }

    .meal-card:hover {
        transform: translateX(8px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.15);
    }

    .meal-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }

    .meal-details {
        font-family: 'Montserrat', sans-serif;
        font-size: 1rem;
        color: var(--text-color);
        opacity: 0.9;
    }

    /* Section headers */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    /* Generate button styling */
    .generate-button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        padding: 1rem 2.5rem !important;
        border-radius: 50px !important;
        border: none !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        margin-top: 2rem !important;
        transition: all 0.4s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        width: 100% !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }

    .generate-button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
    }
    </style>
    """, unsafe_allow_html=True)


# [Previous MEALS dictionary remains the same]
MEALS = {
    'breakfast': {
        'high_protein': [
            {'name': 'Pesarattu (Green Moong Dal Dosa)', 'calories': 320, 'protein': 16, 'tags': ['south_indian', 'vegetarian']},
            {'name': 'Egg Appam with Stew', 'calories': 380, 'protein': 18, 'tags': ['south_indian']},
            {'name': 'Ragi Idli with Sambar', 'calories': 290, 'protein': 12, 'tags': ['south_indian', 'vegetarian']},
            {'name': 'Paneer Paratha with Curd', 'calories': 450, 'protein': 22, 'tags': ['north_indian', 'vegetarian']},
            {'name': 'Chole Kulche', 'calories': 480, 'protein': 18, 'tags': ['north_indian', 'vegetarian']},
            {'name': 'Egg Bhurji with Multigrain Paratha', 'calories': 400, 'protein': 24, 'tags': ['north_indian']},
            {'name': 'Moong Dal Chilla', 'calories': 340, 'protein': 16, 'tags': ['north_indian', 'vegetarian']}, 
            {'name': 'Sprouts Salad', 'calories': 220, 'protein': 14, 'tags': ['vegetarian']}
        ],
        'low_carb': [
            {'name': 'Cauliflower Upma', 'calories': 220, 'protein': 8, 'tags': ['south_indian', 'keto', 'vegetarian']},
            {'name': 'Coconut Flour Uttapam', 'calories': 260, 'protein': 10, 'tags': ['south_indian', 'keto', 'vegetarian']},
            {'name': 'Paneer Bhurji (No Bread)', 'calories': 280, 'protein': 18, 'tags': ['north_indian', 'keto', 'vegetarian']},
            {'name': 'Mushroom Masala Egg White Omelette', 'calories': 200, 'protein': 16, 'tags': ['north_indian', 'keto']},
            {'name': 'Avocado Smoothie Bowl', 'calories': 230, 'protein': 10, 'tags': ['keto', 'vegetarian']}, 
            {'name': 'Spinach and Cheese Stuffed Omelette', 'calories': 240, 'protein': 18, 'tags': ['keto']}
        ],
        'balanced': [
            {'name': 'Pongal with Sambar', 'calories': 340, 'protein': 10, 'tags': ['south_indian', 'vegetarian']},
            {'name': 'Puttu with Kadala Curry', 'calories': 380, 'protein': 12, 'tags': ['kerala', 'vegetarian']},
            {'name': 'Poha with Batata', 'calories': 320, 'protein': 8, 'tags': ['maharashtrian', 'vegetarian']},
            {'name': 'Misal Pav', 'calories': 380, 'protein': 14, 'tags': ['maharashtrian', 'vegetarian']},
            {'name': 'Upma', 'calories': 300, 'protein': 9, 'tags': ['south_indian', 'vegetarian']}, 
            {'name': 'Daliya Khichdi', 'calories': 340, 'protein': 11, 'tags': ['north_indian', 'vegetarian']}
        ]
    },
    'lunch': {
        'high_protein': [
            {'name': 'Andhra Chicken Curry with Quinoa', 'calories': 480, 'protein': 35, 'tags': ['south_indian']},
            {'name': 'Chettinad Fish Curry with Millet', 'calories': 450, 'protein': 32, 'tags': ['south_indian']},
            {'name': 'Tandoori Chicken with Roomali Roti', 'calories': 520, 'protein': 38, 'tags': ['north_indian']},
            {'name': 'Dal Makhani with Paneer Tikka', 'calories': 580, 'protein': 26, 'tags': ['north_indian', 'vegetarian']},
            {'name': 'Lemon Garlic Prawns with Quinoa', 'calories': 460, 'protein': 30, 'tags': ['fusion']}, 
            {'name': 'Grilled Tofu Salad', 'calories': 360, 'protein': 20, 'tags': ['vegetarian']}
        ],
        'low_carb': [
            {'name': 'Cauliflower Rice Bisibelabath', 'calories': 280, 'protein': 12, 'tags': ['south_indian', 'keto', 'vegetarian']},
            {'name': 'Keto Meen Moilee with Cauliflower Rice', 'calories': 320, 'protein': 24, 'tags': ['kerala', 'keto']},
            {'name': 'Keto Butter Chicken (No Rice)', 'calories': 350, 'protein': 28, 'tags': ['north_indian', 'keto']},
            {'name': 'Palak Paneer with Cauliflower Rice', 'calories': 300, 'protein': 18, 'tags': ['north_indian', 'keto', 'vegetarian']},
            {'name': 'Zucchini Noodles with Pesto', 'calories': 260, 'protein': 10, 'tags': ['fusion', 'keto', 'vegetarian']}, 
            {'name': 'Grilled Chicken Salad', 'calories': 280, 'protein': 26, 'tags': ['keto']}
        ],
        'balanced': [
            {'name': 'Sambar Rice with Poriyal', 'calories': 420, 'protein': 12, 'tags': ['south_indian', 'vegetarian']},
            {'name': 'Malabar Biryani', 'calories': 550, 'protein': 18, 'tags': ['kerala']},
            {'name': 'Rajma Chawal', 'calories': 440, 'protein': 16, 'tags': ['north_indian', 'vegetarian']},
            {'name': 'Lucknowi Biryani', 'calories': 580, 'protein': 22, 'tags': ['north_indian']},
            {'name': 'Vegetable Thali', 'calories': 500, 'protein': 15, 'tags': ['north_indian', 'vegetarian']}, 
            {'name': 'Pav Bhaji', 'calories': 450, 'protein': 12, 'tags': ['maharashtrian', 'vegetarian']}
        ]
    },
    'dinner': {
        'high_protein': [
            {'name': 'Mysore Mutton Curry with Ragi Roti', 'calories': 450, 'protein': 32, 'tags': ['south_indian']},
            {'name': 'Andhra Egg Curry with Quinoa', 'calories': 380, 'protein': 24, 'tags': ['south_indian']},
            {'name': 'Amritsari Fish with Mint Chutney', 'calories': 420, 'protein': 34, 'tags': ['north_indian']},
            {'name': 'Dhaba Style Chicken Curry', 'calories': 460, 'protein': 36, 'tags': ['north_indian']},
            {'name': 'Paneer Bhurji with Roti', 'calories': 400, 'protein': 24, 'tags': ['north_indian', 'vegetarian']}, 
            {'name': 'Lamb Keema with Whole Wheat Pita', 'calories': 480, 'protein': 30, 'tags': ['fusion']}, 
            {'name': 'Grilled Salmon with Asparagus', 'calories': 410, 'protein': 35, 'tags': ['fusion']},
            {'name': 'Chicken Tikka Masala with Brown Rice', 'calories': 420, 'protein': 38, 'tags': ['north_indian']}
        ],
        'low_carb': [
            {'name': 'Keto Chicken Chettinad', 'calories': 320, 'protein': 28, 'tags': ['south_indian', 'keto']},
            {'name': 'Cauliflower Rice Vangi Bath', 'calories': 260, 'protein': 10, 'tags': ['south_indian', 'keto', 'vegetarian']},
            {'name': 'Keto Malai Tikka', 'calories': 300, 'protein': 26, 'tags': ['north_indian', 'keto']},
            {'name': 'Tandoori Cauliflower', 'calories': 180, 'protein': 8, 'tags': ['north_indian', 'keto', 'vegetarian']},
            {'name': 'Grilled Fish with Steamed Vegetables', 'calories': 320, 'protein': 28, 'tags': ['keto']}, 
            {'name': 'Stuffed Bell Peppers', 'calories': 240, 'protein': 12, 'tags': ['fusion', 'keto', 'vegetarian']},
            {'name': 'Zucchini and Chicken Stir Fry', 'calories': 280, 'protein': 25, 'tags': ['keto']}
        ],
        'balanced': [
            {'name': 'Curd Rice with Pickle', 'calories': 320, 'protein': 10, 'tags': ['south_indian', 'vegetarian']},
            {'name': 'Kerala Parotta with Beef Fry', 'calories': 580, 'protein': 24, 'tags': ['kerala']},
            {'name': 'Dal Tadka with Jeera Rice', 'calories': 420, 'protein': 14, 'tags': ['north_indian', 'vegetarian']},
            {'name': 'Butter Naan with Paneer Makhani', 'calories': 550, 'protein': 18, 'tags': ['north_indian', 'vegetarian']},
            {'name': 'Vegetable Korma with Pulao', 'calories': 450, 'protein': 12, 'tags': ['south_indian', 'vegetarian']},
            {'name': 'Chicken Biryani', 'calories': 520, 'protein': 28, 'tags': ['north_indian']},
            {'name': 'Chana Masala with Rice', 'calories': 400, 'protein': 15, 'tags': ['north_indian', 'vegetarian']}
        ]
    }
}

def show_header_with_logo(title: str):
    st.markdown(f"""
        <div class="header-container">
            <div class="logo-title-container">
                <div class="logo"></div>
                <h1 class="main-title-with-logo">{title}</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)

class RecipeGenerator:
    def __init__(self, use_api: bool = True):
        self.use_api = use_api
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
        
        if not use_api:
            try:
                self.recipes_df = pd.read_csv('recipes_dataset.csv')
            except FileNotFoundError:
                self.create_sample_dataset()
    
    def create_sample_dataset(self):
        data = {
            'name': [
            'Chicken Curry', 'Vegetable Stir Fry', 'Beef Tacos', 
            'Greek Salad', 'Mushroom Pasta', 'Butter Chicken',
            'Vegetable Biryani', 'Pasta Carbonara', 'Caesar Salad',
            'Sushi Roll', 
            'Paneer Butter Masala', 'Aloo Gobi', 'Chana Masala',
            'Baingan Bharta', 'Palak Paneer', 'Dal Tadka',
            'Rajma Chawal', 'Vegetable Pulao', 'Masoor Dal',
            'Kadhi Pakora', 'Stuffed Capsicum', 'Malai Kofta',
            'Bhindi Masala', 'Vegetable Korma', 'Pav Bhaji'
            ],
            'ingredients': [
            'chicken,onion,tomato,curry powder,garlic,ginger',
            'carrot,broccoli,bell pepper,soy sauce,garlic,ginger',
            'beef,tortilla,lettuce,tomato,cheese,onion',
            'cucumber,tomato,olive,feta cheese,red onion,olive oil',
            'pasta,mushroom,garlic,cream,parmesan,butter',
            'chicken,butter,cream,tomato,garam masala,fenugreek',
            'rice,mixed vegetables,biryani masala,onion,ghee,mint',
            'pasta,eggs,bacon,parmesan,black pepper,garlic',
            'romaine lettuce,croutons,parmesan,caesar dressing,chicken',
            'sushi rice,nori,fish,cucumber,avocado,wasabi',
            'paneer,butter,cream,tomato,garam masala,cashew nuts',
            'potato,cauliflower,onion,ginger,garlic,turmeric',
            'chickpeas,tomato,onion,garam masala,ginger,garlic',
            'eggplant,tomato,onion,garlic,ginger,spices',
            'paneer,spinach,cream,garlic,ginger,spices',
            'yellow lentils,garlic,cumin,onion,red chili,cilantro',
            'kidney beans,rice,onion,ginger,garlic,spices',
            'rice,mixed vegetables,onion,garam masala,ghee,mint',
            'red lentils,onion,tomato,cumin,garlic,spices',
            'yogurt,besan (gram flour),pakoras,onion,ginger,spices',
            'bell pepper,potato,cheese,spices,onion,cilantro',
            'paneer,cream,tomato,cashew nuts,garam masala',
            'okra,onion,tomato,ginger,garlic,spices',
            'mixed vegetables,coconut milk,garam masala,ginger,garlic',
            'potato,tomato,peas,butter,pav bhaji masala,buns'
            ],
            'cuisine': [
            'Indian', 'Asian', 'Mexican', 'Greek', 'Italian',
            'Indian', 'Indian', 'Italian', 'American', 'Japanese',
            'Indian', 'Indian', 'Indian', 'Indian', 'Indian', 'Indian',
            'Indian', 'Indian', 'Indian', 'Indian', 'Indian', 'Indian',
            'Indian', 'Indian', 'Indian'
            ],
            'instructions': [
            'Cut chicken into cubes. Sauté onions and spices. Add chicken and cook. Add tomatoes and simmer.',
            'Cut vegetables. Heat oil. Stir fry vegetables. Add sauce and seasonings.',
            'Brown beef. Season with spices. Warm tortillas. Assemble with toppings.',
            'Chop vegetables. Mix ingredients. Add dressing and toss.',
            'Cook pasta. Sauté mushrooms. Make cream sauce. Combine all ingredients.',
            'Marinate chicken. Make curry base. Cook chicken. Add cream and butter.',
            'Cook rice. Prepare vegetables. Layer with spices. Steam until done.',
            'Cook pasta. Prepare sauce. Mix with eggs and cheese. Add bacon.',
            'Chop lettuce. Make dressing. Combine ingredients. Top with chicken.',
            'Prepare rice. Roll with fillings. Cut into pieces. Serve with wasabi.',
            'Sauté onions and spices. Add tomato puree and cashew paste. Add paneer and cream.',
            'Cook potatoes and cauliflower. Sauté with onions, tomatoes, and spices.',
            'Cook chickpeas. Sauté onions, tomatoes, and spices. Combine and simmer.',
            'Roast eggplant. Mash and sauté with onions, tomatoes, and spices.',
            'Blanch spinach. Make a paste. Cook with spices. Add paneer and cream.',
            'Cook lentils. Temper with garlic, cumin, and chili. Garnish with cilantro.',
            'Cook kidney beans. Make a curry base. Serve with rice.',
            'Cook rice. Prepare vegetables. Sauté with spices and steam.',
            'Cook lentils. Add tempered spices with onion, garlic, and cumin.',
            'Prepare yogurt mixture. Add fried pakoras. Temper with spices and serve.',
            'Stuff peppers with filling. Bake or sauté until cooked.',
            'Make a curry base with spices and cream. Add koftas and simmer.',
            'Sauté okra with onions, tomatoes, and spices.',
            'Cook vegetables with spices and coconut milk. Simmer until done.',
            'Boil vegetables. Mash. Cook with spices and butter. Serve with toasted buns.'
            ],
            'cooking_time': [
            30, 20, 25, 15, 25, 40, 45, 20, 15, 30, 
            40, 30, 35, 40, 45, 30, 50, 35, 30, 40, 
            35, 45, 25, 40, 30
            ],
            'difficulty': [
            'Medium', 'Easy', 'Easy', 'Easy', 'Medium', 
            'Medium', 'Hard', 'Medium', 'Easy', 'Hard',
            'Medium', 'Easy', 'Medium', 'Medium', 'Medium',
            'Easy', 'Medium', 'Medium', 'Easy', 'Medium',
            'Medium', 'Medium', 'Medium', 'Medium', 'Medium'
            ]
        }
        self.recipes_df = pd.DataFrame(data)
        self.recipes_df.to_csv('recipes_dataset.csv', index=False)

    def search_by_ingredients_api(self, ingredients: List[str]) -> List[Dict[str, Any]]:
        recipes = []
        for ingredient in ingredients[:3]:
            endpoint = f"{self.base_url}/filter.php"
            try:
                response = requests.get(endpoint, params={"i": ingredient})
                if response.status_code == 200:
                    data = response.json()
                    if data["meals"]:
                        recipes.extend(data["meals"])
            except Exception as e:
                st.error(f"API Error: {str(e)}")
                continue
        
        return self._get_random_recipes(recipes, 3)

    def search_by_ingredients_local(self, ingredients: List[str]) -> List[Dict[str, Any]]:
        matching_recipes = []
        ingredients = [ing.lower() for ing in ingredients]
        
        for _, recipe in self.recipes_df.iterrows():
            recipe_ingredients = recipe['ingredients'].lower().split(',')
            matching_count = sum(1 for ing in ingredients if any(ing in ri for ri in recipe_ingredients))
            
            if matching_count >= 1:
                matching_recipes.append({
                    'name': recipe['name'],
                    'cuisine': recipe['cuisine'],
                    'ingredients': recipe['ingredients'],
                    'instructions': recipe['instructions'],
                    'cooking_time': recipe['cooking_time'],
                    'difficulty': recipe['difficulty']
                })
        
        return matching_recipes[:3]

    def _get_random_recipes(self, recipes: List[Dict], count: int) -> List[Dict]:
        if not recipes:
            return []
        return random.sample(recipes, min(count, len(recipes)))

    def get_recipe_suggestions(self, ingredients: List[str]) -> Dict[str, Any]:
        if self.use_api:
            recipes = self.search_by_ingredients_api(ingredients)
            detailed_recipes = []
            
            for recipe in recipes:
                endpoint = f"{self.base_url}/lookup.php"
                try:
                    response = requests.get(endpoint, params={"i": recipe["idMeal"]})
                    if response.status_code == 200:
                        data = response.json()
                        if data["meals"]:
                            meal_data = data["meals"][0]
                            detailed_recipes.append({
                                "name": meal_data["strMeal"],
                                "cuisine": meal_data["strArea"],
                                "instructions": meal_data["strInstructions"],
                                "image_url": meal_data["strMealThumb"]
                            })
                except Exception as e:
                    st.error(f"API Error: {str(e)}")
                    continue
                    
            return {"recipes": detailed_recipes}
        else:
            recipes = self.search_by_ingredients_local(ingredients)
            return {"recipes": recipes}


def show_welcome():
    show_header_with_logo("Flavour with Fusion")
    st.markdown('<p class="subtitle">"Fusion that delights , Flavour that Excite." </p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="welcome-card">
                <h2 class="card-title">Recipe Generator</h2>
                <p class="card-text"> Whether you're a seasoned chef or a kitchen novice, we are here to inspire creativity, reduce food waste, and make meal preparation a breeze. Simply input your ingredients, and watch the magic unfold with delicious recipes.🥗</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Recipes"):
            st.session_state.page = "recipe"
            st.rerun()

    with col2:
        st.markdown("""
            <div class="welcome-card">
                <h2 class="card-title">Meal Planner</h2>
                <p class="card-text">Step into a world of customized nutrition with the Personalized Meal Planner. Designed to cater to your unique dietary needs and culinary preferences, this innovative tool helps you plan nutritious and delicious meals effortlessly.🗓️🍽️</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Plan Meals"):
            st.session_state.page = "planner"
            st.rerun()

def show_recipe_generator():
    st.markdown('<h1 class="main-title"> Smart Recipe Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">" Algorithms⚙️ to Appetizing🍴 "</p>', unsafe_allow_html=True)
    st.write("Enter your available ingredients and get recipe suggestions!")

    # Mode selection within the recipe generator page
    mode = st.radio(
        "Choose Recipe Source",
        ["Recipe Generation", "Ready-made Recipes"],
        index=1,
        help="Recipe Generation makes dishes according to ingredients."
    )
    use_api = mode == "Recipe Generation"

    # Initialize recipe generator
    generator = RecipeGenerator(use_api=use_api)

    # Input for ingredients
    ingredients_input = st.text_input(
        "Enter your ingredients (separated by commas)",
        placeholder="e.g., chicken, tomato, onion"
    )

    if st.button("Generate Recipes"):
        if ingredients_input:
            ingredients = [ing.strip() for ing in ingredients_input.split(",")]
            
            with st.spinner("Finding recipes..."):
                results = generator.get_recipe_suggestions(ingredients)
            
            if results["recipes"]:
                st.success(f"Found {len(results['recipes'])} recipes!")
                
                # Display recipes in columns
                cols = st.columns(len(results["recipes"]))
                for i, (recipe, col) in enumerate(zip(results["recipes"], cols)):
                    with col:
                        st.subheader(f"📝 {recipe['name']}")
                        if 'image_url' in recipe:
                            st.image(recipe['image_url'], use_container_width=True)
                        
                        st.write(f"**Cuisine:** {recipe['cuisine']}")
                        
                        if 'cooking_time' in recipe:
                            st.write(f"**Cooking Time:** {recipe['cooking_time']} minutes")
                        
                        if 'difficulty' in recipe:
                            st.write(f"**Difficulty:** {recipe['difficulty']}")
                        
                        if 'match_score' in recipe:
                            match_percentage = recipe['match_score'] * 100
                            st.progress(match_percentage / 100)
                            st.write(f"Match Score: {match_percentage:.0f}%")
                        
                        with st.expander("View Instructions"):
                            st.write(recipe['instructions'])
            else:
                st.warning("No recipes found with those ingredients. Try different ingredients!")
        else:
            st.error("Please enter some ingredients!")

    # Additional information
    with st.expander("About this feature"):
        st.write("""
        This Smart Recipe Generator helps you find recipes based on ingredients you have.
        - Enter multiple ingredients separated by commas
        - Get detailed instructions and cuisine information
        """)

# [MealPlanner class and show_meal_planner function remain exactly the same]
class MealPlanner:
    @staticmethod
    def get_diet_type(user_data):
        if user_data["goal"] == "Weight Loss":
            return "low_carb"
        elif user_data["goal"] == "Weight Gain":
            return "high_protein"
        return "balanced"

    @staticmethod
    def filter_meals(meals, dietary_restrictions):
        if "Vegetarian" in dietary_restrictions:
            return [meal for meal in meals if "vegetarian" in meal["tags"]]
        return meals

    @staticmethod
    def generate_meal_plan(user_data):
        diet_type = MealPlanner.get_diet_type(user_data)
        meal_plan = {}
        
        for i in range(7):
            day = (datetime.now() + timedelta(days=i)).strftime("%A")
            day_meals = {}
            
            for meal_time in ['breakfast', 'lunch', 'dinner']:
                available_meals = MEALS[meal_time][diet_type]
                if user_data["dietary_restrictions"]:
                    available_meals = MealPlanner.filter_meals(available_meals, user_data["dietary_restrictions"])
                
                if available_meals:
                    meal = random.choice(available_meals)
                    day_meals[meal_time] = {
                        "name": meal["name"],
                        "calories": meal["calories"],
                        "protein": meal["protein"]
                    }
                else:
                    # Fallback to balanced meals if no meals match the criteria
                    meal = random.choice(MEALS[meal_time]['balanced'])
                    day_meals[meal_time] = {
                        "name": meal["name"],
                        "calories": meal["calories"],
                        "protein": meal["protein"]
                    }
            
            meal_plan[day] = day_meals
        
        return meal_plan
def show_meal_planner():
    st.markdown('<h1 class="main-title">Personalized Meal Planner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">" Ready to Taste Wellness?🥑🎯" </p>', unsafe_allow_html=True)
    
    
    # Create three columns with minimal spacing
    col1, space1, col2, space2, col3 = st.columns([3, 0.1, 3, 0.1, 3])
    
    with col1:
        st.markdown("""
            <h3 style="color: #FFFFF; 
                       font-size: 2rem; 
                       margin-bottom: 1rem; 
                       font-family: 'Playfair Display', serif;">
                Personal Information
            </h3>
        """, unsafe_allow_html=True)
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=300, value=70)
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity_level = st.selectbox(
            "Activity Level",
            ["Sedentary", "Light", "Moderate", "Very Active"]
        )
    
    with col2:
        st.markdown("""
            <h3 style="color: #FFFFF; 
                       font-size: 2rem; 
                       margin-bottom: 1rem; 
                       font-family: 'Playfair Display', serif;">
                Goals & Preferences
            </h3>
        """, unsafe_allow_html=True)
        goal = st.selectbox("Fitness Goal", ["Weight Loss", "Maintain", "Weight Gain"])
        dietary_restrictions = st.multiselect(
            "Dietary Restrictions",
            ["None", "Vegetarian", "Vegan", "Gluten-free", "Dairy-free"]
        )
    
    with col3:
        st.markdown("""
            <h3 style="color: #FFFFF; 
                       font-size: 2rem; 
                       margin-bottom: 1rem; 
                       font-family: 'Playfair Display', serif;">
                Regional Preferences
            </h3>
        """, unsafe_allow_html=True)
        cuisine_preference = st.multiselect(
            "Preferred Regional Cuisines",
            ["Italian", "Indian", "Chinese", "Mexican", "Mediterranean"]
        )
        spice_preference = st.select_slider(
            "Spice Preference",
            options=["Mild", "Medium", "Very Spicy"]
        )
    
    # Minimal spacing before button
    st.markdown('<div style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    
    # Centered button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_button = st.button("Generate Meal Plan", use_container_width=True)
    
    if generate_button:
        user_data = {
            "age": age,
            "height": height,
            "weight": weight,
            "gender": gender,
            "activity_level": activity_level,
            "goal": goal,
            "dietary_restrictions": dietary_restrictions,
            "cuisine_preference": cuisine_preference,
            "spice_preference": spice_preference
        }
        
        meal_plan = MealPlanner.generate_meal_plan(user_data)
        
        # Clean meal plan display
        st.markdown("""
            <h2 style="color: #FFFFF; 
                       font-size: 4rem; 
                       margin: 2rem 0 1.5rem 0; 
                       text-align: center;
                       font-family: 'Playfair Display', serif;">
                Your Weekly Meal Plan
            </h2>
        """, unsafe_allow_html=True)
        
        for day, meals in meal_plan.items():
            st.markdown(f"""
                <div style="margin: 2.5rem 0;">
                    <h3 style="color: #FFFFF; 
                               font-size: 3rem; 
                               margin-bottom: 0.8rem;
                               font-family: 'Playfair Display', serif;
                               border-bottom: 2px solid #4ECDC4;">
                        {day}
                    </h3>
            """, unsafe_allow_html=True)
            
            for meal_time, meal_info in meals.items():
                st.markdown(f"""
                    <div style="margin: 1rem 0;">
                        <div style="font-size: 1.6rem; 
                                    color: #FFFFF; 
                                    margin-bottom: 0.3rem;
                                    font-family: 'Poppins', sans-serif;">
                            <span style="color: #FF6B6B; font-weight: 600;">
                                {meal_time.title()}:
                            </span> 
                            {meal_info['name']}
                        </div>
                        <div style="color: #FFFFF; 
                                    font-size: 1.4rem;
                                    font-family: 'Montserrat', sans-serif;">
                            🔥 {meal_info['calories']} kcal  |  💪 {meal_info['protein']}g protein
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add subtle separator between days except for the last day
            if day != list(meal_plan.keys())[-1]:
                st.markdown("""
                    <div style="border-bottom: 1px solid #eee; 
                                margin: 1rem 0;">
                    </div>
                """, unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'

    # Sidebar navigation
    with st.sidebar:
        if st.button("🏠 Home"):
            st.session_state.page = 'welcome'
            st.rerun()

    # Main content
    if st.session_state.page == 'welcome':
        show_welcome()
    elif st.session_state.page == 'recipe':
        show_recipe_generator()
    elif st.session_state.page == 'planner':
        show_meal_planner()

if __name__ == "__main__":
    main()