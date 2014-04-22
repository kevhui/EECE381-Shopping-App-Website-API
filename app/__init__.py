from flask import Flask, render_template, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class items(db.Model):
    upc = db.Column(db.VARCHAR(13), primary_key=True)
    name = db.Column(db.VARCHAR(20))
    description = db.Column(db.VARCHAR(40))
    price = db.Column(db.Integer)
    category = db.Column(db.VARCHAR(20))
    image = db.Column(db.VARCHAR(100))
    stock = db.Column(db.Integer)

    def __repr__(self):
        item_values = """<items(
            upc='%s',
            name='%s',
            description='%s',
            price='%d',
            category='%s',
            image='%s',
            stock ='%d')>"""
        return item_values % (
            self.upc,
            self.name,
            self.description,
            self.price,
            self.category,
            self.image,
            self.stock)


@app.route('/')
@app.route('/index')
def index():
    allItems = items.query.all()
    return render_template("index.html", items=allItems)


@app.route('/items')
def get_items():
    allItems = items.query.all()
    results = []
    for i in allItems:
        item = {'upc': i.upc,
                'name': i.name,
                'price': str(i.price),
                'description': i.description,
                'category': i.category,
                'image': i.image
                }
        results.append(item)
    return jsonify({'items': results})


@app.route('/items/<string:upc>')
def get_item(upc):
    i = items.query.get(upc)
    item = {'upc': i.upc,
            'name': i.name,
            'price': str(i.price),
            'description': i.description,
            'category': i.category,
            'image': i.image
            }
    return jsonify({'item': item})


@app.route('/items/filterby/<string:tag>')
def get_item_filter(tag):
    filteredItems = items.query.filter(items.name.like("%" + tag + "%")).all()
    results = []
    for i in filteredItems:
        item = {'upc': i.upc,
                'name': i.name,
                'price': str(i.price),
                'description': i.description,
                'category': i.category,
                'image': i.image
                }
        results.append(item)
    return jsonify({'item': results})


@app.route('/category')
def get_categories():
    allCategories = db.session.query(items.category.distinct())
    results = []
    for i in allCategories:
        category = {'category': i[0]}
        results.append(category)
    return jsonify({'categories': results})


#@app.route('/category/<string:category>')
#def get_category_items(category):
#    allItems = items.query.filter(items.category == category)
#    results = []
#    for i in allItems:
#        item = {'upc': i.upc,
#                'name': i.name,
#                'price': str(i.price),
#                'description': i.description,
#                'category': i.category,
#                'image': i.image
#                }
#        results.append(item)
#
#    return jsonify({'items': results})


@app.route('/category/<category>', methods=['GET'])
def get_category_items_filterby(category):
    tag = request.args.get('tag')
    if tag:
        allItems = items.query.filter(
            items.category == category, items.name.like("%" + tag + "%")).all()
    else:
        allItems = items.query.filter(items.category == category)

    results = []
    for i in allItems:
        item = {'upc': i.upc,
                'name': i.name,
                'price': str(i.price),
                'description': i.description,
                'category': i.category,
                'image': i.image
                }
        results.append(item)

    return jsonify({'items': results})


if __name__ == '__main__':
    app.run()
