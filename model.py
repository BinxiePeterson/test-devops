

# Load libraries
from palmerpenguins import penguins
from pandas import get_dummies
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing

# Get Data
import duckdb
from palmerpenguins import penguins

con = duckdb.connect('my-db.duckdb')
df = penguins.load_penguins()
con.execute('CREATE OR REPLACE TABLE penguins AS SELECT * FROM df')
con.close()

con = duckdb.connect('my-db.duckdb')
df = con.execute("SELECT * FROM penguins").fetchdf().dropna()
con.close()

# Define Model and Fit
X = get_dummies(df[['bill_length_mm', 'species', 'sex']], drop_first = True)
y = df['body_mass_g']

model = LinearRegression().fit(X, y)

# Convert the model into a vetiver model
from vetiver import VetiverModel
v = VetiverModel(model, model_name="penguin_model", prototype_data=X)

# Create a directory for model output
import os
from tempfile import mkdtemp

# Create a temporary directory to store the app.py file for testing
tmpdir = "." + mkdtemp()

if not os.path.exists(tmpdir):
    # Create the directory
    os.makedirs(tmpdir)
    print("Directory created successfully!")

# Create a directory to use as the pin board
board_directory = "data/model"

# Check if the directory already exists
if not os.path.exists(board_directory):
    # Create the directory
    os.makedirs(board_directory)
    print("Directory created successfully!")

# Pin the vetiver model to a board folder
import pins
from pins import board_folder
from vetiver import VetiverModel
from vetiver import VetiverAPI
from vetiver import vetiver_pin_write
from vetiver import write_app

# Create a pin board and save (pin) the model
model_board = pins.board_folder(path="data/model", versioned=True, allow_pickle_read=True)

# Pin the model to the board
vetiver_pin_write(model_board, v)
write_app(model_board, "penguin_model", file=tmpdir + "/penguin_model.py")

app = VetiverAPI(v, check_prototype=True)
app.run(port = 8080)
