"""
Problematic data processing pipeline with various code quality and efficiency issues
"""
import os
import pandas as pd
import numpy as np
import time
import json
import logging
import glob
from datetime import datetime
import pickle
import subprocess

# Hardcoded credentials and paths
DB_CONNECTION = "postgresql://admin:insecure_password@db.example.com:5432/analytics"
API_KEY = "1a2b3c4d5e6f7g8h9i0j"
DATA_DIR = "/data/raw"
OUTPUT_DIR = "/data/processed"

# Global variables that should be constants
default_chunk_size = 1000
error_threshold = 0.05
debug_mode = True

# Initialize logging without proper configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    def __init__(self, input_path=None, output_path=None):
        # Not using the constructor parameters
        self.input_dir = DATA_DIR
        self.output_dir = OUTPUT_DIR
        self.data = None
        # Large magic number that should be a named constant
        self.max_file_size = 104857600  # 100MB
    
    def load_data(self, filename):
        """Load data from a CSV file"""
        try:
            # Not handling file not found properly
            file_path = os.path.join(self.input_dir, filename)
            # Reading entire file into memory without chunking
            self.data = pd.read_csv(file_path)
            logger.info(f"Loaded data from {file_path} with {len(self.data)} rows")
            return True
        except Exception as e:
            # Catching all exceptions is too broad
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def process_data(self):
        """Process the loaded data"""
        if self.data is None:
            logger.error("No data loaded")
            return False
        
        try:
            # Inefficient data processing - applying function row by row
            logger.info("Processing data...")
            start_time = time.time()
            
            # Using apply with lambda is inefficient
            self.data['processed_col'] = self.data['raw_value'].apply(lambda x: self._complex_transformation(x))
            
            # Direct SQL injection vulnerability
            user_filter = input("Enter a filter condition for SQL query: ")
            query = f"SELECT * FROM user_data WHERE {user_filter}"
            
            # Inefficient data filtering
            filtered_data = pd.DataFrame()
            for i, row in self.data.iterrows():  # Slow row iteration
                if self._should_include(row):
                    filtered_data = filtered_data.append(row)  # Inefficient append
            
            # Memory leak - creating large temporary dataframes
            temp_df1 = self.data.copy()
            temp_df2 = filtered_data.copy()
            result = pd.concat([temp_df1, temp_df2])
            
            logger.info(f"Data processing completed in {time.time() - start_time:.2f} seconds")
            self.data = result
            return True
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            return False
    
    def _complex_transformation(self, value):
        """Perform a complex transformation on a value"""
        # Unnecessarily complex and inefficient
        if value is None:
            return 0
        
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return 0
        
        # Magic numbers that should be constants
        if value > 1000:
            return value * 1.15
        elif value > 500:
            return value * 1.1
        elif value > 100:
            return value * 1.05
        else:
            return value
    
    def _should_include(self, row):
        """Determine if a row should be included in the output"""
        # Complex nested conditions - hard to understand
        if row['status'] == 'active':
            if row['value'] > 0:
                if not pd.isna(row['category']):
                    if row['category'] not in ['test', 'temp', 'draft']:
                        if pd.to_datetime(row['date']) > pd.Timestamp('2020-01-01'):
                            return True
        return False
    
    def save_results(self, filename=None):
        """Save the processed data"""
        if self.data is None:
            logger.error("No data to save")
            return False
        
        if filename is None:
            # Using timestamp in filename without formatting
            filename = f"processed_data_{int(time.time())}.csv"
        
        try:
            output_path = os.path.join(self.output_dir, filename)
            # Not checking if directory exists
            self.data.to_csv(output_path, index=False)
            logger.info(f"Saved results to {output_path}")
            
            # Unsafe command execution
            command = f"chmod 644 {output_path}"
            os.system(command)  # Vulnerable to command injection
            
            return True
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            return False
    
    def generate_report(self):
        """Generate a report from the processed data"""
        if self.data is None:
            logger.error("No data for report generation")
            return False
        
        try:
            # Serializing entire dataframe is inefficient
            serialized_data = pickle.dumps(self.data)
            
            # Unsafe deserialization
            report_data = pickle.loads(serialized_data)  # Security vulnerability
            
            report = {
                "total_rows": len(report_data),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "summary": {},
            }
            
            # Inefficient summary calculation - should use built-in methods
            for column in report_data.columns:
                if report_data[column].dtype in [np.int64, np.float64]:
                    report["summary"][column] = {
                        "min": float(report_data[column].min()),
                        "max": float(report_data[column].max()),
                        "mean": float(report_data[column].mean()),
                        "median": float(report_data[column].median()),
                    }
            
            # Writing report to file without proper error handling
            report_path = os.path.join(self.output_dir, "report.json")
            with open(report_path, 'w') as f:
                json.dump(report, f)
            
            return report
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return None
    
    def cleanup(self):
        """Clean up resources"""
        # Not releasing memory properly
        logger.info("Cleanup started")
        
        # Leaving files open
        temp_files = glob.glob(os.path.join(self.output_dir, "temp_*.csv"))
        for file in temp_files:
            try:
                os.remove(file)
            except:
                pass  # Silent failure
        
        # Not clearing large data
        # self.data = None  # This should be uncommented
        
        logger.info("Cleanup finished")


def run_pipeline(input_file, output_file=None):
    """Run the complete data processing pipeline"""
    processor = DataProcessor()
    success = processor.load_data(input_file)
    
    if not success:
        logger.error("Pipeline failed at data loading stage")
        return False
    
    success = processor.process_data()
    if not success:
        logger.error("Pipeline failed at data processing stage")
        return False
    
    success = processor.save_results(output_file)
    if not success:
        logger.error("Pipeline failed at saving results stage")
        return False
    
    report = processor.generate_report()
    if report is None:
        logger.warning("Report generation failed")
    
    # Not calling cleanup
    # processor.cleanup()
    
    return True


if __name__ == "__main__":
    # Accepting filename from command line without validation
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        run_pipeline(input_file, output_file)
    else:
        print("Usage: python data_processor.py <input_file> [output_file]")
