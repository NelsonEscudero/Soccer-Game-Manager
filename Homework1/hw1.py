# Use this file to write your queries. Submit this file to Gradescope after finishing your homework.

# Make sure to test that this script prints out the strings (your SQL queries) correctly.

# To verify your submission is in the correct format: `python3 hw1.py`

# Make sure the program prints out your SQL statements correctly. That means the autograder will read you SQL correctly. Running the Python file will not execute your SQL statements (just prints them).

instr = '''Instructions:
	Please put the queries under the corresponding functions below.
	Running this python file will check if the formatting is okay.
'''

def query1():
	return """
    SELECT order_dow, COUNT(*) AS order_count
	FROM "order"
	GROUP BY order_dow
	ORDER BY order_dow;
	"""

def query2():
	return """
	SELECT COUNT(*) AS sunday_afternoon_orders
	FROM "order"
	WHERE order_dow == 0 AND order_hour_of_day > 11 AND order_hour_of_day < 19;
	"""

def query3():
	return """
	SELECT user_id, COUNT(*) AS order_count
	FROM "order"
	GROUP BY user_id
	HAVING COUNT(*) > 10;
	"""

	
def query4():
	return """
	SELECT d.department, p.product_id, p.product_name
	FROM "product" p, "department" d
	WHERE p.department_id = d.department_id AND d.department = 'dairy eggs' AND p.product_name LIKE '%Swiss Cheese%';
	"""


def query5():
	return """
	SELECT op.order_id
	FROM "order-product" op, "product" p
	WHERE op.product_id = p.product_id AND p.product_name = 'Apple Juice'
	ORDER BY op.order_id;
	"""


def query6():
	return """
	SELECT order_id
	FROM "order-product"
	GROUP BY order_id
	HAVING COUNT(*) > 2;
	"""


def query7():
	return """
	SELECT p.product_name, o.user_id
	FROM "product" p LEFT OUTER JOIN "order-product" op ON p.product_id = op.product_id
	LEFT OUTER JOIN "order" o ON op.order_id = o.order_id
	WHERE p.product_name LIKE '%Swiss Cheese%' AND p.product_name LIKE '%Slices%';
	"""


def query8():
	return """
	SELECT p.product_name, a.aisle, d.department, o.user_id
	FROM "product" p LEFT OUTER JOIN "aisle" a ON p.aisle_id = a.aisle_id
	LEFT OUTER JOIN "department" d ON p.department_id = d.department_id
	LEFT OUTER JOIN "order-product" op ON p.product_id = op.product_id
	LEFT OUTER JOIN "order" o ON op.order_id = o.order_id
	WHERE p.product_name LIKE '%Swiss Cheese%' AND p.product_name LIKE '%Slices%';
	"""


def query9():
	return """
	SELECT department, CAST(FLOOR(AVG(pc)) AS INT) AS avg_products_per_aisle
	FROM (SELECT d.department, a.aisle_id, COUNT(p.product_id) AS pc
		FROM "product" p JOIN "aisle" a ON p.aisle_id = a.aisle_id
		JOIN "department" d ON p.department_id = d.department_id
		WHERE d.department IN ('snacks', 'beverages')
		GROUP BY d.department, a.aisle_id
	) AS temp
	GROUP BY department;
	"""


def query10():
	return """
	SELECT p.product_name, COUNT(DISTINCT o.user_id) AS num_users
	FROM "product" p JOIN "order-product" op ON p.product_id = op.product_id
	JOIN "order" o ON op.order_id = o.order_id
	GROUP BY p.product_name
	HAVING COUNT(DISTINCT o.user_id) > 199
	ORDER BY num_users DESC;
	"""


def query11():
	return """
	SELECT p.product_name, COUNT(op.product_id) AS total_orders
	FROM "product" p JOIN "order-product" op ON p.product_id = op.product_id
	GROUP BY p.product_id
	ORDER BY total_orders DESC
	LIMIT 3;
	"""


def query12():
	return """
	SELECT p1.product_id, p1.product_name, p2.product_id, p2.product_name
	FROM "product" p1 JOIN "product" p2 ON p1.product_id < p2.product_id
	WHERE p1.product_name LIKE '%Chips Ahoy!%' AND p1.product_name LIKE '%Chewy%'
		AND p2.product_name LIKE '%Chips Ahoy!%' AND p2.product_name LIKE '%Chewy%';
	"""


def query13():
	return """
	SELECT o.user_id
	FROM "order" o JOIN "order-product" op ON o.order_id = op.order_id
	JOIN "product" p ON op.product_id = p.product_id
	WHERE p.product_name IN ('Organic Bartlett Pear', 'Organic Bosc Pear')
	GROUP BY o.user_id
	HAVING COUNT(DISTINCT p.product_name) > 1;
	"""

def query14():
	return """
	SELECT p1.product_name AS product1, p2.product_name AS product2, COUNT(*) AS co_occurrence
	FROM "order-product" op1 JOIN "order-product" op2 ON op1.order_id = op2.order_id
	JOIN "product" p1 ON op1.product_id = p1.product_id
	JOIN "product" p2 ON op2.product_id = p2.product_id
	WHERE op1.product_id < op2.product_id
	GROUP BY p1.product_name, p2.product_name
	HAVING COUNT(*) > 1
	ORDER BY p1.product_id;
	"""

def query15():
	return """
	SELECT p.product_name
	FROM product p
	WHERE p.product_name LIKE '%Swiss Cheese%'
		AND p.product_id NOT IN (
			SELECT op.product_id
			FROM "order-product" op
			JOIN "order" o ON op.order_id = o.order_id)
	GROUP BY p.product_name;
	"""

#Do not edit below

if __name__ == "__main__":
	try:
		if all(type(eval(f'print(t:=query{f+1}()),t')[1]) is str for f in range(15)):
			print(f'Your submission is valid.')
		else:
			raise TypeError('Invalid Return Types.')
	except Exception as e:
		print(f'Your submission is invalid.\n{instr}\n{e}')
