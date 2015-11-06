Realtime notification system for model state changes via pusher app

## Basic setup

Add the following to your flask application config:

    app.config.setdefault('PUSHERAPP_ID', '')
    app.config.setdefault('PUSHERAPP_KEY', '')
    app.config.setdefault('PUSHERAPP_SECRET', '')

Add init the extension passing in both the app and SQLAlchemy objects

    from flask.ext.sqlalchemy import SQLAlchemy
    from flask_rt import StateNotifier

    db = SQLAlchemy(app)
    notifier = StateNotifier(app, db)

Then in your views.py give notifier a function that returns the channel
to send to.

    notifier.channel_mapper(lambda: g.user.notifier_channel if hasattr(g, 'user') else None)

If you don't want a particular model to send notifications, just add
`__notifier_skip__ == True` to the SQLAlchemy model definition.

Only declarative models that extend db.Model are currently supported.

If a model includes a 'serialize' property, the notification will include the
serialized object the notification.  Here is an example serialize property:

    @property
    def serialize(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "title": self.title,
            "price": self.price,
        }

Example notification payload that the client would receive (json):

    {
      "model": "Transaction",
      "method": "insert",
      "id": 4,
      "object": {
        "discounts": [
          {
            "amount": "0.75",
            "title": "Senior discount"
          },
          {
            "amount": "0.25",
            "title": "coupon"
          }
        ],
        "items_subtotal": "5.50",
        "total_discount": "1.00",
        "created": 1446836426000,
        "payment_type": 0,
        "items": [
          {
            "amount": "3.00",
            "title": "Shoes"
          },
          {
            "amount": "0.50",
            "title": "Socks"
          },
          {
            "amount": "2.00",
            "title": "Shirt"
          }
        ],
        "total_billed": "6.50",
        "id": 4,
        "taxes": "2.00",
        "total_taxes": null
      }
    }
