import csv
from collections import defaultdict
from datetime import datetime

from .settings import BASE_DIR


class PepParsePipeline:
    def __init__(self):
        self.results_dir = BASE_DIR / 'results'
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.pep_statuses = defaultdict(int)

    def process_item(self, item, spider):
        self.pep_statuses[item.get('status')] += 1
        return item

    def close_spider(self, spider):
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        filename = f'status_summary_{date_time}.csv'
        with open(f'{self.results_dir}/{filename}', 'w',
                  encoding='utf-8', newline='') as f:
            csv.writer(f, dialect=csv.excel).writerows(
                (
                    ('Статус', 'Количество'),
                    *self.pep_statuses.items(),
                    ('Всего', sum(self.pep_statuses.values())),
                )
            )
