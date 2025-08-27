from flask import Flask, request, render_template


class ButtonApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.last_pressed = None

        # register routes that point to *instance* methods
        self.app.add_url_rule('/', view_func=self.home)
        self.app.add_url_rule('/press',
                              view_func=self.press,
                              methods=['POST'])

    # -------- views --------
    def home(self):
        return render_template('index.html')

    def press(self):
        key = request.form.get('key', '')
        if key in {'a', 'w', 's', 'd'}:
            self.last_pressed = key
            print(f"Key pressed: {key}")
        return '', 204

    # -------- helper --------
    def run(self, **kwargs):
        self.app.run(**kwargs)


# if __name__ == '__main__':
#     ButtonApp().run(host='0.0.0.0', port=5000)
