__author__ = 'alex'

from flask import Flask, request, render_template, jsonify, url_for
from celery import Celery
import wiringpi2 as GPIO
import time

def make_celery(app):
	celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'],
							  backend=app.config['CELERY_RESULT_BACKEND'])
	celery.conf.update(app.config)
	TaskBase = celery.Task
	class ContextTask(TaskBase):
		abstract = True
		def __call__(self, *args, **kwargs):
			with app.app_context():
				return TaskBase.__call__(self, *args, **kwargs)
	celery.Task = ContextTask
	return celery

app = Flask(__name__)
app.config.update(
	CELERY_BROKER_URL='redis://127.0.0.1:6379/0',
	CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/0'
)
celery = make_celery(app)

PIN = 10
GPIO.wiringPiSetupSys()
GPIO.pinMode(PIN, 1)
GPIO.digitalWrite(PIN, 1)

@celery.task(bind=True)
def coffee_pot(self, action):
	try:
		if 'Start' in action:
			print 'Heating...'
			self.update_state(state='BREWING',)
			GPIO.digitalWrite(PIN, 0)
			time.sleep(60)
			m['text'] = 'Enjoy!'
			return True
		else:
			print 'Cooling Down...'
			self.update_state(state='OFF',)
			GPIO.digitalWrite(PIN, 1)
			time.sleep(1)
			return True

	finally:
		GPIO.digitalWrite(PIN), 1)



@app.route('/', methods=['GET', 'POST'])
def index():
	message = {'text': 'Ready to brew'}
	if 'POST' in request.method:
		button = request.form['button']
		if 'Brew Coffee!' in button:
			message['text'] = 'Starting'
			action = 'Start'
			task = coffee_pot.delay(action)
			return render_template('index.html', message=message['text'], task_id=task.id)
	return render_template('index.html', message=message['text'], task_id='')


@app.route('/check_status')
def check_status():
	task_id = request.args.get('task_id')
	task = coffee_pot.AsyncResult(task_id)
	if 'SUCCESS' in task.state:
			task_id = ''
	return jsonify(result=task.state, task_id=task_id)


@app.route('/remove', methods=['GET', 'POST'])
def remove():
	message = {'text': 'Stopping'}
	if 'POST' in request.method:
		button = request.form['button']
		task_id = request.form['task_id']
		if 'No Coffee!' in button:
			#from celery.task.control import discard_all
			#discard_all()
			action = 'Stop'
			task = coffee_pot.delay(action)
			return render_template('index.html', message=message['text'], task_id='')






@app.route('/status/<task_id>')
def status(task_id):
	task = coffee_pot.AsyncResult(task_id)
	if 'SUCCESS' in task.state:
		m = task.get()['text']
	else:
		m = ''
	return render_template('status.html', message=m, task_id=task.id)



if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')
