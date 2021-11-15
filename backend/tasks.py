"""
celery -A backend.tasks worker --loglevel=INFO --pool=solo
celery -A backend.tasks beat
"""
from celery.schedules import crontab

from backend import db
from backend import celery
from backend.models.products import Product
from backend.models.users import User
from backend.translation import get_text as _
from backend.utils import scrape_price, send_email


celery.conf.beat_schedule = {
    'scrape-every-hour': {
        'task': 'backend.tasks.check_prices',
        'schedule': crontab()
    },
}


@celery.task
def check_prices():
    products = Product.query.filter_by(is_monitored=True).all()

    for product in products:
        price = scrape_price(product)
        if price and price != product.current_price:
            product.current_price = price
            db.session.commit()
            if price <= product.desired_price:
                user = User.query.get(product.user_id)
                if user:
                    send_email(
                        _('price_drop').format(product.name, price),
                        _('check_product_link').format(product.url),
                        user.email
                    )
