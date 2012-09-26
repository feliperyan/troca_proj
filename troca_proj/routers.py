class AuthRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'troca_app':
            return 'mongo_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'troca_app':
            return 'mongo_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'troca_app' or \
           obj2._meta.app_label == 'troca_app':
           return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the auth app only appears in the 'mongo_db'
        database.
        """
        if db == 'mongo_db':
            return model._meta.app_label == 'troca_app'
        elif model._meta.app_label == 'troca_app':
            return False
        return None