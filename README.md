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
