from flask import Blueprint, render_template, request, g, redirect, url_for
from .forms import TreeholeForm, ReplyForm
from models import TreeholeModel, ReplyModel
from exts import db
from decorators import login_required

qa_bp = Blueprint('qa', __name__, url_prefix='/')

@qa_bp.route('/')
def index():
    treeholes = TreeholeModel.query.order_by(TreeholeModel.create_time.desc()).all()

    return render_template('index.html', treeholes=treeholes)

@qa_bp.route('/qa/create', methods=['GET', 'POST'])
@login_required
def create_treehole():
    if request.method == 'GET':
        return render_template('create.html')
    else:
        form = TreeholeForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            treehole = TreeholeModel(title=title, content=content, author = g.user)
            db.session.add(treehole)
            db.session.commit()
            return redirect('/')
        else:
            print(form.errors)
            return redirect(url_for('qa.create_treehole'))

@qa_bp.route('/qa/detail/<int:treehole_id>')
def detail_treehole(treehole_id):
    treehole = TreeholeModel.query.get(treehole_id)
    return render_template('detail.html', treehole=treehole)


@qa_bp.route('/reply', methods=['POST'])
@login_required
def reply():
    form = ReplyForm(request.form)
    if form.validate():
        content = form.content.data
        treehole_id = form.treehole_id.data
        reply = ReplyModel(content=content, treehole_id=treehole_id, author_id=g.user.id)
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('qa.detail_treehole', treehole_id=treehole_id))
    else:
        print(form.errors)
        return redirect(url_for('qa.detail_treehole', treehole_id = request.form.get('treehole_id')))
    
@qa_bp.route('/search')
def search():
    treehole = request.args.get('treehole')
    if treehole:
        treeholes = TreeholeModel.query.filter(TreeholeModel.title.contains(treehole)).all()
        return render_template('index.html', treeholes=treeholes)
    else:
        return redirect(url_for('qa.index'))
        