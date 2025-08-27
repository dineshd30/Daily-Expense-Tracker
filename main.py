import csv
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from data_entry import get_amount, get_category, get_date, get_description


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod
    def initialise_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        with open(cls.CSV_FILE, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

        print("New row added successfully!")

    @classmethod
    def get_transaction(cls, start_date, end_date):
        start_date = datetime.strptime(start_date, CSV.DATE_FORMAT)
        end_date = datetime.strptime(end_date, CSV.DATE_FORMAT)

        df: pd.DataFrame = pd.read_csv(CSV.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.DATE_FORMAT)
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df: pd.DataFrame = df.loc[mask]

        if filtered_df.empty:
            print("failed find any transactions for given dates")
        else:
            filtered_df = filtered_df.sort_values("date")
            print(
                f"Transactions from {start_date.strftime(CSV.DATE_FORMAT)} to {end_date.strftime(CSV.DATE_FORMAT)}"
            )

            print(
                filtered_df.to_string(
                    index=False,
                    formatters={"date": lambda x: x.strftime(CSV.DATE_FORMAT)},
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()

            print("\n")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${ (total_income-total_expense):.2f}")
            return filtered_df


def add():
    date = get_date("Please enter date in format dd-mm-yyyy: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date=date, amount=amount, category=category, description=description)


def plot(filtered_df: pd.DataFrame):
    filtered_df.set_index("date", inplace=True)
    income_df = (
        filtered_df[filtered_df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(filtered_df.index, fill_value=0)
    )

    expense_df = (
        filtered_df[filtered_df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(filtered_df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    CSV.initialise_csv()
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter you choice(1-3): ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = input("Input start date in format dd-mm-yyyy: ")
            end_date = input("Input end date in format dd-mm-yyyy: ")
            df = CSV.get_transaction(start_date, end_date)
            if input("Do you want to see dashboard for above?(y/n): ").lower() == "y":
                plot(df)
        elif choice == "3":
            print("Exiting....")
            break
        else:
            print("failed to correct choice")


if __name__ == "__main__":
    main()
