import datetime

from src.modules.class_check.courses import createCourseDB
from src.modules.class_check.sqlDB import CourseDataDB


async def makeDB(yearTerm, dbName, filterDB):
    await createCourseDB(yearTerm, dbName, filterDB)


def sqliteDiff(oldDBname, newDBname):
    results = []
    oldDB = CourseDataDB(oldDBname)
    newDB = CourseDataDB(newDBname)
    checkCourses(results, oldDB, newDB)
    checkSections(results, oldDB, newDB)
    checkInstructors(results, oldDB, newDB)
    checkCourseTimes(results, oldDB, newDB)
    oldDB.close()
    newDB.close()
    return results


course_labels = ["Course ID", "Year Term", "Department", "Course Number", "Course Suffix", "Title", "Full Title"]
section_labels = ["Course ID", "Section Number", "Department", "Course Number", "Course Suffix", "Fixed or Variable",
                  "Credit Hours", "Minimum Credit Hours", "Honors", "Credit Type", "Section Type", "Mode"]
instructor_labels = ["Course ID", "Section Number", "Department", "Course Number", "Course Suffix", "Person ID",
                     "Instructor Name"]
courseTime_labels = ["Course ID", "Section Number", "Department", "Course Number", "Course Suffix", "Sequence Number",
                     "Begin Time", "End Time", "Building", "Room", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


indents = ['', ' ', '--| ']
indents_r = ['', ' ', '  | ']

last_indent = -1


def indent(num: int):
    global last_indent
    if num == last_indent:
        out = indents_r[num]
    else:
        out = indents[num]

    last_indent = num
    return out


def courseTimePrettyPrint(courseTime):
    begin_time = None if courseTime[6] is None else datetime.datetime.strptime(courseTime[6], '%H%M').strftime(
        '%I:%M%p')
    end_time = None if courseTime[7] is None else datetime.datetime.strptime(courseTime[7], '%H%M').strftime('%I:%M%p')

    building = courseTime[8]
    room = courseTime[9]

    days = []
    for i in range(10, 17):
        if courseTime[i] is not None:
            days.append(courseTime_labels[i])
    days_string = ','.join(days)

    return f'Bldg:{building} Room:{room} Time:{begin_time}-{end_time} Days:{days_string}'


def checkCourses(results, oldDB, newDB):
    results.append(f'{indent(0)}General Course Changes')
    results.append('')

    old_courses = oldDB.getCourses()
    new_courses = newDB.getCourses()

    diff_courses_new = set(new_courses) - set(old_courses)
    diff_courses_old = set(old_courses) - set(new_courses)

    if len(diff_courses_old) == 0 and len(diff_courses_new) == 0:
        pass
    else:
        for diff_new in diff_courses_new:
            isNew = True
            oldVersion = None
            for diff_old in diff_courses_old:
                if diff_old[0] == diff_new[0]:
                    isNew = False
                    oldVersion = diff_old
            if not isNew:
                if diff_new[4] is None:
                    res = f'{indent(1)}Course {diff_new[2]} {diff_new[3]} {diff_new[6]} changed:'
                else:
                    res = f'{indent(1)}Course {diff_new[2]} {diff_new[3]} {diff_new[4]} {diff_new[6]} changed:'
                results.append(res)
                for i in range(2, 7):
                    if diff_new[i] != oldVersion[i]:
                        results.append(
                            f'{indent(2)} {course_labels[i]} changed from "{oldVersion[i]}" to "{diff_new[i]}"')
                results.append('')

        for diff_new in diff_courses_new:
            isNew = True
            for diff_old in diff_courses_old:
                if diff_old[0] == diff_new[0]:
                    isNew = False
            if isNew:
                if diff_new[4] is None:
                    res = f'{indent(1)}Course Added: {diff_new[2]} {diff_new[3]} {diff_new[6]}'
                else:
                    res = f'{indent(1)}Course Added: {diff_new[2]} {diff_new[3]} {diff_new[4]} {diff_new[6]}'
                results.append(res)

        for diff_old in diff_courses_old:
            isGone = True
            for diff_new in diff_courses_new:
                if diff_old[0] == diff_new[0]:
                    isGone = False

            if isGone:
                if diff_old[4] is None:
                    res = f'{indent(1)}Course Removed: {diff_old[2]} {diff_old[3]} {diff_old[6]}'
                else:
                    res = f'{indent(1)}Course Removed: {diff_old[2]} {diff_old[3]} {diff_old[4]} {diff_old[6]}'
                results.append(res)

    results.append("")
    return


def checkSections(results, oldDB, newDB):
    results.append(f'{indent(0)}General Section Changes')
    results.append('')

    old_courses = oldDB.getCourses()
    new_courses = newDB.getCourses()

    old_sections = []
    new_sections = []

    for course in old_courses:
        old_sections += oldDB.getSections(course[0])
    for course in new_courses:
        new_sections += newDB.getSections(course[0])

    diff_sections_new = set(new_sections) - set(old_sections)
    diff_sections_old = set(old_sections) - set(new_sections)

    if len(diff_sections_old) == 0 and len(diff_sections_new) == 0:
        pass
    else:
        for diff_new in diff_sections_new:
            isNew = True
            oldVersion = None
            for diff_old in diff_sections_old:
                if diff_old[0] == diff_new[0] and diff_old[1] == diff_new[1]:
                    isNew = False
                    oldVersion = diff_old
            if not isNew:
                if diff_new[4] is None:
                    res = f'{indent(1)}Section {diff_new[1]} {diff_new[2]} {diff_new[3]} changed:'
                else:
                    res = f'{indent(1)}Section {diff_new[1]} {diff_new[2]} {diff_new[3]} {diff_new[4]} changed:'
                results.append(res)
                for i in range(5, 12):
                    if diff_new[i] != oldVersion[i]:
                        results.append(
                            f'{indent(2)}{section_labels[i]} changed from "{oldVersion[i]}" to "{diff_new[i]}"')
                results.append('')

        for diff_new in diff_sections_new:
            isNew = True
            for diff_old in diff_sections_old:
                if diff_old[0] == diff_new[0] and diff_old[1] == diff_new[1]:
                    isNew = False
            if isNew:
                if diff_new[4] is None:
                    res = f'{indent(1)}Section Added: {diff_new[2]} {diff_new[3]} Section {diff_new[1]}'
                else:
                    res = f'{indent(1)}Section Added: {diff_new[2]} {diff_new[3]} {diff_new[4]} Section {diff_new[1]}'
                results.append(res)

        for diff_old in diff_sections_old:
            isGone = True
            for diff_new in diff_sections_new:
                if diff_old[0] == diff_new[0] and diff_old[1] == diff_new[1]:
                    isGone = False

            if isGone:
                if diff_old[4] is None:
                    res = f'{indent(1)}Section Removed: {diff_old[2]} {diff_old[3]} Section {diff_old[1]}'
                else:
                    res = f'{indent(1)}Section Removed: {diff_old[2]} {diff_old[3]} {diff_old[4]} Section {diff_old[1]}'
                results.append(res)

    results.append("")
    return


def checkInstructors(results, oldDB, newDB):
    results.append(f'{indent(0)}Checked Instructor Changes')
    results.append('')

    old_filters_courses = oldDB.getOldFilterCourse()
    old_filters_departments = oldDB.getOldFilterDepartment()

    new_filters_courses = newDB.getOldFilterCourse()
    new_filters_departments = newDB.getOldFilterDepartment()

    diff_filters_courses_new = set(new_filters_courses) - set(old_filters_courses)
    diff_filters_courses_old = set(old_filters_courses) - set(new_filters_courses)

    diff_filters_departments_new = set(new_filters_departments) - set(old_filters_departments)
    diff_filters_departments_old = set(old_filters_departments) - set(new_filters_departments)

    old_courses = oldDB.getCourses()
    new_courses = newDB.getCourses()

    old_sections = []
    new_sections = []

    for course in old_courses:
        old_sections += oldDB.getSections(course[0])
    for course in new_courses:
        new_sections += newDB.getSections(course[0])

    old_instructors = []
    new_instructors = []

    for section in old_sections:
        old_instructors += oldDB.getInstructors(section[0], section[1])

    for section in new_sections:
        new_instructors += newDB.getInstructors(section[0], section[1])

    diff_instructors_new = set(new_instructors) - set(old_instructors)
    diff_instructors_old = set(old_instructors) - set(new_instructors)

    if len(diff_instructors_old) == 0 and len(diff_instructors_new) == 0:
        pass
    else:
        for diff_new in diff_instructors_new:
            isNew = True
            oldVersion = None
            for diff_old in diff_instructors_old:
                if diff_old[0] == diff_new[0]:
                    isNew = False
                    oldVersion = diff_old
            if not isNew:
                if diff_new[4] is None:
                    res = f'{indent(1)}Instructors changed: Section {diff_new[1]} {diff_new[2]} {diff_new[3]}'
                else:
                    res = f'{indent(1)}Instructors changed: Section {diff_new[1]} {diff_new[2]} {diff_new[3]} {diff_new[4]}'
                results.append(res)

                if diff_new[5] != oldVersion[5]:
                    results.append(
                        f'{indent(2)}{instructor_labels[6]} changed from "{oldVersion[6]}" to "{diff_new[6]}"')
                results.append('')

        for diff_new in diff_instructors_new:
            isNew = True
            for diff_old in diff_instructors_old:
                if diff_old[0] == diff_new[0]:
                    isNew = False
            if isNew:
                if not (diff_new[2] in diff_filters_departments_new or (
                        diff_new[2], diff_new[3], diff_new[4]) in diff_filters_courses_new):
                    if diff_new[4] is None:
                        res = f'{indent(1)}Instructor Added: {diff_new[2]} {diff_new[3]} Section {diff_new[1]}'
                    else:
                        res = f'{indent(1)}Instructor Added: {diff_new[2]} {diff_new[3]} {diff_new[4]} Section {diff_new[1]}'
                    results.append(res)
                    results.append(f'{indent(2)}{diff_new[6]}')
                    results.append('')

        for diff_old in diff_instructors_old:
            isGone = True
            for diff_new in diff_instructors_new:
                if diff_old[0] == diff_new[0]:
                    isGone = False

            if isGone:
                if not (diff_old[2] in diff_filters_departments_old or (
                        diff_old[2], diff_old[3], diff_old[4]) in diff_filters_courses_old):
                    if diff_old[4] is None:
                        res = f'{indent(1)}Instructor Removed: {diff_old[2]} {diff_old[3]} Section {diff_old[1]}'
                    else:
                        res = f'{indent(1)}Instructor Removed: {diff_old[2]} {diff_old[3]} {diff_old[4]} Section {diff_old[1]}'
                    results.append(res)
                    results.append(f'{indent(2)}{diff_old[6]}')
                    results.append('')

    results.append("")
    return


def checkCourseTimes(results, oldDB, newDB):
    results.append(f'{indent(0)}Checked Course Time Changes')
    results.append('')

    old_filters_courses = oldDB.getOldFilterCourse()
    old_filters_departments = oldDB.getOldFilterDepartment()

    new_filters_courses = newDB.getOldFilterCourse()
    new_filters_departments = newDB.getOldFilterDepartment()

    diff_filters_courses_new = set(new_filters_courses) - set(old_filters_courses)
    diff_filters_courses_old = set(old_filters_courses) - set(new_filters_courses)

    diff_filters_departments_new = set(new_filters_departments) - set(old_filters_departments)
    diff_filters_departments_old = set(old_filters_departments) - set(new_filters_departments)

    old_courses = oldDB.getCourses()
    new_courses = newDB.getCourses()

    old_sections = []
    new_sections = []

    for course in old_courses:
        old_sections += oldDB.getSections(course[0])
    for course in new_courses:
        new_sections += newDB.getSections(course[0])

    old_courseTimes = []
    new_courseTimes = []

    for section in old_sections:
        old_courseTimes += oldDB.getCourseTimes(section[0], section[1])

    for section in new_sections:
        new_courseTimes += newDB.getCourseTimes(section[0], section[1])

    diff_courseTimes_new = set(new_courseTimes) - set(old_courseTimes)
    diff_courseTimes_old = set(old_courseTimes) - set(new_courseTimes)

    if len(diff_courseTimes_old) == 0 and len(diff_courseTimes_new) == 0:
        pass
    else:
        for diff_new in diff_courseTimes_new:
            isNew = True
            oldVersion = None
            for diff_old in diff_courseTimes_old:
                if diff_old[0] == diff_new[0]:
                    isNew = False
                    oldVersion = diff_old
            if not isNew:
                if diff_new[4] is None:
                    res = f'{indent(1)}Course Time changed: Section {diff_new[1]} {diff_new[2]} {diff_new[3]}'
                else:
                    res = f'{indent(1)}Course Time changed: Section {diff_new[1]} {diff_new[2]} {diff_new[3]} {diff_new[4]}'
                results.append(res)
                results.append(f'{indent(2)}Old: {courseTimePrettyPrint(oldVersion)}')
                results.append(f'{indent(2)}New: {courseTimePrettyPrint(diff_new)}')
                results.append('')

        for diff_new in diff_courseTimes_new:
            isNew = True
            for diff_old in diff_courseTimes_old:
                if diff_old[0] == diff_new[0]:
                    isNew = False
            if isNew:
                if not (diff_new[2] in diff_filters_departments_new or (
                        diff_new[2], diff_new[3], diff_new[4]) in diff_filters_courses_new):
                    if diff_new[4] is None:
                        res = f'{indent(1)}Course Time Added: {diff_new[2]} {diff_new[3]} Section {diff_new[1]}'
                    else:
                        res = f'{indent(1)}Course Time Added: {diff_new[2]} {diff_new[3]} {diff_new[4]} Section {diff_new[1]}'
                    results.append(res)
                    results.append(f'{indent(2)}{courseTimePrettyPrint(diff_new)}')
                    results.append('')

        for diff_old in diff_courseTimes_old:
            isGone = True
            for diff_new in diff_courseTimes_new:
                if diff_old[0] == diff_new[0]:
                    isGone = False

            if isGone:
                if not (diff_old[2] in diff_filters_departments_old or (
                        diff_old[2], diff_old[3], diff_old[4]) in diff_filters_courses_old):
                    if diff_old[4] is None:
                        res = f'{indent(1)}Course Time Removed: {diff_old[2]} {diff_old[3]} Section {diff_old[1]}'
                    else:
                        res = f'{indent(1)}Course Time Removed: {diff_old[2]} {diff_old[3]} {diff_old[4]} Section {diff_old[1]}'
                    results.append(res)
                    results.append(f'{indent(2)}{courseTimePrettyPrint(diff_old)}')
                    results.append('')

    results.append("")
    return
