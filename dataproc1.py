import pandas as pd
import numpy as np
import time
import json
from functools import wraps

# ============================================
# DECORATORS SECTION
# ============================================

def timer(func):
    """
    Decorator to measure execution time of any function.
    
    Line-by-line:
    - @wraps preserves original function metadata (name, docstring)
    - wrapper(*args, **kwargs) accepts any arguments
    - Measures time before and after function execution
    - Returns original function result
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'⏱️  {func.__name__} took {end - start:.2f}s')
        return result
    return wrapper

def log_operation(func):
    """
    Decorator to log what operation is being performed.
    
    Why: Helps track what your program is doing, useful for debugging
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'📝 Starting: {func.__name__}')
        result = func(*args, **kwargs)
        print(f'✅ Completed: {func.__name__}')
        return result
    return wrapper

def handle_errors(func):
    """
    Decorator to catch and handle errors gracefully.
    
    Why: Prevents program crashes, shows user-friendly error messages
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'❌ Error in {func.__name__}: {str(e)}')
            return None
    return wrapper

# ============================================
# CUSTOM EXCEPTIONS
# ============================================

class DataProcessorError(Exception):
    """Base exception for DataProcessor"""
    pass

class FileLoadError(DataProcessorError):
    """Raised when file cannot be loaded"""
    pass

class DataCleaningError(DataProcessorError):
    """Raised when data cleaning fails"""
    pass

# ============================================
# MAIN DATA PROCESSOR CLASS
# ============================================

class DataProcessor:
    """
    Main class for processing data files.
    
    Attributes:
        filepath (str): Path to the data file
        data (pd.DataFrame): The loaded data
        original_shape (tuple): Original data dimensions (rows, cols)
    
    Methods:
        clean(): Remove duplicates and missing values
        analyze(): Generate statistical summary
        filter_data(): Filter based on column conditions
        group_by(): Group data by column and aggregate
        plot_graph(): Create visualizations
        save_report(): Export results
    """
    
    def __init__(self, filepath):
        """
        Initialize DataProcessor.
        
        Line-by-line:
        - self.filepath: Store the file path
        - self.data: Load file into pandas DataFrame
        - self.original_shape: Remember original size before cleaning
        """
        self.filepath = filepath
        self.data = self._load_file()
        self.original_shape = self.data.shape
        print(f"📂 Loaded {filepath}: {self.data.shape} rows, {self.data.shape} columns")

    @handle_errors
    def _load_file(self):
        """
        Private method to load different file types.
        
        Why private (_): Internal helper method, users don't call directly
        
        Line-by-line:
        - Check file extension
        - Use appropriate pandas reader
        - Raise custom exception if unsupported
        """
        if self.filepath.endswith('.csv'):
            return pd.read_csv(self.filepath)
        elif self.filepath.endswith('.xlsx') or self.filepath.endswith('.xls'):
            return pd.read_excel(self.filepath)
        elif self.filepath.endswith('.json'):
            return pd.read_json(self.filepath)
        else:
            raise FileLoadError(f"Unsupported file type: {self.filepath}")

    @timer
    @log_operation
    def clean(self):
        """
        Clean data by removing duplicates and missing values.
        
        Line-by-line:
        - before: Store shape before cleaning
        - drop_duplicates(): Remove exact duplicate rows
        - dropna(): Remove rows with any missing values
        - after: Store shape after cleaning
        - Calculate and print how many rows removed
        
        Why @timer and @log_operation: Track performance and log actions
        """
        before = self.data.shape
        self.data.drop_duplicates(inplace=True)
        self.data.dropna(inplace=True)
        after = self.data.shape
        
        rows_removed = before - after
        print(f"🧹 Cleaned: Removed {rows_removed} rows")
        print(f"   Before: {before} → After: {after}")

    @timer
    @log_operation
    def analyze(self):
        """
        Generate comprehensive statistical analysis.
        
        Returns:
            dict: Contains shape, columns, data types, and statistics
        
        Line-by-line:
        - describe(include='all'): Statistics for all columns
        - to_dict(): Convert to dictionary for JSON export
        - dtypes: Data types of each column
        - Build report dictionary with all info
        """
        stats = self.data.describe(include='all').to_dict()
        
        report = {
            'filename': self.filepath,
            'original_shape': self.original_shape,
            'current_shape': self.data.shape,
            'columns': list(self.data.columns),
            'data_types': {col: str(dtype) for col, dtype in self.data.dtypes.items()},
            'statistics': stats,
            'missing_values': self.data.isnull().sum().to_dict()
        }
        
        print(f"📊 Analysis complete: {len(self.data.columns)} columns analyzed")
        return report

    @timer
    def filter_data(self, column, operator, value):
        """
        Filter data based on conditions.
        
        Args:
            column (str): Column name to filter
            operator (str): Comparison operator ('>', '<', '==', '!=', '>=', '<=')
            value: Value to compare against
        
        Example:
            dp.filter_data('Sales', '>', 500)
        
        Line-by-line:
        - Check if column exists
        - Build filter condition based on operator
        - Apply filter to self.data
        - Print how many rows match
        """
        if column not in self.data.columns:
            print(f"❌ Column '{column}' not found")
            return
        
        before = len(self.data)
        
        if operator == '>':
            self.data = self.data[self.data[column] > value]
        elif operator == '<':
            self.data = self.data[self.data[column] < value]
        elif operator == '==':
            self.data = self.data[self.data[column] == value]
        elif operator == '!=':
            self.data = self.data[self.data[column] != value]
        elif operator == '>=':
            self.data = self.data[self.data[column] >= value]
        elif operator == '<=':
            self.data = self.data[self.data[column] <= value]
        else:
            print(f"❌ Invalid operator: {operator}")
            return
        
        after = len(self.data)
        print(f"🔍 Filter applied: {before} → {after} rows (kept {after} rows)")

    @timer
    def group_by(self, column, agg_func='mean'):
        """
        Group data by column and calculate aggregate.
        
        Args:
            column (str): Column to group by
            agg_func (str): Aggregation function ('mean', 'sum', 'count', 'min', 'max')
        
        Returns:
            pd.DataFrame: Grouped results
        
        Line-by-line:
        - Check column exists
        - Select only numeric columns for aggregation
        - Use pandas groupby() with specified aggregation
        - Print results in readable format
        """
        if column not in self.data.columns:
            print(f"❌ Column '{column}' not found")
            return None
        
        # Get numeric columns only
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        if agg_func == 'mean':
            result = self.data.groupby(column)[numeric_cols].mean()
        elif agg_func == 'sum':
            result = self.data.groupby(column)[numeric_cols].sum()
        elif agg_func == 'count':
            result = self.data.groupby(column).size()
        elif agg_func == 'min':
            result = self.data.groupby(column)[numeric_cols].min()
        elif agg_func == 'max':
            result = self.data.groupby(column)[numeric_cols].max()
        else:
            print(f"❌ Invalid aggregation: {agg_func}")
            return None
        
        print(f"📈 Grouped by '{column}' using {agg_func}:")
        print(result)
        return result

    @handle_errors
    def plot_graph(self, x_col, y_col, kind='line'):
        """
        Create visualizations (requires matplotlib).
        
        Args:
            x_col (str): X-axis column
            y_col (str): Y-axis column
            kind (str): Chart type ('line', 'bar', 'scatter', 'hist')
        
        Note: Install matplotlib: pip install matplotlib
        
        Line-by-line:
        - Import matplotlib (lazy import)
        - Check columns exist
        - Use pandas plot() method with specified kind
        - Set labels and title
        - Display the plot
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("❌ matplotlib not installed. Run: pip install matplotlib")
            return
        
        if x_col not in self.data.columns or y_col not in self.data.columns:
            print(f"❌ One or both columns not found")
            return
        
        self.data.plot(x=x_col, y=y_col, kind=kind, figsize=(10, 6))
        plt.title(f'{y_col} vs {x_col}')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.tight_layout()
        plt.savefig(f'plot_{x_col}_{y_col}.png')
        print(f"📊 Plot saved as: plot_{x_col}_{y_col}.png")
        plt.show()

    def save_report(self, report, output_file):
        """
        Save analysis report to file.
        
        Args:
            report (dict): Report data from analyze()
            output_file (str): Output filename
        
        Line-by-line:
        - Check file extension
        - For JSON: use json.dump() with indent for readability
        - For CSV: convert dict to DataFrame and save
        - Print confirmation message
        """
        if output_file.endswith('.json'):
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"💾 Report saved to: {output_file}")
        elif output_file.endswith('.csv'):
            # Convert statistics to DataFrame for CSV export
            stats_df = pd.DataFrame(report['statistics'])
            stats_df.to_csv(output_file)
            print(f"💾 Statistics saved to: {output_file}")
        else:
            print(f"❌ Unsupported output format. Use .json or .csv")

    def show_info(self):
        """
        Display quick overview of current data.
        
        Line-by-line:
        - Print basic info (shape, columns, types)
        - Show first 5 rows using head()
        - Display missing value counts
        """
        print("\n" + "="*50)
        print(f"📋 DATA OVERVIEW: {self.filepath}")
        print("="*50)
        print(f"Shape: {self.data.shape}")
        print(f"Columns: {list(self.data.columns)}")
        print(f"\nData Types:\n{self.data.dtypes}")
        print(f"\nMissing Values:\n{self.data.isnull().sum()}")
        print(f"\nFirst 5 rows:\n{self.data.head()}")
        print("="*50 + "\n")
