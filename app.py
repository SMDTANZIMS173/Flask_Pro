from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

# instantiate the Flask
app = Flask(__name__)

# configuring databbase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'

# Disabling modification Tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the database
db = SQLAlchemy(app)

# create an item model
class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f"<Item {self.name}>"

# create the database and tables
@app.before_request
def create_tables():
    db.create_all()
    
#route to display all items
@app.route("/")
def index():
    items = Item.query.all() # get all items from database
    return render_template("index.html",items = items)

# add the items
@app.route("/add",methods=['POST'])
def add_item():
    # Get form data
    name = request.form["name"]
    description = request.form["description"]
    
    #create new item
    new_item = Item(name=name, description=description)
    db.session.add(new_item)
    db.session.commit()
    
    return redirect(url_for("index"))

# update the existing items 
@app.route("/update/<int:id>",methods=["POST"])       
def update_item(id):
    item = Item.query.get(id)
    if item:
        item.name = request.form["name"]
        item.description = request.form["description"]
        db.session.commit()
    return redirect(url_for("index"))  

# delete the items
@app.route("/delete/<int:id>",methods = ['GET'])
def delete_item(id):
    item = Item.query.get(id) 
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for("index"))

if __name__=="__main__":
    app.run(debug = True)
    