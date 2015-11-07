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
`__rt_skip__ == True` to the SQLAlchemy model definition.

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
        ...
      }
    }

### TODO:

Blocking http requests are not really well suited for flask.  May not scale
well and cause long running http threads.  Tornado may be more suitable or
even using a local intermediate queue.

Include support for private channels.
