from flask import Flask, render_template, session, request, url_for, flash, redirect
import pickle
import pandas as pd
import numpy as np 
from supabase_config import supabase
from hashlib import sha256


app = Flask(__name__)
app.secret_key = "food_delivery_secret"




# Load trained model
model = pickle.load(open("food_delivery_model.pkl", "rb"))

# Feature columns used during training
columns = [
'Delivery_person_Age',
'Delivery_person_Ratings',
'distance_km',
'Type_of_order_buffet',
'Type_of_order_drinks',
'Type_of_order_meal',
'Type_of_order_snack',
'Type_of_vehicle_bicycle',
'Type_of_vehicle_electric_scooter',
'Type_of_vehicle_motorcycle',
'Type_of_vehicle_scooter'
]





def hash_password(password):
      return sha256(password.encode()).hexdigest()


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# SIGNUP
@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name")
        phoneno = request.form.get("phoneno")
        email = request.form.get("email")
        password = request.form.get("password")

        # check existing email
        existing = supabase.table("users").select("*").eq("email",email).execute()

        if existing.data:
            flash("Email already registered","error")
            return redirect(url_for("signup"))

        hashed_password = hash_password(password)

        supabase.table("users").insert({
            "name":name,
            "phoneno":phoneno,
            "email":email,
            "password":hashed_password
        }).execute()

        flash("Registration successful","success")
        return redirect(url_for("login"))

    return render_template("signup.html")









# Login Page
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method=='POST':

        email = request.form.get('email')
        password = request.form.get('password')

        response = supabase.table("users").select("*").eq("email",email).execute()

        if response.data:

            user = response.data[0]

            if hash_password(password) == user['password']:

                session['user_id'] = user['uid']
                session['username'] = user['name']
                session['email'] = user['email']

                flash("Login successful","success")

                return redirect(url_for("predict"))

            else:
                flash("Invalid Password","error")
                return redirect(url_for("login"))

        else:
            flash("Email not registered","error")
            return redirect(url_for("login"))

    return render_template('login.html')




# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))












# Dashboard Page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Prediction Page
@app.route("/predict", methods=["GET","POST"])
def predict():

    if request.method == "POST":

        age = int(request.form["age"])
        rating = float(request.form["ratings"])
        distance = float(request.form["distance"])
        order_type = request.form["order_type"].lower()
        vehicle_type = request.form["vehicle_type"].lower()

        # Create dataframe
        new_order = pd.DataFrame([{
            'Delivery_person_Age': age,
            'Delivery_person_Ratings': rating,
            'distance_km': distance,
            'Type_of_order': order_type,
            'Type_of_vehicle': vehicle_type
        }])

        # Encoding
        new_order_encoded = pd.get_dummies(
            new_order,
            columns=['Type_of_order','Type_of_vehicle'],
            drop_first=False
        )

        # Align with training columns
        new_order_encoded = new_order_encoded.reindex(columns=columns, fill_value=0)

        # Prediction
        prediction = model.predict(new_order_encoded)[0]

        prediction = round(prediction,2)

        return render_template("predict.html", prediction=prediction)

    return render_template("predict.html")

if __name__ == "__main__":
    app.run(debug=True)