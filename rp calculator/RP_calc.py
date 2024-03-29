from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/rp_calc/', methods=['GET', 'POST'])
def rp_calc():
    if request.method == 'POST':
        subj_names = ["H2 Subject 1", "H2 Subject 2", "H2 Subject 3", "H1 Subject", "General Paper"]
        no_of_subj = len(subj_names)
        if request.form['include_pw'] == "1":
            no_of_subj += 1
            subj_names.append("Project Work")
        if request.form['include_mtl'] == "1":
            no_of_subj += 1
            subj_names.append("Mother Tongue")
        return render_template('rp_calc2.html', subj_names=subj_names)

    else:
        return render_template('rp_calc1.html')

@app.route('/rp_result/', methods= ["POST"])
def rp_result():
    temp_dict = dict(request.form)
    result_dict = {}
    for key in temp_dict.keys():
        if type(temp_dict[key]) == list:
            result_dict[key] = temp_dict[key][0]
        else:
            result_dict[key] = temp_dict[key]
    result_mark_dict = {}
    rp_dict = {"A": 20, "B": 17.5, "C": 15, "D": 12.5, "E": 10, "S": 5, "U": 0}
    rp_without_mt, rp_with_mt, rp, total_rp = 0, 0, 0, 0

    for key in result_dict:
        grade = result_dict[key]
        if "H2" in key:
            rp_without_mt += rp_dict[grade]
            total_rp += 20
            result_mark_dict[key] = rp_dict[grade]
        else:  # H1 subject
            if key == "Mother Tongue":
                rp_with_mt = rp_without_mt + rp_dict[grade] / 2
            else:
                rp_without_mt += rp_dict[grade] / 2
            total_rp += 10
            result_mark_dict[key] = rp_dict[grade] / 2

    if rp_with_mt == 0:
        rp = rp_without_mt
    else:
        rp = round(max(rp_without_mt, rp_with_mt/total_rp*(total_rp-10)), 2)
        total_rp -= 10

    return render_template("rp_result.html",
                           rp=rp,
                           total_rp=total_rp,
                           result_dict=result_dict, result_mark_dict=result_mark_dict) 
if __name__ == '__main__':
    app.run(debug=True)
