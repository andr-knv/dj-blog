def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')

    match path:
        case '':
            response_text = 'Hello world'
        case 'about':
            response_text = "It's me"
        case 'say_hello':
            if environ['REQUEST_METHOD'] == 'POST':
                data = environ['wsgi.input'].read().decode('utf-8')
                name = data.split('=')[1].replace('+', ' ') if len(data) > 0 else ''
                response_text = f"Привет, {name}"
            else:
                response_text = """
                <form method="post" action="/say_hello">
                    <label for="name">Enter your name:</label>
                    <input type="text" id="name" name="name" required>
                    <input type="submit" value="Submit">
                </form>
                """
        case _:
            response_text = 'Not Found'

    status = '200 OK'
    response_headers = [('Content-Type', 'text/html; charset=utf-8')]
    start_response(status, response_headers)
    return [response_text.encode('utf-8')]
