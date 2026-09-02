from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expense_tracker.db")

mcp = FastMCP("Expense Tracker")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT '',
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close() 

init_db()

@mcp.tool()
def add_expense(amount: float, category: str, subcategory: str = '', note: str = '', date: str = ''):
    """Add a new expense to the tracker."""
    if not date:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, subcategory, note, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (amount, category, subcategory, note, date)
    )
    conn.commit()
    conn.close()
    return f"Expense of {amount} added under category '{category}'."


@mcp.tool()
def list_expenses(category: str = '', subcategory: str = ''):
    """List all expenses, optionally filtered by category and subcategory."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM expenses"
    params = []
    
    if category and subcategory:
        query += " WHERE category = ? AND subcategory = ?"
        params.extend([category, subcategory])
    elif category:
        query += " WHERE category = ?"
        params.append(category)
    elif subcategory:
        query += " WHERE subcategory = ?"
        params.append(subcategory)

    query += " ORDER BY id"
    cursor.execute(query, params)
    expenses = cursor.fetchall()
    conn.close()
    
    return expenses

@mcp.tool()
def edit_expenses(expense_id: int, amount: float = None, category: str = None, subcategory: str = None, note: str = None, date: str = None):
    """Edit an existing expense by its ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Build the update query dynamically based on provided parameters
    updates = []
    params = []
    
    if amount is not None:
        updates.append("amount = ?")
        params.append(amount)
    if category is not None:
        updates.append("category = ?")
        params.append(category)
    if subcategory is not None:
        updates.append("subcategory = ?")
        params.append(subcategory)
    if note is not None:
        updates.append("note = ?")
        params.append(note)
    if date is not None:
        updates.append("date = ?")
        params.append(date)
    
    if not updates:
        return "No fields to update."
    
    params.append(expense_id)
    query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    
    return f"Expense with ID {expense_id} updated successfully."


@mcp.tool()
def delete_expense(expense_id: int):
    """Delete an expense by its ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    
    return f"Expense with ID {expense_id} deleted successfully."


@mcp.tool()
def add_credit(amount: float, note: str = '', date: str = ''):
    """Record a received credit."""
    if not date:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, subcategory, note, date)
        VALUES (?, 'Credit', '', ?, ?)
    ''', (amount, note, date))
    conn.commit()
    conn.close()
    
    return f"Received credit of {amount} recorded successfully."

@mcp.tool()
def list_credits():
    """List all received credits."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE category = 'Credit'")
    credits = cursor.fetchall()
    conn.close()
    
    return credits

@mcp.tool()
def spending_summary(category: str = '', start_date: str = '', end_date: str = ''):
    """Provide a summary of spending by category."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT category, SUM(amount) AS total_spent
        FROM expenses
        WHERE category != 'Credit'
    '''
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " GROUP BY category"
    cursor.execute(query, params)
    
    summary = cursor.fetchall()
    conn.close()
    
    return summary


if __name__ == "__main__":
    mcp.run()
