from flask import render_template, flash, redirect, url_for, jsonify, session
from .forms import WebsiteForm
from . import main
from ..scraper import scraper
from datetime import datetime



@main.route('/', methods=['GET', 'POST'])
def index():

    # Load Form
    form = WebsiteForm()

    # Scrape Function
    def scrape(form):
        try:
            scrp = scraper.Scraper(form.website.data)
            session['element_data'] = scrp.scrape()
        except:
            flash("This website cannot be scraped: %s" % (form.website.data))
            form.website.data = "https://www.google.com"
            scrp = scraper.Scraper(form.website.data)
            session['element_data'] = scrp.scrape()
            return redirect(url_for('.index'))

    # Scrape Submitted site
    if form.validate_on_submit():
        scrape(form)

    # Scrape Default site
    else:
        form.website.data = "https://www.google.com"
        scrape(form)

    return render_template('index.html', form=form,
                           elements=session['element_data']['list'],
                           totalCount=session['element_data']['totalCount'],
                           uniqueCount=session['element_data']['uniqueCount'])


@main.route('/getchartdata', methods=['GET', 'POST'])
def getchartdata():
    try:
        data = session['element_data']
    except:
        redirect(url_for('.index'))

    return jsonify(data)

