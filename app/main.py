from app import app
from app import mp_items
from config import Config
from flask import render_template, redirect
from cloudant.database import CloudantDatabase
from cloudant.document import Document
from cloudant.client import Cloudant
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


#TODO - REPLACE CREDENTIALS WITH .env variables
#TODO - DATABASE IS OFF BY ONE DATE (e.g entry for November 26 has data for November 27)

#labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

#values = [967.67, 1190.89, 1079.75, 1349.19, 2328.91, 2504.28, 2873.83, 4764.87, 4349.29, 6458.30, 9907, 16297]
colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route('/', methods=['GET', 'POST'])
def main():
    
    class ItemSelect(FlaskForm):
        items = mp_items.itemIDs.items()
        #items = [(3075, "Adorned Empyrean Jewel"),(3070, "Bottled Wind")]
        selected = SelectField(u'Field name', choices = items, validators = [DataRequired()])
        submit = SubmitField('Submit')
    
    def get_cloudant_doc(itemID):

        client = Cloudant.iam(app.config["USER"], app.config["APIKEY"], connect=True)
        client.connect()
        
        database = CloudantDatabase(client,"marketplace-history-database")

        with Document(database,document_id=f"marketplace-history-{itemID}") as document:
            return(document)
        
    def render_document():
        item_ID = form.selected.data or 3075
        item_document = get_cloudant_doc(item_ID)
        item_name, item_history = item_document['name'], item_document['marketplace_history']

        line_labels = [date for date in item_history]
        line_values = [item_history[date]['average_price'] for date in line_labels]
        return render_template('line_chart.html', title=f'Marketplace History for {item_name}', max=17000, labels=line_labels, values=line_values, form=form)

    form = ItemSelect()
    if form.validate_on_submit():
        return render_document()
    return render_document()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
