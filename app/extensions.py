from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

# Initialize SQLAlchemy for database management
db = SQLAlchemy()

# Initialize Flask-Migrate for handling database migrations
migrate = Migrate()

# Initialize Flask-Moment for handling dates and times
moment = Moment()