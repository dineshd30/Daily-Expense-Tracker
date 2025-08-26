from datetime import datetime


def get_date(prompt: str, allow_default: bool):
    date_fmt = "%d-%m-%Y"
    date_str = input(prompt)

    if allow_default and not date_str:
        return datetime.today().strftime(date_fmt)

    try:
        valid_date = datetime.strptime(date_str, date_fmt)
        return valid_date.strftime(date_fmt)
    except ValueError:
        print("failed to get valid date in format dd-mm-yyy")
        get_date(prompt, allow_default)


def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be non-negative non-zero value")
        return amount
    except ValueError as e:
        print(e)
        get_amount()


def get_category():
    categories = {"I": "Income", "E": "Expense"}
    category = input(
        "Please enter category (`I` for Income or `E` for Expense): "
    ).upper()

    if category in categories:
        return categories[category]

    print("failed to get correct category")
    get_category()


def get_description():
    description = input("Please enter description: ")

    if len(description) > 0:
        return description

    print("failed to get correct description")
    get_description()
