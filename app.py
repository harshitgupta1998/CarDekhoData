from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb')) #model is loaded here.
model1 = pickle.load(open('random_forest_regression_model_newdatamodel.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        mileage=int(request.form['mileage'])
        mileage=np.log(mileage)
        engine=int(request.form['engine'])
        engine=np.log(engine)
        seats=int(request.form['seats'])
        max_power=int(request.form['max_power'])
        
        
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        log_Present_Price=np.log(Present_Price)
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0

        owner_Fourth_Above_Owner=0
        owner_Second_Owner=1
        owner_Test_Drive_Car=0
        owner_Third_Owner=0
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual,log_Present_Price]])
        prediction1=model1.predict([[Kms_Driven2, mileage, engine, max_power, seats, Fuel_Type_Diesel,
       Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual,
       Seller_Type_Individual, Transmission_Mannual,
       owner_Fourth_Above_Owner, owner_Second_Owner,
       owner_Test_Drive_Car, owner_Third_Owner, Year]])
        #prediction1=model.predict([[Kms_Driven2, mileage, engine, max_power, seats,  Fuel_Type_Diesel, Fuel_Type_Petrol, , Transmission_Mannual, Year]])
        
        output=round(prediction[0],2)
        output1=round(prediction1[0],2)
        
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {} and {}".format(output,output1))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
