import os
from flask import Flask, make_response, redirect,render_template, request, url_for , flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date , datetime
from sqlalchemy import func

app = Flask(__name__)

# Use DATABASE_URL from environment (Render provides this), fallback to local MySQL for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'mysql+pymysql://root@localhost:3306/expenses_db'
).replace('postgres://', 'postgresql://')  # Render uses postgres:// but SQLAlchemy needs postgresql://

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'my_secret_key')
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, default=date.today)



with app.app_context():
    db.create_all()

CATEGORIES = ['Food', 'Transport', 'Utilities', 'Entertainment','Rent', 'Other']

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

@app.route("/")
def index():
#get the values from query parameters
   start_str = (request.args.get("start") or "").strip()
   end_str = (request.args.get("end") or "").strip()
   selected_category = (request.args.get("category") or "").strip()

   # Parse dates
   start_date = parse_date(start_str) 
   end_date = parse_date(end_str)

   if start_date and end_date and end_date < start_date:
         flash("End date cannot be earlier than start date.", "error")
         start_date = end_date = None
         start_str = end_str = ""

         

   q = Expense.query
   if start_date:
        q = q.filter(Expense.date >= start_date)
   if end_date:
         q = q.filter(Expense.date <= end_date)
         
   if selected_category:
        q = q.filter(Expense.category == selected_category)

           
   expenses = q.order_by(Expense.date.desc(), Expense.id.desc()).all()
   total = round(sum(e.amount for e in expenses), 2)
# this is for pie chart
   cat_query = db.session.query(Expense.category, func.sum(Expense.amount))
   if start_date:
        cat_query = cat_query.filter(Expense.date >= start_date)
   if end_date:
         cat_query = cat_query.filter(Expense.date <= end_date)
   if selected_category:
        cat_query = cat_query.filter(Expense.category == selected_category)  

   cat_rows = cat_query.group_by(Expense.category).all() 
   print( cat_rows) 
   cat_labels = [c for c, _ in cat_rows]   
   cat_values = [round(float(s), 2) for _, s in cat_rows]  
   print(cat_values)
   

   # this is for day chart
   day_query = db.session.query(Expense.category, func.sum(Expense.amount))
   
   if start_date:
        day_query = day_query.filter(Expense.date >= start_date)
   if end_date:
         day_query = day_query.filter(Expense.date <= end_date)
   if selected_category:
        day_query = day_query.filter(Expense.category == selected_category)  

   day_rows = day_query.group_by(Expense.category).order_by(func.max(Expense.date)).all()
   day_labels = [cat for cat, _ in day_rows]   
   day_values = [round(float(s), 2) for _, s in day_rows]  
   
   
   return render_template (
        "index.html", 
        expenses=expenses,
        categories=CATEGORIES,
        today=date.today().isoformat(),
        total=total,
        start_str=start_str,
        end_str=end_str,
        selected_category=selected_category,
        cat_labels=cat_labels,
        cat_values=cat_values,
        day_labels=day_labels,
        day_values=day_values,
        )    

@app.route("/add", methods=['POST'])
def add():
    description = (request.form.get("description") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip() 
    date_str = (request.form.get("date") or "").strip()
    
    if not description or not amount_str or not category:
        flash("All fields are required!", "error")
        return redirect(url_for("index"))
    
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
    except ValueError:
        flash("Invalid amount. Please enter a positive number.", "error")
        return redirect(url_for("index"))
    
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        d= date.today()     

    e = Expense(description=description,amount=amount,category=category,date=d)   
    db.session.add(e)
    db.session.commit()
    flash("Expense added successfully!", "success")
    return redirect(url_for("index")) 

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete(expense_id):
    e = Expense.query.get_or_404(expense_id)
    db.session.delete(e)
    db.session.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for('index'))

@app.route('/edit/<int:expense_id>', methods=['GET'])
def edit(expense_id): 
    e= Expense.query.get_or_404(expense_id)
    return render_template('edit.html', expense=e, categories=CATEGORIES, today=date.today().isoformat())

@app.route('/edit/<int:expense_id>', methods=['POST'])
def edit_post(expense_id):  
    e= Expense.query.get_or_404(expense_id)
    
    description = (request.form.get("description") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip() 
    date_str = (request.form.get("date") or "").strip()
    
    #validation
    if not description or not amount_str or not category:
        flash("All fields are required!", "error")
        return redirect(url_for("edit", expense_id=expense_id))
    
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
    except ValueError:
        flash("Invalid amount. Please enter a positive number.", "error")
        return redirect(url_for("edit", expense_id=expense_id))
    
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        d= date.today()     
    
    e.description= description
    e.amount= amount
    e.category= category
    e.date= d
    
    db.session.commit()
    flash("Expense updated successfully!", "success")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)