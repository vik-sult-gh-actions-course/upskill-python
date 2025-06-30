import pandas as pd


class ExcelFileReader:
    """
    A class to read and process data from Excel (XLSX) files using pandas.

    Attributes:
        df (pd.DataFrame): DataFrame containing the loaded data
    """

    def __init__(self):
        """
        Initialize the ExcelFileReader.
        """
        self.df = None

    def load_data(self, file_path, sheet_name=0):
        """
        Load data from an Excel file into a pandas DataFrame.

        Args:
            file_path (str): Path to the Excel file
            sheet_name (str/int): Name or index of sheet to read (default: first sheet)

        Returns:
            pd.DataFrame: The loaded DataFrame or None if loading fails
        """
        try:
            self.df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Successfully loaded data from {file_path} (sheet: {sheet_name})")
            return self.df
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None

    def get_dataframe(self):
        """
        Get the currently loaded DataFrame.

        Returns:
            pd.DataFrame: The loaded DataFrame or None if not loaded
        """
        return self.df

    def get_summary(self, file_path=None, sheet_name=0):
        """
        Get a summary of the data, optionally loading from a new file first.

        Args:
            file_path (str, optional): Path to a new Excel file to load
            sheet_name (str/int, optional): Sheet name or index to read

        Returns:
            dict: Dictionary containing basic statistics about the data
        """
        if file_path is not None:
            self.load_data(file_path, sheet_name)

        if self.df is None:
            return {"error": "Data not loaded"}

        return {
            "file_info": {
                "columns": list(self.df.columns),
                "shape": self.df.shape,
                "missing_values": self.df.isna().sum().to_dict()
            },
            "sample_data": self.df.head().to_dict(orient='records'),
            "numeric_stats": self._get_numeric_stats()
        }

    def _get_numeric_stats(self):
        """
        Helper method to get statistics for numeric columns.

        Returns:
            dict: Statistics for numeric columns or None if no numeric columns
        """
        numeric_df = self.df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            return numeric_df.describe().to_dict()
        return None