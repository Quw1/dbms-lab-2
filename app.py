from flask import Flask, render_template, request, redirect, jsonify
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.route('/users', methods=["GET"])
def users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers ORDER BY customerid")
            res = cursor.fetchall()
    return render_template('users.html', users=res)


@app.route('/users', methods=["POST"])
def users_crud():
    data = request.form
    uid = data.get('id')
    todo = data.get('todo')
    with connection:
        with connection.cursor() as cursor:
            if todo == "delete":
                stmt = "DELETE FROM customers WHERE customerid=%s"
                try:
                    cursor.execute(stmt, (uid, ))
                except Exception as e:
                    return redirect("/users", code=302)
                connection.commit()
            elif todo == "edit":
                stmt = "UPDATE customers SET firstname=%s, lastname=%s, email=%s WHERE customerid=%s"
                first_name = data.get('firstname')
                last_name = data.get('lastname')
                email = data.get('email')
                try:
                    cursor.execute(stmt, (first_name, last_name, email, uid,))
                except Exception as e:
                    return redirect("/users", code=302)
                connection.commit()
            elif todo == "add":
                stmt = "INSERT INTO customers(firstname, lastname, email) VALUES (%s, %s, %s)"
                first_name = data.get('firstname')
                last_name = data.get('lastname')
                email = data.get('email')
                try:
                    cursor.execute(stmt, (first_name, last_name, email,))
                except Exception as e:
                    connection.commit()

    return redirect("/users", code=302)


@app.route('/suppliers', methods=["GET"])
def suppliers():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM suppliers ORDER BY supplierid")
            res = cursor.fetchall()
    return render_template('suppliers.html', suppliers=res)


@app.route('/suppliers', methods=["POST"])
def suppliers_update_delete():
    data = request.form
    uid = data.get('id')
    todo = data.get('todo')
    with connection:
        with connection.cursor() as cursor:
            if todo == "delete":
                stmt = "DELETE FROM suppliers WHERE supplierid=%s"
                try:
                    cursor.execute(stmt, (uid, ))
                except Exception as e:
                    return redirect("/suppliers", code=302)
                connection.commit()
            elif todo == "edit":
                stmt = "UPDATE suppliers SET suppliername=%s, contactemail=%s WHERE supplierid=%s"
                supplier_name = data.get('suppliername')
                email = data.get('email')
                cursor.execute(stmt, (supplier_name, email, uid,))

                connection.commit()

            elif todo == "add":
                stmt = "INSERT INTO suppliers(suppliername, contactemail) VALUES (%s, %s)"
                supplier_name = data.get('suppliername')
                email = data.get('email')
                try:
                    cursor.execute(stmt, (supplier_name, email,))
                except Exception as e:
                    return redirect("/suppliers", code=302)
                connection.commit()

    return redirect("/suppliers", code=302)


@app.route('/products', methods=["GET"])
def products():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products ORDER BY productid")
            res = cursor.fetchall()
            cursor.execute("SELECT * FROM suppliers ORDER BY supplierid")
            res_sup = cursor.fetchall()
            print(res_sup)
            supp = dict()

            for a, *b in res_sup:
                supp.setdefault(a, []).extend(b)
            print(supp)
    return render_template('products.html', products=res, suppliers=res_sup)


@app.route('/products', methods=["POST"])
def products_update_delete():
    data = request.form
    uid = data.get('id')
    todo = data.get('todo')
    with connection:
        with connection.cursor() as cursor:
            if todo == "delete":
                stmt = "DELETE FROM products WHERE productid=%s"
                try:
                    cursor.execute(stmt, (uid, ))
                except Exception as e:
                    return redirect("/products", code=302)
                connection.commit()
            elif todo == "edit":
                stmt = "UPDATE products SET productname=%s, price=%s, supplierid=%s WHERE productid=%s"
                product_name = data.get('productname')
                price = data.get('price')
                supplier_id = data.get('supplier')
                cursor.execute(stmt, (product_name, price, supplier_id, uid))

                connection.commit()

            elif todo == "add":
                stmt = "INSERT INTO products(productname, price, supplierid) VALUES (%s, %s, %s)"
                product_name = data.get('productname')
                price = data.get('price')
                supplier_id = data.get('supplier')

                cursor.execute(stmt, (product_name, price, supplier_id, ))

                connection.commit()

    return redirect("/products", code=302)


