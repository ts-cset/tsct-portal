from flask import session, flash, render_template

from portal.db import get_db

def keep_prev_info(*args):
    session['cour_name'] = args[0]
    session['cour_num'] = args[1]
    session['cour_maj'] = args[2]
    session['cour_cred'] = args[3]
    session['cour_desc'] = args[4]

def remove_prev_info():
    try:
        del session['cour_name']
        del session['cour_num']
        del session['cour_maj']
        del session['cour_cred']
        del session['cour_desc']
    except KeyError:
        print("Key does not exist in Session.")

def validate_query(action, course_id, *query_args):
    cur = get_db().cursor()
    errors = []

    cur.execute("SELECT * FROM courses WHERE name = %s AND id != %s;", (query_args[0], course_id))
    name_check = cur.fetchall()

    if name_check != []:
        name_error = "A course already exists with that name."
        errors.append(name_error)

    if len(query_args[2]) > 4:
        maj_error = "Course Majors can only have a maximum of 4 letters."
        errors.append(maj_error)

    if int(query_args[3]) > 4 or int(query_args[3]) < 0:
        cred_error = "A course can only have between 1 and 4 credits."
        errors.append(cred_error)

    if len(query_args[4]) > 200:
        desc_error = "Course descriptions should be a maximum of 200 characters."
        errors.append(desc_error)

    if errors != []:
        for error in errors:
            flash(error)
            if action == 'edit':
                keep_prev_info(query_args[0], query_args[1], query_args[2], query_args[3], query_args[4])
                return render_template('portal/editcourse.html', course=query_args[5])
            elif action == 'create':
                keep_prev_info(query_args[0], query_args[1], query_args[2], query_args[3], query_args[4])
                return render_template('portal/createcourse.html')
    else:
        return True
