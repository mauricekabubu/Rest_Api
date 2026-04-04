#NOTE:: In Restapi do not use jsonify unlike normal apis
from flask import jsonify,Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from flask_cors import CORS


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///employee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

db = SQLAlchemy(app)

CORS(app)

api = Api(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"user_{self.username}_{self.email}"
   

class getEmployee(Resource):
    def get(self):
        employees = Employee.query.all()
        emp_list = []

        for emp in employees:
            emp_list.append({
                "id": emp.id,      # use lowercase for consistency
                "username": emp.username,
                "email": emp.email,
                "salary": emp.salary
            })

        # Return a dict with a list of employees
        return {"employee": emp_list}, 200   
        
class postEmployee(Resource):
    def post(self):
        if not request.is_json:
            return{
                    "error":"Request must be json"
                },400
            
                
            
        data = request.get_json()   
        
        emp = Employee.query.filter_by(username=data["username"]).first()
        
        if emp:
            return{"error":f"Account with the above username exists"},400
        
        else:        
            emp = Employee(username= data["username"],
                        email= data["email"],
                        salary= data["salary"])
            db.session.add(emp)
            db.session.commit()
            
            #return response in json
            return{"id":emp.id,"username":emp.username,"email":emp.email,
                    "salary":emp.salary
                },200

    
            

class updateEmployee(Resource):
    def put(self,id):
        if not request.is_json:
            return{
                    "error":"Request must be json"
                },400
            
                
        emp = Employee.query.get(id)
        
        
        if emp is None:
            return{
                    "error":"Not Found"
                },404
                
            
        data = request.get_json()

        emp.username = data["username"]
        emp.email = data["email"]
        emp.salary = data["salary"]
        db.session.commit()
        
        return{
                "message":"Updated successfully"
            },200
                
        

class deleteEmployee(Resource):
    def delete(self,id):
        emp = Employee.query.get(id)
        
        if emp is None:
            return{
                    "Error":"Not Found"
                },404
                
            
        db.session.delete(emp)
        db.session.commit()
        
        return{
                "Message":f"{id} successfully deleted"
            },200
        
            
            

# Routes
api.add_resource(getEmployee, "/employees")
api.add_resource(postEmployee, "/employees")
api.add_resource(updateEmployee, "/employees/<int:id>")
api.add_resource(deleteEmployee, "/employees/<int:id>")

@app.route("/")
def home():
    return {"message": "API is running"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5500)