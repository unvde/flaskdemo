from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
# This Flask app sets app.secret_key, which is an encryption key used "to sign cookies and other things".
# Our app will work without it, but not completely. Without the secret key, we receive an error when searching:
# RuntimeError: The session is unavailable because no secret key was set.
# Storing secrets in plain code like this is not good practice. We know it.
# We don't want you to think we're endorsing this practice!
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'


@app.route('/')
def home():
    """Home page route."""
    return render_template("home.html")


@app.route('/about')
def about():
    """About page route."""
    return "I am still working on this"


@app.route('/search', methods=['POST', 'GET'])
def search():
    """Search page route. Return either form page to search, or search results."""
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")


@app.route('/results')
def results():
    """Results page route. Render the search results."""
    search_term = session.get('search_term')
    result = get_page(search_term)
    return render_template("results.html", page=result["page"], message=result["message"])


def get_page(search_term):
    """Return a dict with page object or error message."""
    try:
        page = wikipedia.page(search_term)
        return {"page": page, "message": None}
    except wikipedia.exceptions.PageError:
        return {"page": None, "message": f'Page id "{search_term}" does not match any pages. Try another id!'}
    except wikipedia.exceptions.DisambiguationError as e:
        return {"page": None, "message": (
            "We need a more specific title. Try one of the following, or a new search:\n"
            + str(e.options))
        }



if __name__ == '__main__':
    app.run()
