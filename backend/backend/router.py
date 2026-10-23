class ExternalDatabaseRouter:
    """
    Send the events app to the social_event database.
    Everything else goes to the default database.
    """

    app_label = "events"
    database = "social_event"

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return self.database

        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return self.database

        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        db1 = self.db_for_read(obj1)
        db2 = self.db_for_read(obj2)

        if db1 == db2:
            return True

        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # events app belongs ONLY in social_event
        if app_label == self.app_label:
            return db == self.database

        # Everything else belongs ONLY in default
        if db == self.database:
            return False

        return db == "default"