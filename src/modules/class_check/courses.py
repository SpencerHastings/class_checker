import asyncio

from src.modules.class_check.byuAPI import getSections, getCourses
from src.modules.class_check.sqlDB import CourseDataDB, FilterDB


def addSectionDetails(courseDB, courseID, yearTerm):
    response = getSections(yearTerm, courseID)
    course_data = response.json()
    sections = course_data["sections"]
    for section in sections:
        sectionNumber = section["section_number"]
        instructors = section["instructors"]
        dept = section["dept_name"]
        number = section["catalog_number"]
        suffix = section["catalog_suffix"]
        for instructor in instructors:
            courseDB.insertInstructor(instructor, courseID, sectionNumber, dept, number, suffix)
        times = section["times"]
        for courseTime in times:
            courseDB.insertCourseTime(courseTime, courseID, sectionNumber, dept, number, suffix)


def checkCourseFilter(course, courseFilter, departmentFilter):
    dept = course["dept_name"]
    number = course["catalog_number"]
    suffix = course["catalog_suffix"]

    if dept in departmentFilter:
        return True

    for filterC in courseFilter:
        if filterC[0] == dept and filterC[1] == number and filterC[2] == suffix:
            return True

    return False


async def createCourseDB(yearTerm, dbname, filterDB):
    print("Getting Courses")
    response = getCourses(yearTerm)
    course_data = response.json() #JsonDecodeError at 8am? check out maybe
    courseDB = CourseDataDB(dbname)
    filterDB = FilterDB(filterDB)
    coursesToFilter = filterDB.getCourses()
    departmentsToFilter = [row[0] for row in filterDB.getDepartments()]
    courseDB.createTables()
    i = 0
    total = len(course_data)

    for courseID in course_data:
        i = i + 1
        course = course_data[courseID]
        dept = course["dept_name"]
        number = course["catalog_number"]
        suffix = course["catalog_suffix"]

        courseDB.insertCourse(course, courseID)

        sections = course["sections"]

        for section in sections:
            courseDB.insertSection(section, courseID, dept, number, suffix)

        if checkCourseFilter(course, coursesToFilter, departmentsToFilter):
            addSectionDetails(courseDB, courseID, yearTerm)
            print("{0}/{1} courses processed".format(i, total))
            await asyncio.sleep(3)

    for course in coursesToFilter:
        courseDB.insertOldFilterCourse(course[0], course[1], course[2])
    for department in departmentsToFilter:
        courseDB.insertOldFilterDepartment(department)

    print("Done")
    courseDB.commit()
    courseDB.close()
    return "done"
