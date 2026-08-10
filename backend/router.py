class ExternalDatabaseRouter:
    target_app = "events"
    target_db = "social_event"

    def db_for_read(self, model, **hints):
        """Send all read operations for the events app to the social_event database."""
        if model._meta.app_label == self.target_app:
            return self.target_db
        return "default"

    def db_for_write(self, model, **hints):
        """Send all write operations for the events app to the social_event database."""
        if model._meta.app_label == self.target_app:
            return self.target_db
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the events app is involved.
        Relations must stay within their respective databases.
        """
        if (
            obj1._meta.app_label == self.target_app
            and obj2._meta.app_label == self.target_app
        ):
            return True
        elif self.target_app not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None  # Let Django handle its own internal relations
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations only for the correct app on the correct database.
        """
        if app_label == self.target_app:
            # If the app is 'events', only allow migrations on the 'social_event' db
            return db == self.target_db
        elif db == self.target_db:
            # If the database is 'social_event', don't allow any other apps
            return False
        # For any other app, allow migrations on the 'default' database
        return None
