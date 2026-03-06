from flask import render_template, Flask

def register_error_handlers(app : Flask):

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404


    