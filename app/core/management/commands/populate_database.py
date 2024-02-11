"""
Command to populate the database with the data from the excel file

"""
from typing import Any
from django.core.management.base import BaseCommand
from core.tasks import import_excel_data
class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        """Entry Point for the Command """

        self.stdout.write('calling the task...')
        import_excel_data.delay()


        self.stdout.write(self.style.SUCCESS('Task to Populate the Database called successfully...'))