from courses import createCourseDB
from sqlDB import CourseDataDB


def makeDB(yearTerm, dbName):
    createCourseDB(yearTerm, dbName)


def sqliteDiff(oldDBname, newDBname):
    results = []
    oldDB = CourseDataDB(oldDBname)
    newDB = CourseDataDB(newDBname)
    checkCourses(results, oldDB, newDB)
    return results


def checkCourses(results, oldDB, newDB):
    return


def checkSections(results, oldDB, newDB):
    return


def checkInstructors(results, oldDB, newDB):
    return


def checkCourseTimes(results, oldDB, newDB):
    return
