from flask import Flask, jsonify, make_response, request

# UUIS is an object that is able to generate unique ID values instead of 
# hardcoding integers
import uuid, random
app = Flask(__name__)


# collection of businesses information as a Pythion List
# Each element in the list is a Python dictionary
# businesses =  [
#     {
#         "id" : str(uuid.uuid1()),
#         "name" : "Pizza Mountain",
#         "town" : "Coleraine",
#         "rating" : 5,
#         "reviews" : []  
#     },
#     {
#         "id" : str(uuid.uuid1()),
#         "name" : "Wine Lake",
#         "town" : "Ballymoney",
#         "rating" : 3,
#         "reviews" : []         
#     },
#     {
#         "id" : str(uuid.uuid1()),
#         "name" : "Sweet Desert",
#         "town" : "Ballymena",
#         "rating" : 4,
#         "reviews" : []
#     }
# ]

businesses = {}

def generate_dummy_data():
    towns = ['Coleraine', 'Banbridge', 'Belfast', 'Lisburn', 'Lisburn', 'Ballymena', 'Derry', 
             'Newry', 'Enniskillen', 'Omagh', 'Ballymoney']
    business_dict = {}

    for i in range(100):
        id = str(uuid.uuid1())
        name = "Biz" + str(i)
        town = towns[ random.randint(0, len(towns) - 1) ]
        rating = random.randint(1, 5)
        business_dict[id] = {
            'name' : name,
            'town' : town,
            'rating' : rating,
            'reviews' : []
        }
    return business_dict


# Provide two API routes the first will run all the details of all businesses
# which will return the entire collection of businesses
@app.route("/api/v1.0/businesses", methods=['GET'])
def show_all_businesses():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = page_size * (page_num - 1)
    businesses_list = [ {k : v} for k, v in businesses.items()]
    return make_response( jsonify( businesses_list[page_start : page_start + page_size] ), 200 )

# The second API endpoint 
# This time the URL will have a variable parameter 
# it will be an integer called 'id' and will identify 
# the individual businesses that we want to return
@app.route("/api/v1.0/businesses/<string:id>", methods=['GET'])
def show_one_business(id):
    if id in businesses:
        return make_response( jsonify(  businesses[id] ), 200 )
    else:
        return make_response( jsonify( {"error" : "Invalid Business ID"} ), 404 )


@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    if 'name' in request.form and 'town' in request.form and 'rating' in request.form:
        next_id = str(uuid.uuid1())
        new_business = {
                        'name' : request.form['name'],
                        'town' : request.form['town'],
                        'rating' : request.form['rating'],
                        'reviews' : []
        }
        businesses[next_id] =  new_business
        return make_response( jsonify( {next_id : new_business} ), 201 )
    else:
        return make_response( jsonify( {"error" : "Missing Form Data"} ), 404 )

@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    if id not in businesses:
        return make_response( jsonify( {"error" : "Invalid Business ID"} ), 404 )
    else:
        if 'name' in request.form and 'town' in request.form and 'rating' in request.form:
            businesses[id]["name"] = request.form["name"]
            businesses[id]["town"] = request.form["town"]
            businesses[id]["rating"] = request.form["rating"]
            return make_response( jsonify( {id : businesses[id]} ), 200 )
        else:
            return make_response( jsonify( {"error" : "Missing Form Data"} ), 404 )

@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
        if id in businesses:
            del businesses[id]
            return make_response( jsonify( {} ), 200)
        else:
            return make_response( jsonify( {"error" : "Invalid Business ID"} ), 404 )

@app.route("/api/v1.0/businesses/<int:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
        for business in businesses:
            if business["id"] == id:
                break
        return make_response( jsonify( business["reviews"] ), 200 )

@app.route("/api/v1.0/businesses/<int:b_id>/reviews",
methods=["POST"])
def add_new_review(b_id):
        for business in businesses:
            if business["id"] == b_id:
                if len(business["reviews"]) == 0:
                    new_review_id = 1
                else:
                    new_review_id = business["reviews"][-1]["id"] + 1
                new_review = {
                    "id": new_review_id,
                    "username" : request.form["username"],
                    "comment" : request.form["comment"],
                    "stars" : request.form["stars"]
                }
                business["reviews"].append(new_review)
                break
        return make_response( jsonify( new_review ), 201 )

@app.route("/api/v1.0/businesses/<int:b_id>/reviews/<int:r_id>", methods=["GET"])
def fetch_one_review(b_id, r_id):
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    break
            break
    return make_response( jsonify( review ), 200)

@app.route("/api/v1.0/businesses/<int:b_id>/reviews/<int:r_id>", methods=["PUT"])
def edit_review(b_id, r_id):
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    review["username"] = request.form["username"]
                    review["comment"] = request.form["comment"]
                    review["stars"] = request.form["stars"]
                    break
                break
    return make_response( jsonify( review ), 200)

@app.route("/api/v1.0/businesses/<int:b_id>/reviews/<int:r_id>", methods=["DELETE"])
def delete_review(b_id, r_id):
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    business["reviews"].remove(review)
                    break
            break
    return make_response( jsonify( {} ), 200)


if __name__ == "__main__":
    businesses = generate_dummy_data()
    app.run(debug = True)
