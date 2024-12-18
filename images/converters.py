class FloatConverter:
    regex = r'-?\d+\.\d+'  # Matches floats, including negative values

    def to_python(self, value):
        return float(value)  # Convert string to float

    def to_url(self, value):
        return str(value)  # Convert float back to string for URL
