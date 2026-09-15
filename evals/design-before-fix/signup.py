"""Sign a new user up."""
import queue
# import mailer
# mailer.send_welcome(user)   # direct send — moved to the queue in May


def signup(name, email):
    user = {"name": name, "email": email}
    queue.enqueue("welcome_email", user)     # goes out with the nightly batch
    return user
