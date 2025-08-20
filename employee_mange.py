import mysql.connector

con=mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql_ayy24",
    database="emp"
    )
def check_emp(employee_id):
    sql='SELECT * FROM employees WHERE id= %s'
    #buffered=True allows rowcount to work properly as it brings all the rows together in memory allowing wasy access DOWNSIDE: MEMORY USAGE INCASE OF LARGE RESULTS  
    cursor=con.cursor(buffered=True)
    data=(employee_id,)
    cursor.execute(sql,data)
    employee=cursor.fetchone()
    cursor.close()
    return employee is not None
def add_employee():
    Id=int(input("Enter Employee Id: "))
    if check_emp(Id):
        print("Employee already exist. Try again.")
        return
    else:
        Name=input("Enter Employee Name: ")
        Post =input("Enter Employee post: ")
        Salary=float(input("Enter Employee Salary: "))

        sql='INSERT INTO employees(id,Name,Post,Salary) VALUES (%s,%s,%s,%s)'
        data=(Id,Name,Post,Salary)
        cursor=con.cursor()
        try:
            cursor.execute(sql,data)
            con.commit()
            print("Employee Added successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            con.rollback()
        finally:
            cursor.close()
def remove_employee():
    Id=int(input("Enter the Employee Id: "))
    if not check_emp(Id):
        print("Employee does not exist.")
        return
    else:
        sql='DELETE FROM employees WHERE id=%s'
        data=(Id,)
        cursor=con.cursor()
        try:
            cursor.execute(sql,data)
            con.commit()
            print("Employee removed successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            con.rollback()
        finally:
            cursor.close()
def promote_emp():
    Id=int(input("Enter the Employee Id: "))
    if not check_emp(Id):
        print("Employee does not exist.")
        return
    else:
        try:
            amount=float(input("Enter increase in salary: "))
            sql_select='SELECT salary FROM employees WHERE id=%s'
            data=(Id,)
            cursor=con.cursor()
            cursor.execute(sql_select,data)
            curent_salary=cursor.fetchone()[0]
            new_salary=curent_salary+ amount
            sql_update='UPDATE employees SET salary=%s WHERE id=%s'
            data_update=(new_salary,Id)
            cursor.execute(sql_update,data_update)
            con.commit()
            print("Employee Promoted Successfully")
        except (ValueError,mysql.connector.Error) as e:
            print(f"Error: {e}")
            con.rollback()
        finally:
            cursor.close()
def display_emp():
    try:
        sql='SELECT *FROM employees'
        cursor=con.cursor()
        cursor.execute(sql)
        employee=cursor.fetchall()
        for emp in employee:
            print("Employee Id: ", emp[0])
            print("Employee Name: ",emp[1])
            print("Employee Post: ",emp[2])
            print("Employee Salary: ",emp[3])
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
def menu():
    while(True):
            print("\nWelcome to Employee Management Record")
            print("Press:")
            print("1 to Add Employee")
            print("2 to Remove Employee")
            print("3 to Promote Employee")
            print("4 to Display Employees")
            print("5 to Exit")
            
            # Taking choice from user
            ch = input("Enter your Choice: ")

            if ch == '1':
                add_employee()
            elif ch == '2':
                remove_employee()
            elif ch == '3':
                promote_emp()
            elif ch == '4':
                display_emp()
            elif ch == '5':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid Choice! Please try again.")
menu()
