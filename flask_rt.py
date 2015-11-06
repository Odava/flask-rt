from pusher import Pusher
from sqlalchemy.event import listen

class StateNotifier(object):


    def __init__(self, app=None, db=None):
        self.app = app
        self.db = db
        self._channel_mapper = lambda: None
        if app is not None:
            self.init_app(app)
        listen(self.db.engine, 'engine_connect', self.receive_engine_connect, named=True)

    def init_app(self, app):
        app.config.setdefault('PUSHERAPP_ID', '')
        app.config.setdefault('PUSHERAPP_KEY', '')
        app.config.setdefault('PUSHERAPP_SECRET', '')

        self.pusher_client = Pusher(
            app_id=app.config['PUSHERAPP_ID'],
            key=app.config['PUSHERAPP_KEY'],
            secret=app.config['PUSHERAPP_SECRET'],
            ssl=True
        )

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions['state_notifier'] = self

    def channel_mapper(self, mapper_func):
        self._channel_mapper = mapper_func

    def get_channel(self):
        return self._channel_mapper()

    def notify_listeners(self, model=None, method=''):
        # print type(model).__name__, model.id, method
        channel = self.get_channel()
        if channel is None:
            return
        event = 'state_notifier'
        state = {}
        state['model'] = type(model).__name__;
        state['method'] = method
        if hasattr(model, 'id'):
            state['id'] = model.id
        if hasattr(model, 'serialize'):
            state['object'] = model.serialize
        self.pusher_client.trigger(channel, event, state)

    def after_insert(self, **kw):
        self.notify_listeners(kw['target'], 'insert')

    def after_update(self, **kw):
        self.notify_listeners(kw['target'], 'update')

    def after_delete(self, **kw):
        self.notify_listeners(kw['target'], 'delete')

    def receive_engine_connect(self, **kw):

        def get_class_by_tablename(tablename):
            for c in self.db.Model._decl_class_registry.values():
                if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
                    return c

        for table in self.db.metadata.sorted_tables:
            table_class = get_class_by_tablename(table.fullname)
            if not table_class:
                continue
            if hasattr(table_class, '__notifier_skip__') and table_class.__notifier_skip__ == True:
                continue
            listen(table_class, 'after_insert', self.after_insert, named=True);
            listen(table_class, 'after_update', self.after_update, named=True);
            listen(table_class, 'after_delete', self.after_delete, named=True);
