from src.backend import app
from src.backend.data_manager import DataManager

DataManager().validate()
app.run(debug=True)
