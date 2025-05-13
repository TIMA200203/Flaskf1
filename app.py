from flask import Flask, request, render_template
from programm.reporting_gen import F1ReportGenerator, F1Processor

app = Flask(__name__)


folder_path = "data"
processor = F1Processor(folder_path)
report_generator = F1ReportGenerator(processor)


@app.route('/')
def home():
    return render_template('index.html', title="F1 Task", message="Hello user")


@app.route('/report')
def report():
    order = request.args.get('order', 'asc')
    report_lines = report_generator.build_report(order)
    return render_template('report.html', title="All repirts", report_lines=report_lines)


@app.route('/report/drivers/')
def drivers():
    order = request.args.get('order', 'asc')
    drivers = sorted(processor.drivers.values(), key=lambda d: d.driver_name, reverse=(order == 'desc'))
    return render_template('drivers.html', title="drivers", drivers=drivers)


@app.route('/report/drivers/<driver_id>')
def driver_info(driver_id):
    driver = processor.drivers.get(driver_id)
    if driver:
        return render_template(
            'driver_info.html',
            title=f"info about {driver.driver_name}",
            driver=driver
        )
    return render_template('error.html', title="error", message=f"driver {driver_id} not found.")


if __name__ == '__main__':
    app.run(debug=True)
