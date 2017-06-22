from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, session as login_session, make_response

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Brands, Base, Items, Users

import json
import random
import string
import httplib2
import requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///brandProducts.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# For Login
CLIENT_ID = json.loads(
     open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Soccer Feet Application"


@app.route('/')
@app.route('/brands')
def displayBrands():
    brands = session.query(Brands).order_by(asc(Brands.name))
    return render_template("brands.html", brands=brands)


@app.route('/brands/<int:brand_id>')
@app.route('/brands/<int:brand_id>/items')
def displayItems(brand_id):
    brand = session.query(Brands).filter_by(id=brand_id).one()
    items = session.query(Items).filter_by(brand_id=brand_id)
    return render_template("items.html", items=items, brand=brand)


@app.route('/brands/new', methods=['GET', 'POST'])
def addBrand():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newBrand = Brands(name=request.form['name'],
                          user_id=login_session['user_id'])
        session.add(newBrand)
        flash('New Brand %s Successfully Created' % newBrand.name)
        session.commit()
        return redirect(url_for('displayBrands'))
    else:
        return render_template('newBrand.html')


@app.route('/brands/<int:brand_id>/edit', methods=['GET', 'POST'])
def editBrand(brand_id):
    if 'username' not in login_session:
        return redirect('/login')
    edit_Brand = session.query(Brands).filter_by(id=brand_id).one()

    # Authorization check
    if edit_Brand.user_id != login_session['user_id']:
        flash('Not Authorized')
        return redirect('/?error=not_authorized')

    if request.method == 'POST':
        if request.form['name']:
            edit_Brand.name = request.form['name']
            flash('Restaurant Successfully Edited %s' % edit_Brand.name)
            return redirect(url_for('displayBrands'))
    else:
        return render_template('editBrand.html', edit_Brand=edit_Brand)


@app.route('/brands/<int:brand_id>/delete', methods=['GET', 'POST'])
def deleteBrand(brand_id):
    if 'username' not in login_session:
        return redirect('/login')
    deleteBrand = session.query(Brands).filter_by(id=brand_id).one()
    # Authorization check
    if deleteBrand.user_id != login_session['user_id']:
        flash('Not Authorized')
        return redirect('/?error=not_authorized')

    deleteItems = session.query(Items).filter_by(brand_id=deleteBrand.id)
    for item in deleteItems:
        print item.name
        session.delete(item)
        session.commit()
    session.delete(deleteBrand)
    session.commit()
    flash('%s Successfully Deleted' % deleteBrand.name)
    return redirect(url_for('displayBrands'))


@app.route('/brands/<int:brand_id>/items/new', methods=['GET', 'POST'])
def addBrandItem(brand_id):
    if 'username' not in login_session:
        return redirect('/login')

    brand = session.query(Brands).filter_by(id=brand_id).one()
    # Authorization check
    if brand.user_id != login_session['user_id']:
        flash('Not Authorized')
        return redirect('/?error=not_authorized')

    if request.method == 'POST':
        newItem = Items(name=request.form['name'],
                        description=request.form['description'],
                        image=request.form['image'],
                        price=request.form['price'],
                        brand_id=brand_id,
                        user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Item %s Successfully Created' % (newItem.name))
        return redirect(url_for('displayItems', brand_id=brand_id))
    else:
        return render_template('addItem.html', brand_id=brand_id)


@app.route('/brands/<int:brand_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editBrandItem(brand_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Items).filter_by(id=item_id).one()
    brand = session.query(Brands).filter_by(id=brand_id).one()

    # Authorization check
    if brand.user_id != login_session['user_id']:
        flash('Not Authorized')
        return redirect('/?error=not_authorized')

    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['image']:
            item.image = request.form['image']
        if request.form['price']:
            item.price = request.form['price']
        item.brand_id = brand.id
        session.add(item)
        session.commit()
        flash('Item Edited %s' % (item.name))
        return redirect(url_for('displayItems', brand_id=brand_id))
    else:
        return render_template('editItem.html', item=item)


@app.route('/brands/<int:brand_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteBrandItem(brand_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    # Authorization check
    brand = session.query(Brands).filter_by(id=brand_id).one()
    if brand.user_id != login_session['user_id']:
        flash('Not Authorized')
        return redirect('/?error=not_authorized')

    item = session.query(Items).filter_by(id=item_id).one()
    session.delete(item)
    session.commit()
    flash('Deleted')
    return redirect(url_for('displayItems', brand_id=brand_id))


# login Components
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    print code

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already'
                                            'connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])

    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'\
              '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = Users(name=login_session['username'], email=login_session[
               'email'], image=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(Users).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    if 'access_token' in login_session:
        access_token = login_session['access_token']
        print 'In gdisconnect access token is %s', access_token
        print 'User name is: '
        print login_session['username']
        if access_token is None:
            print 'Access Token is None'
            response = make_response(json.dumps('Current user not connected.'),
                                     401)
            response.headers['Content-Type'] = 'application/json'
            return response
        url = 'https://accounts.google.com/o/oauth2/' \
              'revoke?token=%s' % login_session['access_token']
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        print 'result is '
        print result
        if result['status'] == '200':
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            response = make_response(json.dumps('Successfully disconnected.'),
                                     200)
            response.headers['Content-Type'] = 'application/json'
            # return response
            flash('Logged Out Successfully ')
            return redirect('/')
        else:
            response = make_response(json.dumps('Failed to revoke token for' +
                                                ' given user.', 400))
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
