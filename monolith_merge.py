def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


def remove_flask_initialization(app_content):
    lines = app_content.splitlines()
    new_content = []
    flask_import_found = False
    flask_init_found = False

    for line in lines:
        if "from flask" in line:
            if not flask_import_found:
                flask_import_found = True
                continue
        if not flask_init_found and "app = Flask(__name__)" in line:
            flask_init_found = True
            continue
        new_content.append(line)

    return "\n".join(new_content)


def add_shop_prefix_to_routes(app_content):
    lines = app_content.splitlines()
    new_content = []

    for line in lines:
        if "@app.route('" in line:
            route = line.split("@app.route('")[1].split("')")[0]
            new_route = f"@app.route('/shop{route}')"
            new_content.append(new_route)
        else:
            new_content.append(line)

    return "\n".join(new_content).replace(")')", "')").replace("']')", "'])")


def update_monolito():
    app_file_path = "app.py"
    monolito_file_path = "flask_api.py"

    # Read the content of app.py
    app_content = read_file(app_file_path)

    # Remove Flask import and initialization from app.py
    modified_app_content = remove_flask_initialization(app_content)

    # Add '/shop' prefix to routes in app.py
    modified_app_content = add_shop_prefix_to_routes(modified_app_content)

    # Read the content of monolito.py
    monolito_content = read_file(monolito_file_path)

    # Find the position to insert modified_app_content into monolito.py
    insert_position = monolito_content.find("# YOU SHOP") + len("# YOU SHOP")

    # Combine the modified app content with monolito content
    new_content = monolito_content[:insert_position] + "\n" + modified_app_content

    # Write the updated content to monolito.py
    write_file(monolito_file_path, new_content)


update_monolito()
