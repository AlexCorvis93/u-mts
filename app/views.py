from app import app, images, Message, mail
from .models import Proposal, db, Product, ProductImage, CompletedProposal
from flask import render_template, request, redirect, url_for, send_from_directory, session
from .admin_session import LoginAdmin
import os

log = LoginAdmin()# класс для работы с сессией админа
menu = [{'url': 'logout_admin', 'title': 'Выход'}]


def random_str(length=32):
    import random
    base_str = 'qwertyuioplkjhgfdsazcxvbnm0123456789'
    return ''.join(random.choice(base_str) for i in range(length))


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOADED_IMAGES_DEST"], name)


@app.route('/loginadm', methods=['POST', 'GET'])
def auth():
    """вход в панель администратора"""
    if log.is_logged():
        return redirect(url_for('admin'))
    if request.method == 'POST':
        if request.form['login'] == os.environ['LOGIN'] and request.form['pswd'] == os.environ['PASSWORD']:
            log.login_admin()
            return redirect(url_for('admin'))
    return render_template('main/auth.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    """Главная страница и отправка заявки"""
    customer = request.form.get('customer')
    email = request.form.get('email')
    phone = request.form.get('phone')
    text = request.form.get('text')

    """Отправка заявки"""
    if request.method == "POST":
        try:
            new_message = Proposal(customer=customer, email=email, phone=phone, text=text)
            db.session.add(new_message)
            db.session.commit() # добавление изменений в бд
            msg = Message('Feedback', sender=new_message.email, recipients=[app.config['MAIL_USERNAME']]) #отправка заявки на рабочую почту
            msg.html = render_template('main/message.html', message=new_message)
            mail.send(msg)
            return redirect(url_for('thanks')) #страница спасибо
        except:
            db.session.rollback()  # откат бд до первоначального состояния
            print('Error add into DB')
    item = Product.query.all()
    im = ProductImage.query.all()
    return render_template('main/main.html', product=item, im=im)


@app.route('/item/<int:product_id>')
def item_detail(product_id):
    """Страница товара"""
    item = db.session.query(Product).filter_by(id=product_id).one()
    item_img = db.session.query(ProductImage).filter_by(prod_id=item.id).one()
    img_url = url_for('download_file', name=item_img.img)
    return render_template('main/item.html', img=img_url, item=item)


@app.route('/equipment', methods=['GET', 'POST'])
def equipment():
    if not log.is_logged():
        return redirect(url_for('auth'))
    """Новое объявление о продаже медтехники"""
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    if request.method == 'POST':
        try:
            """создание товара"""
            new_item = Product(name=name, price=price,  description=description)
            db.session.add(new_item)
            db.session.commit()
            image = request.files['picture']
            """добавление изображений к товару"""
            suffix = os.path.splitext(image.filename)[1]
            filename = random_str() + suffix
            images.save(image, name=filename)
            pic_add_db = ProductImage(img=filename, prod_id=new_item.id)
            db.session.add(pic_add_db)
            db.session.commit()
        except:
            db.session.rollback()  # откат бд до первоначального состояния
            print('Error add into DB')
    return render_template('main/equipment.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not log.is_logged():
        return redirect(url_for('auth'))
    item = Product.query.all()
    proposal = Proposal.query.all()
    return render_template('main/admin.html', menu=menu, item=item, prop=proposal)


@app.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update_item(product_id):
    """Страница редактирования постов"""
    if not log.is_logged():
        return redirect(url_for('auth'))
    item = db.session.query(Product).filter_by(id=product_id).one()
    item_img = db.session.query(ProductImage).filter_by(prod_id=item.id).one()
    img_url = url_for('download_file', name=item_img.img)
    new_name = request.form.get('name')
    new_price = request.form.get('price')
    new_description = request.form.get('description')
    if request.method == 'POST':
        item.name = new_name
        item.price = new_price
        item.description = new_description
        db.session.commit()
        image = request.files['picture']
        os.remove('app/static/media/product/' + str(item_img.img))
        """добавление изображений к товару"""
        suffix = os.path.splitext(image.filename)[1]
        filename = random_str() + suffix
        images.save(image, name=filename)
        item_img.img = filename
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('main/item_udate.html', item=item, menu=menu, img=img_url)


@app.route("/delete/<int:product_id>", methods=["POST"])
def delete_item(product_id):
    """Удалить объявление"""
    item = db.session.query(Product).filter_by(id=product_id).one()
    img = db.session.query(ProductImage).filter_by(prod_id=item.id).one()
    os.remove('app/static/media/product/' + str(img.img))
    db.session.delete(img)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/logout', methods=['POST', 'GET'])
def logout_admin():
    if not log.logout():
        return redirect(url_for('index'))


@app.route("/delete_proposal/<int:proposal_id>", methods=["POST"])
def delete_proposal(proposal_id):
    """Удалить заявку"""
    proposal = db.session.query(Proposal).filter_by(id=proposal_id).one()
    db.session.delete(proposal)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route("/add_complete/<int:proposal_id>", methods=["POST"])
def add_to_complete(proposal_id):
    """Добавить заявку в список отработанных"""
    proposal = db.session.query(Proposal).filter_by(id=proposal_id).one()
    if request.method == "POST":
        complete = CompletedProposal(customer=proposal.customer, email=proposal.email, phone=proposal.phone,
                                     text=proposal.text)
        db.session.add(complete)
        db.session.commit()
        db.session.delete(proposal)
        db.session.commit()
        return redirect(url_for('admin'))


@app.route('/completed', methods=['GET', 'POST'])
def completed_list():
    """Вывести список отработанных заявок"""
    completed_proposals = CompletedProposal.query.all()
    return render_template('main/completed.html', prop=completed_proposals)


@app.route("/delete_completed/<int:completed_id>", methods=["POST"])
def delete_completed(completed_id):
    """Удалить заявку"""
    proposal = db.session.query(CompletedProposal).filter_by(id=completed_id).one()
    db.session.delete(proposal)
    db.session.commit()
    return redirect(url_for('completed_list'))


@app.route('/thanks')
def thanks():
    return render_template('main/thanks.html')
