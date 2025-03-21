from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from http import HTTPStatus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # configurar seu banco de dados aqui
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String)
    password = db.Column(db.String)
    binance_api_key = db.Column(db.String)
    binance_secret_key = db.Column(db.String)
    saldo_inicio = db.Column(db.Float)
    configurations = db.relationship('UserConfiguration', back_populates='user')
    tracking_tickers = db.relationship('UserTrackingTicker', back_populates='user')


class UserConfiguration(db.Model):
    __tablename__ = 'user_configuration'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loss_percent = db.Column(db.Float)
    profit_percent = db.Column(db.Float)
    quantity_per_order = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='configurations')


class UserTrackingTicker(db.Model):
    __tablename__ = 'user_tracking_ticker'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='tracking_tickers')


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        login=data['login'],
        password=data['password'],
        binance_api_key=data['binanceApiKey'],
        binance_secret_key=data['binanceSecretKey'],
        saldo_inicio=data['saldoInicio']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.id), HTTPStatus.CREATED


@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        return jsonify({
            'id': user.id,
            'login': user.login,
            'password': user.password,
            'binanceApiKey': user.binance_api_key,
            'binanceSecretKey': user.binance_secret_key,
            'saldoInicio': user.saldo_inicio
        }), HTTPStatus.OK
    else:
        return '', HTTPStatus.NOT_FOUND


@app.route('/users/<int:id>/configuration', methods=['POST'])
def associate_configuration(id):
    user = User.query.get(id)
    if not user:
        return '', HTTPStatus.NOT_FOUND

    data = request.get_json()
    configuration = UserConfiguration(
        loss_percent=data['lossPercent'],
        profit_percent=data['profitPercent'],
        quantity_per_order=data['quantityPerOrder'],
        user_id=user.id
    )
    db.session.add(configuration)
    db.session.commit()

    user.configurations.append(configuration)
    db.session.commit()

    return jsonify({
        'id': user.id,
        'configurations': [{'id': conf.id, 'lossPercent': conf.loss_percent, 'profitPercent': conf.profit_percent, 'quantityPerOrder': conf.quantity_per_order} for conf in user.configurations]
    }), HTTPStatus.CREATED


@app.route('/users/<int:id>/tracking-ticker', methods=['POST'])
def associate_tracking_ticker(id):
    user = User.query.get(id)
    if not user:
        return '', HTTPStatus.NOT_FOUND

    data = request.get_json()
    ticker = UserTrackingTicker(
        symbol=data['symbol'],
        user_id=user.id
    )
    db.session.add(ticker)
    db.session.commit()

    user.tracking_tickers.append(ticker)
    db.session.commit()

    return jsonify({
        'id': user.id,
        'trackingTickers': [{'id': ticker.id, 'symbol': ticker.symbol} for ticker in user.tracking_tickers]
    }), HTTPStatus.CREATED


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
