from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort
from bson import ObjectId

from planner.auth import login_required
from planner.db import get_db


bp = Blueprint('plan',__name__)

@bp.route('/')
def index():
    mongo = get_db()
    plans = mongo.db.plans.find()
    return render_template("plan/index.html",plans=plans)

@bp.route('/create',methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            mongo = get_db()
            mongo.db.plans.insert({'title':title, 'body':body,'author_id':g.user['_id'],'username':g.user['username']})
            return redirect(url_for('plan.index'))
    return render_template('plan/create.html')

def get_plan(id, check_author=True):
    id = ObjectId(id)
    plan = get_db().db.plans.find_one({"_id":id})
    if plan is None:
        abort(404, "Post id {} doesn't exist.".format(id))

    if check_author and plan['author_id']!=g.user['_id']:
        abort(403)

    return plan

@bp.route('/<id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    plan = get_plan(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            mongo = get_db()
            print('scream')
            mongo.db.plans.update({"_id":ObjectId(id)},{"$set":{"title":title,"body":body}})
            return redirect(url_for('plan.index'))
    
    return render_template('plan/update.html', plan=plan)


@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_plan(id)
    mongo = get_db()
    mongo.db.plans.remove({"_id":ObjectId(id)})
    return redirect(url_for('plan.index'))

