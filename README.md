# Expense Tracker
A simple expense tracker CLI application to manage your finances. 

---

## Installation End-user usage

### 1. Easy install with Pip
```bash
pip install git+https://github.com/flobell/expense-tracker.git
```

## Installation Dev

### 1. Clone the Repository
```bash
git clone https://github.com/flobell/expense-tracker.git
cd expense-tracker
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

- On Windows
```bash
.\venv\scripts\activate
```
- On macOS/Linux
```bash
source venv/bin/activate
```

### 4. Install project package

```bash
pip install -e .
```

## Unit Testing

### Execute unit tests

```
python -m unittest discover -s tests
```

---
## How to Use

### Adding a New Expense
```bash
expense-tracker add --description "sample" --amount 10
```

### Listing Expenses
```bash
expense-tracker list
```

### Summary expenses
```bash
expense-tracker summary
```

### Summary expense by month
```bash
expense-tracker summary --month 1
```

### Delete an expense
```bash
expense-tracker delete --id 1
```
---

## Project URL
- https://roadmap.sh/projects/expense-tracker