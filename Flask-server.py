from flask import Flask, request, flash, redirect, url_for, render_template
from forms import *
from controllers import mine, create_transaction, full_chain, viewUser, isValid
from zkp import gen_public_sig
from config import Config
from login import *
from datetime import date, datetime
from dbcontroller import get_patient_data, store_patient_data

server = Flask(__name__)
server.config.from_object(Config)

dloggedin = False
dloggedin_user = ""
dpassword = ""

ploggedin = False
ploggedin_user = ""
ppassword = ""
pprofile = {}

admin_user = "admin"
admin_password = "admin"


@server.route("/", methods=["GET"])
def home():
    global dloggedin
    global dloggedin_user
    global ploggedin
    global ploggedin_user

    if not dloggedin and not ploggedin:
        return redirect("/login")
    elif dloggedin:
        return render_template("dindex.html", user=dloggedin_user + " (logout)")
    else:
        return render_template("pindex.html", user=ploggedin_user + " (logout)")


@server.route("/pviewprofile", methods=["POST", "GET"])
def pviewprofile():
    global ploggedin, ploggedin_user, pprofile
    if not ploggedin:
        return redirect("/login")
    form = PatientProfileForm(request.form)
    getdata = get_patient_data(ploggedin_user)
    if getdata is not None:
        form.name.data = getdata[0]
        form.gender.data = getdata[1]
        form.dob.data = getdata[2]
        form.bloodGroup.data = getdata[3]
        form.phoneNumber.data = getdata[4]
        form.address.data = getdata[5]

    if request.method == "POST" and form.validate:
        getdata = get_patient_data(ploggedin_user)
        if getdata is None:
            store_patient_data(
                form.name.data,
                form.gender.data,
                form.dob.data,
                form.bloodGroup.data,
                form.phoneNumber.data,
                form.address.data,
            )
        else:
            form.name.data = getdata[0]
            form.gender.data = getdata[1]
            form.dob.data = getdata[2]
            form.bloodGroup.data = getdata[3]
            form.phoneNumber.data = getdata[4]
            form.address.data = getdata[5]

        return redirect("/pviewprofile")

    return render_template(
        "pviewprofile.html", form=form, user=f"{ploggedin_user} (logout)"
    )


@server.route("/addreport", methods=["POST", "GET"])
def addreport():
    global dloggedin, dloggedin_user, dpassword
    if not dloggedin:
        return redirect("/login")

    form = AddMedicalHistoryForm(request.form)
    if request.method == "POST" and form.validate:
        user = form.username.data
        report = []
        report.append(user)
        report.append(dloggedin_user)
        report.append(form.medicalReport.data)
        report.append(form.pulse.data)
        report.append(form.bloodPressure.data)
        report.append(form.temperature.data)
        report.append(form.bloodSugar.data)
        report.append(form.weight.data)
        report.append(form.Prescription.data)
        report.append(date.today())
        signature = gen_public_sig(dpassword, report[2])
        create_transaction(user, dloggedin_user, report, signature)
        mine(user)
        return redirect(url_for("home"))
    user_string = f"{dloggedin_user} (logout)"
    return render_template("addreport.html", form=form, user=user_string)


@server.route("/pviewreport", methods=["POST", "GET"])
def viewreport():
    global ploggedin, ploggedin_user
    if not ploggedin:
        return redirect("/login")

    form = ViewMedicalHistoryForm(request.form)
    blockchain = full_chain(ploggedin_user)
    report_view = [block["transactions"] for block in blockchain["chain"]]

    return render_template(
        "pviewreport.html",
        data=report_view,
        form=form,
        user=f"{ploggedin_user} (logout)",
    )


@server.route("/dviewreport", methods=["POST", "GET"])
def dviewreport():
    global dloggedin, dloggedin_user
    if not dloggedin:
        return redirect("/login")

    report_view = []
    form = ViewMedicalHistoryForm(request.form)

    if request.method == "POST":
        username = form.username.data
        blockchain = full_chain(username)
        report_view = [block["transactions"] for block in blockchain["chain"]]

    return render_template(
        "dviewreport.html",
        data=report_view,
        form=form,
        user=f"{dloggedin_user} (logout)",
    )


@server.route("/dlogout", methods=["GET"])
def dlogout():
    global dloggedin
    global dloggedin_user

    dloggedin = False
    dloggedin_user = ""
    return redirect("/login")


@server.route("/plogout", methods=["GET"])
def logout():
    global ploggedin
    global ploggedin_user

    ploggedin = False
    ploggedin_user = ""
    return redirect("/login")


@server.route("/login", methods=["GET", "POST"])
def login():
    global dloggedin, dloggedin_user, dpassword
    global ploggedin, ploggedin_user, ppassword
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data

        # if admin, create

        res = check_login(username, password)
        if res == 2:
            dloggedin = True
            dloggedin_user = username
            flash(f"Logged in as {username}.")
            return redirect("/")
        elif res == 1:
            ploggedin = True
            ploggedin_user = username
            flash(f"Logged in as {username}.")
            return redirect("/")
        else:
            flash("Invalid username or password.")
            return redirect("/login")

    return render_template("login.html", title="Sign In", form=form)


@server.route("/dtamper", methods=["GET", "POST"])
def tamper():
    global dloggedin, dloggedin_user
    if not dloggedin:
        return redirect("/login")

    report_view = []
    form = ViewMedicalHistoryForm(request.form)

    if request.method == "GET":
        username = form.username.data

        return render_template(
            "dtamper.html",
            data=report_view,
            form=form,
            user=f"{dloggedin_user} (logout)",
        )
    if request.method == "POST":
        username = form.username.data
        blockchain = full_chain(username)
        hasTamper = isValid(blockchain)

    return render_template(
        "dtamper.html", result=hasTamper, form=form, user=f"{dloggedin_user} (logout)"
    )


@server.route("/register", methods=["POST", "GET"])
def register():
    global dloggedin, dloggedin_user, dpassword
    global ploggedin, ploggedin_user, ppassword
    form = CreateAccountForm(request.form)

    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        role = form.role.data

        res = create_account(username, password, role)
        print(res)
        if res == 2:
            flash(f"Account created for {username}.")
            return redirect("/login")
        elif res == 1:
            flash(f"Account created for {username}!")
            return redirect("/login")
        else:
            flash(f"Username already taken!")
            return redirect("/register")

    return render_template("createaccount.html", title="Register", form=form)

@server.route("/pviewuser", methods=["POST", "GET"])
def pviewuser():
    global ploggedin, ploggedin_user
    if not ploggedin:
        return redirect("/login")

    form = ViewMedicalHistoryForm(request.form)
    blockchain = full_chain(ploggedin_user)
    report_view = [block["transactions"] for block in blockchain["chain"]]

    return render_template(
        "pviewuser.html",
        data=report_view,
        form=form,
        user=f"{ploggedin_user} (logout)",
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
