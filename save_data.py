import datetime
import pandas as pd
import os


# current_date = str(datetime.date.today())

def save_file(excel_file_path, topics, sentiments, chunks, pdate, h_score, l_score):
    pdate = pdate.split("T")[0] 
    # Check if the file exists
    if os.path.exists(excel_file_path):
        # Load existing data
        df = pd.read_excel(excel_file_path)
    else:
        # Create a new DataFrame
        df = pd.DataFrame(columns=["Date", "News", "Topic", "Sentiment", "Score Before Rephrasing", "Score After Rephrasing"])

    # Create a new DataFrame with the new data
    for t, s, n, h, l in zip(topics, sentiments, chunks, h_score, l_score):
        new_data_df = pd.DataFrame([{"Date": pdate, "News": n, "Topic": t, "Sentiment": s, "Score Before Rephrasing":h, "Score After Rephrasing":l}])

        # Concatenate the existing data with the new data
        df = pd.concat([df, new_data_df], ignore_index=True)

    # Save the updated DataFrame back to the Excel file
    df.to_excel(excel_file_path, index=False)