"""
Custom Django Command to wait for the database to be available before continuing

"""
import time
from typing import Any
from psycopg2 import OperationalError as Psycopg2OperationalError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        """Entry Point for the Command """

        self.stdout.write('Waiting for database...')
        db_check = False
        while db_check is False:
            try:
                self.check(databases=['default'])
                db_check = True
            except (Psycopg2OperationalError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