@app.route('/orders', methods=["GET"])
def orders():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orders ORDER BY orderid")
            res = cursor.fetchall()
            cursor.execute("SELECT * FROM customers ORDER BY customerid")
            res_cus = cursor.fetchall()
            print(res_cus)
            supp = dict()

            for a, *b in res_cus:
                supp.setdefault(a, []).extend(b)
            print(supp)
    return render_template('orders.html', orders=res, customers=res_cus)


@app.route('/orders', methods=["POST"])
def orders_update_delete():
    data = request.form
    uid = data.get('id')
    todo = data.get('todo')
    with connection:
        with connection.cursor() as cursor:
            if todo == "delete":
                stmt = "DELETE FROM orders WHERE orderid=%s"
                try:
                    cursor.execute(stmt, (uid, ))
                except Exception as e:
                    return redirect("/orders", code=302)
                connection.commit()
            elif todo == "edit":
                stmt = "UPDATE orders SET address=%s, customerid=%s WHERE orderid=%s"
                address = data.get('address')
                customer = data.get('customer')
                cursor.execute(stmt, (address, customer, uid))

                connection.commit()

            elif todo == "add":
                stmt = "INSERT INTO orders(address, customerid) VALUES (%s, %s)"
                address = data.get('address')
                customer = data.get('customer')

                cursor.execute(stmt, (address, customer))

                connection.commit()

    return redirect("/orders", code=302)


@app.route('/order_items', methods=["GET"])
def order_items():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orderitems ORDER BY orderitemid")
            res = cursor.fetchall()
            cursor.execute("SELECT * FROM products ORDER BY productid")
            res_prod = cursor.fetchall()
            cursor.execute("SELECT * FROM orders ORDER BY orderid")
            res_ord = cursor.fetchall()
            print(res_prod)
            supp = dict()

            for a, *b in res_prod:
                supp.setdefault(a, []).extend(b)
            print(supp)
    return render_template('orderitems.html', items=res, products=res_prod, orders=res_ord)


@app.route('/order_items', methods=["POST"])
def order_items_update_delete():
    data = request.form
    uid = data.get('id')
    todo = data.get('todo')
    with connection:
        with connection.cursor() as cursor:
            if todo == "delete":
                stmt = "DELETE FROM orderitems WHERE orderitemid=%s"
                try:
                    cursor.execute(stmt, (uid, ))
                except Exception as e:
                    return redirect("/order_items", code=302)
                connection.commit()
            elif todo == "edit":
                stmt = "UPDATE orderitems SET orderid=%s, productid=%s, quantity=%s WHERE orderitemid=%s"
                orderid = data.get('order')
                productid = data.get('product')
                quantity = data.get('quantity')

                cursor.execute(stmt, (orderid, productid, quantity, uid))

                connection.commit()

            elif todo == "add":
                stmt = "INSERT INTO orderitems(orderid, productid, quantity) VALUES (%s, %s, %s)"
                orderid = data.get('order')
                productid = data.get('product')
                quantity = data.get('quantity')
                cursor.execute(stmt, (orderid, productid, quantity))

                connection.commit()

    return redirect("/order_items", code=302)


@app.route('/queries', methods=["GET"])
def queries():
    return render_template('queries.html')


