import pandas as pd
import numpy as np
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Operation {func.__name__} took {end - start:.2f}s')
        return result
    return wrapper

class DataProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self._load_file()

    def _load_file(self):
        if self.filepath.endswith('.csv'):
            return pd.read_csv(self.filepath)
        elif self.filepath.endswith('.xlsx'):
            return pd.read_excel(self.filepath)
        else:
            raise ValueError("Unsupported file type.")

    @timer
    def clean(self):
        # Remove duplicates and missing values
        before = self.data.shape
        self.data.drop_duplicates(inplace=True)
        self.data.dropna(inplace=True)
        after = self.data.shape
        print(f"Cleaned data: {before} -> {after}")

    @timer
    def analyze(self):
        desc = self.data.describe(include='all').to_dict()
        report = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'summary': desc
        }
        return report

    def save_report(self, report, output_file):
        # Save as JSON or CSV
        import json
        if output_file.endswith('.json'):
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
        elif output_file.endswith('.csv'):
            pd.DataFrame(report['summary']).to_csv(output_file)
        print(f"Report saved to {output_file}")
