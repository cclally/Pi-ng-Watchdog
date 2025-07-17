import sys
import configparser
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
config_file_path = 'config.ini'

# Function to read the config file
def read_config():
	config = configparser.ConfigParser()
	config.read(config_file_path)
	return {section: dict(config.items(section)) for section in config.sections()}
	
# Function to write to config file
def write_config(data):
	config = configparser.ConfigParser()
	for section, section_data in data.items():
		config[section] = section_data
	with open(config_file_path, 'w') as configfile: 
		config.write(configfile)
		
# Route to get the config file data
@app.route('/get_config', methods=['GET'])
def get_config():
	data = read_config()
	return jsonify({'config': data})
	
# Route to update the config file data
@app.route('/update_config', methods=['POST'])
def update_config():
	new_data = request.json.get('config')
	if new_data:
		write_config(new_data)
		return jsonify({'status': 'success'}), 200
	return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
	
# Route to render the HTML form
@app.route('/edit_config', methods=['GET', 'POST'])
def edit_config():
	if request.method == 'POST':
		config_data = request.form.to_dict(flat=False)
		config_dict = {key: value[0] for key, value in config_data.items()}
		sections = list(set(key.split(':')[0] for key in config_dict.keys()))
		new_data = {}
		for section in sections:
			new_data[section] = {key.split(':')[1]: config_dict[key] for key in config_dict if key.startswith(section)}
		write_config(new_data)
		return render_template_string(html_template, config=new_data)
	else:
		data = read_config()
		return render_template_string(html_template, config=data)
		
# HTML template

html_template = '''
<!DOCTYPE html>
<html>
<head>
	<title>Edit Config</title>
</head>
<body>
	<h1>Edit Config</h1>
	<form method="POST">
		{% for section, settings in config.items() %}
			<h2>{{ sections }}</h2>
			{% for key, value in settings.items() %}
				<label>{{ key }}</label>
				<input type="text" name="{{ section }}:{{ key }}" value="{{ value }}"><br>
			{% endfor %}
		{% endfor %}
		<input type="submit" value="Update Config">
	</form>
</body>
</html>
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
