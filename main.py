from flask import Flask, render_template, request
import requests
import smtplib
import os

EMAIL = os.environ.get("EMAIL_KEY")
PASSWORD = os.environ.get("PASSWORD_KEY")
BLOG_ENDPOINT = os.environ.get("NPOINT_ENDPOINT")

app = Flask(__name__)

response = requests.get(url=BLOG_ENDPOINT)
blogs = response.json()


@app.route('/')
def home():
    return render_template("index.html", all_blogs=blogs)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    global EMAIL
    if request.method == "POST":
        name = request.form['user_name']
        email = request.form['user_email']
        phone = request.form['user_phone']
        message = request.form['user_message']
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs="srijayababu@yahoo.com", msg=f"subject:Jaya's Blog\n\nName: {name}\n"
                                                                                       f"Email: {email}\n"
                                                                                       f"Phone: {phone}\n"
                                                                                       f"Message: {message}")
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route('/post/<int:id>')
def post(id):
    for blog in blogs:
        if blog["id"] == id:
            blog_title = blog["title"]
            blog_subtitle = blog["subtitle"]
            blog_body = blog["body"]
            return render_template("post.html", title=blog_title, subtitle=blog_subtitle, body=blog_body)


if __name__ == "__main__":
    app.run(debug=True)



