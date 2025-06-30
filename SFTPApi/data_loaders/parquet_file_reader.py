import pandas as pd

class ParquetReader:
    """
    A class to read and process data from Parquet files using pandas.
    The file path is passed as a parameter to methods rather than being set during initialization.
    """

    def __init__(self):
        """
        Initialize the ParquetReader without requiring a file path.
        """
        self.df = None

    def load_data(self, file_path):
        """
        Load data from the specified Parquet file into a pandas DataFrame.

        Args:
            file_path (str): Path to the Parquet file

        Returns:
            pd.DataFrame: The loaded DataFrame or None if loading fails
        """
        try:
            self.df = pd.read_parquet(file_path)
            print(f"Successfully loaded data from {file_path}")
            return self.df
        except Exception as e:
            print(f"Error loading Parquet file: {e}")
            return None

    def get_dataframe(self):
        """
        Get the currently loaded DataFrame.

        Returns:
            pd.DataFrame: The loaded DataFrame or None if not loaded
        """
        return self.df

    def get_summary(self, file_path=None):
        """
        Get a summary of the data, optionally loading from a new file first.

        Args:
            file_path (str, optional): Path to a new Parquet file to load

        Returns:
            dict: Dictionary containing basic statistics about the data
        """
        if file_path is not None:
            self.load_data(file_path)

        if self.df is None:
            return {"error": "Data not loaded"}

        return {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "head": self.df.head().to_dict(),
            "description": self.df.describe().to_dict()
        }