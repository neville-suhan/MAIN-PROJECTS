from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",   # change this if needed
        database="food_db",
        auth_plugin='mysql_native_password'
    )

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    message = ""
    category = ""

    if request.method == "POST":
        if "all" in request.form:
            # Show all foods
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.category_name, f.food_name, f.description, f.rating
                    FROM foods f
                    JOIN categories c ON f.category_id = c.id  
                    ORDER BY c.category_name, f.rating DESC
                """)
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                message = "🍽️ All Available Foods:"
            except Exception as e:
                message = f"Error: {e}"

        elif "recommend" in request.form:
            # Get recommendations
            category = request.form.get("category_dropdown") or request.form.get("category_text", "").strip()
            if not category:
                message = "⚠️ Please enter or select a category!"
            else:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT f.food_name, f.description, f.rating
                        FROM foods f
                        JOIN categories c ON f.category_id = c.id  
                        WHERE c.category_name = %s
                        ORDER BY f.rating DESC
                        LIMIT 5
                    """, (category,))
                    results = cursor.fetchall()
                    cursor.close()
                    conn.close()
                    if results:
                        message = f"🍽️ Top {category} Food Recommendations:"
                    else:
                        message = f"❌ No {category} food found!"
                except Exception as e:
                    message = f"Error: {e}"

    return render_template("home.html", results=results, message=message, category=category)


if __name__ == "__main__":
    print("Food Recommendation System running at http://127.0.0.1:5000/ 🚀")
    app.run(debug=True,port=5000)
