# Step 1 - Importing the required lib

from flask import Flask,request,render_template
import pickle

# Step 2 - Initializing the flask

app = Flask(__name__)
model = pickle.load(open('classification_rf.pkl', 'rb'))

# Step 3 - Routing to the templates with some functionalities
@app.route('/')
def home():
    return render_template('input.html')


@app.route('/input',methods = ['POST'])
def pred():
    gender = request.form.get('gender')
    age = request.form.get('age')
    salary = request.form.get('salary')
    input = [[int(gender), int(age), float(salary)]]
    import requests

    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "tKA8XFb6dA2aoykejoO0UfWcXNfw-NS3Pc9t_vxSMW3I"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY,"grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["Gender", "Age", "EstimatedSalary"],
                                       "values": [[int(gender), int(age), float(salary)]]}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/87cb8743-2a2c-4f8a-8d19-fa56d49b86ed/predictions?version=2021-05-01',json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    op = response_scoring.json()
    print(op)
    return render_template('input.html',Output=str(op))


# Step 4 - Run the application

if __name__ == '__main__':
    app.run()