from byuAPI import getSections, getCourses
from sqlDB import CourseDataDB, FilterDB

filterDB_name = "filters.db"


def addSectionDetails(courseDB, courseID, yearTerm):
    response = getSections(yearTerm, courseID)
    course_data = response.json()
    sections = course_data["sections"]
    for section in sections:
        sectionNumber = section["section_number"]
        instructors = section["instructors"]
        for instructor in instructors:
            courseDB.insertInstructor(instructor, courseID, sectionNumber)
        times = section["times"]
        for time in times:
            courseDB.insertCourseTime(time, courseID, sectionNumber)


def createCourseDB(yearTerm, dbname):
    print("Getting Courses")
    response = getCourses(yearTerm)
    course_data = response.json()
    courseDB = CourseDataDB(dbname)
    filterDB = FilterDB(filterDB_name)
    coursesToFilter = [row[0] for row in filterDB.getCourses()]
    departmentsToFilter = [row[0] for row in filterDB.getDepartments()]
    try:
        courseDB.createTables()
        i = 0
        total = len(course_data)

        for courseID in course_data:
            i = i + 1
            print("{0}/{1} courses processed".format(i, total))
            course = course_data[courseID]
            dept = course["dept_name"]
            number = course["catalog_number"]

            courseDB.insertCourse(course, courseID)

            sections = course["sections"]

            for section in sections:
                courseDB.insertSection(section, courseID)

            courseLabel = dept + " " + number

            if courseLabel in coursesToFilter or dept in departmentsToFilter:
                addSectionDetails(courseDB, courseID, yearTerm)
        print("Done")
        courseDB.commit()

    except:
        print("error")
    finally:
        courseDB.close()
    return "done"
