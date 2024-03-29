import pandas as pd
from datetime import datetime
from data.stock_data import pull_stocks
from model.model_create import creation_of_the_gods, prediction_of_the_gods
import os


def run_stock_predictions(stocks, mod_choice):
    # Initialize a list to store results
    results = []
    m_choice = mod_choice
    # Loop through each stock ticker
    for stock in stocks:
        model_data, model_input = pull_stocks([stock])
        model, base, random, grid = creation_of_the_gods(model_data, m_choice)

        # Predictions
        preds = prediction_of_the_gods(model_input, model)
        base_preds = prediction_of_the_gods(model_input, base)
        random_preds = prediction_of_the_gods(model_input, random)
        grid_preds = prediction_of_the_gods(model_input, grid)

        # Extract the numerical value from the Pandas Series and round it
        previous_close_value = model_input["Prev_Day_Close"].iloc[
            0
        ]  # Assuming you want the first (or only) value
        previous_close_rounded = round(previous_close_value, 2)

        # Round predicted values
        predicted_close_rounded = round(preds[0], 2)
        base_predicted_close_rounded = round(base_preds[0], 2)
        random_predicted_close_rounded = round(random_preds[0], 2)
        grid_predicted_close_rounded = round(grid_preds[0], 2)

        # Compile results
        results.append(
            {
                "TICKER": stock,
                "PREVIOUS CLOSE": previous_close_rounded,
                "PREDICTED CLOSE": predicted_close_rounded,
                "PREDICTED BASE CLOSE": base_predicted_close_rounded,
                "PREDICTED RANDOM CLOSE": random_predicted_close_rounded,
                "PREDICTED GRID CLOSE": grid_predicted_close_rounded,
            }
        )

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Generate filename with today's date
    filename = f"{datetime.now().strftime('%Y-%m-%d')}_stock_predictions.csv"
    current_directory = os.getcwd()
    predictions_folder_path = os.path.join(current_directory, "csv")
    if not os.path.exists(predictions_folder_path):
        os.makedirs(predictions_folder_path)
    full_file_path = os.path.join(predictions_folder_path, filename)

    # Export to CSV
    results_df.to_csv(full_file_path, index=False)

    print(f"Predictions saved to {filename}")
