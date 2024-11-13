from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BAZADANIX.db'
db = SQLAlchemy(app)

class BAZADANIX(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bidd_number = db.Column(db.String(20), nullable=False) 
    pozelaniya = db.Column(db.Text, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Номер забронирован')
    responsible = db.Column(db.String(100), nullable=True)
    apartment_number = db.Column(db.String(20), nullable=False)
    date_completed = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Adres_otelya = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<BAZADANIX {self.bidd_number}>'  



@app.route('/add', methods=['GET', 'POST'])
def add_application():
    if request.method == 'POST':
        bidd_number = request.form['bidd_number']  
        apartment_number = request.form['apartment_number']
        pozelaniya = request.form['pozelaniya']
        client_name = request.form['client_name']
        phone_number = request.form['phone_number']
        status = request.form['status']
        Adres_otelya = request.form['Adres_otelya']
        new_application = BAZADANIX(  
            bidd_number=bidd_number,  
            apartment_number=apartment_number,
            pozelaniya=pozelaniya,
            client_name=client_name,
            phone_number=phone_number,
            status = status,
            Adres_otelya =  Adres_otelya
        )
        db.session.add(new_application)
        db.session.commit() 
        return redirect(url_for('index'))

    return render_template('add_application.html')  

@app.route('/')
def index():
    applications = BAZADANIX.query.all()  
    return render_template('index.html', applications=applications)  

@app.route('/update/<int:application_id>', methods=['GET', 'POST']) 
def update_application(application_id):  
    application = BAZADANIX.query.get_or_404(application_id)  
    if request.method == 'POST':
        application.status = request.form['status']
        application.pozelaniya = request.form['pozelaniya']
        application.responsible = request.form['responsible']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_application.html', application=application)  


@app.route('/statistics')
def statistics():
    completed_applications = BAZADANIX.query.filter_by(status='Клиент покинул номер').count()

    total_time_in_days = 0
    completed_applications = BAZADANIX.query.filter_by(status='Клиент покинул номер').all()
    for app in completed_applications:
        if app.date_completed and app.date_added:
            time_delta = app.date_completed - app.date_added  
            total_time_in_days += time_delta.days  
    average_time_in_days = total_time_in_days / len(completed_applications) if len(completed_applications) < 0 else 0
    completed_applications = BAZADANIX.query.filter_by(status='Клиент покинул номер').count()
   
    return render_template('statistics.html', 
                           completed_applications=completed_applications,
                           average_time_in_days =average_time_in_days)


@app.route('/search', methods=['GET', 'POST'])
def search_application():
    if request.method == 'POST':
        search_id = request.form['search_id']
        application = BAZADANIX.query.filter_by(bidd_number=search_id).first()
        if application:
            return render_template('application_details.html', application=application)
        else:
            return "Заявка не найдена."
    return render_template('index.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

