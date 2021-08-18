import os, json

from flask import Flask
from prosegrinder import Dictionary


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'prosegrinder.sqlite'),
    # )
    dictionary = Dictionary()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    @app.route('/word/<word>')
    def word(word):
        w = dictionary.get_word(word)
        d = {
            "text": w.text,
            "phones": w.phones,
            "normalized_phones": w.normalized_phones,
            "phone_count": w.phone_count,
            "syllable_count": w.syllable_count,
            "character_count": w.character_count,
            "is_dictionary_word": w.is_dictionary_word,
            "is_numeric_word": w.is_numeric,
            "is_complex_word": w.is_complex_word,
            "is_pov_word": w.is_pov_word,
            "is_first_person_word": w.is_first_person_word,
            "is_second_person_word": w.is_second_person_word,
            "is_third_person_word": w.is_third_person_word,
            "pov": w.pov,
        }
        return json.dumps(d)

    return app
