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

course_labels = ["Course ID", "Year Term", "Department", "Course Number", "Course Suffix", "Title", "Full Title"]

def checkCourses(results, oldDB, newDB):
    results.append("General Course Changes:")

    old_courses = oldDB.getCourses()
    new_courses = newDB.getCourses()

    diff_courses_new = set(new_courses) - set(old_courses)
    diff_courses_old = set(old_courses) - set(new_courses)

    if len(diff_courses_old) == 0 and len(diff_courses_new) == 0:
        results.append("-- No course changes")
    else:
        for diff_new in diff_courses_new:
            isNew = True
            oldVersion = None
            for diff_old in diff_courses_old:
                if diff_old[0] == diff_new[0]:
                    isNew = False
                    oldVersion = diff_old
            if isNew:
                if diff_new[4] is None:
                    res = "-- New Course Added: " + diff_new[2] + " " + diff_new[3] + " " + diff_new[6]
                else:
                    res = "-- New Course Added: " + diff_new[2] + " " + diff_new[3] + " " + diff_new[4] + " " + diff_new[6]
                results.append(res)
            else:
                results.append("-- Course \"" + diff_new[6] + " " + diff_new[2] + " " + diff_new[3] + "\" changed:")
                for i in range(2, 7):
                    if diff_new[i] != oldVersion[i]:
                        results.append("  -- " + course_labels[i] + " changed from \"" + str(oldVersion[i]) + "\" to \"" + str(diff_new[i]) + "\"")

        for diff_old in diff_courses_old:
            isGone = True
            for diff_new in diff_courses_new:
                if diff_old[0] == diff_new[0]:
                    isGone = False

            if isGone:
                if diff_old[4] is None:
                    res = "-- Course Removed: " + diff_old[2] + " " + diff_old[3] + " " + diff_old[6]
                else:
                    res = "-- Course Removed: " + diff_old[2] + " " + diff_old[3] + " " + diff_old[4] + " " + diff_old[6]
                results.append(res)

    results.append("")
    checkSections(results, oldDB, newDB)
    return


def checkSections(results, oldDB, newDB):
    return


def checkInstructors(results, oldDB, newDB):
    return


def checkCourseTimes(results, oldDB, newDB):
    return
