import time

from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = "Check DB connections"

    def add_arguments(self, parser):
        parser.add_argument(
            '--max-counter', type=int, help="Max iteration for check."
        )
        parser.add_argument(
            '--sleep-interval', type=int, help="Interval after not successful attempt, sec."
        )

    def handle(self, *args, **options):
        max_counter = options.get('max-counter', 60)
        sleep_interval = options.get('sleep-interval', 1)

        for counter in range(max_counter):
            try:
                connection = connections['default']
                connection.connect()
                connection.close()
                self.stdout.write('Database is alive')
                break
            except KeyError:
                self.stderr.write("Database is not configured")
            except Exception as err:
                self.stderr.write(str(err))
                self.stderr.write('Database is dead, wait for {} sec'.format(max_counter - counter))
                time.sleep(sleep_interval)
