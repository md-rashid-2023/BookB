"""
Populate Default values
"""
import logging

from django.core.management.base import BaseCommand

from book_store_app.models import *

# Set up the logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        components = [
            'home-page','customer-profile', 'admin-page','ticket-page', 'ticket-handler', 'can-see-ticket', 'can-raise-ticket', 'can-close-ticket' ]

        for c in components:
            BBComponents.objects.create(
                key = c,
                description = c.upper()
            )
        
        logger.info('added default components')
        
        roles = [
            'admin',
            'customer',
            'employee'
        ]

        for r in roles:

            BBRoles.objects.create(
                key = r,
                description = r.upper()
            )


        logger.info('added default roles')