@app.route('/ajax', methods=["POST"])
def ajax():
    data = request.form
    with connection:
        with connection.cursor() as cursor:
            todo = data.get('todo')
            if todo == '1':
                userid = data.get('userid')
                print(userid)
                stmt = "SELECT o.customerid, COUNT(oi.orderitemid) " \
                       "AS orderitem_count FROM public.orders o " \
                       "JOIN public.orderitems oi ON o.orderid = oi.orderid " \
                       "WHERE o.customerid = %s GROUP BY o.customerid;"
                cursor.execute(stmt, (userid,))
                res = cursor.fetchall()
                if res:
                    res = res[0][1]

            if todo == '2':
                email = data.get('email')
                stmt = "SELECT o.address FROM public.orders o JOIN public.customers c " \
                       "ON o.customerid = c.customerid WHERE c.email = %s;"
                cursor.execute(stmt, (email,))
                r = cursor.fetchall()
                res = ""
                if r:
                    for q in r:
                        res += q[0] + '<br>'

            if todo == '3':
                email = data.get('email')
                stmt = "SELECT p.productname FROM public.products p JOIN " \
                       "public.suppliers s ON p.supplierid = s.supplierid " \
                       "WHERE s.contactemail = %s;"
                cursor.execute(stmt, (email,))
                r = cursor.fetchall()
                res = ""
                if r:
                    for q in r:
                        res += q[0] + '<br>'

            if todo == '4':
                prodid = data.get('productid')
                stmt = "SELECT s.contactemail FROM public.products p " \
                       "JOIN public.suppliers s ON p.supplierid = s.supplierid " \
                       "WHERE p.productid = %s;"
                cursor.execute(stmt, (prodid,))
                res = cursor.fetchall()
                print(res)

            if todo == '5':
                prodid = data.get('productid')
                stmt = "SELECT o.address FROM public.orders o J" \
                       "OIN public.orderitems oi ON o.orderid = oi.orderid " \
                       "JOIN public.products p ON oi.productid = p.productid " \
                       "WHERE p.productid = %s;"
                cursor.execute(stmt, (prodid,))
                r = cursor.fetchall()
                res = ""
                if r:
                    for q in r:
                        res += q[0] + '<br>'

            if todo == '6':
                uemail = data.get('uemail')
                semail = data.get('semail')
                stmt = "SELECT p.productname FROM public.products p " \
                       "JOIN public.orderitems oi ON p.productid = oi.productid " \
                       "JOIN public.orders o ON oi.orderid = o.orderid " \
                       "JOIN public.customers c ON o.customerid = c.customerid " \
                       "JOIN public.suppliers s ON p.supplierid = s.supplierid " \
                       "WHERE c.email = %s AND s.contactemail = %s;"
                cursor.execute(stmt, (uemail, semail,))
                r = cursor.fetchall()
                res = ""
                if r:
                    for q in r:
                        res += q[0] + '<br>'

            if todo == '7':
                sid = data.get('sid')
                stmt = """
WITH target_user_products AS (
    SELECT oi.productid
    FROM public.orderitems oi
    JOIN public.orders o ON oi.orderid = o.orderid
    WHERE o.customerid = %s
),
user_last_names AS (
    SELECT c.lastname
    FROM public.customers c
    JOIN public.orders o ON c.customerid = o.customerid
    JOIN public.orderitems oi ON o.orderid = oi.orderid
    WHERE oi.productid IN (SELECT productid FROM target_user_products)
    GROUP BY c.lastname
)
SELECT lastname
FROM user_last_names;"""
                cursor.execute(stmt, (sid,))
                r = cursor.fetchall()
                res = ""
                if r:
                    for q in r:
                        res += q[0] + '<br>'


            if todo == '8':
                prodid = data.get('prodid')
                stmt = """
                SELECT DISTINCT s.supplierid, s.suppliername
FROM public.suppliers s
JOIN public.products p ON s.supplierid = p.supplierid
WHERE p.price > (
    SELECT price
    FROM public.products
    WHERE productid = %s
);"""
                cursor.execute(stmt, (prodid,))
                r = cursor.fetchall()
                res = ""
                if r:
                    for q in r:
                        res += q[1] + '<br>'

            if todo == '9':
                oiid = data.get('orderitemid')
                stmt = """
SELECT DISTINCT o.address
FROM public.orders o
JOIN public.orderitems oi ON o.orderid = oi.orderid
WHERE oi.quantity > (
    SELECT quantity
    FROM public.orderitems
    WHERE orderitemid = %s
);"""
                cursor.execute(stmt, (oiid,))
                r = cursor.fetchall()
                res = ""
                if r:
                    for q in r:
                        res += q[0] + '<br>'

    if res == "" or res == []:
        res = "No data"
    return jsonify(res)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')
