from companyConnect import create_conn
from sqlalchemy import create_engine, text # "Text" is only included with the newest call
import pandas as pd

conn = create_conn()

# create a connection to the database
# We are going to use a formatted string to connect using the lambda function
engine = create_engine("mysql+mysqlconnector://", creator=lambda: conn)

# Set a custom display format for floats
pd.options.display.float_format = '{:,.2f}'.format

# Select records
# sql_query = "select Store, Weekly_Sales from sales where Store = 1;"

# sql_query = "select Dept AS Department, Weekly_Sales from sales where Dept = 5;"

#sql_query = "select sales.Dept AS Department, sales.Weekly_Sales, expenses_month_dept.Expense_Allocation AS Expense from sales inner join expenses_month_dept on sales.Dept = expenses_month_dept.Dept where sales.Dept = 5;"

#sql_query = "select sales.Dept AS Department, sales.Weekly_Sales, expenses_month_dept.Expense_Allocation AS Expense,\
#    expenses_month_dept.ExpenseDate, sales.SalesDate from sales inner join expenses_month_dept on sales.Dept = expenses_month_dept.Dept where sales.Dept = 5;"

sql_query = "select sales.Dept AS Department, format(sales.SalesDate, 'yyyy-MM') AS SalesMonth, sum(sales.Weekly_Sales) AS TotalWeeklySales, \
    expenses_month_dept.Expense_Allocation AS MonthlyExpense, expenses_month_dept.ExpenseDate, \
        (sum(sales.Weekly_Sales) - expenses_month_dept.Expense_Allocation) AS Profit from sales inner join expenses_month_dept \
            on sales.Dept = expenses_month_dept.Dept where sales.Dept = 5 group by sales.Dept, format(sales.SalesDate, 'yyyy-MM'), \
                expenses_month_dept.Expense_allocation, expenses_month_dept.ExpenseDate;"


sql = text(sql_query)

# Execute the query and return the results into a Pandas dataframe
sales_df = pd.read_sql_query(sql, engine)
# sales_df.info

# Print the results
print(sales_df)
