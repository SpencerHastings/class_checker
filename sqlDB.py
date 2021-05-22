import sqlite3


class CourseDataDB:

    def __init__(self, dbName):
        self.dbConnection = sqlite3.connect(dbName)
        self.dbCursor = self.dbConnection.cursor()

    def commit(self):
        self.dbConnection.commit()

    def close(self):
        self.dbConnection.close()

    def createTables(self):
        self.dbCursor.execute(
            '''CREATE TABLE "courses" ("course_id" TEXT, "year_term" TEXT, "dept_name" TEXT, "catalog_number" TEXT, "catalog_suffix" TEXT, title TEXT, full_title TEXT)''')
        self.dbCursor.execute(
            '''CREATE TABLE "sections" ("course_id"	TEXT, "section_number" TEXT, "fixed_or_variable" TEXT, "credit_hours" TEXT, "minimum_credit_hours" TEXT, "honors" TEXT, "credit_type" TEXT, "section_type" TEXT, "mode" TEXT)''')
        self.dbCursor.execute(
            '''CREATE TABLE "instructors" ("course_id" TEXT, "section_number" TEXT, "person_id" TEXT, "sort_name" TEXT)''')
        self.dbCursor.execute(
            '''CREATE TABLE "course_time" ("course_id" TEXT, "section_number" TEXT, "sequence_number" TEXT, "begin_time" TEXT, "end_time" TEXT, "building" TEXT, "room" TEXT, "mon" TEXT, "tue" TEXT, "wed" TEXT, "thu" TEXT, "fri" TEXT, "sat" TEXT, "sun" TEXT)''')

    def clearTables(self):
        self.dbCursor.execute("DELETE FROM courses")
        self.dbCursor.execute("DELETE FROM sections")
        self.dbCursor.execute("DELETE FROM instructors")
        self.dbCursor.execute("DELETE FROM course_time")

    def insertCourse(self, course, course_id):
        self.dbCursor.execute("insert into courses values (?,?,?,?,?,?,?)",
                              [course_id, course["year_term"], course["dept_name"], course["catalog_number"],
                               course["catalog_suffix"], course["title"], course["full_title"]])

    def insertSection(self, section, course_id):
        self.dbCursor.execute("INSERT INTO sections VALUES (?,?,?,?,?,?,?,?,?)",
                              [course_id, section["section_number"], section["fixed_or_variable"],
                               section["credit_hours"], section["minimum_credit_hours"], section["honors"],
                               section["credit_type"], section["section_type"], section["mode"]])

    def insertInstructor(self, instructor, course_id, section_number):
        self.dbCursor.execute("INSERT INTO instructors VALUES (?,?,?,?)",
                              [course_id, section_number, instructor["person_id"], instructor["sort_name"]])

    def insertCourseTime(self, courseTime, course_id, section_number):
        self.dbCursor.execute("INSERT INTO course_time VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                              [course_id, section_number, courseTime["sequence_number"], courseTime["begin_time"],
                               courseTime["end_time"], courseTime["building"], courseTime["room"], courseTime["mon"],
                               courseTime["tue"], courseTime["wed"], courseTime["thu"], courseTime["fri"],
                               courseTime["sat"], courseTime["sun"]])

    def getDepartments(self):
        self.dbCursor.execute("SELECT DISTINCT dept_name FROM courses")
        return self.dbCursor.fetchall()

    def getCourses(self):
        self.dbCursor.execute("SELECT * FROM courses")
        return self.dbCursor.fetchall()

    def getSections(self, course_id):
        self.dbCursor.execute("SELECT * FROM sections WHERE course_id = ?", [course_id])
        return self.dbCursor.fetchall()

    def getInstructors(self, course_id, section_number):
        self.dbCursor.execute("SELECT * FROM instructors WHERE course_id = ? AND section_number = ?",
                              [course_id, section_number])
        return self.dbCursor.fetchall()

    def getCourseTimes(self, course_id, section_number):
        self.dbCursor.execute("SELECT * FROM course_time WHERE course_id = ? AND section_number = ?",
                              [course_id, section_number])
        return self.dbCursor.fetchall()


class FilterDB:
    def __init__(self, dbName):
        self.dbConnection = sqlite3.connect(dbName)
        self.dbCursor = self.dbConnection.cursor()

    def commit(self):
        self.dbConnection.commit()

    def close(self):
        self.dbConnection.close()

    def createTables(self):
        self.dbCursor.execute('''CREATE TABLE "courses" ("course" TEXT UNIQUE)''')
        self.dbCursor.execute('''CREATE TABLE "departments" ("department" TEXT UNIQUE)''')

    def clearTables(self):
        self.dbCursor.execute("DELETE FROM courses")
        self.dbCursor.execute("DELETE FROM departments")

    def addCourse(self, course):
        self.dbCursor.execute("INSERT INTO courses VALUES (?)",
                              [course])

    def addDepartment(self, department):
        self.dbCursor.execute("INSERT INTO departments VALUES (?)",
                              [department])

    def getCourses(self):
        self.dbCursor.execute("SELECT * FROM courses")
        return self.dbCursor.fetchall()

    def getDepartments(self):
        self.dbCursor.execute("SELECT * FROM departments")
        return self.dbCursor.fetchall()
