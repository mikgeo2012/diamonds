from flask import render_template, flash, redirect, request, jsonify, url_for
from app import app, db
from forms import DiamondForm
import utils as ut
from app.models import Diamond
import json

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        jsond = request.get_json()
        if 'row_id' not in jsond:
            # print "Refreshing Table...."

            # diamonds = Diamond.query.all()
            # d_url = {d.id: d.url for d in diamonds}
            # result = ut.refreshTable(d_url)

            # for k, v in result.iteritems():
            #     if not v:
            #         try:
            #             ut.deleteRow(k)
            #         except:
            #             print "Error when deleting diamond"
            print "Deleting Table...."
            ut.deleteTable()
            print "finished with delete"
            redirect(url_for('index'))
        else:
            row = jsond['row_id']
            diamond = Diamond.query.get(row)
            db.session.delete(diamond)
            db.session.commit()
            return jsonify(result=jsond)


    diamonds = Diamond.query.all()


    return render_template('index.html',
                           diamonds=diamonds)


@app.route('/submit_url', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        attributes = []
        entry = False
        commit = False

        if 'file' in request.files:
            print "FILE"
            f = request.files['file']
            index = 0
            num_eval = 0
            for line in f:
                if line.strip() is not '':
                    index += 1
                    print "Index: " + str(index)
                    di_data = ut.consumeURL(line.strip())
                    if di_data:
                        try:
                            diamond = Diamond(**di_data)
                            db.session.add(diamond)
                            db.session.commit()
                        except Exception:
                            print"ERROR: Problem adding diamond to DB"

                        commit = True
                        num_eval += 1

                    entry = True
            print "SUMMARY => {0} url's read | {1} diamonds added to table | {2} failed url's".format(index, num_eval, index - num_eval)

        else:
            print "URL"
            index = 0
            num_eval = 0
            for i in range(len(request.form)):
              if request.form['url{0}'.format(i)]:
                    index += 1
                    print "Index: " + str(index)
                    attributes.append(ut.consumeURL(request.form['url{0}'.format(i)]))

                    if attributes[i] is not None:
                        try:
                            diamond = Diamond(**attributes[i])
                            db.session.add(diamond)
                            db.session.commit()
                        except Exception:
                            print"ERROR: Problem adding diamond to DB"

                        commit = True
                        entry = True
                        num_eval += 1
                    else:
                        print "ERROR: Problem getting diamond attributes from url"

            print "SUMMARY => {0} url's read | {1} diamonds added to table | {2} failed url's".format(index, num_eval, index - num_eval)


        if not entry:
            # flash('Please submit a url/file', 'error')
            return redirect('/index')
        elif not commit:
            # flash('Diamond is already in the database', 'duplicates')
            return redirect('/index')
        else:
            # flash('Record(s) was(were) successfully added', 'success')
            return redirect('/index')

    return render_template('submit_url.html')

